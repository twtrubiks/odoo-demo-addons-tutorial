# odoo15 架構流程

這篇文章紀錄 odoo 載入 addons 流程 以及 頁面生成流程,

紀錄一些比較重要的 code, 追 code 時可能會比較清楚.

## 載入 addons 流程

首先載入 base, 會透過 `odoo/modules/graph.py` 載入 graph 關係圖,

透過 graph 加載 addons 之間的 dependency,

```python
""" Modules dependency graph. """
......

class Graph(dict):
    """ Modules dependency graph.

    The graph is a mapping from module name to Nodes.

    """
......
```

`load_modules` 開始載入 modules.

`odoo/modules/loading.py`

```python

......

def load_modules(registry, force_demo=False, status=None, update_module=False):
    """ Load the modules for a registry object that has just been created.  This
        function is part of Registry.new() and should not be used anywhere else.
    """
    initialize_sys_path()

    force = []
    if force_demo:
        force.append('demo')
    ......
    # processed_modules: for cleanup step after install
    # loaded_modules: to avoid double loading
    report = registry._assertion_report
    loaded_modules, processed_modules = load_module_graph(
        cr, graph, status, perform_checks=update_module,
        report=report, models_to_check=models_to_check)

    ......
    while previously_processed < len(processed_modules):
        previously_processed = len(processed_modules)
        processed_modules += load_marked_modules(cr, graph,
            ['installed', 'to upgrade', 'to remove'],
            force, status, report, loaded_modules, update_module, models_to_check)
        if update_module:
            processed_modules += load_marked_modules(cr, graph,
                ['to install'], force, status, report,
                loaded_modules, update_module, models_to_check)
    ......
```

呼叫流程,

`load_modules` -> `load_module_graph` -> `load_data`

-> `convert_file` -> `convert_xml_import`

透過 `/odoo/tools/convert.py` 中的 convert_file 依照類型解析資料


```python
def convert_file(cr, module, filename, idref, mode='update', noupdate=False, kind=None, pathname=None):
    if pathname is None:
        pathname = os.path.join(module, filename)
    ext = os.path.splitext(filename)[1].lower()

    with file_open(pathname, 'rb') as fp:
        if ext == '.csv':
            convert_csv_import(cr, module, pathname, fp.read(), idref, mode, noupdate)
        elif ext == '.sql':
            convert_sql_import(cr, fp)
        elif ext == '.xml':
            convert_xml_import(cr, module, fp, idref, mode, noupdate)
        elif ext == '.js':
            pass # .js files are valid but ignored here.
        else:
            raise ValueError("Can't load unknown file type %s.", filename)

......

def convert_xml_import(cr, module, xmlfile, idref=None, mode='init', noupdate=False, report=None):
    ......
    obj = xml_import(cr, module, idref, mode, noupdate=noupdate, xml_filename=xml_filename)
    obj.parse(doc.getroot())

```

最後呼叫 `xml_import`,

使用 `lxml` 歷遍整個樹, 依照不同的類型使用對應的函數,

安裝 addons 時會觸發,

```python
class xml_import(object):

    def _tag_record(self, rec):
        ......
        record = self.env['ir.model.data']._load_xmlid(xid)
        ......

    def _tag_template(self, el):
        # This helper transforms a <template> element into a <record> and forwards it
        ......
        return self._tag_record(record)

    ......

    def __init__(self, cr, module, idref, mode, noupdate=False, xml_filename=None):
        .......
        self._tags = {
            'record': self._tag_record,
            'delete': self._tag_delete,
            'function': self._tag_function,
            'menuitem': self._tag_menuitem,
            'template': self._tag_template,
            'report': self._tag_report,
            'act_window': self._tag_act_window,

            **dict.fromkeys(self.DATA_ROOTS, self._tag_root)
        }
```

部份資料會保存進 `ir.model.data`


## 頁面生成流程

透過 `index` 呼叫 `web_client`,

`web/controllers/main.py`

```python
class Home(http.Controller):

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        return request.redirect_query('/web', query=request.params)

    # ideally, this route should be `auth="user"` but that don't work in non-monodb mode.
    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ......
            response = request.render('web.webclient_bootstrap', qcontext=context)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        ......

```

`odoo/http.py`

接著看 `HttpRequest` 以及 `Response` 結構,

