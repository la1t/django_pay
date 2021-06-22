from django.test import SimpleTestCase
import pytest

from django_pay2.settings import ImportDict, ObjDict, PaymentSettings

from .models import TestInvoice


class TestObjDict:
    def test_raise_err_if_init_with_not_a_dict(self):
        with pytest.raises(ValueError):
            ObjDict("not_a_dict")

    def test_raise_err_if_attr_does_not_exist(self):
        obj_dict = ObjDict({})

        with pytest.raises(AttributeError):
            obj_dict.does_not_exist

    def test_return_val_by_attr(self):
        obj_dict = ObjDict({"foo": "bar"})

        assert obj_dict.foo == "bar"


class TestImportDict:
    def test_return_imported_obj_if_val_is_string(self):
        import_dict = ImportDict({"invoice_model": "tests.models.TestInvoice"})

        assert import_dict.invoice_model == TestInvoice

    def test_return_list_of_imported_objs_if_val_is_list(self):
        import_dict = ImportDict(
            {
                "sample": [
                    "tests.models.TestInvoice",
                    "django_pay2.settings.PaymentSettings",
                ]
            }
        )

        assert import_dict.sample[0] == TestInvoice
        assert import_dict.sample[1] == PaymentSettings

    def test_raise_err_if_result_does_not_a_string(self):
        import_dict = ImportDict({"sample": TestInvoice})

        with pytest.raises(ValueError):
            import_dict.sample


class TestPaymentSettings:
    def test_return_val_from_default_if_settings_does_not_defined(self):
        defaults = {"TEST": True}
        user_settings = {}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )

        assert payment_settings.TEST

    def test_return_value_from_user_settings_if_it_is_defined(self):
        defaults = {"TEST": True}
        user_settings = {"TEST": False}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )

        assert not payment_settings.TEST

    def test_reload_drop_cache(self):
        defaults = {"TEST": True}
        user_settings = {"TEST": False}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )

        payment_settings.reload()

        assert payment_settings

    def test_raise_err_if_attr_is_not_in_defaults(self):
        defaults = {"TEST": True}
        user_settings = {}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )

        with pytest.raises(AttributeError):
            payment_settings.NOT_EXIST

    def test_transform_dict_to_obj_if_dict_does_not_in_import_dicts(self):
        defaults = {"TEMPLATES": {}}
        user_settings = {"TEMPLATES": {"success": "test.html"}}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )

        assert isinstance(payment_settings.TEMPLATES, ObjDict)

    def test_transform_dict_to_import_dict_if_dict_in_import_dicts(self):
        defaults = {"MODULES": {}}
        user_settings = {"MODULES": {"payments": "django_pay2"}}
        import_dicts = ["MODULES"]
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults, import_dicts=import_dicts
        )

        assert isinstance(payment_settings.MODULES, ImportDict)

    def test_merge_user_settings_obj_dict_with_defaults(self):
        defaults = {"MODULES": {"payment": "django_pay2", "tests": "tests"}}
        user_settings = {"MODULES": {"tests": "testproject"}}
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults
        )

        assert payment_settings.MODULES == ObjDict(
            {"payment": "django_pay2", "tests": "testproject"}
        )

    def test_merge_user_settings_import_dict_with_defaults(self):
        defaults = {"MODULES": {"payment": "django_pay2", "tests": "tests"}}
        user_settings = {"MODULES": {"tests": "testproject"}}
        import_dicts = ["MODULES"]
        payment_settings = PaymentSettings(
            user_settings=user_settings, defaults=defaults, import_dicts=import_dicts
        )

        assert payment_settings.MODULES == ImportDict(
            {"payment": "django_pay2", "tests": "testproject"}
        )
