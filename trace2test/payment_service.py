def process_payment(order_id, amount, quantity):
    if quantity == 0:
        raise ValueError("quantity must be greater than zero")
    total_amount = amount
    items = quantity
    price_per_unit = total_amount / items
    return f"Processed {order_id} at {price_per_unit:.2f} per unit"


def write_crash_log():
    log_content = """ERROR TYPE: ZeroDivisionError
ERROR MESSAGE: division by zero
FUNCTION: process_payment
LINE: 4
FILE: payment_service.py
INPUT PARAMS: order_id=ORD-001, amount=100.0, quantity=0
TRACEBACK:

  File "payment_service.py", line 4, in process_payment
    price_per_unit = amount / quantity
ZeroDivisionError: division by zero
"""
    with open("trace2test/crash.log", "w", encoding="utf-8") as log_file:
        log_file.write(log_content)


def main():
    try:
        process_payment("ORD-001", 100.0, 0)
    except ZeroDivisionError:
        write_crash_log()
        print("Service crashed. crash.log written.")
        raise SystemExit(1)
    except ValueError as error:
        print(error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

# Made with Bob
