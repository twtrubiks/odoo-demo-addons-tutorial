# Odoo 15 中的 LISTEN/NOTIFY 運作原理

* [Youtube Tutorial - Odoo 15 中的 LISTEN/NOTIFY 運作原理](https://youtu.be/xySBGaX_oSk)

# 說明

本篇教學主要介紹 odoo 如何透過 Postgresql 中的 LISTEN/NOTIFY

來完成聊天室的建立, 我將會帶大家追蹤一下 code, 分別追蹤到觸發 LISTEN/NOTIFY.

如果大家不了解 Postgresql 中的 LISTEN/NOTIFY.

非常建議大家先去看之前介紹的 [Postgresql LISTEN/NOTIFY](https://github.com/twtrubiks/postgresql-note/tree/main/pg-listen-notify)

## 觸發 LISTEN

主要是由 `/longpolling/poll` 這個 URL 觸發 LISTEN,

原始碼路徑 `odoo15/addons/bus/controllers/main.py`

```python

def _poll(self, dbname, channels, last, options):
    channels = list(channels)  # do not alter original list
    ......
    return dispatch.poll(dbname, channels, last, options)

@route('/longpolling/poll', type="json", auth="public", cors="*")
def poll(self, channels, last, options=None):
    if options is None:
        options = {}
    if not dispatch:
        raise Exception("bus.Bus unavailable")
    if [c for c in channels if not isinstance(c, str)]:
        raise Exception("bus.Bus only string channels are allowed.")
    if request.registry.in_test_mode():
        raise exceptions.UserError(_("bus.Bus not available in test mode"))
    return self._poll(request.db, channels, last, options)
```

一路追蹤下去, 最後會發現觸發 `loop`,

也就是 LISTEN 的部份,

原始碼路徑 `odoo15/addons/bus/models/bus.py`,

```python

def poll(self, dbname, channels, last, options=None, timeout=None):
    ......
    # or wait for future ones
    if not notifications:
        if not self.started:
            # Lazy start of events listener
            self.start()

    ......
    return notifications

def loop(self):
    """ Dispatch postgres notifications to the relevant polling threads/greenlets """
    _logger.info("Bus.loop listen imbus on db postgres")
    with odoo.sql_db.db_connect('postgres').cursor() as cr:
        conn = cr._cnx
        cr.execute("listen imbus")
        cr.commit();
        while True:
            if select.select([conn], [], [], TIMEOUT) == ([], [], []):
                pass
            else:
                conn.poll()
                channels = []
                while conn.notifies:
                    channels.extend(json.loads(conn.notifies.pop().payload))
                # dispatch to local threads/greenlets
                events = set()
                for channel in channels:
                    events.update(self.channels.pop(hashable(channel), set()))
                for event in events:
                    event.set()

def run(self):
    while True:
        try:
            self.loop()
        except Exception as e:
            _logger.exception("Bus.loop error, sleep and retry")
            time.sleep(TIMEOUT)

def start(self):
    if odoo.evented:
        # gevent mode
        import gevent
        self.Event = gevent.event.Event
        gevent.spawn(self.run)
    else:
        # threaded mode
        self.Event = threading.Event
        t = threading.Thread(name="%s.Bus" % __name__, target=self.run)
        t.daemon = True
        t.start()
    self.started = True
    return self
```

最後說一下 longpolling timeout connection 的時間,

原始碼路徑 `odoo15/addons/bus/models/bus.py`,

```python
......
# longpolling timeout connection
TIMEOUT = 50
......
```

這也就可以解釋為甚麼你有時候會看到很多請求 timeout 的原因 :smile:

![alt tag](https://i.imgur.com/bw9K7zP.png)

## 觸發 NOTIFY

當在討論 (Discuss) 中發送訊息, 也就是按下 Send 的時候,

js 會觸發 `/mail/message/post` 這個 URL,

原始碼路徑 `odoo15/addons/mail/controllers/discuss.py`

```python
......
@http.route('/mail/message/post', methods=['POST'], type='json', auth='public')
def mail_message_post(self, thread_model, thread_id, post_data, **kwargs):
    if thread_model == 'mail.channel':
        channel_partner_sudo = request.env['mail.channel.partner']._get_as_sudo_from_request_or_raise(request=request, channel_id=int(thread_id))
        thread = channel_partner_sudo.channel_id
    else:
        thread = request.env[thread_model].browse(int(thread_id)).exists()
    allowed_params = {'attachment_ids', 'body', 'message_type', 'partner_ids', 'subtype_xmlid', 'parent_id'}
    return thread.message_post(**{key: value for key, value in post_data.items() if key in allowed_params}).message_format()[0]
......
```

接著觸發 `message_post`,

原始碼路徑 `odoo15/addons/mail/models/mail_thread.py`

```python
@api.returns('mail.message', lambda value: value.id)
def message_post(self, *,
                    body='', subject=None, message_type='notification',
                    email_from=None, author_id=None, parent_id=False,
                    subtype_xmlid=None, subtype_id=False, partner_ids=None,
                    attachments=None, attachment_ids=None,
                    add_sign=True, record_name=False,
                    **kwargs):
    ......
    self.ensure_one()  # should always be posted on a record, use message_notify if no
    ......
    new_message = self._message_create(values)

    # Set main attachment field if necessary
    self._message_set_main_attachment_id(values['attachment_ids'])

    if values['author_id'] and values['message_type'] != 'notification' and not self._context.get('mail_create_nosubscribe'):
        if self.env['res.partner'].browse(values['author_id']).active:  # we dont want to add odoobot/inactive as a follower
            self._message_subscribe(partner_ids=[values['author_id']])

    self._message_post_after_hook(new_message, values)
    self._notify_thread(new_message, values, **notif_kwargs)
    return new_message
```

接著觸發 `_notify_thread`,

原始碼路徑 `odoo15/addons/mail/models/mail_channel.py`

```python
def _notify_thread(self, message, msg_vals=False, **kwargs):
    # link message to channel
    rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)

    message_format_values = message.message_format()[0]
    bus_notifications = self._channel_message_notifications(message, message_format_values)
    self.env['bus.bus'].sudo()._sendmany(bus_notifications)
    # Last interest is updated for a chat when posting a message.
    # So a notification is needed to update UI.
    if self.is_chat or self.channel_type == 'group':
        ......
        self.env['bus.bus']._sendmany(notifications)
    return rdata

```

最後觸發 `_sendmany`, 也就觸發了 NOTIFY,

原始碼路徑 `odoo15/addons/bus/models/bus.py`

```python
@api.model
def _sendmany(self, notifications):
    channels = set()
    values = []
    for target, notification_type, message in notifications:
        channel = channel_with_db(self.env.cr.dbname, target)
        channels.add(channel)
        values.append({
            'channel': json_dump(channel),
            'message': json_dump({
                'type': notification_type,
                'payload': message,
            })
        })
    self.sudo().create(values)
    if channels:
        # We have to wait until the notifications are commited in database.
        # When calling `NOTIFY imbus`, some concurrent threads will be
        # awakened and will fetch the notification in the bus table. If the
        # transaction is not commited yet, there will be nothing to fetch,
        # and the longpolling will return no notification.
        @self.env.cr.postcommit.add
        def notify():
            with odoo.sql_db.db_connect('postgres').cursor() as cr:
                cr.execute("notify imbus, %s", (json_dump(list(channels)),))
```

