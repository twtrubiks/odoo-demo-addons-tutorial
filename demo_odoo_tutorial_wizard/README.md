# odoo 17 觀念 - TransientModel - Wizard

建議在閱讀這篇文章之前, 請先確保了解看過 odoo 12 的教學,

[odoo 觀念 - TransientModel - Wizard](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial_wizard)

因為本篇只會說明差異的部份,

## 說明

直接看以下的 odoo17 的 code

```python
class DemoWizard(models.TransientModel):
    ......

    @api.model
    def default_get(self, fields):
        res = super(DemoWizard, self).default_get(fields)
        context = clean_context(self.env.context) # pass "default_"

        self._dirty_check()
        ......
        return res

    def _dirty_check(self):
        _logger.warning('_dirty_check function')
        active_id = self._context.get('active_id')
        _logger.warning(f'active_id: {active_id}')

    # @api.model
    # def get_view(self, view_id=None, view_type='form', **options):
    #     """
    #     Overrides orm field_view_get.
    #     @return: Dictionary of Fields, arch and toolbar.
    #     """
    #     res = super().get_view(view_id, view_type, **options)
    #     return res
```

在 odoo16 中 `get_view` 可以取到 `active_id`,

但是在 odoo17 中, 你會發現取不到, 所以將取 `active_id` 的部份移動到 `default_get` 裡面,

這樣就可以正常取值了.

說穿了主要就是 `self._dirty_check()` 換了一個地方放而已,

另外, 如果 `get_view` 不需要也是可以整個註解掉.
