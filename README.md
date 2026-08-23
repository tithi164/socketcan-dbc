# AI-Assisted DBC Generation and CAN Data Visualization Using SocketCAN

A software-only automotive CAN communication project demonstrating CAN message creation, DBC-based signal decoding, Linux SocketCAN communication, and CAN data visualization using SavvyCAN.

---

## Project Overview

This project implements a virtual automotive CAN network using Linux SocketCAN and a virtual CAN interface (`vcan0`).

A DBC (CAN Database) file is used to define CAN messages, signals, scaling factors, offsets, ranges, and units.

A Python-based CAN transmitter generates vehicle parameters, encodes them according to the DBC definitions, and transmits CAN frames through SocketCAN.

SavvyCAN is used to connect to the virtual CAN interface, load the DBC file, decode the CAN frames, and display the signals as engineering values.

The complete workflow is:

```text
Vehicle Signals
        ↓
CAN Message Definition
        ↓
DBC File Creation
        ↓
DBC Validation
        ↓
SocketCAN Transmission
        ↓
Raw CAN Frames
        ↓
DBC Decoding
        ↓
SavvyCAN Visualization
```

---

# Implemented CAN Network

The project contains the following vehicle signals:

| CAN ID | Message Name | Signal Name | Factor | Offset | Range | Unit |
|--------|--------------|-------------|--------|--------|-------|------|
| 0x100 | VehicleSpeed | Vehicle_Speed | 0.1 | 0 | 0-120 | km/h |
| 0x101 | EngineRPM | Engine_RPM | 1 | 0 | 800-5000 | rpm |
| 0x102 | CoolantTemperature | Coolant_Temperature | 0.1 | -40 | 20-120 | °C |
| 0x103 | FuelLevel | Fuel_Level | 0.1 | 0 | 0-100 | % |
| 0x104 | BatteryVoltage | Battery_Voltage | 0.01 | 0 | 11-15 | V |
| 0x105 | AmbientTemperature | Ambient_Temperature | 0.1 | -40 | -40-80 | °C |

`AmbientTemperature` was added as the additional signal for Challenge 3.

---

# Repository Structure

```text
socketcan-dbc/
│
├── dbc/
│   ├── vehicle_network.dbc
│   └── challenge2_modified.dbc
│
├── src/
│   ├── can_transmitter.py
│   ├── validate_dbc.py
│   └── test_dbc_decoding.py
│
├── README.md
├── AI_USAGE_REPORT.md
├── TECHNICAL_REPORT.pdf
└── .gitignore
```

---

# File Description

## DBC Files

### `vehicle_network.dbc`

Final validated CAN database containing all vehicle messages and signal definitions.

### `challenge2_modified.dbc`

Modified DBC file used to demonstrate incorrect decoding caused by changing signal scaling.

---

## Source Files

### `src/can_transmitter.py`

Generates changing vehicle values, encodes them using the DBC file, and sends CAN frames through SocketCAN.

### `src/validate_dbc.py`

Checks the correctness of CAN message and signal definitions.

Validation includes:

- CAN identifiers
- DLC values
- Signal length
- Start bit positions
- Scaling factors
- Offsets
- Ranges
- Units

### `src/test_dbc_decoding.py`

Tests DBC decoding using predefined CAN data samples.

---

# Requirements

The project was developed using:

- Ubuntu Linux
- Python 3
- Linux SocketCAN
- Virtual CAN interface (`vcan0`)
- cantools
- python-can
- SavvyCAN

No physical CAN hardware is required.

---

# Setup

## 1. Create Virtual CAN Interface

Load the CAN virtual interface module:

```bash
sudo modprobe vcan
```

Create the virtual CAN interface:

```bash
sudo ip link add dev vcan0 type vcan
```

Enable the interface:

```bash
sudo ip link set up vcan0
```

Verify:

```bash
ip link show vcan0
```

Expected:

```text
vcan0: <NOARP,UP,LOWER_UP>
```

---

