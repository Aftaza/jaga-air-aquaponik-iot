# Flutter App Setup Guide

## Prerequisites

- Flutter SDK (≥ 3.9.2)
- Android Studio / VS Code
- Android SDK atau Xcode (untuk iOS)
- Physical device atau emulator

## Installation Steps

### 1. Install Dependencies

```bash
cd jagaair_app
flutter pub get
```

### 2. Check Flutter Setup

```bash
flutter doctor
```

Pastikan semua checkmarks hijau untuk platform yang ingin Anda gunakan.

### 3. Run Application

#### Android

```bash
# Run on connected device
flutter run

# Build APK
flutter build apk --release
```

#### iOS

```bash
# Run on simulator
flutter run

# Build IPA
flutter build ios --release
```

## Dependencies

Package yang digunakan:

- `fl_chart: ^0.69.2` - Charts untuk data visualization
- `provider: ^6.1.2` - State management
- `intl: ^0.19.0` - Date/time formatting
- `shared_preferences: ^2.3.3` - Local storage
- `http: ^1.2.2` - HTTP client (untuk ThingSpeak API di masa depan)

## Project Structure

```
lib/
├── models/              # Data models
├── screens/            # UI screens
├── widgets/            # Reusable widgets
├── services/           # Business logic & services
├── theme/              # App theming
└── main.dart           # Entry point
```

## Features

### Dashboard Screen
- Real-time sensor readings
- Device status (battery, signal, connection)
- Actuator controls (pump, light)
- Pull-to-refresh

### Chart Screen
- Historical data visualization
- Multiple time ranges (24h, 7d, 30d)
- Interactive charts dengan threshold lines
- Sensor-specific color coding

### Settings Screen
- WiFi configuration
- ThingSpeak API settings
- Threshold configuration
- Device information

## Current Limitations

⚠️ **Mock Data**: Aplikasi saat ini menggunakan `MockDataService` untuk generate data dummy. ThingSpeak API integration akan ditambahkan di versi berikutnya.

## Future Enhancements

Untuk mengintegrasikan dengan ThingSpeak API:

1. Create `ThingSpeakService` class
2. Implement HTTP GET untuk read data
3. Replace `MockDataService` dengan `ThingSpeakService`
4. Add API key configuration di Settings

## Troubleshooting

### Build Errors

```bash
# Clean build cache
flutter clean
flutter pub get
flutter run
```

### Dependency Conflicts

```bash
# Update dependencies
flutter pub upgrade
```

### Hot Reload Not Working

- Restart app dengan `R` di terminal
- Atau restart IDE

## Testing

```bash
# Run tests
flutter test

# Run with coverage
flutter test --coverage
```

## Color Scheme

- **Primary**: Green (#2E7D32) - Main theme
- **Temperature**: Blue (#1976D2)
- **pH**: Purple (#7B1FA2)
- **TDS**: Cyan (#0097A7)
- **Warning**: Orange (#FF9800)
- **Error**: Red (#D32F2F)

## Support

Untuk issues atau pertanyaan, lihat [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
