# odoo15-tutorial

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

3. 全新的 HTML Editor 以及新的 commands `/` - [Youtube Tutorial - odoo15 全新的 HTML Editor 以及新的 commands `/`](https://youtu.be/UHMvLnPZSVM)

4. 能夠 Group By Many2many Field - [Youtube Tutorial - odoo15 能夠 Group By Many2many Field](https://youtu.be/pUKO2DaecCs)

5. 新功能 Project Sharing - backend view - [Youtube Tutorial - odoo15 新功能 Project Sharing - backend view](https://youtu.be/_DQSuCx-no4)

我認為 odoo15 把很多 Collaborators 的概念放進來, 而這功能也是其中的一個,

只不過他是實作在 project 中,

測試時, 請載入 demo data, 以及安裝 `project` 和 `website` 這裡兩個 addons,

找到 project 中的 Office Design, Settings 中的 Visibility,

也可以設定 portal user,

![alt tag](https://i.imgur.com/tQJ0sGs.png)

當然, 你也可以依照你的需求設定 Share Readonly 或 Share Editable

![alt tag](https://i.imgur.com/R1hr891.png)

如果你設定正確, 你所指定的對象可以看到 project 中的 backend view,

這邊選剛剛設定的 Office Design

![alt tag](https://i.imgur.com/FqjAWg1.png)

他會判斷你現在的權限是否可以進入到 backend view,

![alt tag](https://i.imgur.com/nIZyEub.png)

如果你有任何的修改, 想可以在 Collaborators 中看紀錄

![alt tag](https://i.imgur.com/RALEJo2.png)

如果想看如何實作, 這邊給大家一些關鍵字,

Project Sharing,

以及 `addons/project/controllers/portal.py` 中的 `render_project_backend_view`,

`addons/project/views/project_sharing_templates.xml` 中的 `project_sharing_embed`,

`project_sharing_embed` 這個 view 應該就是如何呈現 backend view.

6. 新功能命令面板 command palette 以及一些新東西 - [Youtube Tutorial - odoo15 新功能命令面板 command palette 以及一些新東西](https://youtu.be/2Q8sg2reV30)

命令面板 command palette, 當你在任意的地方按下 Shortcut ( ctrl +k ), 就會看到這個畫面

![alt tag](https://i.imgur.com/J2NcXll.png)

也請注意圖上下方的 TIP, 可以依照 `@user` `#chammels` `/menu` 去做變化.

* sale order 模組中可以設定 Customer Signature

* 產品可以加入 favourites (星星), 你的 favourites 會被排在最前面

* odoo15 import 改版

* discuss 按方向鍵 上 可以編輯, 可以刪除, 可以針對特定訊息回復.
