from dataclasses import dataclass
from typing import Dict


@dataclass
class PaymentRedirect:
    method = "redirect"
    url: str


@dataclass
class PaymentForm:
    method = "form"
    url: str
    fields: Dict[str, str]
