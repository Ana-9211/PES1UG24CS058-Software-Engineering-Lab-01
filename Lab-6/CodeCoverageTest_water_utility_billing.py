import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


def acct(blocks, active=True, commercial=False, waiver=False):
    return {"is_active": active, "is_commercial": commercial,
            "has_leak_waiver": waiver, "usage_blocks": blocks}


# ---- Code (line) coverage tests ----
def test_single_active_residential():
    result = calculate_water_bill([acct([30])], 10.0)
    assert result["total_billed"] == 55.0
    assert result["status"] == "NORMAL"


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        calculate_water_bill("not a list", 10.0)
    with pytest.raises(ValueError):
        calculate_water_bill([], -1)


def test_inactive_account_skipped():
    result = calculate_water_bill([acct([30], active=False)], 10.0)
    assert result == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


def test_non_positive_usage_flagged():
    result = calculate_water_bill([acct([0])], 10.0)
    assert result["total_billed"] == 10.0


def test_medium_usage_rate():
    assert calculate_water_bill([acct([60])], 10.0)["total_billed"] == 160.0


def test_residential_over_100_breaks():
    result = calculate_water_bill([acct([120, 10])], 10.0)
    assert result["total_billed"] == 10.0 + 120 * 4.5


def test_commercial_over_100():
    result = calculate_water_bill([acct([120], commercial=True)], 10.0)
    assert result["total_billed"] == 10.0 + 120 * 3.5


def test_leak_waiver_applied():
    result = calculate_water_bill([acct([120], waiver=True)], 10.0)
    assert result["total_billed"] == 10.0 + 120 * 4.5 - 50.0


def test_excessive_flags():
    result = calculate_water_bill([acct([0, 0, 0, 0, 0, 0])], 10.0)
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_tampering_no_data():
    assert check_meter_tampering([]) == "NO_DATA"


def test_tampering_suspected():
    assert check_meter_tampering([[5, -1, -2]]) == "TAMPER_SUSPECTED"


def test_tampering_clear():
    assert check_meter_tampering([[5, -1, 3, -1, 2]]) == "CLEAR"
