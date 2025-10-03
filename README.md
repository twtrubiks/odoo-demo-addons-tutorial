# odoo19 教學

這個分支主要是紀錄 odoo19 一些新的特性,

以下紀錄就按照我的摸索慢慢補充 :smile:

官方也有整理改動的內容 [Migration-to-version-19.0](https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-19.0)

- [Odoo 19 JSON-2 API 完整使用指南](odoo-json2-client)

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

## Testing 相關

- [Testing your code in Odoo: Why and how should you do it?](https://www.odoo.com/event/odoo-experience-2025-6601/track/testing-your-code-in-odoo-why-and-how-should-you-do-it-8761)

介紹了 Testing (單元測試 以及 整合測試 ) 的重要性, 以及新增了

Tour Recorder (Testing Odoo - Integration Testing)功能.

Odoo 測試是走 TDD 這個流程.

## Odoo Shell

- [Odoo Shell: The DevOps ally](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-shell-the-devops-ally-8756)

介紹了很多 Odoo Shell 的特殊用法

## Odoo CLI

- [Simplifying the CLI, one command at a time](https://www.odoo.com/event/odoo-experience-2025-6601/track/simplifying-the-cli-one-command-at-a-time-8375)

odoo19 開始, 很多 CLI 功能被切成更小塊, 且預設的新指令不啟動 odoo server,

介紹了自定義 CLI Command,

不用擔心舊的指令無法使用, 多數都有並存保留下來.

## JSON-2 API

- [Odoo API 101: discover the new blazing fast api](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-api-101-how-does-it-work-and-whats-new-in-odoo-19-8823)

主要講了 JSON-2 API, 講者提到最好一次就呼叫完你要的東西(透過 group_by),

避免 n+1 query(也就是用 loop 的方式呼叫).

## 資料庫相關

- [Multiple PostgreSQL servers behind Odoo - Nicolas Seinlet](https://www.odoo.com/event/odoo-experience-2025-6601/track/multiple-postgresql-servers-behind-odoo-8755)

介紹了 Odoo 和 PostgreSQL 的整合, 主要是水平垂直拓展的概念, 以及是否你真的需要水平拓展.

## 分析效能相關

- [Database autopsy: A performance post-mortem](https://www.odoo.com/event/odoo-experience-2025-6601/track/database-autopsy-a-performance-post-mortem-8211)

介紹了一些工具讓你去分析 odoo 慢的原因, 像是 lnav 這套工具.

## report 相關 (wkhtmltopdf)

- [Turning Web pages into beautiful print: The architecture of Paper-Muncher](https://www.odoo.com/event/odoo-experience-2025-6601/track/turning-web-pages-into-beautiful-print-the-architecture-of-paper-muncher-8399)

主要說明了為什麼現在還是使用 wkhtmltopdf

簡單說是歷史包袱, 影響範圍太大, 慢的原因其實是 wkhtmltopdf 會用類似無頭瀏覽器的概念在背景執行, 所以速度慢,

未來有機會改成 [Paper Muncher](https://github.com/odoo/paper-muncher) 但短期應該看不到,

影片中有 demo 兩者列印 report 速度的差異, Paper Muncher 真的明顯快很多.

## 整合外部 api 的企業級解決方案

- [Master Data Management with Odoo](https://www.odoo.com/event/odoo-experience-2025-6601/track/master-data-management-with-odoo-7453)

影片介紹了他們的解決方案(也做了多方案的比較優缺點), 目標是解決外部同步到 odoo 或 odoo 要去同步別人的東西,

說明了 pull 或 push 的概念, 提供了企業級的解決方案.

## 升級

- [Odoo upgrades: Core concepts and tools](https://www.odoo.com/event/odoo-experience-2025-6601/track/odoo-upgrades-core-concepts-and-tools-8771)

介紹了升級的部份, 主要推薦兩個參數, 幾乎可以修正遇到的大部分的情況,

`nouptdate="1"` flag to prevent updates to existing records.

`forcecreate="0"` inside a nouptdate="1" block, prevents record creation during a module update.

也介紹了 [upgrade-util](https://github.com/odoo/upgrade-util),

後來查了一下相關的文章, 才發現有了 [upgrade.odoo.com](upgrade.odoo.com) 這個網站.

## Odoo Language Server

- [Introducing Odoo Language Server: Your coding companion](https://www.odoo.com/event/odoo-experience-2025-6601/track/introducing-odoo-language-server-your-coding-companion-8319)

介紹了 Language Server. LSP 的全名是 Language Server Protocol (語言伺服器協定).

功能有 自動完成, 懸停提示, 跳至定義, 程式碼診斷.

可參考專案 [odoo-ls](https://github.com/odoo/odoo-ls)
