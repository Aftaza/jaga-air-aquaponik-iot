import 'dart:math';
import '../models/sensor_data.dart';
import '../models/actuator_status.dart';
import '../models/device_status.dart';

class MockDataService {
  static final MockDataService _instance = MockDataService._internal();
  factory MockDataService() => _instance;
  MockDataService._internal();

  final Random _random = Random();

  // Current device status
  DeviceStatus get currentDeviceStatus {
    return DeviceStatus(
      deviceId: 'AQP-001',
      battery: 85 + _random.nextInt(15), // 85-100%
      rssi: -45 + _random.nextInt(15), // -45 to -30 dBm
      isConnected: true,
    );
  }

  // Current sensor data
  SensorData get currentSensorData {
    return SensorData(
      temperature: 26.0 + (_random.nextDouble() * 2.0), // 26-28°C
      ph: 6.7 + (_random.nextDouble() * 0.6), // 6.7-7.3
      tds: 400 + _random.nextInt(100), // 400-500 ppm
      waterLevel: true,
    );
  }

  // Current actuator status
  ActuatorStatus get currentActuatorStatus {
    return ActuatorStatus(
      pumpStatus: false,
      lightStatus: true,
    );
  }

  // Generate historical data for charts
  List<SensorData> generateHistoricalData({
    required Duration duration,
    required Duration interval,
  }) {
    final List<SensorData> data = [];
    final now = DateTime.now();
    final start = now.subtract(duration);

    DateTime current = start;
    while (current.isBefore(now)) {
      data.add(_generateSensorDataAtTime(current));
      current = current.add(interval);
    }

    return data;
  }

  SensorData _generateSensorDataAtTime(DateTime time) {
    // Simulate realistic patterns
    final hour = time.hour;
    
    // Temperature varies with time of day
    double baseTemp = 26.0;
    if (hour >= 10 && hour <= 16) {
      baseTemp = 27.5; // Warmer during day
    } else if (hour >= 0 && hour <= 6) {
      baseTemp = 25.0; // Cooler at night
    }
    
    // pH slowly drifts
    final minutesSinceStart = time.difference(DateTime(2025, 1, 1)).inMinutes;
    final phDrift = sin(minutesSinceStart / 1000.0) * 0.3;
    
    // TDS varies slightly
    final tdsVariation = (_random.nextDouble() - 0.5) * 50;

    return SensorData(
      temperature: baseTemp + (_random.nextDouble() - 0.5) * 1.0,
      ph: 6.9 + phDrift + (_random.nextDouble() - 0.5) * 0.2,
      tds: (450 + tdsVariation).toInt(),
      waterLevel: true,
      timestamp: time,
    );
  }

  // Generate last 24 hours of data (every 30 seconds)
  List<SensorData> get last24Hours {
    return generateHistoricalData(
      duration: const Duration(hours: 24),
      interval: const Duration(seconds: 30),
    );
  }

  // Generate last 7 days of data (every 5 minutes)
  List<SensorData> get last7Days {
    return generateHistoricalData(
      duration: const Duration(days: 7),
      interval: const Duration(minutes: 5),
    );
  }

  // Generate last 30 days of data (every 30 minutes)
  List<SensorData> get last30Days {
    return generateHistoricalData(
      duration: const Duration(days: 30),
      interval: const Duration(minutes: 30),
    );
  }
}
