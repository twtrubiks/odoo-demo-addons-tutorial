# 如何使用 python xmlrpc 連接 odoo-12

此版本為 odoo12, odoo14 版本請參考 [odoo14](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/xml-rpc-odoo) 分支.

建議觀看影片, 會更清楚:smile:

* [Youtube Tutorial - 如何使用 python xmlrpc 連接 odoo - part1](https://youtu.be/MuMBF8a9ko8)

* [Youtube Tutorial - 如何使用 python xmlrpc 連接 odoo - part2](https://youtu.be/KFBaTB_XRJM)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[demo_odoo_tutorial](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial) -  odoo 手把手建立第一個 addons

主要介紹 xmlrpc

## 說明

External API 官方文件

[https://www.odoo.com/documentation/12.0/webservices/odoo.html](https://www.odoo.com/documentation/12.0/webservices/odoo.html)

`xmlrpc/2/common`

provides meta-calls which don’t require authentication.

`xmlrpc/2/object`

is used to call methods of odoo models via the execute_kw RPC function.

程式碼請參考 [demo.py](demo.py), 每個 function 都能執行,

(記得要先啟動一個 odoo 並填上 url, name, password, 也要選擇載入 demo data 哦)

此外, 裡面用到很多的 m2x 的 add, edit, update, delete 語法, 請參考下方

```xml
(0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
(1, ID, { values })    update the linked record with id = ID (write *values* on it)
(2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
(3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
(4, ID)                link to existing record with id = ID (adds a relationship)
(5)                    unlink all (like using (3,ID) for all linked records)
(6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
```

## 其他第三方工具

多數都是從 xmlrpc 衍生出來的

[https://github.com/OCA/odoorpc](https://github.com/OCA/odoorpc)

[https://github.com/tinyerp/erppeek](https://github.com/tinyerp/erppeek)