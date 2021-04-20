# odoo 觀念 - 實作 init hook

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - 實作 init hook](https://youtu.be/2ZmfH3wBHm8)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 init hook 這部份

## 說明

還記得之前我們介紹過 [介紹 security, menu, tree, form](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#%E4%BB%8B%E7%B4%B9-security-menu-tree-form)

裡面有提到很多時候會透過 `data/xxx.xml` 的方式自動產生一些預設資料,

但是, 有時候我們的邏輯比較複雜, 無法簡單的使用 xml 表示, 這時候, 就可以透過 hook 的方式.

先來看 `__manifest__.py`

```python
{
    ......

    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'post_load': 'post_load_hook',

    'application': True,
}

```

在 odoo 中, hook 總共有 4 種,

`pre_init_hook` 在安裝 addons 之前, 會先執行他, 執行完畢後, 才開始安裝 addons. (更新不會生效)

`post_init_hook` 在安裝 addons 完之後, 才會執行他. (更新不會生效)

`uninstall_hook` 在移除 addons 完之後, 才會執行他.

`post_load` 這個比較特殊, 他只會生效在當你使用 odoo-bin CLI 安裝或更新時, 優先於 `pre_init_hook`.

`post_load` 比較進階, 常常搭配 [介紹 Monkey Patch](https://github.com/twtrubiks/fluent-python-notes/tree/master/what_is_the_Monkey_Patch), 請參考 odoo source code.

請參考 `__init__.py`

```python
from odoo import api, SUPERUSER_ID

import logging

_logger = logging.getLogger(__name__)

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # data = env[......].search([......])

    _logger.warning('=== pre_init_hook ===')

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # data = env[......].search([......])

    _logger.warning('=== post_init_hook ===')

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # data = env[......].search([......])

    _logger.warning('=== uninstall_hook ===')

def post_load_hook():
    _logger.warning('=== post_load_hook ===')
```

當我們透過 odoo-bin CLI 安裝 addons 時,

執行順序為 `post_load_hook` -> `pre_init_hook` -> `post_init_hook`

(如果從 odoo 介面安裝 addons 則不會有 `post_load_hook` )

![alt tag](https://i.imgur.com/zFeoeNl.png)

從 odoo 介面移除 addons

![alt tag](https://i.imgur.com/viGukst.png)

透過這個方法, 當我們在安裝或是移除 addons 時, 可以針對資料面再進行一次檢查或清理.

像是有時候繼承既有的 rule, 當你移除 addons 時, 該 rule 並不會被還原,

這時候, 就可以用 hook 的方式來處理:satisfied:
