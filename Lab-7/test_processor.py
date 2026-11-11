from hypothesis import given, strategies as st
from processor import sanitize_meter_id, parse_consumption_readings, format_billing_summary


@given(st.text() | st.none())
def test_sanitize_meter_id_no_crash(s):
    try:
        result = sanitize_meter_id(s)
    except Exception as e:
        assert False, f"sanitize_meter_id crashed with: {e!r}"
    assert isinstance(result, str)
    assert not any(ch in result for ch in "!@#$%")
    assert result == result.upper()


@given(st.text() | st.none())
def test_parse_consumption_readings_safe(s):
    try:
        result = parse_consumption_readings(s)
    except Exception as e:
        assert False, f"parse_consumption_readings crashed with: {e!r}"
    assert isinstance(result, list)
    assert all(isinstance(r, int) for r in result)


@given(st.text() | st.none())
def test_format_billing_summary_safe(s):
    try:
        result = format_billing_summary(s)
    except Exception as e:
        assert False, f"format_billing_summary crashed with: {e!r}"
    assert isinstance(result, str)
