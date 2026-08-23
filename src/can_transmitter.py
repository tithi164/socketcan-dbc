import time
import math
import random
import can
import cantools

DBC_FILE = "dbc/vehicle_network.dbc"
CAN_INTERFACE = "vcan0"

db = cantools.database.load_file(DBC_FILE)

bus = can.Bus(
    interface="socketcan",
    channel=CAN_INTERFACE,
    receive_own_messages=False
)

print("=" * 60)
print("        Vehicle Information CAN Transmitter")
print("=" * 60)
print(f"CAN interface : {CAN_INTERFACE}")
print(f"DBC file      : {DBC_FILE}")
print("Status        : Running")
print("Press Ctrl+C to stop")
print("=" * 60)

start_time = time.time()

try:
    while True:
        elapsed = time.time() - start_time

        # Generate realistic changing vehicle values
        speed = 60 + 40 * math.sin(elapsed / 5)
        speed = max(0, min(120, speed))

        rpm = 800 + (speed / 120) * 4200
        rpm += random.uniform(-50, 50)
        rpm = max(800, min(5000, rpm))

        coolant = 70 + 15 * math.sin(elapsed / 15)
        coolant += random.uniform(-0.5, 0.5)
        coolant = max(20, min(120, coolant))

        fuel = 90 - elapsed / 120
        fuel = max(0, min(100, fuel))

        battery = 13.2 + 0.4 * math.sin(elapsed / 8)
        battery += random.uniform(-0.03, 0.03)
        battery = max(11, min(15, battery))

        ambient = 28 + 3 * math.sin(elapsed / 20)
        ambient += random.uniform(-0.2, 0.2)
        ambient = max(-40, min(80, ambient))

        signals = [
            ("VehicleSpeed", {"Vehicle_Speed": speed}),
            ("EngineRPM", {"Engine_RPM": rpm}),
            ("CoolantTemperature", {"Coolant_Temperature": coolant}),
            ("FuelLevel", {"Fuel_Level": fuel}),
            ("BatteryVoltage", {"Battery_Voltage": battery}),
            ("AmbientTemperature", {"Ambient_Temperature": ambient}),
        ]

        for message_name, signal_data in signals:
            message_definition = db.get_message_by_name(message_name)

            encoded_data = message_definition.encode(signal_data)

            message = can.Message(
                arbitration_id=message_definition.frame_id,
                data=encoded_data,
                is_extended_id=False
            )

            bus.send(message)

        print(
            f"Speed={speed:6.1f} km/h | "
            f"RPM={rpm:7.0f} rpm | "
            f"Coolant={coolant:5.1f} °C | "
            f"Fuel={fuel:5.1f} % | "
            f"Battery={battery:4.2f} V | "
            f"Ambient={ambient:5.1f} °C"
        )

        time.sleep(1)

except KeyboardInterrupt:
    print("\nTransmitter stopped.")

finally:
    bus.shutdown()
