# Odoo Domain 教學

[Youtube Tutorial - odoo 手把手教學 - Odoo Domain 教學](https://youtu.be/Gr8eXYRSrtM)

先附上 odoo [domains](https://www.odoo.com/documentation/12.0/howtos/backend.html#domains) 的文件

首先, odoo 是使用 波蘭表示法. (小技巧, 從後面看回來)

這邊先說一下規則, 等等會帶大家看,

從 右 向 左 開始看, 當遇到運算符號的時候, 找它的右側的兩個值去做運算.

符號說明如下,

`&` -> `AND` (這是預設邏輯，可以不寫, 不寫就代表 `&`)

`|` -> `OR`

`!` -> `NOT`

來看幾個範例

```python
domain = [A, B]

domain = ['&', A, B]
```

上述兩個都是 A AND B

```python
domain = ['&', A, '&', B, C]
```

上述代表 A AND (B AND C)

```python
domain = [A, B, C]
```

上述代表 (A AND B) AND C

如果都是 AND 的情況下, 上述兩個可以看成是相等的.

```python
domain = ['|', A, B, C]
```

分解如下

```text
從右邊開始看

-> (A OR B), C

-> (A OR B) AND C
```

上述代表 (A OR B) AND C

```python
domain = [A, B, '|', C, D]
```

上述代表 (A AND B) AND (C OR D)

分解如下

```text
從右邊開始看

-> A, B, (C OR D)

-> A, B AND (C OR D)

-> A AND B AND (C OR D)
```

```python
domain = ['|', A, B, C, D]
```

上述代表 ((A OR B) AND C ) AND D

分解如下

```text
從右邊開始看

-> (A OR B), C, D

-> (A OR B) AND C, D

-> (A OR B) AND C AND D
```

接下來看一個比較複雜的

```python
domain = ['|', A, '!', '&', B, C]
```

上述代表 A OR ( NOT B OR NOT C)

也等於 A OR ( NOT (B AND C))

分解如下

```text
從右邊開始看

-> '|', A, '!', (B AND C)

-> '|', A, NOT (B AND C)

-> A OR ( NOT (B AND C) )
```

接下來看一個更複雜的

```python
domain = [
     '&', '&', '&',
     A,
     B,
     C,
     '|', '&',
     D,
     E,
     F,
]
```

上述代表 A AND B AND C AND ((D AND E) OR F)

分解如下

```text
從右邊開始看

-> '&', '&', '&', A, B, C, '|', (D AND E), F

-> '&', '&', '&', A, B, C, (D AND E) OR F

-> '&', '&', '&', A, B, C AND ((D AND E) OR F)

-> A AND B AND C AND ((D AND E) OR F)
```

推薦這個網站, 他可以幫助你檢查邏輯是不是相同的 [wolframalpha](https://www.wolframalpha.com)

如果你和我一樣實在還是搞不懂 波蘭表示法

可以嘗試另外一個土法煉鋼的方法, 看看下面這個例子,

透過之前教過的 [odoo - 如何透過 log_level 了解 ORM RAW SQL](https://github.com/twtrubiks/odoo-docker-tutorial#odoo---%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8E-log_level-%E4%BA%86%E8%A7%A3-orm-raw-sql) 搭配 shell,

在 odoo shell 底下執行,

```python
domain = [('parent_id', '=', 9), ('company_id', '=', 1),
          '|', ('city','=','Columbia'), ('city','=','Jonesboro')]
self.env['res.partner'].search(domain)
```

會輸出以下的 sql ( 經過 格式化 處理 )

```sql
SELECT "res_partner".id
FROM "res_partner"
WHERE (((("res_partner"."active" = TRUE)
         AND ("res_partner"."parent_id" = 9))
        AND ("res_partner"."company_id" = 1))
       AND (("res_partner"."city" = 'Columbia')
            OR ("res_partner"."city" = 'Jonesboro')))
ORDER BY "res_partner"."display_name"
```

我們先把 domain 改成比較簡單的格式

```python
domain = [A, B, '|', C, D]
```

再把 SQL 也修改一下

```sql
SELECT "res_partner".id
FROM "res_partner"
WHERE (((("res_partner"."active" = TRUE)
         AND A)
        AND B)
       AND (C
            OR D))
ORDER BY "res_partner"."display_name"
```

再把不相關的移除就變成了我們想要看到的邏輯了

(A AND B) AND (C OR D)

延伸閱讀 [Odoo Domain Operator 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/domain_operator_tutorial)

## 更進階複雜的查詢

有時候我們會需要更複雜的查詢, 這時候可以這樣使用

`from odoo.osv.expression import AND, OR`

```python
from odoo.osv.expression import AND, OR
condition1 = [('login', '=', 'admin')]
condition2 = [('partner_id', '=', 7)]

combined_condition_or = OR([condition1, condition2])
combined_condition_and = AND([condition1, condition2])

self.env['res.users'].search(combined_condition_or)
self.env['res.users'].search(combined_condition_and)
```