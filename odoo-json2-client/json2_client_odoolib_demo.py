"""
Odoo 19 JSON-2 API 測試腳本 - 使用 odoo-client-lib

https://pypi.org/project/odoo-client-lib/2.0.0/

安裝：
pip install odoo-client-lib==2.0.0

使用方法：
1. 設置環境變數：
   export ODOO_URL="http://localhost:8069"
   export ODOO_API_KEY="your_api_key_here"
   export ODOO_DATABASE="your_database"  # 可選，多資料庫環境需要

2. 執行測試：
   python3 json2_client_odoolib_demo.py
"""

import os
import sys
import logging
from datetime import datetime
import odoolib

# 設定 logging
logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    format='%(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)


def test_connection(connection):
    """測試連線"""
    _logger.info("\n=== 測試連線 ===")
    try:
        # 測試簡單的搜尋
        user_model = connection.get_model('res.users')
        user_ids = user_model.search([('id', '=', 2)], limit=1)
        if user_ids:
            _logger.info(f"✅ 連線成功！找到用戶 ID: {user_ids[0]}")
            return True
        else:
            _logger.warning("⚠️  連線成功但找不到管理員用戶")
            return True
    except Exception as e:
        _logger.error(f"❌ 連線失敗: {e}")
        return False


def test_crud_operations(connection):
    """測試 CRUD 操作"""
    _logger.info("\n=== 測試 CRUD 操作 ===")
    test_partner_id = None
    partner_model = connection.get_model('res.partner')

    try:
        # 1. CREATE - 創建測試合作夥伴
        _logger.info("\n1. CREATE - 創建合作夥伴")
        test_partner_id = partner_model.create({
            'name': f'API 測試客戶 {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'is_company': True,
            'email': 'api_test@example.com',
            'phone': '+886-2-12345678',
            'comment': '透過 JSON-2 API 創建的測試資料'
        })
        _logger.info(f"   ✅ 成功創建合作夥伴，ID: {test_partner_id}")

        # 2. READ - 讀取剛創建的記錄
        _logger.info("\n2. READ - 讀取合作夥伴")
        partner = partner_model.read(test_partner_id, ['name', 'email', 'phone', 'comment'])
        if partner:
            _logger.info(f"   ✅ 成功讀取:")
            _logger.info(f"      名稱: {partner['name']}")
            _logger.info(f"      Email: {partner['email']}")
            _logger.info(f"      電話: {partner['phone']}")

        # 3. UPDATE - 更新記錄
        _logger.info("\n3. UPDATE - 更新合作夥伴")
        success = partner_model.write(test_partner_id, {
            'phone': '+886-2-87654321',
            'website': 'https://api-test.example.com',
            'comment': '已更新 - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        if success:
            _logger.info("   ✅ 成功更新合作夥伴資料")

            # 驗證更新
            updated = partner_model.read(test_partner_id, ['phone', 'website'])
            if updated:
                _logger.info(f"      新電話: {updated['phone']}")
                _logger.info(f"      新網站: {updated['website']}")

        # 4. SEARCH - 搜尋記錄
        _logger.info("\n4. SEARCH - 搜尋合作夥伴")
        found_ids = partner_model.search(
            [('name', 'ilike', 'API 測試客戶%')],
            limit=5
        )
        _logger.info(f"   ✅ 找到 {len(found_ids)} 筆符合的記錄")

        # 5. SEARCH_READ - 搜尋並讀取
        _logger.info("\n5. SEARCH_READ - 搜尋並讀取")
        test_partners = partner_model.search_read(
            [('name', 'ilike', 'API 測試客戶%')],
            ['name', 'create_date'],
            limit=3,
            order='create_date desc'
        )
        _logger.info(f"   ✅ 找到 {len(test_partners)} 筆測試資料:")
        for p in test_partners:
            _logger.info(f"      - {p['name']} (建立於 {p['create_date']})")

        # 6. DELETE - 刪除測試資料
        _logger.info("\n6. DELETE - 刪除測試資料")
        if test_partner_id:
            success = partner_model.unlink(test_partner_id)
            if success:
                _logger.info(f"   ✅ 成功刪除測試合作夥伴 ID: {test_partner_id}")
                test_partner_id = None

    except Exception as e:
        _logger.error(f"❌ CRUD 測試失敗: {e}")
        # 清理測試資料
        if test_partner_id:
            try:
                partner_model.unlink(test_partner_id)
                _logger.warning(f"   ⚠️  已清理測試資料 ID: {test_partner_id}")
            except:
                pass


def test_many2many_operations(connection):
    """測試 Many2Many 欄位操作"""
    _logger.info("\n=== 測試 Many2Many 欄位操作 ===")
    test_user_id = None
    new_user_id = None
    user_model = connection.get_model('res.users')
    group_model = connection.get_model('res.groups')

    try:
        # 1. 創建測試用戶
        _logger.info("\n1. 創建測試用戶")
        test_user_id = user_model.create({
            'name': f'M2M 測試用戶 {datetime.now().strftime("%H%M%S")}',
            'login': f'test_m2m_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
            'email': f'test_m2m_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
        })
        _logger.info(f"   ✅ 創建測試用戶 ID: {test_user_id}")

        # 2. 搜尋可用的群組
        _logger.info("\n2. 搜尋可用群組")
        all_groups = group_model.search([], limit=5)
        _logger.info(f"   ✅ 找到 {len(all_groups)} 個群組可供測試")

        # 列出群組名稱
        if all_groups:
            # 讀取多筆記錄需要逐個讀取，因為 read 只接受單個 ID
            _logger.info("   群組列表：")
            for group_id in all_groups:
                group_data = group_model.read(group_id, ['name', 'display_name'])
                _logger.info(f"      - ID {group_data['id']}: {group_data['display_name']}")

        # 3. 使用 (4, id) 添加群組（連結現有記錄）
        _logger.info("\n3. 添加群組 - 使用 (4, id)")
        if all_groups:
            user_model.write(test_user_id, {
                'group_ids': [(4, all_groups[0])]
            })
            _logger.info(f"   ✅ 添加群組 ID: {all_groups[0]}")

            # 讀取驗證
            user_data = user_model.read(test_user_id, ['group_ids'])
            _logger.info(f"      目前群組數量: {len(user_data['group_ids'])}")

        # 4. 測試 Many2Many 在創建時設定
        _logger.info("\n4. 創建時設定 M2M 欄位")
        if len(all_groups) >= 2:
            new_user_id = user_model.create({
                'name': f'M2M 新用戶 {datetime.now().strftime("%H%M%S")}',
                'login': f'new_m2m_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
                'group_ids': [(6, 0, all_groups[:2])]  # 創建時直接設定群組
            })
            _logger.info(f"   ✅ 創建新用戶並設定 {len(all_groups[:2])} 個群組")

    except Exception as e:
        _logger.error(f"❌ Many2Many 測試失敗: {e}")
    finally:
        # 清理測試資料
        user_ids_to_clean = [uid for uid in [test_user_id, new_user_id] if uid]
        for user_id in user_ids_to_clean:
            try:
                user_model.unlink(user_id)
                _logger.info(f"\n✅ 清理測試用戶 ID: {user_id}")
            except Exception as e:
                _logger.warning(f"⚠️  無法清理測試用戶 {user_id}: {e}")


def test_model_methods(connection):
    """測試呼叫模型方法"""
    _logger.info("\n=== 測試呼叫模型方法 ===")

    try:
        # 呼叫 get_company_currency_id - 取得公司貨幣
        _logger.info("\n呼叫 res.users.get_company_currency_id")
        user_model = connection.get_model('res.users')

        # 使用 execute 方法呼叫自定義方法
        currency_id = user_model.get_company_currency_id()
        _logger.info(f"   ✅ 公司貨幣 ID: {currency_id}")

        # 可選：讀取貨幣資訊
        if currency_id:
            currency_model = connection.get_model('res.currency')
            currency_info = currency_model.read(currency_id, ['name', 'symbol'])
            if currency_info:
                _logger.info(f"   ✅ 貨幣資訊: {currency_info['name']} ({currency_info['symbol']})")

    except Exception as e:
        _logger.error(f"❌ 模型方法測試失敗: {e}")


def test_error_handling(connection):
    """測試錯誤處理 - 符合 Odoo 標準錯誤類型"""
    _logger.info("\n=== 測試錯誤處理 ===")

    # 1. 測試無效的模型 (UserError 或類似錯誤)
    _logger.info("\n1. 測試無效的模型")
    try:
        invalid_model = connection.get_model('invalid.model')
        invalid_model.search([])
        _logger.error("   ❌ 應該要觸發錯誤")
    except Exception as e:
        error_msg = str(e)
        if 'does not exist' in error_msg or 'NotFound' in error_msg or 'UserError' in error_msg:
            _logger.info("   ✅ 正確捕獲無效模型錯誤")
            _logger.debug(f"      錯誤訊息: {error_msg[:100]}")
        else:
            _logger.warning(f"   ⚠️  錯誤類型不符預期: {e}")

    # 2. 測試無效的方法
    _logger.info("\n2. 測試無效的方法")
    try:
        partner_model = connection.get_model('res.partner')
        partner_model.invalid_method()
        _logger.error("   ❌ 應該要觸發錯誤")
    except Exception as e:
        error_msg = str(e)
        if 'NotFound' in error_msg or 'does not have' in error_msg or 'AttributeError' in error_msg:
            _logger.info("   ✅ 正確捕獲無效方法錯誤")
            _logger.debug(f"      錯誤訊息: {error_msg[:100]}")
        else:
            _logger.warning(f"   ⚠️  錯誤類型不符預期: {e}")

    # 3. 測試缺少必要參數
    _logger.info("\n3. 測試缺少必要參數")
    try:
        partner_model = connection.get_model('res.partner')
        # search 需要 domain 參數
        partner_model.search()  # 缺少 domain 參數
        _logger.error("   ❌ 應該要觸發錯誤")
    except Exception as e:
        error_msg = str(e).lower()
        if 'missing' in error_msg or 'required' in error_msg or 'typeerror' in error_msg:
            _logger.info("   ✅ 正確捕獲缺少參數錯誤")
            _logger.debug(f"      錯誤訊息: {str(e)[:100]}")
        else:
            _logger.warning(f"   ⚠️  錯誤類型不符預期: {e}")

    # 4. 測試權限錯誤 (AccessError)
    _logger.info("\n4. 測試權限錯誤 (AccessError)")
    try:
        # ir.cron 通常需要管理員權限
        cron_model = connection.get_model('ir.cron')
        cron_model.search([])
        _logger.warning("   ⚠️  用戶可能有管理員權限，無法測試權限錯誤")
    except Exception as e:
        error_msg = str(e)
        if 'AccessError' in error_msg or 'Access' in error_msg or '403' in error_msg:
            _logger.info("   ✅ 正確捕獲權限錯誤 (AccessError)")
            _logger.debug(f"      錯誤訊息: {error_msg[:100]}")
        else:
            _logger.warning(f"   ⚠️  可能的權限錯誤: {e}")

    # 5. 測試不存在的記錄 (MissingError)
    _logger.info("\n5. 測試不存在的記錄 (MissingError)")
    try:
        # 嘗試讀取不存在的記錄
        partner_model = connection.get_model('res.partner')
        partner_model.read(999999999, ['name'])
        _logger.warning("   ⚠️  記錄可能存在")
    except Exception as e:
        error_msg = str(e)
        if 'MissingError' in error_msg or 'does not exist' in error_msg or '404' in error_msg:
            _logger.info("   ✅ 正確捕獲記錄不存在錯誤 (MissingError)")
            _logger.debug(f"      錯誤訊息: {error_msg[:100]}")
        else:
            _logger.info(f"   ✅ 捕獲到錯誤: {e}")

    # 6. 測試資料驗證錯誤 (ValidationError)
    _logger.info("\n6. 測試資料驗證錯誤 (ValidationError)")
    try:
        # 嘗試創建重複的用戶登入名稱
        user_model = connection.get_model('res.users')
        user_model.create({
            'name': 'Test User',
            'login': 'admin'  # admin 通常已存在
        })
        _logger.warning("   ⚠️  可能沒有觸發驗證錯誤")
    except Exception as e:
        error_msg = str(e)
        if 'ValidationError' in error_msg or 'already exists' in error_msg or 'duplicate' in error_msg.lower():
            _logger.info("   ✅ 正確捕獲資料驗證錯誤 (ValidationError)")
            _logger.debug(f"      錯誤訊息: {error_msg[:100]}")
        else:
            _logger.info(f"   ✅ 捕獲到錯誤: {e}")


def main():
    """主測試函數"""
    _logger.info("=" * 60)
    _logger.info("Odoo 19 JSON-2 API 測試腳本 (使用 odoolib)")
    _logger.info("=" * 60)

    # 從環境變數讀取配置
    hostname = os.environ.get('ODOO_URL', 'http://localhost:8069')
    # 處理 URL，提取主機名和端口
    if hostname.startswith('http://'):
        hostname = hostname.replace('http://', '')
    elif hostname.startswith('https://'):
        hostname = hostname.replace('https://', '')

    # 分離主機名和端口
    if ':' in hostname:
        host_parts = hostname.split(':')
        hostname = host_parts[0]
        port = int(host_parts[1])
    else:
        hostname = hostname
        port = 8069

    api_key = os.environ.get('ODOO_API_KEY', 'ODOO_API_KEY')
    database = os.environ.get('ODOO_DATABASE', 'odoo')

    if not api_key:
        _logger.error("❌ 錯誤：請設置環境變數 ODOO_API_KEY")
        _logger.error("   export ODOO_API_KEY='your_api_key_here'")
        sys.exit(1)

    _logger.info(f"\n配置資訊:")
    _logger.info(f"  Hostname: {hostname}")
    _logger.info(f"  Port: {port}")
    _logger.info(f"  Protocol: json2")
    _logger.info(f"  Database: {database}")
    _logger.info(f"  API Key: {'*' * 20}...{api_key[-4:] if len(api_key) > 4 else '****'}")

    try:
        # 使用 odoolib 建立連接，指定使用 json2 協議
        connection = odoolib.get_connection(
            hostname=hostname,
            protocol="json2",
            port=port,
            database=database,
            # In json2 connection, this can only be an API key.
            password=api_key  # 對於 API key 認證
        )
        _logger.info("\n✅ 使用 JSON-2 協議成功建立連接")
    except Exception as e:
        _logger.error(f"❌ 連接失敗: {e}")
        sys.exit(1)

    # 執行測試
    if test_connection(connection):
        test_crud_operations(connection)
        # test_model_methods(connection)  # 測試呼叫模型方法
        # test_many2many_operations(connection)  # 測試 M2M 欄位操作
        # test_error_handling(connection)
    else:
        _logger.error("\n❌ 連線失敗，請檢查配置")
        sys.exit(1)

    _logger.info("\n" + "=" * 60)
    _logger.info("✅ 測試完成！")
    _logger.info("=" * 60)


if __name__ == "__main__":
    main()