# Lab 7: Fuzzing for Input Validation Bugs

Repo assigned: L6_L7_01 Water Utility Billing. Fuzzed with Hypothesis and pytest.

## Files

| File | Description |
|------|-------------|
| `processor.py` | Fixed application script (hardened against fuzzed inputs) |
| `processor_buggy.py` | Original buggy starter code, kept for reference |
| `test_processor.py` | Completed Hypothesis fuzz tests |
| `test_processor_starter.py` | Original starter test file |
| `Lab7_Fuzz_Testing_Report_PES1UG24CS058.pdf` | PDF with all screenshots (Steps 2, 4, 5, 6) |
| `evidence/` | Individual screenshot images |

## Bugs found

- `sanitize_meter_id`: `None` raises `AttributeError`.
- `parse_consumption_readings`: `None` raises `AttributeError`; empty or non-numeric elements raise `ValueError`.
- `format_billing_summary`: `None` raises `AttributeError`; missing fields raise `IndexError`; non-integer usage raises `ValueError`.

## Run

    pip install hypothesis pytest
    python processor.py
    python -m pytest test_processor.py
