# odoo20 教學

這個分支主要是紀錄 odoo20 一些新的特性,

詳細的介紹可參考 [odoo-20-release-notes](https://www.odoo.com/odoo-20-release-notes)

分支可參考 [20.0](https://github.com/odoo/odoo/tree/20.0)

今年的議程可參考 [odoo-experience-2026 agenda](https://www.odoo.com/event/odoo-experience-2026-9099/agenda), 有些議程有影片, 需要的可以去觀看.

之前在 saas-19.4 介紹的特性, 都已經進入 odoo20 了, 沒改動的部份這邊就不重複寫,

請直接參考 [saas-19.4](https://github.com/twtrubiks/odoo-demo-addons-tutorial/commits/saas-19.4/) (Youtube 教學影片也在那邊),

這邊只補充 20.0 跟 saas-19.4 不一樣的地方, 最後再整理從 19.0 升上來要注意的改動.

以下紀錄就按照我的摸索慢慢補充 :smile:

* [Youtube Tutorial - Odoo 20 新特性一次看懂：AI 改點數、MCP OAuth、populate #Odoo20 #MCP #ClaudeCode #AI #ERP](https://youtu.be/Rcm0LL6nFKg)

## 目錄

* [環境需求](#環境需求)
* [AI 不能再用自己的 key, 改用點數 (企業版限定)](#ai-不能再用自己的-key-改用點數-企業版限定)
* [讓 odoo 自己變成 MCP Server - ai_mcp (企業版限定)](#讓-odoo-自己變成-mcp-server---ai_mcp-企業版限定)
* [權限系統 ir.access](#權限系統-iraccess)
* [Paper-Muncher](#paper-muncher)
* [populate 產生大量測試資料](#populate-產生大量測試資料)
* [其他改動](#其他改動)
* [從 19.0 升級要注意的改動](#從-190-升級要注意的改動)

## 環境需求

最低版本 Python 3.12 / PostgreSQL 16, 最高支援到 Python 3.14.

## AI 不能再用自己的 key, 改用點數 (企業版限定)

19.4 要在設定填自己的 OpenAI / Gemini key (`ai.openai_key` / `ai.google_key`) 才能用, 20.0 全部拿掉, 改成只能用 Odoo 的 IAP 點數, 也不能選 OpenAI / Gemini.

* Agent 對話 / embedding / 語音轉錄 / AI 欄位都走 IAP 的 `odoo_ai` 服務扣 Credits, 用哪個模型由 Odoo 決定
* 點數到 開發者模式 > 設定 > 技術 > IAP > In-App Purchase Accounts 找 `odoo_ai` 查看, 按 Buy Credits 購買
* 自架要注意, Agent 對話是非同步的, Odoo AI 算完會回呼你的 `web.base.url` + `/ai/completion_result_ready`, 外部連不到你的 Odoo 的話會一直等不到回覆.
* ai_mcp 不受影響, LLM 是 mcp client 自己的 (例如 claude), 預設的 tools 不會呼叫 odoo 的 AI, 所以不扣點

## 讓 odoo 自己變成 MCP Server - ai_mcp (企業版限定)

跟 saas-19.4 一樣, odoo 自己就是 MCP server, 啟用方式請參考 [saas-19.4](https://github.com/twtrubiks/odoo-demo-addons-tutorial/commits/saas-19.4/).

20.0 的改動

* 支援 OAuth 2.1, 不用再手動建 api key 貼到 header, 預設白名單有 claude.ai / claude code / chatgpt / grok
* 寫入的 tool (update / create) 多了防呆, 不能寫 `ir.*` 等系統 model, update 也不能用 `[]` 一次改整張表

OAuth 範例 (claude code)

```shell
claude mcp add --transport http odoo http://localhost:8069/mcp
```

本機測試要注意一下網址, 必須要都是一樣的.

加完後在 claude code 輸入 `/mcp` 選 odoo 認證, 會開瀏覽器登入 odoo 並同意授權.

## 權限系統 ir.access

跟 saas-19.4 一樣, `ir.model.access` 跟 `ir.rule` 合併成 `ir.access`, 轉換腳本 `19.4-00-ir-access` 也一樣能用, 詳細請參考 [saas-19.4](https://github.com/twtrubiks/odoo-demo-addons-tutorial/commits/saas-19.4/).

這個轉換腳本除了遷移, 還會標出可疑的權限設定, 例如 A 群組有 model 存取權限, B / C 群組有 record rule, 但這幾個群組彼此沒有關聯, 可能是漏設了群組之間的 implied 關係, 建議正式遷移前先看一下輸出, 手動修掉.

20.0 的改動

* `ir.access` 的 `_get_domain_for` 被刪掉, 邏輯搬進 ORM, 改用 `self.env['sale.order']._access_domain('read')`
* `_check_access` 被標成 deprecated, 改用 `_access_domain`

## Paper-Muncher

跟 saas-19.4 一樣, 預設還是 wkhtmltopdf, 啟用方式請參考 [saas-19.4](https://github.com/twtrubiks/odoo-demo-addons-tutorial/commits/saas-19.4/).

20.0 的改動

* paper-muncher 版本要 0.6 以上, 舊版記得到 [releases](https://github.com/odoo/paper-muncher/releases) 更新
* header / footer 改由 paper-muncher 自己排版

## populate 產生大量測試資料

目標是產生大量、分布接近真實的假資料, 主要拿來做效能測試, 也可以用在 demo 或開發環境.

* 舊的 `odoo-bin populate` (18 / 19.0, 用 SQL 複製現有資料) 在 saas-19.4 改名成 `odoo-bin duplicate`, 17 那種 `_populate_factories` 寫法也已經沒有了
* 新的 `populate` 是一個模組, 用 Blueprint (XML / JSON) 描述要產生什麼資料, 資料走 ORM 建立, compute 和 constraint 都會跑, 支援 `-j` 平行處理、`--resume` 中斷後續跑

20.0 的改動

* Blueprint 語法 `<model>` 改成 `<create>` / `<write>` / `<function>`, `virtual="True"` 改成 `<value>`, 19.4 寫的 Blueprint 要改 (還用 `<model>` 會直接報錯)
* 新增 `<import>` 可以引用別的 Blueprint, 還有 `--profile` 可以看每個 job 的效能

用法

```shell
# 內建 Blueprint 大多用到 faker, 要先裝
pip install -r addons/populate/requirements.txt

# 安裝 populate 模組
odoo-bin -d mydb -i populate --stop-after-init

# 用 sale 內建的 Blueprint 產生資料
odoo-bin populate -d mydb -b sale.fake_sale_demo

# 資料量 x10, 用全部 CPU 平行跑
odoo-bin populate -d mydb -b sale.fake_sale_demo --scale 10 -j auto

# 中斷後續跑
odoo-bin populate -d mydb --resume
```

* 出現 `Blueprint ... was not found` 的話, 先跑 `-u populate` 重新載入 Blueprint
* 自訂模組只要在模組裡建 `populate/*.xml`, 不用寫進 manifest, populate 會自己掃描載入, 寫法可參考 `addons/sale/populate/populate_demo.xml` 和 `addons/populate/README.md`

## 其他改動

* **FontAwesome 換成 Material Symbols** - 19.4 還是 FontAwesome 4.7, 20.0 整個拿掉了, 可用的圖示名稱請參考 `addons/web/tooling/icons/icons_wishlist.txt`
* **report_file 欄位被刪掉** - `ir.actions.report` 的 XML 如果還有寫 `<field name="report_file">`, 安裝時會拋 `ValueError: Invalid field 'report_file' in 'ir.actions.report'`
* **upgrade_code 多了 `19.5-00-tuple-rec_names_search`** - 把 `_rec_names_search = ['name']` 改成 tuple `('name',)`, 純風格, list 還是能用
* **模組調整** - `stock_picking_batch` 併入 `stock`, `base_vat` 模組被移除了

## 從 19.0 升級要注意的改動

以下這些在 saas-19.x 就改了, 從 19.0 升上來一定會碰到

* **Owl 2 → Owl 3** - saas-19.4 從 2.8.4 升到 3.0.0-alpha, 20.0 有附 `owl3_compatibility_layer.js` 讓舊程式先跑, 官方也有轉換腳本 `python odoo-bin upgrade_code --script owl3-migration --addons-path /your/addons --dry-run` (處理 useState / useEffect / t-model 等), 但元件寫了 `static props` / `static defaultProps` 會直接 throw, 腳本不會轉, 要自己改成 `props = useProps({...})`
* **compute_sql** - 沒有 stored 的 compute 欄位也能搜尋、排序、group by, 要明確寫 `compute_sudo` (related 欄位會自動帶), `Domain.custom(to_sql=...)` 也改成收 `TableSQL`
* **Query / TableSQL** - 一般 ORM 寫法不受影響, 只有用 `Query` 組 raw SQL, 或 override `_order_to_sql`、`_read_group_*` 這類 hook 時才要改 (第一個參數改成收 `table`)
* **ir.config_parameter 刪掉 get_param / set_param** - 改用 `get_str` / `get_int` / `get_float` / `get_bool` 和對應的 `set_*`, 移植 17 或 19 的模組一定要改
* **移除 pytz, 改用 zoneinfo** - `env.tz` 是 `ZoneInfo`, 沒有 `localize()`, 改用 `dt.replace(tzinfo=tz)`. 要小心本機 venv 還裝著 pytz 的話, `import pytz` 不會報 ImportError, 問題會被蓋掉
* **Binary 改成 BinaryValue** - `ir.attachment` 的 `datas` 已刪除, 寫進去會被丟掉 (只有 warning), 改用 `raw`; 空值是 `EMPTY_BINARY`. 另外 20.0 的 RPC 回傳改成 dict `{'content', 'size', 'filename'}`, 外部腳本要改成取 `['content']`
* **odoo.osv 刪除** - `from odoo.osv import expression` 改用 `from odoo.fields import Domain`
* **check_access_rights / check_access_rule 刪除** - 改用 `check_access()` / `has_access()`
* **registry.clear_cache 刪除** - 改用 `env.transaction.invalidate_ormcache()`
* **odoo.service.db 刪除** - 搬到 `odoo.modules.db`
* **res.partner 刪掉 company_type** - `is_company` 改成 stored compute
* **mail.tracking.value 拆到 mail_tracking** - 預設不會安裝
* **t-call 裡的 t-set 不再傳給被呼叫的模板** - 改成 `<t t-call="x" foo="expr"/>`
* **publicWidget / jQuery 刪除** - 網站前台改用 `Interaction`
* **模組合併** - `hr_org_chart` / `hr_homeworking` 併入 `hr`, `website_sale_wishlist` / `website_sale_comparison` 併入 `website_sale`, `base_iban` 刪除

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
