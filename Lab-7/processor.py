INVALID_RECORD_MSG = "Invalid account record"


def sanitize_meter_id(meter_id):
    """Strip whitespace and the prefix symbols !@#$%, then upper-case.

    Non-string input (e.g. None) yields an empty string instead of crashing.
    """
    if not isinstance(meter_id, str):
        return ""
    meter_id = meter_id.strip()
    for ch in ['!', '@', '#', '$', '%']:
        meter_id = meter_id.replace(ch, '')
    return meter_id.upper()


def parse_consumption_readings(readings_csv):
    """Parse a comma-separated string of integers.

    Empty, malformed or non-numeric elements are skipped; non-string input
    yields an empty list.
    """
    if not isinstance(readings_csv, str):
        return []
    readings = []
    for item in readings_csv.split(','):
        try:
            readings.append(int(item.strip()))
        except ValueError:
            continue
    return readings


def format_billing_summary(account_record):
    """Format a 'Name:Usage:Zone' record as a billing summary.

    Returns INVALID_RECORD_MSG for non-string input, a wrong number of
    fields, an empty name/zone, or non-integer / negative usage.
    """
    if not isinstance(account_record, str):
        return INVALID_RECORD_MSG
    parts = account_record.split(':')
    if len(parts) != 3:
        return INVALID_RECORD_MSG
    customer_name = parts[0].strip()
    zone = parts[2].strip()
    if not customer_name or not zone:
        return INVALID_RECORD_MSG
    try:
        units = int(parts[1].strip())
    except ValueError:
        return INVALID_RECORD_MSG
    if units < 0:
        return INVALID_RECORD_MSG
    return f"Customer {customer_name} billed {units * 2} USD in {zone}"


def main():
    print("==== Running sanitize_meter_id ====")
    raw_id = input("Enter a meter ID with prefixes (!,@,#,$,%): ")
    clean_id = sanitize_meter_id(raw_id)
    print("Sanitized Meter ID:", clean_id)

    print("\n==== Running parse_consumption_readings ====")
    csv_input = input("Enter consumption readings (e.g. 10,25,30): ")
    readings_list = parse_consumption_readings(csv_input)
    print("Parsed Readings:", readings_list)

    print("\n==== Running format_billing_summary ====")
    summary_input = input("Enter account record (Name:Usage:Zone): ")
    summary = format_billing_summary(summary_input)
    print("Billing Summary:", summary)

if __name__ == "__main__":
    main()