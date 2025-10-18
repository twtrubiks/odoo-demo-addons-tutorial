# odoo19 教學

這個分支主要是紀錄 odoo19 一些新的特性,

以下紀錄就按照我的摸索慢慢補充 :smile:

* [Youtube Tutorial - Odoo 19 JSON-2 API 完整教學！告別 XML-RPC 迎接新世代](https://youtu.be/edWMCN6z6nw)

* [Youtube Tutorial - Odoo 19 IndexedDB 快取策略, Odoo Runtime Doc api 文檔](https://youtu.be/ckEHImNHxL4)

* [Youtube Tutorial - 告別手動測試！ 全新 CLI 指令 & Odoo 19 Tour Recorder 實戰教學](https://youtu.be/2W3YPz47oLs)

官方也有整理改動的內容 [Migration-to-version-19.0](https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-19.0)

- [Odoo 19 JSON-2 API 完整使用指南](odoo-json2-client)

- [Odoo 19 CLI](odoo-cli)

## odoo 2025 影片

[odoo-experience-2025 track](https://www.odoo.com/event/odoo-experience-2025-6601/track)

整理一下自己稍微有看的官方影片

## What's new in the Python framework

- [What's new in the Python framework? - Raphael Collet](https://www.odoo.com/event/odoo-experience-2025-6601/track/whats-new-in-the-python-framework-8412)

基本上我每年都看他的, 因為主要是 python 的改動都是他說的, 很多是效能的改進.

然後多了新的 `widget` `res_user_group_ids_privilege`, 目的是把整個 user 和 group 整個調整了,

講者說這個之前都是透過很 hack 的方式去完成的, 現在是真正的 clean code.

## 如何貢獻 odoo

- [A guide to contributing to Odoo's code base](https://www.odoo.com/event/odoo-experience-2025-6601/track/a-guide-to-contributing-to-odoos-code-base-8776)

如何貢獻 odoo code, odoo 的 policy 是 不會使用 `-u` 去重新啟動 odoo, 所以不能增加欄位,

不能修改 view template, 以及如何寫出好的 code 送 PR.

### 安全性議題

- [Odoo Security 101](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-security-101-8752)

主要講了 odoo 安全性以及 CVEs 的概念. (更新只需要 git pull & odoo restart)

- [Unveiling the most common security issues Developer](https://www.odoo.com/event/odoo-experience-2025-6601/track/unveiling-the-most-common-security-issues-8753)

更深入的介紹 odoo 的安全性, 以及攻擊者通常會怎麼攻擊, 如何避免, 像是

使用 SQL Wrapper (避免 SQL injection), 不要過度使用 sudo (錯誤的用法以及如何正確的使用),

注意 `compute_sudo` 使用 (會 pass 權限), 了解 odoo 中的 ACLs 以及 record rules.

### AI 相關議題

- [Developing Odoo modules using AI: a practical guide](https://www.youtube.com/watch?v=2JViJFJhF-g)

介紹了 odoo AI 模組的互動架構, 以及 RAG (使用了 pgvector),

demo 如何寫 AI 相關功能 addons, addons 中如何定義 **Tool Calling** 給 AI 呼叫.

雖然沒有 MCP, 但架構符合 MCP 的規範.

- [NLP search and AI tools: How does it work and what are the benefits?](https://www.youtube.com/watch?v=t1jLPpmRGMo)

介紹了 odoo AI 中實際的應用, 用自然語言和它溝通, 它會幫你自動切換到對應的畫面以及合適的 domain,

也說明了架構以及 System Prompt (目前是使用 人工撰寫 + AI生成 混合的 Prompt).

為什麼不直接把內容放到 Prompt 中就好, 而要使用 **Tool Calling** 增加複雜度,

首先是 context window 不是無限制的, 就算無限制, 這作法會產生高昂的費用(龐大資料), 速度也會很慢.

結論是 **Tool Calling** 是必要的.

安全性考量的話, 目前是給 AI 供應商決定他們會不會訓練你的資料.

目前只支援 Gemini 以及 ChatGPT, 暫時不支援本地的 Ollama.

目標是打造很多對應的專業 agent, 而不是建立一個通用 agent (因為這樣 AI 容易幻覺).

也說明了目前的侷限性.

- [Website import tool: How AI can rebuild your website](https://www.odoo.com/event/odoo-experience-2025-6601/track/website-import-tool-how-ai-can-rebuild-your-website-8405)

透過輸入網址, 就可以把整個目標網站的結構抓進來並且符合 odoo 的架構, 是透過 AI 的方式, 目前只有企業板.

- [Beyond Code Generation: Integrating AI into Odoo's Development Lifecycle – Lessons Learned](https://www.odoo.com/event/odoo-experience-2025-6601/track/beyond-code-generation-integrating-ai-into-odoos-development-lifecycle-lessons-learned-7931)

不要讓 AI 外包核心的 code, 說明 AI 主要是輔助你完成工程師不喜歡做的事情, 如果你喜歡用 AI 寫 code 必看.

## Testing 相關

- [Testing your code in Odoo: Why and how should you do it?](https://www.odoo.com/event/odoo-experience-2025-6601/track/testing-your-code-in-odoo-why-and-how-should-you-do-it-8761)

介紹了 Testing (單元測試 以及 整合測試) 的重要性, 以及新增了

Tour Recorder (Testing Odoo - Integration Testing)功能.

Odoo 講者推薦 TDD 這個流程.

也有人問到為什麼不用 pytest, 講者說明可能是歷史的關係(包袱).

## Code Quality 相關

- [Improving Odoo Quality with Automated Code Checks](https://www.odoo.com/event/odoo-experience-2025-6601/track/improving-odoo-quality-with-automated-code-checks-8006)

介紹了很多自動化檢查的工具, 用 pre-commit 完成 black, isort, flake8, pylint-odoo 這些,

以及使用 github action 完成更深度的檢查(odoo test, xenon, bandit, SonarQube).

## Odoo Shell

- [Odoo Shell: The DevOps ally](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-shell-the-devops-ally-8756)

介紹了很多 Odoo Shell 的特殊用法

## Odoo CLI

- [Simplifying the CLI, one command at a time](https://www.odoo.com/event/odoo-experience-2025-6601/track/simplifying-the-cli-one-command-at-a-time-8375)

odoo19 開始, 很多 CLI 功能被切成更小塊, 且預設的新指令不啟動 odoo server,

介紹了自定義 CLI Command,

不用擔心舊的指令無法使用, 多數都有並存保留下來.

## JSON-2 API

- [Odoo API 101: How does it work and what's new in Odoo 19?](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-api-101-how-does-it-work-and-whats-new-in-odoo-19-8823)

主要講了 JSON-2 API, 講者提到最好一次就呼叫完你要的東西(透過 group_by),

避免 n+1 query(也就是用 loop 的方式呼叫).

- [XMLRPC is dead. All Hail JSON-2.](https://www.odoo.com/event/odoo-experience-2025-6601/track/xmlrpc-is-dead-all-hail-json-2-8760)

團隊有嘗試往 REST API 的方向, 但最後沒採用, 因為 REST API 和 XML 架構差太多了, 無法克服,

所以最後採用新的 JSON-2.

如果你想要嘗試類似 GraphQL, 可以看 `web_search_read` 中的 `specification` 這個.

## 資料庫相關

- [Multiple PostgreSQL servers behind Odoo - Nicolas Seinlet](https://www.odoo.com/event/odoo-experience-2025-6601/track/multiple-postgresql-servers-behind-odoo-8755)

介紹了 Odoo 和 PostgreSQL 的整合, 主要是水平垂直拓展的概念, 以及是否你真的需要水平拓展.

## 分析效能相關

- [Database autopsy: A performance post-mortem](https://www.odoo.com/event/odoo-experience-2025-6601/track/database-autopsy-a-performance-post-mortem-8211)

介紹了一些工具讓你去分析 odoo 慢的原因, 像是 lnav 這套工具.

- [Database Whodunit: Root Cause Analysis of Performance Issues](https://www.odoo.com/event/odoo-experience-2025-6601/track/database-whodunit-root-cause-analysis-of-performance-issues-8445)

說明怎麼一步一步找到慢的原因, 排除法.

也推薦大家可以是用 odoo 內建的 Profiler 工具,

以下指令可以看到全部的 Field dependencies

```python
model = self.env['res.partner']
field = model._fields.get('name')
registry = self.env.registry
registry.get_field_trigger_tree(field)
```

## report 相關 (wkhtmltopdf and Paper-Muncher)

- [Turning Web pages into beautiful print: The architecture of Paper-Muncher](https://www.odoo.com/event/odoo-experience-2025-6601/track/turning-web-pages-into-beautiful-print-the-architecture-of-paper-muncher-8399)

主要說明了為什麼現在還是使用 wkhtmltopdf

簡單說是歷史包袱, 影響範圍太大, 慢的原因其實是 wkhtmltopdf 會用類似無頭瀏覽器的概念在背景執行, 所以速度慢,

未來有機會改成 [Paper Muncher](https://github.com/odoo/paper-muncher) 但短期應該看不到,

影片中有 demo 兩者列印 report 速度的差異, Paper Muncher 真的明顯快很多.

- [Unveiling Paper-Muncher: The secret of web engines and understanding large document generation](https://www.odoo.com/event/odoo-experience-2025-6601/track/unveiling-paper-muncher-the-secret-of-web-engines-and-understanding-large-document-generation-8816)

介紹了為什麼最後選擇 Paper-Muncher, 以及小團隊(2~4人)怎麼規劃完成這個專案(花了非常多的時間規劃後才實做).

介紹了升級的部份, 主要推薦兩個參數, 幾乎可以修正遇到的大部分的情況,

## 升級

- [Odoo upgrades: Core concepts and tools](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-upgrades-core-concepts-and-tools-8771)

介紹了升級的部份, 主要推薦兩個參數, 幾乎可以修正遇到的大部分的情況,

`nouptdate="1"` flag to prevent updates to existing records.

`forcecreate="0"` inside a nouptdate="1" block, prevents record creation during a module update.

也介紹了 [upgrade-util](https://github.com/odoo/upgrade-util),

後來查了一下相關的文章, 才發現有了 [upgrade.odoo.com](upgrade.odoo.com) 這個網站(官方維護).

也有社群維護板, 可參考 [OpenUpgrade](https://github.com/OCA/OpenUpgrade)

## Odoo crons (排程)

- [Best practices to design Odoo crons](https://www.odoo.com/event/odoo-experience-2025-6601/track/best-practices-to-design-odoo-crons-8754)

蠻推薦這影片的, 介紹了很多設計一個好的 crons,

冪等操作 (Idempotent)

意思是「一個操作執行一次和執行 N 次的結果應該是完全一樣的」.

例如，一個 cron 如果因為意外而被重複執行了兩次，不應該會重複發送兩封郵件或重複計算兩次庫存。

故障安全的 (Failure-safe)

當 cron 在執行過程中遇到錯誤（例如網路中斷）時，應該要有能力從中恢復，或在下次執行時能接續處理，

而不是留下一堆處理到一半的髒數據.

處理大資料時, 使用 分批 (batch) 處理, 避免超時(timeout),

把大任務切成小塊多次 commit.

在 odoo19 中多了新特性, 如果排程多次失敗, 會自動幫你停用.

影片中也提到 `env.cr.rollback()` 的概念.

## Odoo Language Server

- [Introducing Odoo Language Server: Your coding companion](https://www.odoo.com/event/odoo-experience-2025-6601/track/introducing-odoo-language-server-your-coding-companion-8319)

介紹了 Language Server. LSP 的全名是 Language Server Protocol (語言伺服器協定).

功能有 自動完成, 懸停提示, 跳至定義, 程式碼診斷.

可參考專案 [odoo-ls](https://github.com/odoo/odoo-ls)

## SEO, Website

- [Discover Odoo's SEO basics](https://www.odoo.com/event/odoo-experience-2025-6601/track/discover-odoos-seo-basics-8819)

介紹了很基礎的 SEO 觀念, 一頁盡量一個主題, 圖片盡量有描述之類的.

但有了 AI 之類, 這類規則肯定會被打破.

- [What's new in SEO?](https://www.odoo.com/event/odoo-experience-2025-6601/track/whats-new-in-seo-8425)

介紹了 odoo 在 SEO 努力的方向, 以及新功能, 也提昇了整體 Website 的速度.

## Odoo Studio

- [A developer’s guide to building importable SaaS-ready modules](https://www.odoo.com/event/odoo-experience-2025-6601/track/a-developers-guide-to-building-importable-saas-ready-modules-8751)

其實就是在介紹 Odoo Studio, 本質上就是把 python 的部份都轉成了 xml 的格式(有一些限制).

## IoT Box

- [How to integrate hardware with Odoo IoT Box?](https://www.odoo.com/event/odoo-experience-2025-6601/track/how-to-integrate-hardware-with-odoo-iot-box-8770)

介紹 IoT Box, IoT Box 本身就是一台 Raspberry Pi, 負責轉接(翻譯官),

如果你的解決方案, 有其他更好的(像是你的硬體有 api), 請使用 api 的方式, 因為用了 IoT Box,

等於多一層架構, 更難維護. 也介紹了一些 debug IoT Box 的技巧.

## Translations

- [Translations, Odoo, and you!](https://www.odoo.com/event/odoo-experience-2025-6601/track/translations-odoo-and-you-8763)

介紹了 i18n 以及 l10n, 說明了 i18n 的架構, 翻譯上的一些技巧以及 issue

## 整合外部 api 的企業級解決方案

- [Master Data Management with Odoo](https://www.odoo.com/event/odoo-experience-2025-6601/track/master-data-management-with-odoo-7453)

影片介紹了他們的解決方案(也做了多方案的比較優缺點), 目標是解決外部同步到 odoo 或 odoo 要去同步別人的東西,

說明了 pull 或 push 的概念, 提供了企業級的解決方案.

## odoo 搭配 redis

- [Boosting Odoo Performance with Redis Caching](https://www.odoo.com/event/odoo-experience-2025-6601/track/boosting-odoo-performance-with-redis-caching-7707)

使用 redis 快取了 odoo website 的部份(redis 保存了 odoo 的 html),

雖然沒有明確說明他們的作法, 但介紹了一些 redis 基本概念以及注意事項,

像是在 redis 中不要放入遺失會造成問題(重大損失)的資料.

## IndexedDB 快取策略

- [Discover how we made Odoo blazing fast](https://www.youtube.com/watch?v=enwWRebkyK4)

odoo19 透過瀏覽器的 IndexedDB 去加速瀏覽畫面的速度(快取, 離線也可以讀取, 只要你有讀取過),

使用的策略是儲存 API 回應 (RPC's Responses), 資料加解密使用 AES-GCM.

目前只實做在 view kanban, list, form 上面以及一些 RPC 上面

`get_views` `web_search_read` `web_read_group` `web_read` `on_change`

打開 debug mode, 在 action 中, 可以看到 Data Caching 這個選項.

這概念使用了部份的 PWA 這類的技術.

## OCA

- [Why OCA Modules Are Like Magic Beans](https://www.odoo.com/event/odoo-experience-2025-6601/track/why-oca-modules-are-like-magic-beans-7665)

如果你想多了解 OCA, 可以看一下這個影片.

- [Odoo Community Association (OCA) : From 2013 to now, the history!](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-community-association-oca-from-2013-to-now-the-history-7886)

這也是在介紹 OCA, 包含為什麼成立以及歷史, 他們也有自己的組織架構.

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