```python
class HttpRequest(WebRequest):
    ......
    def render(self, template, qcontext=None, lazy=True, **kw):
        ......
        response = Response(template=template, qcontext=qcontext, **kw)
        if not lazy:
            return response.render()
        return response

......

class Response(werkzeug.wrappers.Response):

    def render(self):
        """ Renders the Response's template, returns the result
        """
        env = request.env(user=self.uid or request.uid or odoo.SUPERUSER_ID)
        self.qcontext['request'] = request
        return env["ir.ui.view"]._render_template(self.template, self.qcontext)
```

最後回傳了 `ir.ui.view` 中的 `_render_template`.

非常建議大家用中斷點下去追 code, 測試的時候要注意 orm cache,

重新啟動可以清除 cache,

`addons/base/models/ir_ui_view.py`

```python

class View(models.Model):
    _name = 'ir.ui.view'

    ......

    @api.model
    def get_view_id(self, template):
        ......
        if isinstance(template, int):
            return template
        if '.' not in template:
            raise ValueError('Invalid template id: %r' % template)
        view = self.sudo().search([('key', '=', template)], limit=1)
        return view and view.id or self.env['ir.model.data']._xmlid_to_res_id(template, raise_if_not_found=True)

    def _render_template(self, template, values=None, engine='ir.qweb'):
        return self.browse(self.get_view_id(template))._render(values, engine)

    def _render(self, values=None, engine='ir.qweb', minimal_qcontext=False):
        ......

        return self.env[engine]._render(self.id, qcontext)
```

```python

class IrModelData(models.Model):
    ......
    _name = 'ir.model.data'
    _description = 'Model Data'
    _order = 'module, model, name'

    # NEW V8 API
    @api.model
    @tools.ormcache('xmlid')
    def _xmlid_lookup(self, xmlid):
        """Low level xmlid lookup
        Return (id, res_model, res_id) or raise ValueError if not found
        """
        module, name = xmlid.split('.', 1)
        query = "SELECT id, model, res_id FROM ir_model_data WHERE module=%s AND name=%s"
        self.env.cr.execute(query, [module, name])
        result = self.env.cr.fetchone()
        if not (result and result[2]):
            raise ValueError('External ID not found in the system: %s' % xmlid)
        return result

    @api.model
    def _xmlid_to_res_model_res_id(self, xmlid, raise_if_not_found=False):
        """ Return (res_model, res_id)"""
        try:
            return self._xmlid_lookup(xmlid)[1:3]
        except ValueError:
            if raise_if_not_found:
                raise
            return (False, False)

    @api.model
    def _xmlid_to_res_id(self, xmlid, raise_if_not_found=False):
        """ Returns res_id """
        return self._xmlid_to_res_model_res_id(xmlid, raise_if_not_found)[1]
```


```python
class IrQWeb(models.AbstractModel, QWeb):
    ......
    _name = 'ir.qweb'
    _description = 'Qweb'
    ......

    @QwebTracker.wrap_render
    @api.model
    def _render(self, template, values=None, **options):
        ......
        result = super()._render(template, values=values, **compile_options)
        ......

    ......

    @QwebTracker.wrap_compile
    def _compile(self, id_or_xml_id, options):
        try:
            id_or_xml_id = int(id_or_xml_id)
        except:
            pass
        return super()._compile(id_or_xml_id, options=options)
    ......

    def _load(self, name, options):
        lang = options.get('lang', get_lang(self.env).code)
        env = self.env
        if lang != env.context.get('lang'):
            env = env(context=dict(env.context, lang=lang))

        view_id = self.env['ir.ui.view'].get_view_id(name)
        template = env['ir.ui.view'].sudo()._read_template(view_id)
        ......
        def is_child_view(view_name):
            view_id = self.env['ir.ui.view'].get_view_id(view_name)
            view = self.env['ir.ui.view'].sudo().browse(view_id)
            return view.inherit_id is not None

        if isinstance(name, int) or is_child_view(name):
            view = etree.fromstring(template)
            for node in view:
                if node.get('t-name'):
                    node.set('t-name', str(name))
            return (view, view_id)
        else:
            return (template, view_id)

```

