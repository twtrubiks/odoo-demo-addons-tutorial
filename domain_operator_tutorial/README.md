# Odoo Domain Operator 教學

[Youtube Tutorial - odoo 手把手教學 - Odoo Domain Operator 教學(等待新增)]()

建議在閱讀這篇文章前, 先了解這些概念
[Odoo Domain 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/odoo_domain_tutorial), [odoo - 如何透過 log_level 了解 ORM RAW SQL](https://github.com/twtrubiks/odoo-docker-tutorial#odoo---%E5%A6%82%E4%BD%95%E9%80%8F%E9%81%8E-log_level-%E4%BA%86%E8%A7%A3-orm-raw-sql)

主要是要介紹 sql `like` 的一些變化,

請隨便找一個 model , 進入 `shell` 測試, 例如這邊使用 `res.partner`,

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
domain = [('name', 'ilike', 'twtrubiks')]
```

```sql
WHERE "name"::text ilike '%twtrubiks%'
```

範例三

```python
domain = [('name', '=like', 'twtrubiks')]
```

在這種情況下, `=like` 和 `=` 是一樣的.

```sql
WHERE "name"::text like 'twtrubiks'
```

範例四

```python
domain = [('name', '=ilike', 'twtrubiks')]
```

```sql
WHERE "name"::text ilike 'twtrubiks'
```

在這種情況下, `=ilike` 和 `=` 是一樣的.

範例五

```python
domain = [('name', '=like', 'twtrubiks%')]
```

```sql
WHERE "name"::text like 'twtrubiks%'
```

範例六

```python
domain = [('name', '=ilike', 'twtrubiks%')]
```

```sql
WHERE "name"::text ilike 'twtrubiks%')
```
