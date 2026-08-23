
import cantools

DBC_FILE = "dbc/vehicle_network.dbc"

db = cantools.database.load_file(DBC_FILE)

test_vectors = [
    ("VehicleSpeed", 0x100, bytes([0x8A, 0x02]), "Vehicle_Speed", 65.0),
    ("EngineRPM", 0x101, bytes([0x92, 0x09]), "Engine_RPM", 2450),
    ("CoolantTemperature", 0x102, bytes([0xF6, 0x04]), "Coolant_Temperature", 87.0),
    ("FuelLevel", 0x103, bytes([0xD0, 0x02]), "Fuel_Level", 72.0),
    ("BatteryVoltage", 0x104, bytes([0xE2, 0x04]), "Battery_Voltage", 12.50),
    ("AmbientTemperature", 0x105, bytes([0xBC, 0x03]), "Ambient_Temperature", 55.6),
]

print("=" * 60)
print("             DBC DECODING TEST")
print("=" * 60)

all_passed = True

for message_name, can_id, data, signal_name, expected in test_vectors:

    message = db.get_message_by_frame_id(can_id)

    decoded = message.decode(data)

    actual = decoded[signal_name]

    passed = abs(actual - expected) < 0.001

    status = "PASS" if passed else "FAIL"

    print(f"{status}: {message_name}")
    print(f"  CAN ID  : 0x{can_id:X}")
    print(f"  Raw     : {' '.join(f'{b:02X}' for b in data)}")
    print(f"  Signal  : {signal_name}")
    print(f"  Expected: {expected}")
    print(f"  Decoded : {actual}")
    print()

    if not passed:
        all_passed = False

print("=" * 60)

if all_passed:
    print("DECODING RESULT: PASS")
else:
    print("DECODING RESULT: FAIL")

print("=" * 60)