# Python Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install cantools python-can
```

---

# DBC Validation

Run:

```bash
python3 src/validate_dbc.py
```

The script verifies the correctness of the DBC definitions.

Example output:

```text
DBC Definition Validation : PASS
```

Run decoding tests:

```bash
python3 src/test_dbc_decoding.py
```

Example output:

```text
DBC Decoding Validation : PASS
```

---

# CAN Transmission

Start the CAN transmitter:

```bash
python3 src/can_transmitter.py
```

The transmitter generates vehicle parameters and sends CAN frames through:

```text
vcan0
```

---

# Viewing Raw CAN Frames

Open another terminal:

```bash
candump vcan0
```

Example output:

```text
vcan0  100   [2]  97 02
vcan0  101   [2]  XX XX
vcan0  102   [2]  XX XX
vcan0  103   [2]  XX XX
vcan0  104   [2]  XX XX
vcan0  105   [2]  C2 02
```

The payload changes according to the transmitted vehicle values.

---

# DBC Decoding Example

Captured CAN frame:

```text
vcan0 100 [2] 97 02
```

Raw data:

```text
0x0297 = 663
```

DBC scaling:

```text
Factor = 0.1
```

Decoded value:

```text
663 × 0.1 = 66.3 km/h
```

Result:

```text
Vehicle_Speed = 66.3 km/h
```

---

# SavvyCAN Visualization

SavvyCAN was used to analyze and visualize CAN communication.

The connection flow:

```text
Python CAN Transmitter
        ↓
SocketCAN
        ↓
vcan0
        ↓
SavvyCAN
        ↓
vehicle_network.dbc
        ↓
Decoded Engineering Values
```

SavvyCAN was connected using:

```text
Interface : SocketCAN
Device    : vcan0
DBC       : vehicle_network.dbc
```

The following signals were monitored:

```text
Vehicle_Speed
Engine_RPM
Coolant_Temperature
Fuel_Level
Battery_Voltage
Ambient_Temperature
```

---

# Challenges Completed

## Challenge 1 — Raw Data vs Decoded Data

A raw CAN frame was compared with its DBC-decoded engineering value.

Example:

```text
Raw CAN Frame:

vcan0 100 [2] 97 02


Decoded Value:

Vehicle_Speed = 66.3 km/h
```

This demonstrates conversion of raw CAN bytes into meaningful engineering data.

---

## Challenge 2 — DBC Modification

The Vehicle Speed scaling factor was intentionally modified:

Original:

```text
Factor = 0.1
```

Modified:

```text
Factor = 1
```

The incorrect DBC produced incorrect engineering values.

The original DBC was restored after verification.

---

## Challenge 3 — Adding New Signal

A new signal was added:

```text
Signal Name : Ambient_Temperature
CAN ID      : 0x105
Factor      : 0.1
Offset      : -40
Unit        : °C
```

Example frame:

```text
vcan0 105 [2] C2 02
```

Calculation:

```text
0x02C2 = 706

706 × 0.1 - 40

= 30.6 °C
```

The new signal was successfully transmitted, decoded, and visualized.

---

## Challenge 4 — AI-Assisted Review

AI assistance was used for reviewing:

- DBC structure
- Signal definitions
- Scaling values
- Naming consistency
- Documentation quality

All suggestions were manually reviewed before implementation.

---

# Final Validation

The completed project successfully passed:

```text
DBC Definition Validation : PASS

DBC Decoding Validation : PASS
```

All CAN messages and signals were verified against their expected engineering values.

---

# Learning Outcomes

This project demonstrates:

- CAN message and signal design
- DBC file creation
- DBC validation
- CAN encoding and decoding
- Linux SocketCAN communication
- Software-only CAN testing
- Virtual CAN interface usage
- SavvyCAN analysis and visualization
- Effects of incorrect DBC definitions
- Adding and validating new CAN signals

---

# Conclusion

This project demonstrates the complete automotive CAN data workflow:

```text
Engineering Values
        ↓
DBC Definition
        ↓
CAN Frames
        ↓
SocketCAN Communication
        ↓
DBC Decoding
        ↓
Human Readable Data
```

Using SocketCAN, cantools, python-can, and SavvyCAN provides a complete software-only environment for developing and validating CAN communication without requiring physical CAN hardware.
