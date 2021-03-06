# odoo 觀念 - recruitment_website_form 介紹

[Youtube Tutorial - odoo 觀念 - recruitment_website_form 介紹](https://youtu.be/FDvl1eBIC_Q)

今天來介紹 odoo 中的 website_form, 順便來看一下 code 是怎麼跑的,

就使用 `website_hr_recruitment` 這個 addons 來介紹:smile:

請先把 `website_hr_recruitment` 裝起來 (記得安裝 demo data),

接著到 [http://0.0.0.0:8069/jobs](http://0.0.0.0:8069/jobs) 裡面隨便點一個,

你會看到以下的畫面, 今天就是要來介紹當你把這個 form 送出的時候會發生甚麼事情,

以及如果你要在這個 form 上加上新的 field 要注意些甚麼,

![alt tag](https://i.imgur.com/GIxr4pC.png)

首先, 先找到這個頁面對應的 view,

路徑在 odoo source code 中的 `addons/website_hr_recruitment/views/website_hr_recruitment_templates.xml`

```xml
<template id="apply">
    <t t-call="website.layout">
        <t t-set="additional_title">Apply Job</t>

        <div id="wrap"  class="container">
            <h1 class="text-center mt-2">
                Job Application Form
            </h1>
            <h2 t-if="job" class="text-center text-muted">
                <span t-field="job.name"/>
            </h2>

            <div class="row mt-3">
                <section id="forms" class="col">
                    <form action="/website_form/" method="post" class="s_website_form" enctype="multipart/form-data" data-model_name="hr.applicant" data-success_page="/job-thank-you" t-att-data-form_field_department_id="job and job.department_id.id or False" t-att-data-form_field_job_id="job and job.id or False">
                        <div class="form-group row form-field o_website_form_required_custom">
                            <div class="col-lg-3 col-md-4 text-right">
                                <label class="col-form-label" for="partner_name">Your Name</label>
                            </div>
                            <div class="col-lg-7 col-md-8">
                                <input type="text" class="form-control o_website_form_input" name="partner_name" required=""/>
                            </div>
                        </div>
                        ......
                    </form>
                </section>
            </div>
        </div>
    </t>
</template>
```

從這邊可以看出 `action="/website_form/" method="post"`, 也就代表會對 website_form route post,

而且個 website_form 被定義在 odoo source code 中的 `addons/website_form/controllers/main.py`

```python
class WebsiteForm(http.Controller):

    # Check and insert values from the form on the model <model>
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def website_form(self, model_name, **kwargs):
        # Partial CSRF check, only performed when session is authenticated, as there
        # is no real risk for unauthenticated sessions here. It's a common case for
        # embedded forms now: SameSite policy rejects the cookies, so the session
        # is lost, and the CSRF check fails, breaking the post for no good reason.
        csrf_token = request.params.pop('csrf_token', None)
        if request.session.uid and not request.validate_csrf(csrf_token):
            raise BadRequest('Session expired (invalid CSRF token)')

        model_record = request.env['ir.model'].sudo().search([('model', '=', model_name), ('website_form_access', '=', True)])
        if not model_record:
            return json.dumps(False)

        try:
            data = self.extract_data(model_record, request.params)
        # If we encounter an issue while extracting data
        except ValidationError as e:
            # I couldn't find a cleaner way to pass data to an exception
            return json.dumps({'error_fields' : e.args[0]})
    ......

    # Extract all data sent by the form and sort its on several properties
    def extract_data(self, model, values):
        dest_model = request.env[model.sudo().model]

        data = {
            'record': {},        # Values to create record
            'attachments': [],  # Attached files
            'custom': '',        # Custom fields values
            'meta': '',         # Add metadata if enabled
        }

        authorized_fields = model.sudo()._get_form_writable_fields()
        error_fields = []
        custom_fields = []
    ......
```

website_form 裡面要注意的是 `data = self.extract_data(model_record, request.params)`,

在 extract_data 裡面去呼叫了 `_get_form_writable_fields()` 也就是底下的

`authorized_fields = model.sudo()._get_form_writable_fields()`

而定義 _get_form_writable_fields() 在 odoo source code 中的

`addons/website_form/models/models.py`

```python
......
class website_form_model(models.Model):
    _name = 'ir.model'
    _description = 'Models'
    _inherit = 'ir.model'

    ......

    def _get_form_writable_fields(self):
        """
        Restriction of "authorized fields" (fields which can be used in the
        form builders) to fields which have actually been opted into form
        builders and are writable. By default no field is writable by the
        form builder.
        """
        included = {
            field.name
            for field in self.env['ir.model.fields'].sudo().search([
                ('model_id', '=', self.id),
                ('website_form_blacklisted', '=', False)
            ])
        }
        return {
            k: v for k, v in self.get_authorized_fields(self.model).items()
            if k in included
        }
    ......

```

你應該發現了 `website_form_blacklisted` 這個 field,

他會將 `website_form_blacklisted` 為 False 的撈出來,

我們再來看 `website_form_blacklisted` 這個 field 定義了哪些東西,

路徑在 odoo source code 中的 `addons/website_form/models/models.py`

```python
......

class website_form_model_fields(models.Model):
    """ fields configuration for form builder """
    _name = 'ir.model.fields'
    _description = 'Fields'
    _inherit = 'ir.model.fields'

    @api.model_cr
    def init(self):
        # set all existing unset website_form_blacklisted fields to ``true``
        #  (so that we can use it as a whitelist rather than a blacklist)
        self._cr.execute('UPDATE ir_model_fields'
                         ' SET website_form_blacklisted=true'
                         ' WHERE website_form_blacklisted IS NULL')
        # add an SQL-level default value on website_form_blacklisted to that
        # pure-SQL ir.model.field creations (e.g. in _reflect) generate
        # the right default value for a whitelist (aka fields should be
        # blacklisted by default)
        self._cr.execute('ALTER TABLE ir_model_fields '
                         ' ALTER COLUMN website_form_blacklisted SET DEFAULT true')

    @api.model
    def formbuilder_whitelist(self, model, fields):
        """
        :param str model: name of the model on which to whitelist fields
        :param list(str) fields: list of fields to whitelist on the model
        :return: nothing of import
        """
        # postgres does *not* like ``in [EMPTY TUPLE]`` queries
        if not fields: return False

        # only allow users who can change the website structure
        if not self.env['res.users'].has_group('website.group_website_designer'):
            return False

        # the ORM only allows writing on custom fields and will trigger a
        # registry reload once that's happened. We want to be able to
        # whitelist non-custom fields and the registry reload absolutely
        # isn't desirable, so go with a method and raw SQL
        self.env.cr.execute(
            "UPDATE ir_model_fields"
            " SET website_form_blacklisted=false"
            " WHERE model=%s AND name in %s", (model, tuple(fields)))
        return True

    website_form_blacklisted = fields.Boolean(
        'Blacklisted in web forms', default=True, index=True, # required=True,
        help='Blacklist this field for web forms'
    )

```

`website_form_blacklisted` field 預設會是 True,

在 odoo 的設計中, 所有 website_form 的 field 預設都是 True,

並需要設定成 False 才可以搭配 website_form 使用.

這樣我們該怎麼設定 `website_form_blacklisted` 為 False 呢:question:

odoo source code 路徑為 `addons/website_hr_recruitment/data/config_data.xml`

```xml
......
<function model="ir.model.fields" name="formbuilder_whitelist">
            <value>hr.applicant</value>
            <value eval="[
                'description',
                'email_from',
                'partner_name',
                'partner_phone',
                'job_id',
                'department_id',
            ]"/>
</function>
```

這段程式碼會去呼叫 `addons/website_form/models/models.py` 裡面的 `formbuilder_whitelist` function,

然後你可以看到 `formbuilder_whitelist` 中有一段 code

```python
self.env.cr.execute(
    "UPDATE ir_model_fields"
    " SET website_form_blacklisted=false"
    " WHERE model=%s AND name in %s", (model, tuple(fields)))
```

會將我們設定的 fields (必須存在) 以及對應的 model (必須存在) 改為 `website_form_blacklisted=false`,

而 `addons/website_hr_recruitment/data/config_data.xml` 這段 code 執行的時間點是安裝 addons 的時候,

安裝 addons 完, 也可以到資料庫裡面看

```sql
SELECT id, name, model, relation, relation_field, website_form_blacklisted
	FROM public.ir_model_fields where model='hr.applicant' and website_form_blacklisted='False';
```

![alt tag](https://i.imgur.com/U8gNTsu.png)

你會發現所設定的 fields 的 `website_form_blacklisted` 都變成 False 了.

### 結論

如果我們希望在 odoo source code 中的

`addons/website_hr_recruitment/views/website_hr_recruitment_templates.xml` 加一個欄位,

舉個例子, 就加 `reference` 這個 fields,

除了在 `website_hr_recruitment_templates.xml` 上面多加 input 之外,

```xml
......

<div class="form-group row form-field o_website_form_required_custom">
    <div class="col-lg-3 col-md-4 text-right">
        <label class="col-form-label" for="reference">Reference</label>
    </div>
    <div class="col-lg-7 col-md-8">
        <input type="text" class="form-control o_website_form_input" name="reference"/>
    </div>
</div>

......

```

你還必須加入 `reference` fields (並呼叫 `formbuilder_whitelist` function),

```xml
<function model="ir.model.fields" name="formbuilder_whitelist">
    <value>hr.applicant</value>
    <value eval="[
      ......
      'reference',
    ]"/>
</function>
```

這樣才可以成功的把 form 的 input 帶到 model 裡面, 因為預設的 field 都被列為黑名單,

必須透過 data 中呼叫 `formbuilder_whitelist` function,

將需要的 fields 的 `website_form_blacklisted` 設為 False,

因為 odoo 只會取出 `website_form_blacklisted` 為 False 的 fields.
