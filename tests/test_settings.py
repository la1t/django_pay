from django.test import SimpleTestCase

from django_pay2.settings import ImportDict, ObjDict, PaymentSettings

from .models import TestInvoice


class ObjDictTests(SimpleTestCase):
    def test_raise_error_if_init_with_not_a_dict(self):
        with self.assertRaises(ValueError):
            ObjDict("not_a_dict")

    def test_return_value_by_attribute(self):
        obj_dict = ObjDict({"foo": "bar"})
        self.assertEqual(obj_dict.foo, "bar")

    def test_raise_error_if_attr_does_not_exist(self):
        obj_dict = ObjDict({})
        with self.assertRaises(AttributeError):
            obj_dict.does_not_exist


class ImportDictTests(SimpleTestCase):
    def test_return_imported_object_if_value_is_string(self):
        import_dict = ImportDict({"invoice_model": "tests.models.TestInvoice"})
        self.assertEqual(import_dict.invoice_model, TestInvoice)

    def test_return_list_of_imported_objects_if_value_is_list(self):
        import_dict = ImportDict(
            {
                "sample": [
                    "tests.models.TestInvoice",
                    "django_pay2.settings.PaymentSettings",
                ]
            }
        )
        self.assertEqual(import_dict.sample[0], TestInvoice)
        self.assertEqual(import_dict.sample[1], PaymentSettings)

    def test_raise_error_if_result_does_not_a_string(self):
        import_dict = ImportDict({"sample": TestInvoice})
        with self.assertRaises(ValueError):
            import_dict.sample


class PaymentSettingsTests(SimpleTestCase):
    def test_return_value_from_default_if_setting_does_not_defined(self):
        defaults = {"TEST": True}
        user_settings = {}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )
        self.assertTrue(payment_settings.TEST)

    def test_return_value_from_user_settings_if_this_defined(self):
        defaults = {"TEST": True}
        user_settings = {"TEST": False}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )
        self.assertFalse(payment_settings.TEST)

    def test_reload_drop_cache(self):
        defaults = {"TEST": True}
        user_settings = {"TEST": False}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )
        payment_settings.reload()
        self.assertTrue(payment_settings)

    def test_raise_error_if_attr_is_not_in_defaults(self):
        defaults = {"TEST": True}
        user_settings = {}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )
        with self.assertRaises(AttributeError):
            payment_settings.NOT_EXIST

    def test_transform_dict_to_obj_dict_if_dict_does_not_in_import_dicts(self):
        defaults = {"TEMPLATES": {}}
        user_settings = {"TEMPLATES": {"success": "test.html"}}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )
        self.assertIsInstance(payment_settings.TEMPLATES, ObjDict)

    def test_transform_dict_to_import_dict_if_dict_in_import_dicts(self):
        defaults = {"MODULES": {}}
        user_settings = {"MODULES": {"payments": "django_pay2"}}
        import_dicts = ["MODULES"]
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults, import_dicts=import_dicts
        )
        self.assertIsInstance(payment_settings.MODULES, ImportDict)

    def test_merge_user_settings_obj_dict_with_defaults(self):
        defaults = {"MODULES": {"payment": "django_pay2", "tests": "tests"}}
        user_settings = {"MODULES": {"tests": "testproject"}}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )
        self.assertEqual(
            payment_settings.MODULES,
            ObjDict({"payment": "django_pay2", "tests": "testproject"}),
        )

    def test_merge_user_settings_import_dict_with_defaults(self):
        defaults = {"MODULES": {"payment": "django_pay2", "tests": "tests"}}
        user_settings = {"MODULES": {"tests": "testproject"}}
        import_dicts = ["MODULES"]
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults, import_dicts=import_dicts
        )
        self.assertEqual(
            payment_settings.MODULES,
            ImportDict({"payment": "django_pay2", "tests": "testproject"}),
        )
