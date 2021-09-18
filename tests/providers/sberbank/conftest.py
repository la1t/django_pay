import pytest


@pytest.fixture(autouse=True)
def set_sberbank_settings(settings):
    settings.PAYMENTS = {
        "SBERBANK": {
            "username": "username",
            "password": "password",
            "return_url": "return_url",
            "fail_url": "fail_url",
            "public_key": """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwtuGKbQ4WmfdV1gjWWys
5jyHKTWXnxX3zVa5/Cx5aKwJpOsjrXnHh6l8bOPQ6Sgj3iSeKJ9plZ3i7rPjkfmw
qUOJ1eLU5NvGkVjOgyi11aUKgEKwS5Iq5HZvXmPLzu+U22EUCTQwjBqnE/Wf0hnI
wYABDgc0fJeJJAHYHMBcJXTuxF8DmDf4DpbLrQ2bpGaCPKcX+04POS4zVLVCHF6N
6gYtM7U2QXYcTMTGsAvmIqSj1vddGwvNGeeUVoPbo6enMBbvZgjN5p6j3ItTziMb
Vba3m/u7bU1dOG2/79UpGAGR10qEFHiOqS6WpO7CuIR2tL9EznXRc7D9JZKwGfoY
/QIDAQAB
-----END PUBLIC KEY-----""",
        }
    }
