# JagaAir: IoT Aquaponics Monitor

Final project for the IoT course at Universitas Brawijaya (2025). An ESP32 reads water temperature, pH, TDS and
water level in a small aquaponics tank, drives a pump and a grow light through relays, and publishes readings to
ThingSpeak over MQTT with TLS. A Flutter app shows the dashboard, history charts and settings.

## Parts

| Folder | What it is |
| --- | --- |
| [`scripts/`](scripts/) | ESP32 firmware in MicroPython: sensor drivers, relay control, Wi-Fi reconnect, MQTT client, watchdog |
| [`lib/`](lib/) | Flutter app: dashboard, charts (24 h / 7 d / 30 d), actuator toggles, threshold settings |
| [`docs/`](docs/) | Setup, wiring, sensor calibration, ThingSpeak and TLS notes (Indonesian), plus the technical report PDF |

## How it works

```
DS18B20 · pH · TDS · float switch
        │  (ESP32, MicroPython, every 15 s)
        ▼
 MQTT over TLS :8883 ──► ThingSpeak channel ──► charts / Flutter app
        ▲
 relays: pump, grow light
```

- Each sensor is checked at boot. When one is missing, the firmware sends realistic dummy values so the pipeline
  can still be tested end to end.
- Threshold checks flag readings outside the normal range (temperature 22–30 °C, pH 6.5–7.5, TDS 300–600 ppm).
- A hardware watchdog restarts the board if the main loop hangs.

## Status

The firmware publishes live data to ThingSpeak. The Flutter app currently runs on a mock data service
(`lib/services/mock_data_service.dart`); wiring it to the ThingSpeak read API is the next step.

## Running it

**Firmware**

1. Flash MicroPython to an ESP32 DevKit V1.
2. Fill in Wi-Fi and ThingSpeak credentials in `scripts/config.py` (keep real values out of git).
3. Upload everything in `scripts/` to the board, then reset it.

Pin map, wiring and calibration: [`docs/WIRING_DIAGRAM.md`](docs/WIRING_DIAGRAM.md),
[`docs/SENSOR_CALIBRATION.md`](docs/SENSOR_CALIBRATION.md), [`docs/ESP32_SETUP.md`](docs/ESP32_SETUP.md).

**App**

```bash
flutter pub get
flutter run
```

## Stack

ESP32 · MicroPython · MQTT (TLS) · ThingSpeak · Flutter · fl_chart
