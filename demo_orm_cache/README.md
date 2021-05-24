# odoo 觀念 - orm cache 說明

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - (等待新增)orm cache 說明]()

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 orm cache

## 說明

cache 的觀念在 python 中其實主要就是使用 dict 來完成的,

如果有興趣也可以參考底下的兩篇文章:smile:

[什麼是 functools.lru_cache in python](https://github.com/twtrubiks/python-notes/tree/master/what_is_the_functools.lru_cache)

[fibonacci numbers ( 費氏數列 )](https://github.com/twtrubiks/python-notes/tree/master/fibonacci_numbers_tutorial)

要記住 cache 都是保存在 ram 中, 所以請不要拿來存大型的圖片.

範例 code 都是放在 [models/model.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/master/demo_orm_cache/models/model.py) 之中,

先來看一個最簡單的例子,

```python
from odoo import models, fields, tools
......
    @tools.ormcache()
    def demo_ormcache(self):
        result = '{} {}'.format('hello', 'world')
        _logger.warning(result)
        return result
```

點選對應的 `demo ormcache` button,

![alt tag](https://i.imgur.com/SV6uZOx.png)

你會看到只有第一次會輸出 logger, 第二次開始就不會輸出了, 因為他直接從 cache 中取資料.

![alt tag](https://i.imgur.com/fqQ3zWb.png)

還可以依照 user 快取,

```python
......
    @tools.ormcache('self.env.uid')
    def demo_ormcache_by_env(self):
        result = '{} {} env uid'.format('hello', 'world')
        _logger.warning(result)
        return result
```

測試方法就是分別登入兩個 user, 你會發現 user 自己會擁有自己快取.

甚至可以依照語言去快取 (注意, 這邊是使用 `ormcache_context` )

```python
......
    @tools.ormcache_context(keys=('lang',))
    def demo_ormcache_context(self):
        result = '{} {} context'.format('hello', 'world')
        _logger.warning(result)
        return result
```

測試方法就是多建立一個語言, 你會發現語言之間也會擁有自己的快取.

還有一個是 `ormcache_multi`, 但這個似乎比較少用.

清除 cache 的方式

```python
......
 def demo_clear_cache(self):
    # self.env[model_name].clear_caches()
    self.env['demo.cache'].clear_caches()
    raise ValidationError('clear cache')
```

這邊要注意一下, 當你重新啟動 odoo 時, cache 也會自動被清除哦:exclamation::exclamation:

然後我們也可以去查看 cache 的狀況,

透過 htop 去查看他的 PID, 然後發送 SIGUSR1 訊號,

如果不知道甚麼是 htop, 可參考 [Linux htop tutorial](https://github.com/twtrubiks/linux-note/tree/master/htop-tutorial)

```cmd
kill -SIGUSR1 PID
```

![alt tag](https://i.imgur.com/xyge3Zx.png)
