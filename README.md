# odoo15-docker-tutorial

這個分支主要是紀錄 odoo15 一些新的特性,

以下紀錄就按照我的摸索慢慢補充

1. Discuss 新增視訊功能 - [Youtube Tutorial - odoo15 Discuss 新增視訊功能](https://youtu.be/DUd5f1-wlDQ)

新增了視訊通話, 螢幕分享的功能, 很類似 google meeting, 採用 WebRTC 技術.

在測試這個的時候, 可能會遇到瀏覽器安全性的限制導致無法取得 mic, 相機的權限,

請到你的瀏覽器增加以下設定, 這邊使用 brave 示範

`brave://flags/#unsafely-treat-insecure-origin-as-secure`

![alt tag](https://i.imgur.com/niZhppx.png)

2. 增加 collaborative 協同編輯欄位 - [Youtube Tutorial - odoo15 增加 collaborative 協同編輯欄位](https://youtu.be/aqEJ7CMfEIo)

主要是透過 `options="{'collaborative': true}"` 這個新的參數.

可參考 view_id `project.view_task_form2` 中的 xml.

3. 全新的 HTML Editor 以及新的 commands `/` - [Youtube Tutorial - odoo15 全新的 HTML Editor 以及新的 commands `/`]()

4. 能夠 Group By Many2many Field - [Youtube Tutorial - odoo15 能夠 Group By Many2many Field]()
