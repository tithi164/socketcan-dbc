
import cantools

DBC_FILE = "dbc/vehicle_network.dbc"

db = cantools.database.load_file(DBC_FILE)

print("=" * 60)
print("           DBC VALIDATION")
print("=" * 60)

print(f"DBC file: {DBC_FILE}")
print(f"Messages found: {len(db.messages)}")
print()

expected = {
    "VehicleSpeed": {
        "id": 0x100,
        "signal": "Vehicle_Speed",
        "length": 16,
        "factor": 0.1,
        "offset": 0,
        "minimum": 0,
        "maximum": 120,
        "unit": "km/h",
    },
    "EngineRPM": {
        "id": 0x101,
        "signal": "Engine_RPM",
        "length": 16,
        "factor": 1,
        "offset": 0,
        "minimum": 800,
        "maximum": 5000,
        "unit": "rpm",
    },
    "CoolantTemperature": {
        "id": 0x102,
        "signal": "Coolant_Temperature",
        "length": 16,
        "factor": 0.1,
        "offset": -40,
        "minimum": 20,
        "maximum": 120,
        "unit": "degC",
    },
    "FuelLevel": {
        "id": 0x103,
        "signal": "Fuel_Level",
        "length": 16,
        "factor": 0.1,
        "offset": 0,
        "minimum": 0,
        "maximum": 100,
        "unit": "%",
    },
    "BatteryVoltage": {
        "id": 0x104,
        "signal": "Battery_Voltage",
        "length": 16,
        "factor": 0.01,
        "offset": 0,
        "minimum": 11,
        "maximum": 15,
        "unit": "V",
    },
    "AmbientTemperature": {
        "id": 0x105,
        "signal": "Ambient_Temperature",
        "length": 16,
        "factor": 0.1,
        "offset": -40,
        "minimum": -40,
        "maximum": 80,
        "unit": "degC",
    },
}

all_passed = True

for message_name, expected_data in expected.items():

    try:
        message = db.get_message_by_name(message_name)
    except KeyError:
        print(f"[FAIL] Message not found: {message_name}")
        all_passed = False
        continue

    signal = message.get_signal_by_name(expected_data["signal"])

    print(f"Message: {message.name}")
    print(f"  CAN ID       : 0x{message.frame_id:X}")
    print(f"  DLC          : {message.length}")
    print(f"  Signal       : {signal.name}")
    print(f"  Start bit    : {signal.start}")
    print(f"  Length       : {signal.length}")
    print(f"  Signed       : {signal.is_signed}")
    print(f"  Factor       : {signal.scale}")
    print(f"  Offset       : {signal.offset}")
    print(f"  Range        : {signal.minimum} to {signal.maximum}")
    print(f"  Unit         : {signal.unit}")

    checks = [
        ("CAN ID", message.frame_id, expected_data["id"]),
        ("Signal length", signal.length, expected_data["length"]),
        ("Scaling", signal.scale, expected_data["factor"]),
        ("Offset", signal.offset, expected_data["offset"]),
        ("Minimum", signal.minimum, expected_data["minimum"]),
        ("Maximum", signal.maximum, expected_data["maximum"]),
        ("Unit", signal.unit, expected_data["unit"]),
    ]

    for check_name, actual, expected_value in checks:
        if actual != expected_value:
            print(
                f"  [FAIL] {check_name}: "
                f"expected {expected_value}, got {actual}"
            )
            all_passed = False

    print()

print("=" * 60)

if all_passed:
    print("VALIDATION RESULT: PASS")
    print("All message and signal definitions match the design.")
else:
    print("VALIDATION RESULT: FAIL")
    print("One or more DBC definitions require correction.")

print("=" * 60)
