# Odoo Domain Operator 教學

建議在閱讀這邊文章前, 可以先閱讀這裡篇文章
[Odoo Domain 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/odoo_domain_tutorial), [odoo - 如何透過 log_level 了解 ORM RAW SQL](https://github.com/twtrubiks/odoo-docker-tutorial#odoo---%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8E-log_level-%E4%BA%86%E8%A7%A3-orm-raw-sql)

隨便找一個 model 測試

```python
self.env['res.partner'].search(domain)
```

先說明一下,

`like` 區分大小寫

`ilike` 不區分大小寫

範例一

```python
domain = [('name', 'like', 'twtrubiks')]
```

```sql
WHERE "name"::text like '%twtrubiks%'
```

`"name"::text` 這個是 Type Casts, 可參考 [postgresql - 4.2.9. Type Casts](https://www.postgresql.org/docs/10/sql-expressions.html#SQL-SYNTAX-TYPE-CASTS)

以下兩種寫法都可以, 主要是轉換類型.

例如這邊是將 `name` 轉換成 `text`

```sql
CAST ( expression AS type )
expression::type
```

範例二

```python
domain = [('name', '=like', 'twtrubiks')]
```

`=like` 其實幾乎和 `=` 是一樣的.

```sql
WHERE "name"::text like 'twtrubiks'
```

範例三

```python
domain = [('name', 'ilike', 'twtrubiks')]
```

```sql
WHERE "name"::text ilike '%twtrubiks%'
```

範例四

```python
domain = [('name', '=ilike', 'twtrubiks')]
```

```sql
WHERE "name"::text ilike 'twtrubiks'
```

範例五

```python
domain = [('name', '=ilike', 'twtrubiks%')]
```

```sql
WHERE "name"::text ilike 'twtrubiks%')
```

範例六

```python
domain = [('name', '=like', 'twtrubiks%')]
```

```sql
WHERE "name"::text like 'twtrubiks%'
```
