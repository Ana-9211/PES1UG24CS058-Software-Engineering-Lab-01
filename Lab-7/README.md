# Lab 7: Fuzzing for Input Validation Bugs

SRN: PES1UG24CS058 | Student: Anagha N | Assigned repo: L6_L7_01 Water Utility Billing

Property-based fuzz testing of `processor.py` using Hypothesis and pytest. Fuzzing found crashes in all three functions, which were then fixed and re-tested.

## Files

| File | Description |
|------|-------------|
| `processor.py` | Fixed application script (hardened against fuzzed inputs) |
| `processor_buggy.py` | Original buggy starter code, kept for reference |
| `test_processor.py` | Completed Hypothesis fuzz tests |
| `test_processor_starter.py` | Original starter test file |
| `Lab7_Fuzz_Testing_Report_PES1UG24CS058.pdf` | PDF report with all screenshots and code |
| `evidence/` | Individual real terminal screenshots (PNG) |

## Bugs found by fuzzing

| Function | Failing input | Exception |
|----------|---------------|-----------|
| `sanitize_meter_id` | `None` | `AttributeError` |
| `parse_consumption_readings` | `None` | `AttributeError` |
| `parse_consumption_readings` | `''`, `'abc'`, empty element such as `'1,,3'` | `ValueError` |
| `format_billing_summary` | `None` | `AttributeError` |
| `format_billing_summary` | `''`, `'a'` (missing fields) | `IndexError` |
| `format_billing_summary` | `':'`, `'a:b:c'` (non-integer usage) | `ValueError` |

## Fixes

- `sanitize_meter_id`: returns `""` for non-string input.
- `parse_consumption_readings`: returns `[]` for non-string input and skips elements that are not integers.
- `format_billing_summary`: returns `"Invalid account record"` for non-string input, a wrong number of fields, an empty name or zone, non-integer usage, or negative usage.

## Tests

Each test uses `@given(st.text() | st.none())`, calls the function inside try/except so any exception fails the test, and also checks the result type. `sanitize_meter_id` is additionally checked to contain no `!@#$%` and to be upper-case.

Result: 3 failed against `processor_buggy.py`, 3 passed against `processor.py`.

## Screenshots (`evidence/`)

| Handout step | Files |
|--------------|-------|
| 1. Install dependencies | `step1_install.png` |
| 2. Run buggy `processor.py` | `step2a_buggy_run_readings_crash.png`, `step2b_buggy_run_record_crash.png` |
| 4. pytest on buggy code (failing) | `step4_pytest_failing_part1of5.png` to `part5of5.png`, `step4_summary_tb_no.png` |
| 5. Run fixed `processor.py` | `step5a_fixed_run_same_inputs_1.png`, `step5b_fixed_run_same_inputs_2.png`, `step5c_fixed_run_valid_inputs.png` |
| 6. pytest on fixed code (passing) | `step6_pytest_passing.png` |

## Run

    pip install hypothesis pytest
    python processor.py
    python -m pytest test_processor.py
