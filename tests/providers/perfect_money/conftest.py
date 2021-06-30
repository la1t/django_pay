import pytest

from django_pay2.providers.perfect_money.api import PerfectMoneyApi


@pytest.fixture
def api():
    return PerfectMoneyApi(
        "U123456", "E123456", "john.due", "/success/", "/failed/", "ohboyi'msogood1"
    )
