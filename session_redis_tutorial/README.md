# odoo session_redis 教學

[Youtube Tutorial - odoo 手把手教學 - session_redis 教學](https://youtu.be/WD7W9RwusS0)

## 簡介

這篇主要是教大家如何在 odoo 中使用 redis,

就使用現成的 addons [https://apps.odoo.com/apps/modules/12.0/session_redis/](https://apps.odoo.com/apps/modules/12.0/session_redis/) 來示範.

在開始介紹前, 要知道在 odoo 中, session 是保存在實體檔案 (filesystem) 的,

通常也就是 [odoo.conf](https://github.com/twtrubiks/odoo-docker-tutorial/blob/master/config/odoo.conf) 中的 data_dir 路徑,

如果你到該路徑的 sessions 底下查看, 會看到很多 `.sess` 檔

![alt tag](https://i.imgur.com/SxfvBfE.png)

如果你把這些檔案全部都刪除, 你會發現每個 user 都被登出了,

因為 odoo 用這些檔案決定使用者多久後會被登出(也就是使用這些session).

這個 addon 只要是將保存在 file 中的 session 全部改成存在 redis 中,

你可能會問我有甚麼好處:question:

速度絕對變快, 然後如果你有多 odoo 的機器, 也比較好方便統一管理 session.

## redis

redis 的部份這邊我就簡單放個 [docker-compose.yml](docker-compose.yml),

因為之前在 [django-docker-redis-tutorial](https://github.com/twtrubiks/django-docker-redis-tutorial) 都有介紹過了.

docker redis 的 image 是使用 [https://hub.docker.com/_/redis](https://hub.docker.com/_/redis)

直接執行即可

```cmd
docker-compose up -d
```

## session_redis

有了這些觀念, 接下來就來看 [https://apps.odoo.com/apps/modules/12.0/session_redis/](https://apps.odoo.com/apps/modules/12.0/session_redis/)

請先把 addon 下載下來, 然後放到目錄資料夾底下,

之後先安裝 redis 套件,

```cmd
pip install redis
```

接著設定環境變數,

暫時的設定環境參數(退出 shell 會自動消失)

```cmd
export ODOO_SESSION_REDIS=1
export ODOO_SESSION_REDIS_COPY_EXISTING_FS_SESSIONS=1
export ODOO_SESSION_REDIS_PURGE_EXISTING_FS_SESSIONS=1

# 還有很多設定請參考文件說明
export ODOO_SESSION_REDIS_EXPIRATION
```

如果要查看設定

```cmd
echo $ODOO_SESSION_REDIS
echo $ODOO_SESSION_REDIS_COPY_EXISTING_FS_SESSIONS
```

最後要到 [odoo.conf](https://github.com/twtrubiks/odoo-docker-tutorial/blob/master/config/odoo.conf) 中多設定 `server_wide_modules`,

```conf
......
server_wide_modules=base,web,session_redis
......
```

或是也可以寫在 command line 上 ( 兩者擇一即可 ),

```cmd
python3 odoo-bin -d odoo -c odoo.conf --load=base,web,session_redis
```

`--load` 和 `server_wide_modules` 是一樣的.

可參考原始碼中的 `odoo/tools/config.py`

```python
class configmanager(object):
    def __init__(self, fname=None):
        ......
        group.add_option("--load", dest="server_wide_modules", help="Comma-separated list of server-wide modules.", my_default='base,web')
        ......
```

`session_redis` 就是這個 addon 的名稱,

其中, `base,web` 是預設的, 可參考以下文件

[https://odoo-development.readthedocs.io/en/latest/admin/server_wide_modules.html](https://odoo-development.readthedocs.io/en/latest/admin/server_wide_modules.html)

預設為 `base,web` 也可參考原始碼中的 `addons/web/controllers/main.py`

```python
......
def module_boot(db=None):
    server_wide_modules = odoo.conf.server_wide_modules or []
    serverside = ['base', 'web']
    ......

```

關於 `load` 的說明還可以參考官方文件,

[https://www.odoo.com/documentation/15.0/developer/misc/other/cmdline.html#cmdoption-odoo-bin-load](https://www.odoo.com/documentation/15.0/developer/misc/other/cmdline.html#cmdoption-odoo-bin-load)

`--load <modules>`

```text
list of server-wide modules to load. Those modules are supposed to provide features not necessarily tied to a particular database. This is in contrast to modules that are always bound to a specific database when they are installed (i.e. the majority of Odoo addons). Default is base,web.
```

將著啟動 odoo, 然後 **不需要** 安裝 `session_redis`.

( 因為已經透過 `server_wide_modules` 的方式啟動了 )

理論上, 這時候你的 `data_dir` 中的 sessions 資料夾應該是空的.

然後你可以 access redis 確認是否有資料寫入,

```cmd
docker exec -it <container id> redis-cli
```

查看全部的 keys

```cmd
keys *
```

查看某個 key 的資料

```cmd
get <key>
```

![alt tag](https://i.imgur.com/7i4UT2h.png)

也可以透過 `ttl` 查看還有多久這個 session 會過期

```cmd
ttl <key>
```

刪除全部的 keys

```cmd
flushall
```

如果 redis 中也有資料, 這樣就對表成功了:smile:

成功將 session 從檔案中移動至 redis,

新的 session 也都會保存在 redis 裡面.

如果你想看實作, 可以再參考 [https://apps.odoo.com/apps/modules/12.0/session_redis/](https://apps.odoo.com/apps/modules/12.0/session_redis/).
