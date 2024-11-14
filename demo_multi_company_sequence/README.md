# odoo17 - 多公司的 sequence

如果你不懂 sequence 的基本運作, 請參考 [odoo 觀念 - sequence](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_sequence)

本篇文章主要介紹 odoo 中的多公司 sequence 自動建立, 並且 sequence 獨立.

## 說明

我自己也是參考原始碼發現這種寫法的, 我是參考 [stock/data/stock_data.xml](https://github.com/odoo/odoo/blob/17.0/addons/stock/data/stock_data.xml) 底下的 `create_missing_scrap_sequence`

比較重要的觀念就是在建立公司的時候, 要去建立對應的 sequence,

開始介紹,

[models/res_company.py](models/res_company.py)

```python
......
class Company(models.Model):
    _inherit = "res.company"

    def _create_demo_sequence(self):
        demo_vals = []
        for company in self:
            demo_vals.append({
                'name': f'demo_sequence_sequence - {company.name} company',
                'code': 'demo.sequence',
                'company_id': company.id,
                'prefix': '%(year)s%(month)s%(day)s',
                'padding': 5,
                'number_next': 1,
                'number_increment': 1
            })
        if demo_vals:
            self.env['ir.sequence'].create(demo_vals)

    @api.model
    def create_missing_demo_sequence_sequence(self):
        company_ids  = self.env['res.company'].search([])
        domain = [('code', '=', 'demo.sequence')]
        company_has_demo_seq = self.env['ir.sequence'].search(domain).mapped('company_id')
        company_todo_sequence = company_ids - company_has_demo_seq
        company_todo_sequence._create_demo_sequence()

    def _create_per_company_sequences(self):
        self.ensure_one()
        self._create_demo_sequence()

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company in companies:
            company.sudo()._create_per_company_sequences()

        # 如果有建立分公司要多建立的東西可以寫在這邊
        return companies
```

整個流程會是這樣, 當建立公司時觸發 `create`, 然後會去呼 `_create_per_company_sequences`,

對應再呼叫 `_create_demo_sequence` 去建立該公司的 sequence.

你一定好奇我們怎麼沒有使用到 `create_missing_demo_sequence_sequence` :question:

這個是被定義在 [data.xml](data/data.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- 如果想要更新 addons 就觸發修改為 <data noupdate="0"> -->

    <data noupdate="1">
        <!-- create the demo_sequence_sequence for each company existing -->
        <function model="res.company" name="create_missing_demo_sequence_sequence"/>
    </data>
</odoo>
```

那它哪時候會被觸發呢 :question:

如果你想要強制觸發, 可以修改為 `<data noupdate="0">` 然後更新 addons.

不然它正常被觸發的時間點是你已經有多公司了, 但是你還沒有安裝這個 addons,

這樣當你安裝這個 addons 的時候就會被觸發了.

只要你建立新公司, 就會建立對應的 sequence

![alt tag](https://i.imgur.com/2G36MPF.png)

各公司的序號也是獨立的, 不會共用

![alt tag](https://i.imgur.com/oMAOI8m.png)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡 :laughing:

綠界科技ECPAY ( 不需註冊會員 )

![alt tag](https://payment.ecpay.com.tw/Upload/QRCode/201906/QRCode_672351b8-5ab3-42dd-9c7c-c24c3e6a10a0.png)

[贊助者付款](http://bit.ly/2F7Jrha)

歐付寶 ( 需註冊會員 )

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## 贊助名單

[贊助名單](https://github.com/twtrubiks/Thank-you-for-donate)

## License

MIT license
