import 'package:flutter/material.dart';
import '../models/sensor_data.dart';
import '../models/actuator_status.dart';
import '../models/device_status.dart';
import '../services/mock_data_service.dart';
import '../widgets/sensor_card.dart';
import '../widgets/actuator_card.dart';
import '../theme/app_theme.dart';
import 'dart:async';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final MockDataService _dataService = MockDataService();
  late Timer _timer;

  SensorData _sensorData = SensorData(
    temperature: 0,
    ph: 0,
    tds: 0,
    waterLevel: false,
  );
  
  ActuatorStatus _actuatorStatus = ActuatorStatus(
    pumpStatus: false,
    lightStatus: false,
  );
  
  DeviceStatus _deviceStatus = DeviceStatus(
    deviceId: 'AQP-001',
    battery: 0,
    rssi: 0,
    isConnected: false,
  );

  @override
  void initState() {
    super.initState();
    _loadData();
    // Refresh data every 5 seconds
    _timer = Timer.periodic(const Duration(seconds: 5), (timer) {
      _loadData();
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  void _loadData() {
    setState(() {
      _sensorData = _dataService.currentSensorData;
      _actuatorStatus = _dataService.currentActuatorStatus;
      _deviceStatus = _dataService.currentDeviceStatus;
    });
  }

  void _togglePump(bool value) {
    setState(() {
      _actuatorStatus = _actuatorStatus.copyWith(pumpStatus: value);
    });
    // TODO: Send command to device via MQTT
  }

  void _toggleLight(bool value) {
    setState(() {
      _actuatorStatus = _actuatorStatus.copyWith(lightStatus: value);
    });
    // TODO: Send command to device via MQTT
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Aquaponik Monitor'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadData,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          _loadData();
        },
        child: ListView(
          padding: const EdgeInsets.all(8.0),
          children: [
            // Device Status Card
            _buildDeviceStatusCard(),
            
            const SizedBox(height: 8),
            
            // Sensor Cards
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Text(
                'Sensor Readings',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            
            SensorCard(
              title: 'Water Temperature',
              icon: Icons.thermostat,
              value: _sensorData.temperature.toStringAsFixed(1),
              unit: '°C',
              isNormal: _sensorData.isTemperatureNormal,
              isWarning: _sensorData.isTemperatureWarning,
              isCritical: _sensorData.isTemperatureCritical,
              sensorColor: AppTheme.temperature,
            ),
            
            SensorCard(
              title: 'pH Level',
              icon: Icons.science,
              value: _sensorData.ph.toStringAsFixed(2),
              unit: 'pH',
              isNormal: _sensorData.isPhNormal,
              isWarning: _sensorData.isPhWarning,
              isCritical: _sensorData.isPhCritical,
              sensorColor: AppTheme.ph,
            ),
            
            SensorCard(
              title: 'TDS',
              icon: Icons.water_drop,
              value: _sensorData.tds.toString(),
              unit: 'ppm',
              isNormal: _sensorData.isTdsNormal,
              isWarning: _sensorData.isTdsWarning,
              isCritical: _sensorData.isTdsCritical,
              sensorColor: AppTheme.tds,
            ),
            
            SensorCard(
              title: 'Water Level',
              icon: Icons.waves,
              value: _sensorData.waterLevel ? 'Normal' : 'Low',
              unit: '',
              isNormal: _sensorData.isWaterLevelNormal,
              isWarning: false,
              isCritical: _sensorData.isWaterLevelCritical,
              sensorColor: AppTheme.info,
            ),
            
            const SizedBox(height: 8),
            
            // Actuator Controls
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Text(
                'Actuator Controls',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            
            ActuatorCard(
              title: 'Water Pump',
              icon: Icons.water,
              isActive: _actuatorStatus.pumpStatus,
              onToggle: _togglePump,
              activeLabel: 'Running',
              inactiveLabel: 'Stopped',
            ),
            
            ActuatorCard(
              title: 'Grow Light',
              icon: Icons.lightbulb,
              isActive: _actuatorStatus.lightStatus,
              onToggle: _toggleLight,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDeviceStatusCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  _deviceStatus.isConnected
                      ? Icons.cloud_done
                      : Icons.cloud_off,
                  color: _deviceStatus.isConnected
                      ? AppTheme.success
                      : AppTheme.error,
                ),
                const SizedBox(width: 8),
                Text(
                  _deviceStatus.deviceId,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: _deviceStatus.isConnected
                        ? AppTheme.success.withOpacity(0.1)
                        : AppTheme.error.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _deviceStatus.isConnected ? 'Connected' : 'Offline',
                    style: TextStyle(
                      color: _deviceStatus.isConnected
                          ? AppTheme.success
                          : AppTheme.error,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildStatusItem(
                    Icons.battery_std,
                    'Battery',
                    '${_deviceStatus.battery}%',
                    _deviceStatus.isBatteryNormal
                        ? AppTheme.success
                        : (_deviceStatus.isBatteryWarning
                            ? AppTheme.warning
                            : AppTheme.error),
                  ),
                ),
                Expanded(
                  child: _buildStatusItem(
                    Icons.signal_cellular_alt,
                    'Signal',
                    _deviceStatus.signalStrength,
                    _deviceStatus.isSignalGood
                        ? AppTheme.success
                        : (_deviceStatus.isSignalWeak
                            ? AppTheme.error
                            : AppTheme.warning),
                  ),
                ),
                Expanded(
                  child: _buildStatusItem(
                    Icons.update,
                    'Last Update',
                    _formatTimeDifference(_deviceStatus.lastUpdate),
                    AppTheme.info,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusItem(
    IconData icon,
    String label,
    String value,
    Color color,
  ) {
    return Column(
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(height: 4),
        Text(
          label,
          style: const TextStyle(
            fontSize: 10,
            color: AppTheme.textSecondary,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          value,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w600,
            color: color,
          ),
        ),
      ],
    );
  }

  String _formatTimeDifference(DateTime time) {
    final difference = DateTime.now().difference(time);
    if (difference.inSeconds < 60) {
      return '${difference.inSeconds}s ago';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h ago';
    } else {
      return '${difference.inDays}d ago';
    }
  }
}
