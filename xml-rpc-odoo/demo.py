import xmlrpc.client
from pprint import pprint

# use xmlrpc 時, 建議回傳 true
# The reason is that not all client implementations of the XML-RPC protocol
# support None/Null values, and may raise errors when such a value is returned
# by a method.

url = 'http://0.0.0.0:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

def common_version():
    # provides meta-calls which don’t require authentication
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    common.version()
    print(common.version())
    return common

def get_uid():
    # Logging in
    common = common_version()
    uid = common.authenticate(db, username, password, {})
    print('uid:', uid)
    return uid

def endpoint_object():
    #  is used to call methods of odoo models via the execute_kw RPC function.
    return xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def call_check_access_rights():
    # Calling methods
    models = endpoint_object()
    uid = get_uid()
    data = models.execute_kw(db, uid, password,
        'res.partner', 'check_access_rights',
        ['read'], {'raise_exception': False})
    print(data)

def list_all_records():
    models = endpoint_object()
    uid = get_uid()
    # List all records
    records_data = models.execute_kw(db, uid, password,
        'res.partner', 'search',[[]])
    print(records_data)

def list_records():
    models = endpoint_object()
    uid = get_uid()
    # List records
    records_data = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True]]])
    print(records_data)

def count_records():
    models = endpoint_object()
    uid = get_uid()
    # Count records
    records_count = models.execute_kw(db, uid, password,
        'res.partner', 'search_count',
        [[['is_company', '=', True]]])
    print(records_count)

def read_records():
    models = endpoint_object()
    uid = get_uid()
    # Read records
    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['is_company', '=', True]]],
        {'limit': 1})
    print('ids:', ids)
    return ids

def read_all_field():
    models = endpoint_object()
    uid = get_uid()
    # Read records ids
    ids = read_records()
    # all field
    record = models.execute_kw(db, uid, password,
        'res.partner', 'read', [ids])
    print('record')
    pprint(record)

def read_need_field():
    models = endpoint_object()
    uid = get_uid()
    # Read records ids
    ids = read_records()
    # need field
    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [ids], {'fields': ['name', 'country_id', 'comment']})
    print('record')
    pprint(record)

def listing_record_fields_attributes():
    models = endpoint_object()
    uid = get_uid()
    # Listing record fields attributes
    listing_record_fields = models.execute_kw(
        db, uid, password, 'res.partner', 'fields_get',
        [], {'attributes': ['string', 'help', 'type']})
    print('Listing record fields')
    pprint(listing_record_fields)

def search_and_read():
    models = endpoint_object()
    uid = get_uid()
    # Search and read
    search_and_read = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['is_company', '=', True]]],
        {'fields': ['name', 'country_id', 'comment'], 'limit': 5})
    print('Search and read')
    pprint(search_and_read)

def create_reads():
    models = endpoint_object()
    uid = get_uid()
    # Create records
    models.execute_kw(db, uid, password, 'res.partner', 'create', [{
        'name': "New Partner_2",
    }])

    # read Create records
    search_and_read = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['name', '=', 'New Partner_2']]],
        {'fields': ['name'], 'limit': 5})
    pprint(search_and_read)

def update_records():
    models = endpoint_object()
    uid = get_uid()

    # read res.partner
    search_and_read = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['name', '=', 'New Partner_2']]],
        {'fields': ['id'], 'limit': 1})
    my_partner_id = search_and_read[0]['id']
    print('my_partner_id:', my_partner_id)

    # Update records
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[my_partner_id], {
        'name': "hello"
    }])
    # get record name after having changed it
    my_data = models.execute_kw(db, uid, password, 'res.partner', 'name_get',[[my_partner_id]])
    pprint(my_data)

def delete_record():
    # please installl sale addons
    models = endpoint_object()
    uid = get_uid()

    # read res.partner
    my_partner_id = 40

    # Delete records
    models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[my_partner_id]])
    # check if the deleted record is still in the database
    my_data = models.execute_kw(db, uid, password,
        'res.partner', 'search', [[['id', '=', my_partner_id]]])
    pprint(my_data)

