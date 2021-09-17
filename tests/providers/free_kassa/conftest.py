import pytest


@pytest.fixture(autouse=True)
def set_free_kassa_settings(settings):
    settings.PAYMENTS = {
        "FREE_KASSA": {
            "merchant_id": "qwerty",
            "secret_word_2": "qwerty",
        }
    }


@pytest.fixture
def sample_uid():
    return "9234e6e7-d737-40f8-8fd3-e876116aab0b"
