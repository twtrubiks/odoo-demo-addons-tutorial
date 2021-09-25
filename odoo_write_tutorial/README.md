# odoo 觀念 - odoo12 和 odoo14 的 ORM Write 差異

[Youtube Tutorial - odoo 觀念 - odoo12 和 odoo14 的 ORM Write 差異]()

這隻影片主要是要和大家說明

odoo12 和 odoo13, odoo14 中的 orm write 有一點點稍微不同:smirk:

## 說明

一樣使用 shell 的方式來看看哪裡不同, 如果不了解 odoo shell 請參考以下文章

[odoo - 如何透過 log_level 了解 ORM RAW SQL](https://github.com/twtrubiks/odoo-docker-tutorial#odoo---%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8E-log_level-%E4%BA%86%E8%A7%A3-orm-raw-sql)

這邊使用 `sale.order` 來示範,

```python
order = self.env['sale.order'].browse(2)
```

如果我們想要更新或寫入資料, 可以使用以下兩種寫法,

方法一

```python
order.name = 'name'
order.note = 'note'
```

方法二

```python
order.write({'name': 'name', 'note':'note'})
```

在 odoo13, odoo14 中, 方法一 和 方法二 都是執行一次 SQL,

也就是兩個都一樣的.

(在 odoo13, odoo14 中, 多了 `flush()`, odoo12 沒有這個方法).

但是在 odoo12 中, 方法一會執行**兩次** SQL, 方法二會執行一次 SQL,

所以在 odoo12 中, 如果想要一次寫入多欄位的資料,

請儘量使用第二種方法.(效能會稍微好一點:smile:)

結論說完了, 接下來實際執行一次來驗證:smirk:

在 odoo14 中,

方法一 (執行了一次 SQL), 需要多執行 `flush()`

![alt tag](https://i.imgur.com/XYTMht9.png)

方法二 (執行了一次 SQL), 需要多執行 `flush()`

![alt tag](https://i.imgur.com/fVlVvYY.png)

在 odoo12 中,

方法一 (執行了**兩次** SQL)

![alt tag](https://i.imgur.com/Kjob5FY.png)

方法二 (執行了一次 SQL)

![alt tag](https://i.imgur.com/ZdPXQzX.png)

最後之前說過了, 如果在 `shell` 中要把資料永久的保存進 db,

要執行 `self.env.cr.commit()`.
