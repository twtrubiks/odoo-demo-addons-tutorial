# odoo 觀念 - 如何繼承 inherit controller

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - 如何繼承 inherit controller](https://youtu.be/kZG-CKQ2M7A)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 繼承 - class inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_class_inheritance)

本篇文章主要介紹 odoo 中的繼承 controller 這部份:smile:

## 說明

今天來繼承 sale addons 裡面的 `portal_my_quotes`,

路徑在 `addons/sale/controllers/portal.py`,

安裝好這個範例 addons, 可直接瀏覽 [http://0.0.0.0:8069/my/quotes](http://0.0.0.0:8069/my/quotes)

請查看 [controllers/portal.py](controllers/portal.py)

```python
from odoo import http
from odoo.addons.sale.controllers.portal import CustomerPortal

class TutorialPortal(CustomerPortal):

    @http.route(['/my/quotes', '/my/quotes/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_quotes(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        res = super(TutorialPortal, self).portal_my_quotes(page=1, date_begin=None, date_end=None, sortby=None, **kw)
        # res = super().portal_my_quotes(page=1, date_begin=None, date_end=None, sortby=None, **kw)
        print('inherit controller')
        return res
......
```

從上述的 code 你可以發現, 我們先 import 了 `CustomerPortal`,

`from odoo.addons.sale.controllers.portal import CustomerPortal`

因為需要繼承 CustomerPortal.

接著找到對應的 function, 也就是 `portal_my_quotes`, 基本上,

`http.route` 以及 `portal_my_quotes` 都保持一樣即可.

接著透過 super 去呼叫父類別,

`res = super(TutorialPortal, self).portal_my_quotes(......)`

如果是 python3, 可以使用更精簡的寫法,

`res = super().portal_my_quotes(......)`

把你需要增加的東西寫在這邊(可能是對 `res` 做修改), 這裡使用簡單的 print 代替,

`print('inherit controller')`

最後我們回傳 res.

整流程就是, 先呼叫原始的 `portal_my_quotes` 之後, 再執行 `print('inherit controller')` 這段.

(非常建議用中斷點看 code 如何跑的, 可直接看影片的說明)

在某些情況下, 對 res 做修改可能無法完全符合我們的需求, 這時候可以使用更快的方法(但不推薦),

就是直接整個去覆蓋掉 `portal_my_quotes`, 也就是直接把原始的 code, 再貼上一遍,

然後再加上自己需要的功能.

```python
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.sale.controllers.portal import CustomerPortal

class TutorialPortal(CustomerPortal):

    ......

    @http.route(['/my/quotes', '/my/quotes/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_quotes(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sent', 'cancel'])
        ]

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('sale.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        quotation_count = SaleOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/quotes",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=quotation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        quotations = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_quotations_history'] = quotations.ids[:100]

        values.update({
            'date': date_begin,
            'quotations': quotations.sudo(),
            'page_name': 'quote',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/quotes',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("sale.portal_my_quotations", values)
```

注意, 這邊也有多 import 了一些東西, 因為 `portal_my_quotes` 有使用到,

如果使用這種方法, 流程就是直接跑你定義的 `portal_my_quotes`.

(而不會再去呼叫原始的, 因為沒透過 `super` 去呼叫)
