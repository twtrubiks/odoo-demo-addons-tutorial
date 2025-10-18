# Odoo 19 CLI

也推薦看官方的相關影片

* [Simplifying the CLI, one command at a time](https://www.odoo.com/event/odoo-experience-2025-6601/track/simplifying-the-cli-one-command-at-a-time-8375)

在 Odoo 19 中, CLI 有增加不少, 但也不用擔心舊的指令不使用, 因為有向下兼容.

新的 CLI 功能被切成更小塊, 且預設的新指令不啟動 odoo server,

詳細的文檔可參考 [Command-line interface (CLI)](https://www.odoo.com/documentation/19.0/developer/reference/cli.html)

## db

`init`

```cmd
./odoo-bin db -c odoo.conf init new-db
```

`rename`

```cmd
./odoo-bin db -c odoo.conf rename new-db new-db-rename
```

`duplicate`

```cmd
./odoo-bin db -c odoo.conf duplicate new-db-rename new-db-duplicate
```

如果想要想要加上 neutralize, 使用 `-n` neutralize

```cmd
./odoo-bin db -c odoo.conf duplicate new-db-rename new-db-duplicate -n
```

`drop`

```cmd
./odoo-bin db -c odoo.conf drop new-db-duplicate
```

`dump`

zip

```cmd
./odoo-bin db -c odoo.conf dump --format zip new-db /home/twtrubiks/下載/new-db.zip
```

dump

```cmd
./odoo-bin db -c odoo.conf dump --format dump new-db /home/twtrubiks/下載/new-db.dump
```

`load`

```cmd
./odoo-bin db -c odoo.conf load load-new-db /home/twtrubiks/下載/new-db.zip
```

## module

`install`

```cmd
./odoo-bin module install hr_expense -d odoo19 -c odoo.conf
```

`upgrade`

```cmd
./odoo-bin module upgrade hr_expense -d odoo19 -c odoo.conf
```

你可能會問為什麼已經有了 `-i <modules>` `-u <modules>` 還要有這個,

你可以把 module 想程式單純管理模組的工具, 然後原本的 `-i` `-u` 是連同起 server 一起.

`uninstall` (終於有移除的指令了, 以前第三方才有這個功能)

```cmd
./odoo-bin module uninstall hr_expense -d odoo19 -c odoo.conf
```
