# Wiring Diagram

## Component List

### Main Components
- ESP32 DevKit V1 (30-pin)
- DS18B20 Waterproof Temperature Sensor
- Analog pH Meter V4.0
- Analog TDS Sensor
- Float Switch (NC - Normally Closed)
- 2-Channel Relay Module (5V, Active LOW)
- Power Supply 5V 3A

### Additional Components
- 4.7kΩ Resistor (for DS18B20 pull-up)
- Jumper wires
- Breadboard (optional, untuk prototyping)
- Screw terminals (untuk sensor connections)

## ESP32 Pinout Reference

```
                    ESP32 DevKit V1
                   ┌─────────────┐
              EN  ─┤  1      30  ├─ D23
             VP   ─┤  2      29  ├─ D22  
             VN   ─┤  3      28  ├─ TXD0
             D34* ─┤  4      27  ├─ RXD0
             D35* ─┤  5      26  ├─ D21
             D32* ─┤  6      25  ├─ D19
             D33  ─┤  7      24  ├─ D18
   DS18B20→  D25  ─┤  8      23  ├─ D5
             D26  ─┤  9      22  ├─ D17  ←Light Relay
Float SW →   D27  ─┤ 10      21  ├─ D16  ←Pump Relay
             D14  ─┤ 11      20  ├─ GND
             D12  ─┤ 12      19  ├─ 3V3
             GND  ─┤ 13      18  ├─ D15
             D13  ─┤ 14      17  ├─ D2
             D9   ─┤ 15      16  ├─ D0
             D10  ─┤ 16      15  ├─ D4
             D11  ─┤ 17      14  ├─ D3
             VIN  ─┤ 18      13  ├─ D1
             GND  ─┤ 19      12  ├─ 5V
             3V3  ─┤ 20      11  ├─ CMD
             NC   ─┤ 21      10  ├─ SD3
       TDS→  D32* ─┤ 22       9  ├─ SD2
             D33  ─┤ 23       8  ├─ SD1
        pH→  D34* ─┤ 24       7  ├─ SD0
             D35* ─┤ 25       6  ├─ CLK
             D36* ─┤ 26       5  ├─ D8
             D39* ─┤ 27       4  ├─ D7
             EN   ─┤ 28       3  ├─ D6
             GND  ─┤ 29       2  ├─ D5
             3V3  ─┤ 30       1  ├─ GND
                   └─────────────┘

* = Input only (ADC capable)
```

## Pin Assignments

| Function | GPIO | ESP32 Pin |
|----------|------|-----------|
| DS18B20 (OneWire) | GPIO 25 | Pin 8 |
| pH Sensor (Analog) | GPIO 34 | Pin 24 (ADC1_CH6) |
| TDS Sensor (Analog) | GPIO 32 | Pin 22 (ADC1_CH4) |
| Float Switch | GPIO 27 | Pin 10 |
| Pump Relay | GPIO 16 | Pin 21 |
| Light Relay | GPIO 17 | Pin 22 |

## Detailed Wiring

### 1. DS18B20 Temperature Sensor

```
DS18B20               ESP32
┌─────────┐          ┌─────────┐
│  RED    ├──────────┤  3.3V   │
│ (VCC)   │          │         │
│         │   4.7kΩ  │         │
│  YELLOW ├───/\/\───┤  3.3V   │ (Pull-up resistor)
│ (DATA)  ├──────────┤  D25    │
│         │          │         │
│  BLACK  ├──────────┤  GND    │
│ (GND)   │          │         │
└─────────┘          └─────────┘
```

**Important**: 
- 4.7kΩ pull-up resistor between DATA and VCC sangat penting
- Gunakan 3.3V, BUKAN 5V (ESP32 is 3.3V logic)

### 2. pH Sensor

```
pH Sensor V4.0        ESP32
┌─────────┐          ┌─────────┐
│  RED    ├──────────┤  5V     │ (atau VIN dari USB)
│ (VCC)   │          │         │
│         │          │         │
│  BLUE   ├──────────┤  D34    │ (ADC pin)
│ (SIGNAL)│          │         │
│         │          │         │
│  BLACK  ├──────────┤  GND    │
│ (GND)   │          │         │
└─────────┘          └─────────┘
```

**Notes**:
- pH sensor needs 5V power
- Signal output sudah 0-3.3V compatible
- D34 adalah input-only pin (ADC1_CH6)

### 3. TDS Sensor

```
TDS Sensor            ESP32
┌─────────┐          ┌─────────┐
│  RED    ├──────────┤  3.3V   │
│ (VCC)   │          │         │
│         │          │         │
│  BLACK  ├──────────┤  D32    │ (ADC pin)
│ (SIGNAL)│          │         │
│         │          │         │
│  BLACK  ├──────────┤  GND    │
│ (GND)   │          │         │
└─────────┘          └─────────┘
```

**Notes**:
- TDS sensor menggunakan 3.3V
- D32 adalah ADC1_CH4

### 4. Float Switch

