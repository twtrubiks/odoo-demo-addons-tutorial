# odoo19.4 教學

這個分支主要是紀錄 saas-19.4 一些新的特性,

詳細的介紹可參考 [odoo-19-4-release-notes](https://www.odoo.com/odoo-19-4-release-notes)

分支可參考 [saas-19.4](https://github.com/odoo/odoo/tree/saas-19.4)

我這邊會介紹一些, 理論上, 這些應該都會進入 odoo20

以下紀錄就按照我的摸索慢慢補充 :smile:

* [Youtube Tutorial - Odoo 19.4 兩大改動 ！PDF 引擎換 Paper-Muncher、權限系統整個重寫](https://youtu.be/ZHba80GN04A)

* [Youtube Tutorial - Odoo 19.4 AI 架構全換血！順便讓 Odoo 自己變成 MCP Server](https://youtu.be/j9wuy120J9c)

## 目錄

* [Paper-Muncher](#paper-muncher)
* [權限系統重寫 ir.access - ir.model.access 與 ir.rule 合併](#權限系統重寫-iraccess---irmodelaccess-與-irrule-合併)
* [讓 odoo 自己變成 MCP Server - ai_mcp (企業版限定)](#讓-odoo-自己變成-mcp-server---ai_mcp-企業版限定)

## Paper-Muncher

目前在 saas-19.4 上, 已經可以選用 Paper-Muncher (對應 addons [base_report_paper_muncher](https://github.com/odoo/odoo/tree/saas-19.4/addons/base_report_paper_muncher)),

但預設還是 wkhtmltopdf (對應 addons [base_report_wkhtmltox](https://github.com/odoo/odoo/tree/saas-19.4/addons/base_report_wkhtmltox))

他的架構是變成可插拔(engine plugin)的介面, 所以你可以自由切換.

現在是兩引擎並存的過渡期, 因為 wkhtmltopdf 實在太舊了, 總有一天會被移除.

之前也有介紹過, Paper Muncher 速度快很多, 先來介紹怎麼啟用它,

首先, 要先到 [Paper Muncher](https://github.com/odoo/paper-muncher) 中的 releases 頁面下載然後安裝,

基本上安裝完會在你的 `/opt/paper-muncher/bin/paper-muncher` 這個路徑下.

接著你就安裝 addons [base_report_paper_muncher](https://github.com/odoo/odoo/tree/saas-19.4/addons/base_report_paper_muncher),

然後你有兩個方法可以切換到 Paper Muncher

方法一, 全域修改, 你直接到 系統參數 找到 report.pdf_engine_default 改成 paper-muncher (預設是 wkhtmltopdf).

![alt text](https://cdn.imgpile.com/f/ZgbpOBL_md.png)

方法二, 去單獨修改 report 的 report_type 設成 qweb-pdf-paper-muncher.

![alt text](https://cdn.imgpile.com/f/WLnN46y_xl.png)

接著去下載 pdf, 你會發現改呼叫 paper-muncher 了, 類似底下的 log

```cmd
INFO odoo19-saas-new odoo.http.server: - SF364hij - [26/Jul/2026 05:39:07] "GET /paper-muncher/3.html HTTP/1.1" 200 22561 43 0.034 0.848 rw
INFO odoo19-saas-new odoo.http.server: - SF364hij - [26/Jul/2026 05:39:07] "GET /paper-muncher/4.html HTTP/1.1" 200 22594 43 0.034 1.058 rw
```

Paper Muncher 還藏了一個環境變數 `ODOO_PAPER_MUNCHER_FEATURE`, 可以打開實驗性的功能,

對應的原始碼在 `addons/base_report_paper_muncher/models/ir_actions_report.py`

```python
if os.getenv('ODOO_PAPER_MUNCHER_FEATURE') == '1':
    extra_args += ['--feature', '*=on']  # activate all experimental/optional features
```

### Paper-Muncher 的好處

簡單整理一下換過去的好處

* **不用再開兩個 worker** - wkhtmltopdf 在單 worker 下會死鎖 (worker 卡著等 wkhtmltopdf, 而 wkhtmltopdf 在等那個 worker 回它圖片), 所以原始碼裡直接把 `workers == 1` 判定成不可用, paper-muncher 沒這個限制.

* **不會產生一堆暫存檔** - wkhtmltopdf 每次都要寫 cookie / header / footer / 每個 body / 輸出的 pdf, paper-muncher 全部走 pipe.

* **session 不會外流** - 兩者都會開臨時 session, 但 wkhtmltopdf 得把 cookie 寫進暫存檔用 `--cookie-jar` 交給外部程式, paper-muncher 的 cookie 只留在 odoo 行程的記憶體裡.

* **不用煩惱 base_url** - wkhtmltopdf 要真的連得回 odoo, 多租戶下 domain / 反向代理 / 內網 DNS 都要對齊, 錯一個就是 pdf 缺圖, paper-muncher 完全不經過網路, 這點對 SaaS 部署特別有感.

* **不需要拆表的 workaround** - wkhtmltopdf 遇到大表格效能會爆掉, 原始碼註解寫 250k 行要跑一小時, 所以 odoo 特地寫了 `_split_table` 每 500 行拆一次, paper-muncher 沒有這段 hack.

### 為什麼會用到 h11 這個套件

看原始碼會發現 `base_report_paper_muncher` 用了 [h11](https://github.com/python-hyper/h11),

他也已經是 odoo 正式的相依套件了, 可以在 [requirements.txt](https://github.com/odoo/odoo/blob/saas-19.4/requirements.txt) 裡面找到

```txt
h11==0.16.0  # packaged as 0.14.0~1 on debian/ubuntu, ~1 is a CVE patch, 0.16.0 has the patch.
```

先講 wkhtmltopdf 是怎麼做的, 他內嵌一個很舊的 Qt WebKit, 遇到 `<img src="/web/image/123">` 的時候, 他是真的發 TCP 請求連回 odoo 的 http server 要圖片,

上面講的那些毛病 (要兩個 worker / 要傳 cookie / base_url 要連得到) 全都是從這裡來的.

paper-muncher 則是走 stdin / stdout 的 pipe, 但管線上流動的東西是 HTTP 訊息, 大概像這樣

* `GET /paper-muncher/0.html` - 跟 odoo 要第幾份要渲染的文件
* `PUT /paper-muncher/output.pdf` - 把做好的 pdf 交回來
* 其他路徑 (圖片 / css / assets) - odoo 直接餵進自己的 WSGI 處理

而 h11 的定位是 sans-IO 的 HTTP/1.1 狀態機, 他只負責 bytes 跟 HTTP 事件之間的轉換, 完全不碰 socket, 所以才有辦法套在 pipe 上面用.

換句話說, odoo 根本沒有開任何 port, 而是在一條 pipe 上假裝自己是 HTTP server.

那為什麼不乾脆自己定一套協定就好? 因為 paper-muncher 本質上就是個瀏覽器引擎, 他抓資源的語意天生就是 HTTP,

既然是 HTTP, 收到的請求就可以直接轉成 WSGI 的 environ 丟給 odoo, 原本的 controller / 權限 / assets 機制通通不用改就能用.

## 權限系統重寫 ir.access - ir.model.access 與 ir.rule 合併

一句話定義他是什麼 - 舊的 `ir.model.access` 跟 `ir.rule` 被合併成同一個模型 `ir.access`.

`odoo/addons/base/models/ir_rule.py` 這個檔案直接被刪掉了, 換成 [ir_access.py](https://github.com/odoo/odoo/blob/saas-19.4/odoo/addons/base/models/ir_access.py).

連帶所有模組的 `security/ir.model.access.csv` 也全部改名成 `ir.access.csv`, 欄位長得完全不一樣了

```txt
舊: id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
新: id,name,model_id,group_id/id,operation,domain
```

四個 `perm_*` boolean 被縮成一個 `operation` 字串 (`r` / `cru` / `crud` 這樣), domain 則直接寫在同一列,

這就是 record rule 消失的真相 - 他沒有消失, 只是被併進來了.

### permission 與 restriction

新的權限判斷就是 `ir_access.py` 裡的這一行

```python
return Domain.OR(permissions) & Domain.AND(restrictions)
```

差別只在有沒有填 `group_id`

* **有填 group_id** - 叫 permission, 是「授權」, 彼此之間用 OR
* **沒填 group_id** - 叫 restriction, 是「全域限制」, 彼此之間用 AND

要注意 restriction 只會扣分不會加分, 他永遠不會給予任何權限,

所以 `group_id` 跟 domain 都留空的話, 那筆記錄等於什麼都沒做 (odoo 自己在 website_slides 就有兩筆這種死記錄).

對應到舊的東西大概是這樣

| 舊的 | 新的 |
| --- | --- |
| `ir.model.access` 一列 | permission + domain 留空 |
| `ir.rule` 有掛 groups | permission + domain |
| `ir.rule` 沒掛 groups (global) | restriction |
| **沒有符合的 record rule → 不過濾** | **沒有符合的 permission → 全鎖** |

OR + AND 這套算法其實舊的 `ir.rule` 就有了, 所以前面三列只是改名字而已.

真正變的是最後一列 - 舊的是兩層閘門, `ir.model.access` 那層沒設定就是全關 (直接丟 AccessError), 但 `ir.rule` 那層沒設定是放行的,

現在合成一層之後只剩一套預設值, 沒有符合的 permission, `Domain.OR([])` 直接就是 `FALSE`, 也就是全鎖.

換句話說, ACL 被拉進了這條公式 (變成一條 domain 留空的 permission), 而 rule 那層的「預設放行」就消失了.

### 多了一個 access domain operator

domain 裡面多了一個 `access` 運算子, 像這樣 (出自 `addons/sale/security/ir.access.csv`)

```csv
base_user_account_move_line_rule,Normal User Account Move Line,account.move.line,sales_team.group_sale_salesman,r,"[('move_id', 'access', 'read')]"
```

意思是「如果我讀得到這筆分錄的 `move_id`, 我就讀得到這筆分錄」.

以前子模型想跟隨父模型的權限, 只能把父模型的 domain 整段抄過來自己加 `move_id.` 前綴,

這個例子 odoo 自己就有, 19.0 的 `addons/sale/security/ir_rules.xml` 裡面, 父子兩條規則是這樣寫的

```xml
<!-- 父模型 account.move -->
<record id="account_invoice_rule_see_personal" model="ir.rule">
    <field name="model_id" ref="model_account_move"/>
    <field name="domain_force">[('move_type', 'in', ('out_invoice', 'out_refund')), '|', ('invoice_user_id', '=', user.id), ('invoice_user_id', '=', False)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
</record>

<!-- 子模型 account.move.line -->
<record id="account_invoice_line_rule_see_personal" model="ir.rule">
    <field name="model_id" ref="model_account_move_line"/>
    <field name="domain_force">[('move_id.move_type', 'in', ('out_invoice', 'out_refund')), '|', ('move_id.invoice_user_id', '=', user.id), ('move_id.invoice_user_id', '=', False)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
</record>
```

一模一樣的 domain, 只是每個欄位前面都多加了 `move_id.`, 而且這種還不只一條, 旁邊的 `see_all` 也是同樣的複製關係, 一個 model 兩條規則就得維護四條.

問題出在哪天父模型要多支援一種單據 (假設加個 `out_receipt`), 你得記得把每一條抄過的規則都跟著改,

漏改的結果是使用者看得到收據, 卻看不到收據的明細行 - 不會拋錯, 只會少資料, 而且測試通常只測父模型的可見性, 所以很難查.

換成 `[('move_id', 'access', 'read')]` 之後, 子模型沒有寫死任何條件, 父模型改什麼他就跟什麼.

現在他變成一等公民了, 三個位置都有限制, 寫錯會直接拋錯, 不是安靜失敗

| 位置 | 允許的值 |
| --- | --- |
| 欄位 | 只能是 many2one 或 `id` |
| 運算子 | 固定字串 `'access'` |
| 值 | 只能是 `'read'` / `'write'` / `'create'` / `'unlink'` 四選一 |

對應的檢查在 [odoo/orm/domains.py](https://github.com/odoo/odoo/blob/saas-19.4/odoo/orm/domains.py) 的 `_operator_access_rule_domain`

```python
@operator_optimization(['access'], level=OptimizationLevel.DYNAMIC_VALUES)
def _operator_access_rule_domain(condition, model):
    ...
    else:
        condition._raise("The 'access' operator works only for many2one and 'id' fields")

    operation = condition.value
    if operation not in ('read', 'write', 'create', 'unlink'):
        condition._raise("Invalid value for 'access' operator")
```

### 自訂模組要注意什麼

odoo 有附一支轉換腳本 `odoo/upgrade_code/19.4-00-ir-access.py`, 官方的模組就是跑他轉的 (commit `e7cc76b2907d`),

用法像這樣, 建議先加 `--dry-run` 看看會動到哪些檔案

```cmd
python odoo-bin upgrade_code --script 19.4-00-ir-access --addons-path /your/addons --dry-run
```

強烈建議不要手動改, 因為 `perm_*` 的預設值兩邊剛好相反 - 舊的 `ir.rule` 預設是 `True` (套用到全部四種操作), 舊的 `ir.model.access` 預設是 `False`,

兩個預設相反的東西要合併成同一個 `operation` 欄位, 手動改很容易錯.

另外一個要注意的是 groups 從 many2many 變成了 many2one, 所以一條掛多個 group 的 rule 會被裂成多筆記錄,

拿 `hr_expense` 來看, 19.0 原本是一條掛兩個 group

```xml
<record id="ir_rule_hr_expense_manager" model="ir.rule">
    <field name="name">Manager Expense</field>
    <field name="model_id" ref="model_hr_expense"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[
        (4, ref('account.group_account_user')),
        (4, ref('hr_expense.group_hr_expense_user'))]"/>
</record>
```

19.4 變成兩行

```csv
ir_rule_hr_expense_manager,Manager Expense,hr.expense,account.group_account_user,crud,
ir_rule_hr_expense_manager_1,Manager Expense,hr.expense,hr_expense.group_hr_expense_user,crud,
```

順便可以看到另外兩件事, `[(1, '=', 1)]` 被正規化成留空 (他跟 `[]` 跟留空都是同一個 `Domain.TRUE`), 而沒寫 `perm_*` 的 rule 因為預設是 `True`, 所以 operation 直接變成 `crud`.

upgrade_code 自己的 docstring 也講得很白

```txt
Please note that all the scripts are doing a best-effort a migrating the
source code, they only help do the heavy-lifting, they are not silver
bullets.
```

## 讓 odoo 自己變成 MCP Server - ai_mcp (企業版限定)

一句話定義他是什麼 - odoo 自己就是 MCP server, 不需要中間人.

對應的企業版 addons 是 ai_mcp, 想體驗可到 [odoo runbot](https://runbot.odoo.com/).

一般我們自己寫的 mcp server 是獨立跑一個 process, 再透過 JSON-RPC 從外面連回 odoo 拿資料,

而 ai_mcp 是直接在 odoo 裡面開一條 `/mcp` 的 route, 沒有中間人, 也不用另外部署, 裝了 addons 就有.

### 怎麼啟用

現在 api key 的部份, 多一個 mcp 可以選擇,

![alt text](https://cdn.imgpile.com/f/Bvzyaec_xl.png)

然後他的架構是看 Server Actions 中的 Available in MCP 欄位,

把這些有打勾的變成 tools, 所以你可以到這邊依照自己的需求去設定,

![alt text](https://cdn.imgpile.com/f/ljhEUPi_xl.png)

這邊使用 claude 當範例

```cmd
claude mcp add --transport http odoo https://your-company.odoo.com/mcp --header "Authorization: Bearer xxxx"
```

完整的設定大約會像這樣 (使用本機測試也是可行的)

```json
 "mcpServers": {
    "odoo": {
      "type": "http",
      "url": "http://0.0.0.0:8019/mcp",
      "headers": {
        "Authorization": "Bearer xxxxx"
      }
    }
}
```

然後使用的時候要注意, 一次只能顯示一個 db, 不然會抓不到, 比較簡單的設定方法是, 假設我們的 db 是 odoo19-saas,

把 dbfilter 設定好你的 odoo19-saas, 然後啟動的時候也指定你的 db `python3 odoo-bin .... -d odoo19-saas`

### 本質上他就是把 ir.actions.server 當成 tools

沒有註冊機制, 也沒有 decorator, tool 就是資料庫裡的一筆記錄.

這跟自己用 python 寫 mcp server (`@mcp.tool` 那種) 是相反的思路, 一個是程式碼定義 tool, 一個是資料定義 tool.

好處是增減 tool 不用改程式碼也不用重啟, 壞處是沒有版本控制, 裝了某個 addons 就可能默默多出工具.

### 預設只能讀, 但寫入隨時可以打開

預設只有 5 個唯讀的 tool, 不過這只是出廠設定保守而已.

ai 這個 addons 早就準備好 ai_tool_update_records 跟 ai_tool_create_records 了, 你只要把他們的 Available in MCP 勾起來, mcp client 立刻就有增改能力, 一行程式都不用寫.

要注意 Readonly Tool (`is_readonly`) 這個欄位沒有任何強制力, 他只是貼給 client 看的標籤, 一個實際上在寫資料的 tool, 你勾了 Readonly 他照樣寫.

### 每個使用者看到的 tools 是不一樣的

api key 是綁在 odoo 使用者身上的, 而 tools/list 每次都會逐一跑權限檢查, 過不了的直接跳過,

所以同一個 `/mcp` 網址, 會計跟業務拿到的工具清單不一樣.

而且他是直接在 odoo 行程內走 ORM, 不像外部的 mcp server 得透過 JSON-RPC 從外面打進來,

tool 裡拿到的 record 是 `sudo(False)`, 所以 ACL / record rules / 多公司規則全部照常生效, 不用自己寫任何權限判斷.

自架的 mcp server 通常是一把 api key 放在環境變數裡, 所有人共用同一個 odoo 身分, 要做到這件事得幫每個使用者跑一個 process.

### ai_tool_schema 不只是說明文件

他不只是寫給 AI 看的文件, 驗證過的參數會直接變成 code 裡面的變數,

所以 schema 裡 properties 的每個 key, 就是你在 code 裡可以直接用的變數名, 打錯字就是 NameError.

換句話說, schema 是 function signature, description 才是 docstring.

### MCP Retrieve initial context 是在補瀏覽器少掉的 context

他是 ai_mcp 唯一自己新建的 tool, 用途是補 mcp 缺掉的 session context, 回傳使用者的時區 / 當前公司 / 可用的公司.

在網頁上這些是瀏覽器帶上來的, 走 mcp 就完全沒有, 少了他, LLM 算「這個月的銷售」會用錯時區, 多公司下也不知道現在是哪一間.

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
