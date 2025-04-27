# Odoo 15 建立簡易 REST API

這邊提供兩種作法

* 使用 jsonrpc 的方式 [demo_controller_api_jsonrpc](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/15.0/demo_controller_api/demo_controller_api_jsonrpc)

* 使用 http 的方式 [demo_controller_api_http](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/15.0/demo_controller_api/demo_controller_api_http)

兩種方式程式碼有一點點不同 :smile:

## 結論

雖然這個 REST API 看起來可能沒有那麼完整, 但應該還可以用.

如果想要建立完整的 REST API, 目前我這邊有兩個想法,

第一, 嘗試去了解 [https://github.com/OCA/rest-framework](https://github.com/OCA/rest-framework)

(但我覺得這有點複雜 :sweat: 而且不想在 odoo 上再加其他的東西, 所以選擇用現有的功能完成).

第二, 透過類似 django 去連 odoo db 建立 REST API.

至於要使用哪一種, 我覺得還是看各位的需求, 如果是簡單的 api, 應該是這個範例就可以了 :smile:
