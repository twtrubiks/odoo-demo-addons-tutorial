# odoo index 教學

odoo 的 index 主要就是 postgresql 的 index,

所以讓我們來看看 postgresql 的官方文件吧:smile:

首先, 請先看看 [postgresql-explain-plan](https://use-the-index-luke.com/sql/explain-plan/postgresql/operations),

然後 Scan 的方式也有多種, 可參考 [postgresql-explain](https://docs.postgresql.tw/the-sql-language/performance-tips/using-explain)

`Seq Scan` `Index Scan` `Index Only Scan (since PostgreSQL 9.2)`

`Bitmap Index Scan` `Bitmap Heap Scan` `Recheck Cond`

接著看一下 odoo sourcecode 中的 [odoo/fields.py](odoo/fields.py),

你會發現, 預設的 index 為 `False`

```python
......
class Field(MetaField('DummyField', (object,), {})):
    """
	......
    :param bool index: whether the field is indexed in database. Note: no effect
        on non-stored and virtual fields. (default: ``False``)

	......
    """

    ......

    store = True                        # whether the field is stored in database
    index = False                       # whether the field is indexed in database
......

```

使用方法也很簡單, 在需要的 fields 中加上 `index=True` 即可,

```python
sequence = fields.Integer(index=True, help="Gives the sequence order", default=1)
```

確認 index 有成功加入的方法,

可以從 odoo 的後台觀看

![alt tag](https://i.imgur.com/CfAfRxr.png)

也可以從工具(pgadmin4)觀看

![alt tag](https://i.imgur.com/VQ3ffeG.png)

使用 `explain` 指令查看 explain

```sql
explain
SELECT * FROM demo_expense_tutorial where name='123';
```

![alt tag](https://i.imgur.com/nP1W2JU.png)

也可以使用工具(pgadmin4)觀看

![alt tag](https://i.imgur.com/AKHXfym.png)

但這邊要注意一下:exclamation: 不是你有設定 index, 就代表 postgresql 會去使用你的 index,

它可能會根據你的資料量決定要不要使用 index, 所以你會發現儘管你設定了 index,

但它卻還是使用 `Seq Scan`, 因為 postgresql 的演算法可能覺得在這個情況下 `Seq Scan` 更快:smile:
