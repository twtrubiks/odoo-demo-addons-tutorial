# odoo 觀念 - Translating 翻譯教學 i18n

建議觀看影片, 會更清楚:smile:

* [Youtube Tutorial - odoo 觀念 - Translating 翻譯教學 i18n - part1](https://youtu.be/_gGmwgk8250) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_i18n_expense_tutorial#%E5%9F%BA%E6%9C%AC%E8%A7%80%E5%BF%B5)

* [Youtube Tutorial - odoo 觀念 - Translating 翻譯教學 i18n - part2](https://youtu.be/Ka7ucdDnfHA) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_i18n_expense_tutorial#%E4%BD%BF%E7%94%A8%E7%A8%8B%E5%BC%8F%E7%A2%BC%E7%BF%BB%E8%AD%AF)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 Translating 翻譯教學,

也就是 i18n 的資料夾, 會教你如何繼承(覆蓋)它.

官方文件可參考 [translations.html](https://www.odoo.com/documentation/12.0/reference/translations.html)

## 基本觀念

* [Youtube Tutorial - odoo 觀念 - Translating 翻譯教學 i18n - part1](https://youtu.be/_gGmwgk8250)

先和大家說如果你要開啟其他語言要如何開啟,

Translations -> Languages 選擇要啟用的語言即可

![alt tag](https://i.imgur.com/H1X8nP2.png)

也可以使用指令的方式啟用語言

```cmd
python3 odoo-bin -d odoo --load-language=zh_TW -c odoo.conf
```

在需要翻譯的頁面底下選擇 Technical Translation

這邊強烈建議大家先切換語系到**英文**, 再下去進行翻譯, 不然很容易怪怪的:joy:

![alt tag](https://i.imgur.com/tYUDr68.png)

就會看到以下的畫面

![alt tag](https://i.imgur.com/6wm36X2.png)

## 後台設定

當然也可以從 odoo 後台管理這些翻譯檔案

Translations -> Import / Export

![alt tag](https://i.imgur.com/HnCWsc9.png)

Export Translation

匯出 po 檔案,

![alt tag](https://i.imgur.com/pWaJYC1.png)

也可以使用指令的方式匯出 po 檔案

```cmd
python3 odoo-bin -d odoo --i18n-export=hr_expense.po --modules=hr_expense -c odoo.conf
```

指定匯出 po 檔案(特定語言), 注意, odoo 必須已經安裝對應的語言

```cmd
python3 odoo-bin -d odoo --i18n-export=zh_TW.po --modules=hr_expense --language=zh_TW -c odoo.conf
```

執行完後, 可查看路徑底下是否有對應的檔案.

Import Translation

匯入 po 檔案,

注意 :exclamation::exclamation: Overwrite Existing Terms 請記住一定要打勾, 否則不會生效.

![alt tag](https://i.imgur.com/TGevO7f.png)

也可以使用指令的方式匯入 po 檔案,

請記得將 zh_TW.po (檔名可自訂) 放入任意 addons 的路徑中.

```cmd
python3 odoo-bin -d odoo --i18n-import=zh_TW.po --language=zh_TW -c odoo.conf
```

如果沒有生效, 請再加上 `--i18n-overwrite`.

## 使用程式碼翻譯

[Youtube Tutorial - odoo 觀念 - Translating 翻譯教學 i18n - part2](https://youtu.be/Ka7ucdDnfHA)

除了從 odoo 的後台翻譯之外, 也可以從程式碼翻譯,

也就是教大家如何去覆寫(覆蓋) po 翻譯檔案(i18n 資料夾),

這邊使用覆蓋內建的 `hr_expense` 當作範例,

只需要建立一個 addons, 然後有 i18n 的資料夾, 直接覆蓋掉需要的翻譯即可

[i18n/zh_TW.po](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/master/demo_i18n_expense_tutorial/i18n/zh_TW.po)

```po
#. module: hr_expense
#: model:ir.model.fields,field_description:hr_expense.field_hr_expense__name
msgid "Description"
msgstr "測試描述"
```

直接安裝即可

```cmd
python3 odoo-bin -i demo_i18n_expense_tutorial -d odoo -c odoo.conf
```

如果你有修改(更新)翻譯的 po 檔案, 指令需要加上 `--i18n-overwrite`

```cmd
python3 odoo-bin --i18n-overwrite -u demo_i18n_expense_tutorial -d odoo -c odoo.conf
```

如果不想用指令更新, 也可以從 odoo 的後台進行更新, 注意, 更新的方法不是更新 addons.

是先重起 odoo, 然後到 odoo 後台的 Load a Translation (如下圖)

![alt tag](https://i.imgur.com/E5X1h7I.png)

選擇對應的語言,

注意 :exclamation::exclamation: Overwrite Existing Terms 請記住一定要打勾, 否則不會生效.

![alt tag](https://i.imgur.com/2FbZie6.png)

如果更新時出現以下錯誤訊息

```text
psycopg2.ProgrammingError: ON CONFLICT DO UPDATE command cannot affect row a second time
HINT:  Ensure that no rows proposed for insertion within the same command have duplicate constrained values.
```

![alt tag](https://i.imgur.com/1OVRBIv.png)

代表你的 po 檔案裡面可能有重複翻譯的字段, 可以使用 terminal 找出是哪個 addons 的翻譯檔出錯 (如下圖).

![alt tag](https://i.imgur.com/LTgKdx8.png)



