# Odoo 18 RESTful API 多種建立方法比較與實踐

* [Youtube Tutorial - Odoo 18 RESTful API 多種建立方法比較與實踐](https://youtu.be/tQYbuCZjojY)

這個其實很久以前就介紹過了, 這邊再整理一下給各位, 目前有三個方法

## 方法一 - 透過 Odoo controller 的概念

[Odoo 15 建立簡易 REST API](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/15.0/demo_controller_api)

這個方法透過 Odoo Controller 的概念建立的, 可以用 http 或是 JSON-RPC

但我認為這個方法, 只適合很簡單的需求.

## 方法二 - Django Ninja + Odoo

就是自己維護一台 REST API 的機器, 然後透過 XML-RPC 的方式呼叫 Odoo,

這就可以實做非常多的事情.

這邊不一定要用 Django Ninja, 你喜歡 Flask 或是 FastAPI 都可以,

但是影片我用 Django Ninja + Odoo 當範例.

* 優點 : 解耦與關注點分離(API 與 Odoo 核心完全分離), 獨立擴展, 彈性.

* 缺點 : 額外的部署與維護, 身份驗證規劃, 網路延遲與 XML-RPC 連線開銷, 需自行撰寫 XML-RPC 邏輯, XML-RPC 高併發 (High Concurrency) 瓶頸.

## 方法三 - OCA FastAPI 套件

使用現成的 OCA FastAPI 套件,

這個使用上非常簡單, 直接安裝就可以使用了, 也會產生 api 文件,

[OCA - rest-framework/fastapi](https://github.com/OCA/rest-framework/tree/18.0/fastapi)

它 depend 下面這個 addons

[OCA - web-api/endpoint_route_handler](https://github.com/OCA/web-api/tree/18.0/endpoint_route_handler)

記得也要安裝 `requirements.txt` (因為你需要把 FastAPI 裝起來).

它的概念是去攔截 `ir.http` model, 然後實現 FastAPI 與 Odoo HTTP 層整合的核心.

透過增加 `Dispatcher` 去定義屬於 `fastapi` 的請求.

* 優點 : 緊密整合, 統一的身份驗證(可以直接使用 Odoo 的驗證), 簡化部署, 可直接使用 Odoo ORM.

* 缺點 : 耦合性高, FastAPI 學習曲線, 穩定性考量.