def many2one_create():
    # please installl sale addons
    models = endpoint_object()
    uid = get_uid()

    # read res.partner
    search_and_read = models.execute_kw(db, uid, password,
        'res.partner', 'search_read',
        [[['name', '=', 'hello']]],
        {'fields': ['id'], 'limit': 1})
    my_partner_id = search_and_read[0]['id']
    print('my_partner_id:', my_partner_id)

    # Many2one - create
    id_ = models.execute_kw(db, uid, password, 'sale.order', 'create', [{
        'partner_id': my_partner_id,
    }])

    # get record name after having changed it
    # check form pgadmin4
    my_data = models.execute_kw(db, uid, password, 'sale.order', 'name_get',[[id_]])
    pprint(my_data)

def many2many_add_record():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 7

    # res.partner
    # check form pgadmin4
    res_partner_id = 38

    # (4, id, _) links an already existing record.
    # add many2many field,
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[res_partner_id], {
        'category_id': [(4, category_id, 0)]
    }])

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

def many2many_add_mutil_record():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_ids = [6, 7]

    # res.partner
    # check form pgadmin4
    res_partner_id = 37

    # (6, _, [ids]) replaces the list of linked records with the provided list.
    # add mutil many2many field
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[res_partner_id], {
        'category_id': [(6, 0, category_ids)]
    }])

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

def many2many_update_record():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 6

    # res.partner
    # check form pgadmin4
    res_partner_id = 37

    record = models.execute_kw(db, uid, password, 'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

    # update many2many field value
    # (1, ID, { values }) update the linked record with id = ID
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[res_partner_id], {
        'category_id': [(1, category_id, {'name':'hello2'})]
    }])

    record = models.execute_kw(db, uid, password,
        'res.partner.category', 'read',
        [category_id], {'fields': ['id', 'name']})
    print('record:', record)


def many2many_delete_record_2():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 6

    # res.partner
    # check form pgadmin4
    res_partner_id = 37

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

    # delete many2many field.
    # 2, ID) remove and delete the linked record with id = ID
    # (calls unlink on ID, that will delete the object completely,
    # and the link to it as well)
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[res_partner_id], {
        'category_id': [(2, category_id, 0)]
    }])

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

    # res.partner.category
    # check form pgadmin4
    # id = 6 deleted

    record = models.execute_kw(db, uid, password,
        'res.partner.category', 'read',
        [category_id], {'fields': ['id', 'name']})
    print('record:', record)

def many2many_delete_record_3():
    models = endpoint_object()
    uid = get_uid()

    # res.partner.category
    # check form pgadmin4
    category_id = 7

    # res.partner
    # check form pgadmin4
    res_partner_id = 37

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

    # delete many2many field.
    # (3, ID) cut the link to the linked record with id = ID
    # (delete the relationship between the two objects
    # but does not delete the target object itself)
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[res_partner_id], {
        'category_id': [(3, category_id, 0)]
    }])

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

    # res.partner.category
    # check form pgadmin4
    # id = 7 not deleted

    record = models.execute_kw(db, uid, password,
        'res.partner.category', 'read',
        [category_id], {'fields': ['id', 'name']})
    print('record:', record)


def many2many_delete_record_5():
    models = endpoint_object()
    uid = get_uid()

    # res.partner
    # check form pgadmin4
    res_partner_id = 38

    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)

    # delete many2many field.
    # (5, 0, 0) unlink all
    # (like using (3,ID, 0) for all linked records)
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[res_partner_id], {
        'category_id': [(5, 0, 0)]
    }])

    # res.partner.category
    # check form pgadmin4
    # ids not deleted
    record = models.execute_kw(db, uid, password,
        'res.partner', 'read',
        [res_partner_id], {'fields': ['id', 'name', 'category_id']})
    print('record:', record)




# common_version()
# get_uid()
call_check_access_rights()
# list_all_records()
# list_records()
# count_records()
# read_records()
# read_all_field()
# read_need_field()
# listing_record_fields_attributes()
# search_and_read()

# create_reads()
# update_records()
# delete_record()
# many2one_create()
# many2many_add_record()
# many2many_add_mutil_record()

# many2many_update_record()
# many2many_delete_record_2()
# many2many_delete_record_3()
# many2many_delete_record_5()
