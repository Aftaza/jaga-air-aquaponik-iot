# IoT Aquaponik Mini - Monitoring System

Sistem monitoring aquaponik berbasis IoT menggunakan ESP32 dan Flutter mobile app. Sistem ini memonitor suhu, pH, TDS, dan level air secara real-time dengan data dikirim ke ThingSpeak via MQTT.

## 📋 Fitur Utama

### Flutter Mobile App
- **Dashboard Real-time**: Menampilkan pembacaan sensor secara real-time
  - Suhu air (DS18B20)
  - pH level (Analog pH Meter V4.0)
  - TDS - Total Dissolved Solids (Analog TDS Sensor)
  - Water level (Float Switch)
- **Grafik Historical Data**: Visualisasi data dalam berbagai rentang waktu (24 jam, 7 hari, 30 hari)
- **Kontrol Aktuator**: Toggle ON/OFF untuk pompa air dan lampu grow light
- **Settings**: Konfigurasi WiFi, ThingSpeak, dan threshold parameter
- **Status Monitoring**: Battery level, sinyal WiFi (RSSI), connection status

### ESP32 MicroPython
- **Pembacaan Sensor**: Multi-sensor monitoring dengan interval yang dapat dikonfigurasi
- **Kontrol Aktuator**: 2-channel relay untuk pompa dan lampu
- **WiFi Connectivity**: Auto-connect dan auto-reconnect
- **MQTT Client**: Publish data ke ThingSpeak dengan field mapping
- **Threshold Checking**: Alert ketika nilai sensor melewati batas
- **Watchdog Timer**: System recovery pada error

## 🛠️ Teknologi

- **Mobile App**: Flutter/Dart
- **Hardware**: ESP32 DevKit V1
- **Firmware**: MicroPython
- **Cloud IoT**: ThingSpeak (MQTT)
- **Charts**: fl_chart package

## 📁 Struktur Project

```
jagaair_app/
├── lib/                          # Flutter application
│   ├── models/                   # Data models
│   │   ├── sensor_data.dart
│   │   ├── actuator_status.dart
│   │   └── device_status.dart
│   ├── screens/                  # UI screens
│   │   ├── splash_screen.dart
│   │   ├── dashboard_screen.dart
│   │   ├── chart_screen.dart
│   │   └── settings_screen.dart
│   ├── widgets/                  # Reusable widgets
│   │   ├── sensor_card.dart
│   │   ├── actuator_card.dart
│   │   └── main_navigation_bar.dart
│   ├── services/                 # Services
│   │   └── mock_data_service.dart
│   ├── theme/                    # App theme
│   │   └── app_theme.dart
│   └── main.dart                 # App entry point
├── scripts/                      # ESP32 MicroPython code
│   ├── sensors/                  # Sensor drivers
│   │   ├── ds18b20.py
│   │   ├── ph_sensor.py
│   │   ├── tds_sensor.py
│   │   └── float_switch.py
│   ├── actuators/                # Actuator drivers
│   │   └── relay.py
│   ├── wifi_manager.py           # WiFi connection manager
│   ├── mqtt_client.py            # ThingSpeak MQTT client
│   ├── config.py                 # Configuration file
│   ├── boot.py                   # Boot script
│   └── main.py                   # Main application
└── docs/                         # Documentation
    ├── README.md
    ├── FLUTTER_SETUP.md
    ├── ESP32_SETUP.md
    ├── SENSOR_CALIBRATION.md
    ├── THINGSPEAK_SETUP.md
    ├── WIRING_DIAGRAM.md
    └── TROUBLESHOOTING.md
```

## 🚀 Quick Start

### 1. Flutter App

```bash
# Install dependencies
cd jagaair_app
flutter pub get

# Run on device/emulator
flutter run
```

Lihat [FLUTTER_SETUP.md](FLUTTER_SETUP.md) untuk detail lengkap.

### 2. ESP32 Setup

1. Flash MicroPython ke ESP32
2. Edit `scripts/config.py` dengan WiFi dan ThingSpeak credentials
3. Upload semua file di folder `scripts/` ke ESP32
4. Reset ESP32

Lihat [ESP32_SETUP.md](ESP32_SETUP.md) untuk detail lengkap.

### 3. ThingSpeak Setup

1. Buat channel di ThingSpeak
2. Konfigurasi field mapping
3. Generate API keys dan MQTT credentials

Lihat [THINGSPEAK_SETUP.md](THINGSPEAK_SETUP.md) untuk detail lengkap.

## 📊 Sensor Specifications

| Sensor | Range | Akurasi | Update Interval |
|--------|-------|---------|-----------------|
| DS18B20 (Suhu) | -55°C to +125°C | ±0.5°C | 30 detik |
| pH Meter | 0-14 pH | Linear 0-3.3V | 5 menit |
| TDS Sensor | 0-1000 ppm | ±10% F.S. | 2 menit |
| Float Switch | ON/OFF | Digital | Continuous |

## 🎯 Threshold Defaults

| Parameter | Min Normal | Max Normal | Critical Min | Critical Max |
|-----------|------------|------------|--------------|--------------|
| Suhu | 22°C | 30°C | 20°C | 32°C |
| pH | 6.5 | 7.5 | 6.0 | 8.0 |
| TDS | 300 ppm | 600 ppm | 200 ppm | 800 ppm |

## 🔌 Pin Configuration

| Component | GPIO Pin |
|-----------|----------|
| DS18B20 (OneWire) | GPIO 25 |
| pH Sensor (ADC) | GPIO 34 |
| TDS Sensor (ADC) | GPIO 32 |
| Float Switch | GPIO 27 |
| Pump Relay | GPIO 16 |
| Light Relay | GPIO 17 |

## 📚 Documentation

- [Flutter App Setup](FLUTTER_SETUP.md)
- [ESP32 Setup Guide](ESP32_SETUP.md)
- [Sensor Calibration](SENSOR_CALIBRATION.md)
- [ThingSpeak Configuration](THINGSPEAK_SETUP.md)
- [Wiring Diagram](WIRING_DIAGRAM.md)
- [Troubleshooting](TROUBLESHOOTING.md)

## ⚠️ Catatan Penting

- **Mock Data**: Saat ini Flutter app menggunakan mock data service. Integrasi dengan ThingSpeak API akan ditambahkan di versi berikutnya.
- **Calibration**: Sensor pH dan TDS memerlukan kalibrasi sebelum penggunaan. Lihat [SENSOR_CALIBRATION.md](SENSOR_CALIBRATION.md).
- **Power Supply**: Gunakan adapter 5V 3A atau power bank dengan passthrough charging.
- **WiFi**: Pastikan ESP32 dalam jangkauan WiFi yang stabil untuk koneksi MQTT yang reliable.

## 📝 License

Personal Project - IoT Aquaponik Mini v1.0

## 👥 Author

Proyek Akhir IoT - 2025
