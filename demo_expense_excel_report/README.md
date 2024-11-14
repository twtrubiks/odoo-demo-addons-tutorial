# odoo 17 透過 controller 以及 js 列印 excel

因為版本之間還是有一點寫法上的差異,

odoo16 版本請參考 [demo_expense_excel_report](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/16.0/demo_expense_excel_report)

在 odoo 中如果要列印 excel,

我以前是使用 [report_xlsx](https://github.com/OCA/reporting-engine/tree/17.0/report_xlsx),

但是今天發現可以不需要使用這個 addons, 直接列印 excel,

但是必須額外撰寫 controller 以及 js.

# 教學

整個流程是這樣

[hr_expense.py](models/hr_expense.py)

```python
class HrExpenseCustom(models.Model):
    _inherit = "hr.expense"

    def button_excel_report(self):
        data = {
            'model_id': self.id,
            'name': self.name,
        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'hr.expense',
                'options': json.dumps(data),
                'output_format': 'xlsx',
                'report_name': 'Expense Custom Excel Report',
            },
            'report_type': 'xlsx',
        }
```

當呼叫 `button_excel_report` 時, 會去觸發 [action_excel_report.js](static/src/js/action_excel_report.js)

```js
......
registry.category("ir.actions.report handlers").add("custom_excel_xlsx", async function (action) {
    if (action.report_type === 'xlsx') {
        BlockUI;

        await download({
            url: '/custom_xlsx_reports',
            data: action.data,
            complete: () => unblockUI,
            error: (error) => self.call('crash_manager', 'rpc_error', error),
            });
    }
});
```

然後這個 js 會再去呼叫 `/custom_xlsx_reports`,

這個就是在 [controllers/main.py](controllers/main.py) 中定義的.

```python
......

class XLSXReportController(http.Controller):

    @http.route('/custom_xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name, **kw):
        """
        Generate an XLSX report based on the provided data and return it as a
        response.
        """
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(f"{report_name}.xlsx"))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
```

再透過這個 controllers 呼叫 model 中的 get_xlsx_report 完成下載流程.

執行畫面如下, 我把按鈕放在 hr_expense 中

![alt tag](https://i.imgur.com/AkLu0T4.png)

輸出結果

![alt tag](https://i.imgur.com/BhvlBwS.png)

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
