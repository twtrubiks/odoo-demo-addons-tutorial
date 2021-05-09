from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tests.common import SingleTransactionCase

class TestDemoOdooSingleTransactionCase(SingleTransactionCase):

    def setUp(self, *args, **kwargs):
        """setUp"""
        super(TestDemoOdooSingleTransactionCase, self).setUp(*args, **kwargs)
        print('Run setUp')

    def test_hello_world(self):
        """test_hello_world"""
        self.assertEqual(0, 0, 'test hello world')

    def test_datetime_validation(self):
        """test_datetime_validation"""
        values = {
            'name': 'hello',
            'start_datetime': '2020-02-01',
            'stop_datetime': '2020-01-01',
        }
        with self.assertRaises(ValidationError):
            self.env['demo.odoo.tutorial'].create(values)

    def test_field_compute_demo(self):
        """test_field_compute_demo"""
        values = {
            'name': 'hello',
            'input_number': 2
        }
        data = self.env['demo.odoo.tutorial'].create(values)
        self.assertEqual(data.field_compute_demo, data.input_number * 1000)
