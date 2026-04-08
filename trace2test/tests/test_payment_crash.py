import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from payment_service import process_payment


def test_process_payment_raises_value_error():
    with pytest.raises(ValueError, match="quantity must be greater than zero"):
        process_payment(order_id="ORD-001", amount=100.0, quantity=0)

# Made with Bob