```python
class QWeb(object):

    def _render(self, template, values=None, **options):
        ......

        render_template = self._compile(template, options)
        rendering = render_template(self, values or {})
        result = ''.join(rendering)

        return Markup(result)

    def _compile(self, template, options):
        """ Compile the given template into a rendering function (generator)::

            render(qweb, values)

        where ``qweb`` is a QWeb instance and ``values`` are the values to render.
        """
        if options is None:
            options = {}

        element, document, ref = self._get_template(template, options)
        ......

        # generate code

        def_name = f"template_{ref}" if isinstance(ref, int) else "template"

        ......

        # compile code and defined default values

        try:
            # noinspection PyBroadException
            compiled = compile(code, f'<{def_name}>', 'exec')
            globals_dict = self._prepare_globals({}, options)
            globals_dict['__builtins__'] = globals_dict # So that unknown/unsafe builtins are never added.
            ......

        # return the wrapped function

        def render_template(self, values):
            try:
                log = {'last_path_node': None}
                values = self._prepare_values(values, options)
                yield from compiled_fn(self, values, log)
            except (QWebException, TransactionRollbackError) as e:
                raise e
            except Exception as e:
                raise QWebException("Error when render the template", self, options,
                    error=e, template=template, path=log.get('last_path_node'), code=code)

        return render_template

    def _get_template(self, template, options):
        ......
                loaded = options.get('load', self._load)(template, options)
                if not loaded:
                    raise ValueError("Can not load template '%s'" % template)
        ......

    def _load(self, template, options):
        """ Load a given template and return a tuple ``(xml, ref)``` """
        return (template, None)

```

上面的 code 比較多, 主要是呼叫間比較重要的函式整理出來給大家,

另外要特別注意 `IrQWeb`, 因為他是繼承 `QWeb`.

```python
class View(models.Model):
    _name = 'ir.ui.view'
    _description = 'View'
    _order = "priority,name,id"

    ......
    arch = fields.Text(compute='_compute_arch', inverse='_inverse_arch', string='View Architecture')
    ......
    arch_db = fields.Text(string='Arch Blob', translate=xml_translate,)

    arch_fs = fields.Char(string='Arch Filename', )
    ......

    mode = fields.Selection([('primary', "Base view"), ('extension', "Extension View")],string="View inheritance mode", default='primary', required=True,

    ......

    @api.depends('arch_db', 'arch_fs', 'arch_updated')
    @api.depends_context('read_arch_from_file', 'lang')
    def _compute_arch(self):
        ......
        return m.group('prefix') + str(self.env['ir.model.data']._xmlid_to_res_id(xmlid))
        ......

    def locate_node(self, arch, spec):
        ......
        return locate_node(arch, spec)

    @api.model
    def apply_inheritance_specs(self, source, specs_tree, pre_locate=lambda s: True):
        source = apply_inheritance_specs(
                source, specs_tree,
                inherit_branding=self._context.get('inherit_branding'),
                pre_locate=pre_locate,
            )
        ......

    def _combine(self, hierarchy: dict):
        """
        Return self's arch combined with its inherited views archs.

        :param hierarchy: mapping from parent views to their child views
        :return: combined architecture
        :rtype: Element
        """
        self.ensure_one()
        assert self.mode == 'primary'

        # We achieve a pre-order depth-first hierarchy traversal where
        # primary views (and their children) are traversed after all the
        # extensions for the current primary view have been visited.
        ......

    def _get_combined_arch(self):
        """ Return the arch of ``self`` (as an etree) combined with its inherited views. """
        root = self
        view_ids = []
        while True:
            view_ids.append(root.id)
            if not root.inherit_id:
                break
            root = root.inherit_id

        ......
        # optimization: make root part of the prefetch set, too
        arch = root.with_prefetch(tree_views._prefetch_ids)._combine(hierarchy)
        return arch

    def get_combined_arch(self):
        """ Return the arch of ``self`` (as a string) combined with its inherited views. """
        return etree.tostring(self._get_combined_arch(), encoding='unicode')

    ......

    def _read_template(self, view_id):
        arch_tree = self.browse(view_id)._get_combined_arch()
        self.distribute_branding(arch_tree)
        return etree.tostring(arch_tree, encoding='unicode')

```

model `ir.ui.view`, 主要保存了 xml view,

可看 `arch` `arch_db` fields.

`locate_node` 位置在 `odoo/tools/template_inheritance.py`,

這邊選擇繼承的方式 ( `xpath` 或是 `fields` ).

`_combine` 這個函式主要是透過 DFS 二元樹走訪找出誰是 primary, children,

然後說明可參考 source code 中的 `_combine`.

odoo 中的模板, 是使用 python 中的 `ast` 來完成的,

透過 `ast` 再編輯成 html.
