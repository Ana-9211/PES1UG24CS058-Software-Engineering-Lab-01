import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


def acct(blocks, active=True, commercial=False, waiver=False):
    return {"is_active": active, "is_commercial": commercial,
            "has_leak_waiver": waiver, "usage_blocks": blocks}


# ---- Branch coverage tests: every decision taken both True and False ----
def test_single_active_residential():
    result = calculate_water_bill([acct([30])], 10.0)
    assert result == {"total_billed": 55.0, "status": "NORMAL"}


@pytest.mark.parametrize("accounts,fee", [("x", 10.0), (None, 10.0), ([], -0.01)])
def test_invalid_inputs_raise(accounts, fee):
    with pytest.raises(ValueError):
        calculate_water_bill(accounts, fee)


def test_zero_fee_and_empty_list_is_valid():
    assert calculate_water_bill([], 0) == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


def test_inactive_and_missing_is_active_skipped():
    accounts = [acct([30], active=False), {"usage_blocks": [30]}]
    assert calculate_water_bill(accounts, 10.0)["status"] == "NO_ACTIVITY"


def test_active_account_without_usage_blocks():
    result = calculate_water_bill([{"is_active": True}], 10.0)
    assert result == {"total_billed": 10.0, "status": "NORMAL"}


def test_zero_and_negative_usage_flagged_and_skipped():
    result = calculate_water_bill([acct([0, -5, 10])], 10.0)
    assert result["total_billed"] == 25.0


def test_tier_boundaries():
    assert calculate_water_bill([acct([50])], 0)["total_billed"] == 75.0    # <=50
    assert calculate_water_bill([acct([51])], 0)["total_billed"] == 127.5   # >50
    assert calculate_water_bill([acct([100])], 0)["total_billed"] == 250.0  # <=100
    assert calculate_water_bill([acct([101])], 0)["total_billed"] == 454.5  # >100


def test_residential_over_100_breaks_loop():
    result = calculate_water_bill([acct([120, 10])], 10.0)
    assert result["total_billed"] == 10.0 + 120 * 4.5


def test_commercial_over_100_continues_loop():
    result = calculate_water_bill([acct([120, 10], commercial=True)], 10.0)
    assert result["total_billed"] == 10.0 + 120 * 3.5 + 10 * 1.5


def test_leak_waiver_over_threshold():
    result = calculate_water_bill([acct([120], waiver=True)], 10.0)
    assert result["total_billed"] == 500.0


def test_leak_waiver_at_threshold_not_applied():
    # 140 + 40 * 1.5 = 200.0 exactly, not > 200, so no discount
    result = calculate_water_bill([acct([40], waiver=True)], 140.0)
    assert result["total_billed"] == 200.0


def test_no_waiver_over_threshold_not_discounted():
    result = calculate_water_bill([acct([120], waiver=False)], 10.0)
    assert result["total_billed"] == 550.0


def test_flags_boundary_five_vs_six():
    five = calculate_water_bill([acct([0] * 5)], 10.0)
    six = calculate_water_bill([acct([0] * 6)], 10.0)
    assert five["status"] == "NORMAL"
    assert six["status"] == "EXCESSIVE_FLAGS"


def test_no_activity_status_zero_total():
    assert calculate_water_bill([acct([0, 0], active=False)], 10.0)["status"] == "NO_ACTIVITY"


def test_zero_base_fee_zero_usage_is_no_activity():
    assert calculate_water_bill([acct([])], 0)["status"] == "NO_ACTIVITY"


def test_tampering_no_data():
    assert check_meter_tampering([]) == "NO_DATA"
    assert check_meter_tampering(None) == "NO_DATA"


def test_tampering_two_consecutive_negatives():
    assert check_meter_tampering([[5, -1, -2]]) == "TAMPER_SUSPECTED"


def test_tampering_negative_then_positive_resets():
    assert check_meter_tampering([[-1, 3, -1, 2]]) == "CLEAR"


def test_tampering_empty_meter_and_later_meter():
    assert check_meter_tampering([[], [1, 2], [-1, -1]]) == "TAMPER_SUSPECTED"


def test_tampering_clear():
    assert check_meter_tampering([[1, 2, 3], [0, 0]]) == "CLEAR"