```
Float Switch          ESP32
┌─────────┐          ┌─────────┐
│  COM    ├──────────┤  D27    │
│ (Common)│          │         │
│         │          │         │
│   NC    ├──────────┤  GND    │
│(Normally│          │         │
│ Closed) │          │         │
└─────────┘          └─────────┘
```

**Notes**:
- NC (Normally Closed) configuration
- Internal pull-up resistor di ESP32 diaktifkan di code
- Float DOWN (low water) = LOW signal
- Float UP (normal water) = HIGH signal

### 5. 2-Channel Relay Module

```
Relay Module          ESP32
┌─────────┐          ┌─────────┐
│  VCC    ├──────────┤  5V     │
│         │          │         │
│  GND    ├──────────┤  GND    │
│         │          │         │
│  IN1    ├──────────┤  D16    │ (Pump)
│         │          │         │
│  IN2    ├──────────┤  D17    │ (Light)
│         │          │         │
└─────────┘          └─────────┘
```

**AC Load Connections**:
```
Relay 1 (Pump)
┌──────┐
│  COM ├───── AC Line
│      │
│  NO  ├───── To Pump
│      │
│  NC  │ (not used)
└──────┘

Relay 2 (Light)
┌──────┐
│  COM ├───── AC Line
│      │
│  NO  ├───── To Light
│      │
│  NC  │ (not used)
└──────┘
```

**Notes**:
- Relay adalah Active LOW (LOW = ON, HIGH = OFF)
- MAX rating: 10A 250VAC or 10A 30VDC
- ⚠️ **DANGER**: AC voltage! Pastikan wiring benar dan aman!

## Power Supply

### Option 1: USB Power (untuk testing)
```
USB 5V ─────► ESP32 (via USB port)
     │
     └──────► 5V pin (untuk Relay Module & pH sensor)
```

**Limitations**:
- Maksimum ~500mA dari USB
- Might not enough untuk relay + pompa

### Option 2: External Power Supply (recommended)
```
Power Supply 5V 3A
     │
     ├──────► VIN pin (ESP32)
     │
     ├──────► Relay Module VCC
     │
     └──────► Common GND
```

## Complete System Diagram

```
                    ┌─────────────────────────────┐
                    │    ESP32 DevKit V1          │
                    │                             │
        ┌───────────┤ D25                     5V  ├──────┐
        │           │                             │      │
     DS18B20        │ D34                    GND  ├──┐   │
    (OneWire)       │                             │  │   │
                    │ D32                    3.3V ├─┐│   │
        ┌───────────┤                             │ ││   │
        │           │ D27                         │ ││   │
     TDS Sensor  ┌──┤                             │ ││   │
                 │  │ D16 (Pump)                  │ ││   │
    Float    ────┘  │                             │ ││   │
    Switch          │ D17 (Light)                 │ ││   │
                    └─────────────────────────────┘ ││   │
        │                   │           │           ││   │
        │                   │           │           ││   │
    pH Sensor          Relay Module    │           ││   │
    (5V power) ────────────┬────────────┘           ││   │
                           │                        ││   │
                        Pump & Light                ││   │
                        (AC Load)                   ││   │
                                                    ││   │
    Common Ground ──────────────────────────────────┘│   │
    3.3V Rail ───────────────────────────────────────┘   │
    5V Rail ─────────────────────────────────────────────┘
```

## Safety Considerations

⚠️ **IMPORTANT SAFETY WARNINGS**:

1. **High Voltage**
   - Relay outputs switch AC 220V
   - Only qualified personnel should wire AC side
   - Use proper insulation dan enclosure

2. **Water + Electricity**
   - Keep ESP32 dan relay module DRY
   - Use waterproof sensors only
   - Proper grounding essential

3. **Power Supply**
   - Use stable 5V 3A power supply
   - Avoid voltage spikes
   - Add fuse protection (recommended)

4. **Testing**
   - Test wiring WITHOUT AC power first
   - Use multimeter to verify connections
   - Check for shorts before powering on

## Troubleshooting Wiring

### Sensor Not Reading

1. **Check Power**: Measure voltage at sensor VCC dan GND pins
2. **Check Continuity**: Test wire connections dengan multimeter
3. **Check Pin Assignment**: Verify GPIO numbers dalam config.py match wiring

### Relay Not Switching

1. **Check Signal**: Measure voltage at IN1/IN2 (should be 0V or 3.3V)
2. **Check Relay Power**: Verify 5V VCC at relay module
3. **Listen**: Relay should "click" when switching
4. **LED Indicator**: Most relay modules memiliki LED indicator

### DS18B20 Specific

1. **Pull-up Resistor**: Essential! 4.7kΩ between DATA dan VCC
2. **Parasitic Power**: Tidak recommended - use separate VCC
3. **Multiple Sensors**: Each sensor needs unique ROM address

## Testing Procedure

1. **Visual Inspection**: Check semua connections
2. **Power Test**: Measure voltages (3.3V, 5V, GND)
3. **Continuity Test**: Verify wire connections
4. **Individual Sensor Test**: Test tiap sensor di REPL
5. **Full System Test**: Run main.py dan monitor serial output
