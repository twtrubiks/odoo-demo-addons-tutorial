"""
Odoo 19 JSON-2 API 測試腳本

使用方法：
1. 設置環境變數：
   export ODOO_URL="http://localhost:8069"
   export ODOO_API_KEY="your_api_key_here"
   export ODOO_DATABASE="your_database"  # 可選，多資料庫環境需要

2. 執行測試：
   python3 json2_client_demo.py
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# 設定 logging
logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    format='%(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)

class OdooJSON2Client:
    """Odoo 19 JSON-2 API 客戶端"""

    def __init__(self, url: str, api_key: str, database: Optional[str] = None):
        self.url = url.rstrip('/')
        self.api_key = api_key
        self.database = database
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """設置 session headers"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        })
        if self.database:
            self.session.headers['X-odoo-database'] = self.database

    def call(self, model: str, method: str, **kwargs) -> Any:
        """呼叫 Odoo 方法"""
        endpoint = f"{self.url}/json/2/{model}/{method}"
        _logger.info(f"📡 呼叫 API: {endpoint}")

        data = {}
        if 'ids' in kwargs:
            data['ids'] = kwargs.pop('ids')
        if 'context' in kwargs:
            data['context'] = kwargs.pop('context')

        data.update(kwargs)

        response = self.session.post(endpoint, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            try:
                error = response.json()
                error_msg = f"Odoo Error ({response.status_code}): {error.get('message', 'Unknown error')}"
                _logger.error(f"❌ {error_msg}")
                if 'debug' in error:
                    _logger.debug(f"Debug: {error['debug']}")
                raise Exception(error_msg)
            except json.JSONDecodeError:
                _logger.error(f"❌ HTTP Error {response.status_code}: {response.text[:200]}")
                response.raise_for_status()

    def search(self, model: str, domain: List = None, **kwargs) -> List[int]:
        """搜尋記錄"""
        return self.call(model, 'search', domain=domain or [], **kwargs)

    def search_read(self, model: str, domain: List = None, fields: List = None, **kwargs) -> List[Dict]:
        """搜尋並讀取記錄"""
        return self.call(model, 'search_read',
                        domain=domain or [],
                        fields=fields or [],
                        **kwargs)

    def read(self, model: str, ids: List[int], fields: List = None) -> List[Dict]:
        """讀取記錄"""
        return self.call(model, 'read', ids=ids, fields=fields or [])

    def create(self, model: str, values: Union[Dict, List[Dict]]) -> Union[int, List[int]]:
        """創建記錄"""
        # Odoo 19 的 create 方法需要 vals_list 參數（必須是列表）
        if not isinstance(values, list):
            values = [values]
        result = self.call(model, 'create', vals_list=values)
        # 如果只創建一筆記錄，返回單個 ID
        if len(values) == 1 and isinstance(result, list):
            return result[0] if result else None
        return result

    def write(self, model: str, ids: List[int], values: Dict) -> bool:
        """更新記錄"""
        # Odoo 19 的 write 方法使用 vals 參數（單數）
        return self.call(model, 'write', ids=ids, vals=values)

    def unlink(self, model: str, ids: List[int]) -> bool:
        """刪除記錄"""
        return self.call(model, 'unlink', ids=ids)


def test_connection(client: OdooJSON2Client):
    """測試連線"""
    _logger.info("\n=== 測試連線 ===")
    try:
        # 測試簡單的搜尋
        user_ids = client.search('res.users', [('id', '=', 2)], limit=1)
        if user_ids:
            _logger.info(f"✅ 連線成功！找到用戶 ID: {user_ids[0]}")
            return True
        else:
            _logger.warning("⚠️  連線成功但找不到管理員用戶")
            return True
    except Exception as e:
        _logger.error(f"❌ 連線失敗: {e}")
        return False


def test_crud_operations(client: OdooJSON2Client):
    """測試 CRUD 操作"""
    _logger.info("\n=== 測試 CRUD 操作 ===")
    test_partner_id = None

    try:
        # 1. CREATE - 創建測試合作夥伴
        _logger.info("\n1. CREATE - 創建合作夥伴")
        test_partner_id = client.create('res.partner', {
            'name': f'API 測試客戶 {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'is_company': True,
            'email': 'api_test@example.com',
            'phone': '+886-2-12345678',
            'comment': '透過 JSON-2 API 創建的測試資料'
        })
        _logger.info(f"   ✅ 成功創建合作夥伴，ID: {test_partner_id}")

        # 2. READ - 讀取剛創建的記錄
        _logger.info("\n2. READ - 讀取合作夥伴")
        partners = client.read('res.partner', [test_partner_id],
                              fields=['name', 'email', 'phone', 'comment'])
        if partners:
            partner = partners[0]
            _logger.info(f"   ✅ 成功讀取:")
            _logger.info(f"      名稱: {partner['name']}")
            _logger.info(f"      Email: {partner['email']}")
            _logger.info(f"      電話: {partner['phone']}")

        # 3. UPDATE - 更新記錄
        _logger.info("\n3. UPDATE - 更新合作夥伴")
        success = client.write('res.partner', [test_partner_id], {
            'phone': '+886-2-87654321',
            'website': 'https://api-test.example.com',
            'comment': '已更新 - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        if success:
            _logger.info("   ✅ 成功更新合作夥伴資料")

            # 驗證更新
            updated = client.read('res.partner', [test_partner_id], ['phone', 'website'])
            if updated:
                _logger.info(f"      新電話: {updated[0]['phone']}")
                _logger.info(f"      新網站: {updated[0]['website']}")

        # 4. SEARCH - 搜尋記錄
        _logger.info("\n4. SEARCH - 搜尋合作夥伴")
        found_ids = client.search('res.partner',
                                 [('name', 'ilike', 'API 測試客戶%')],
                                 limit=5)
        _logger.info(f"   ✅ 找到 {len(found_ids)} 筆符合的記錄")

        # 5. SEARCH_READ - 搜尋並讀取
        _logger.info("\n5. SEARCH_READ - 搜尋並讀取")
        test_partners = client.search_read('res.partner',
            domain=[('name', 'ilike', 'API 測試客戶%')],
            fields=['name', 'create_date'],
            limit=3,
            order='create_date desc'
        )
        _logger.info(f"   ✅ 找到 {len(test_partners)} 筆測試資料:")
        for p in test_partners:
            _logger.info(f"      - {p['name']} (建立於 {p['create_date']})")

        # 6. DELETE - 刪除測試資料
        _logger.info("\n6. DELETE - 刪除測試資料")
        if test_partner_id:
            success = client.unlink('res.partner', [test_partner_id])
            if success:
                _logger.info(f"   ✅ 成功刪除測試合作夥伴 ID: {test_partner_id}")
                test_partner_id = None

    except Exception as e:
        _logger.error(f"❌ CRUD 測試失敗: {e}")
        # 清理測試資料
        if test_partner_id:
            try:
                client.unlink('res.partner', [test_partner_id])
                _logger.warning(f"   ⚠️  已清理測試資料 ID: {test_partner_id}")
            except:
                pass

def test_many2many_operations(client: OdooJSON2Client):
    """測試 Many2Many 欄位操作"""
    _logger.info("\n=== 測試 Many2Many 欄位操作 ===")
    test_user_id = None

    try:
        # 1. 創建測試用戶
        _logger.info("\n1. 創建測試用戶")
        test_user_id = client.create('res.users', {
            'name': f'M2M 測試用戶 {datetime.now().strftime("%H%M%S")}',
            'login': f'test_m2m_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
            'email': f'test_m2m_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
        })
        _logger.info(f"   ✅ 創建測試用戶 ID: {test_user_id}")

        # 2. 搜尋可用的群組
        _logger.info("\n2. 搜尋可用群組")
        all_groups = client.search('res.groups', [], limit=5)
        _logger.info(f"   ✅ 找到 {len(all_groups)} 個群組可供測試")

        # 列出群組名稱
        if all_groups:
            groups_data = client.read('res.groups', all_groups, ['name', 'display_name'])
            _logger.info("   群組列表：")
            for group in groups_data:
                _logger.info(f"      - ID {group['id']}: {group['display_name']}")

        # 3. 使用 (4, id) 添加群組（連結現有記錄）
        _logger.info("\n3. 添加群組 - 使用 (4, id)")
        if all_groups:
            client.write('res.users', [test_user_id], {
                'group_ids': [(4, all_groups[0])]
            })
            _logger.info(f"   ✅ 添加群組 ID: {all_groups[0]}")

            # 讀取驗證
            user_data = client.read('res.users', [test_user_id], ['group_ids'])[0]
            _logger.info(f"      目前群組數量: {len(user_data['group_ids'])}")

        # 4. 測試 Many2Many 在創建時設定
        _logger.info("\n4. 創建時設定 M2M 欄位")
        if len(all_groups) >= 2:
            new_user_id = client.create('res.users', {
                'name': f'M2M 新用戶 {datetime.now().strftime("%H%M%S")}',
                'login': f'new_m2m_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
                'group_ids': [(6, 0, all_groups[:2])]  # 創建時直接設定群組
            })
            _logger.info(f"   ✅ 創建新用戶並設定 {all_groups[:2]} 個群組")
    except Exception as e:
        _logger.error(f"❌ Many2Many 測試失敗: {e}")
    finally:
        # 清理測試資料
        user_ids_to_clean = [uid for uid in [test_user_id, new_user_id] if uid]
        for user_id in user_ids_to_clean:
            try:
                client.unlink('res.users', [user_id])
                _logger.info(f"\n✅ 清理測試用戶 ID: {user_id}")
            except Exception as e:
                _logger.warning(f"⚠️  無法清理測試用戶 {user_id}: {e}")


def test_model_methods(client: OdooJSON2Client):
    """測試呼叫模型方法"""
    _logger.info("\n=== 測試呼叫模型方法 ===")

    try:
        # 呼叫 get_company_currency_id - 取得公司貨幣
        _logger.info("\n呼叫 res.users.get_company_currency_id")
        currency_id = client.call('res.users', 'get_company_currency_id')
        _logger.info(f"   ✅ 公司貨幣 ID: {currency_id}")

        # 可選：讀取貨幣資訊
        if currency_id:
            currency_info = client.read('res.currency', [currency_id], ['name', 'symbol'])
            if currency_info:
                _logger.info(f"   ✅ 貨幣資訊: {currency_info[0]['name']} ({currency_info[0]['symbol']})")

    except Exception as e:
        _logger.error(f"❌ 模型方法測試失敗: {e}")


def test_error_handling(client: OdooJSON2Client):
    """測試錯誤處理 - 符合 Odoo 標準錯誤類型"""
    _logger.info("\n=== 測試錯誤處理 ===")

    # 1. 測試無效的模型 (UserError 或類似錯誤)
    _logger.info("\n1. 測試無效的模型")
    try:
        client.search('invalid.model', [])
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
        client.call('res.partner', 'invalid_method')
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
        client.call('res.partner', 'search')  # 缺少 domain 參數
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
        client.search('ir.cron', [])
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
        client.read('res.partner', [999999999])
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
        client.create('res.users', {
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
    _logger.info("Odoo 19 JSON-2 API 測試腳本")
    _logger.info("=" * 60)

    # 從環境變數讀取配置
    url = os.environ.get('ODOO_URL', 'http://localhost:8069')
    api_key = os.environ.get('ODOO_API_KEY', 'ODOO_API_KEY')
    database = os.environ.get('ODOO_DATABASE', 'odoo')

    if not api_key:
        _logger.error("❌ 錯誤：請設置環境變數 ODOO_API_KEY")
        _logger.error("   export ODOO_API_KEY='your_api_key_here'")
        sys.exit(1)

    _logger.info(f"\n配置資訊:")
    _logger.info(f"  URL: {url}")
    _logger.info(f"  Database: {database or '(使用預設)'}")
    _logger.info(f"  API Key: {'*' * 20}...{api_key[-4:] if len(api_key) > 4 else '****'}")

    # 初始化客戶端
    client = OdooJSON2Client(url, api_key, database)

    # 執行測試
    if test_connection(client):
        test_crud_operations(client)
        # test_model_methods(client)  # 測試呼叫模型方法
        # test_many2many_operations(client)  # 測試 M2M 欄位操作
        # test_error_handling(client)
    else:
        _logger.error("\n❌ 連線失敗，請檢查配置")
        sys.exit(1)

    _logger.info("\n" + "=" * 60)
    _logger.info("✅ 測試完成！")
    _logger.info("=" * 60)


if __name__ == "__main__":
    main()