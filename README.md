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

4. 新功能 Group By Many2many Fields 以及更快速的編輯 Edit - [Youtube Tutorial - odoo15 新功能 Group By Many2many Fields 以及更快速的編輯 Edit](xx)

現在 Many2many Fields 可以被 Group By 了,

實作內容可參考以下兩個 PR [odoo/pull/74985](https://github.com/odoo/odoo/pull/74985) [odoo/pull/75692](https://github.com/odoo/odoo/pull/75692).

更快速的編輯 Edit, 在任意 Fields 底下, 點一下滑鼠左鍵大約0.5秒放開, 會自動進入編輯模式.

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

7. 新功能 Website Bulider, Configuration Wizards, new Jinja mail templates - [Youtube Tutorial - odoo15 新功能 Website Bulider, Configuration Wizards, new Jinja mail templates]()

* 新功能 Website Bulider, 把 website addons 裝上即可體驗

* 新功能 Configuration Wizards

位置在 Technical -> Configuration Wizards

![alt tag](https://i.imgur.com/ZcmOgk6.png)

這個功用應該是要拿來初始化第一次進入特定頁面

![alt tag](https://i.imgur.com/H9QyhiR.png)

像是你如果安裝 `website` 或 `blog` 以及....,

安裝完都會被導到特定的 Configuration Wizards,

不管你有沒有設定, 第一次進入 Wizard 之後, 狀態就會被改成 done,

但如果你需要重新設定, 可以點 Set as Todo, 然後重新 Lanch 即可,

會導到設定的 `ir.actions.act_url`.

![alt tag](https://i.imgur.com/OZ5c6vp.png)

相關 source code 關鍵字可查詢 `ir.actions.todo`.

* New Jinja mail templates

相關 pr 可參考 [pull/67868](https://github.com/odoo/odoo/pull/67868#issuecomment-820467701)

現在可以直接在上面看 UI 的 html 的 (點選了 `</>`), 這樣要找 html 也比較方便

![alt tag](https://i.imgur.com/YgP6sWk.png)

也可以強制 template 為特定的語言

![alt tag](https://i.imgur.com/AYflPvN.png)

