class DeviceStatus {
  final String deviceId;
  final int battery; // 0-100%
  final int rssi; // Signal strength in dBm (-99 to 0)
  final bool isConnected;
  final DateTime lastUpdate;

  DeviceStatus({
    required this.deviceId,
    required this.battery,
    required this.rssi,
    required this.isConnected,
    DateTime? lastUpdate,
  }) : lastUpdate = lastUpdate ?? DateTime.now();

  // Battery status helpers
  bool get isBatteryLow => battery < 20;
  bool get isBatteryWarning => battery >= 20 && battery < 50;
  bool get isBatteryNormal => battery >= 50;

  // Signal strength helpers
  String get signalStrength {
    if (rssi >= -50) return 'Excellent';
    if (rssi >= -60) return 'Good';
    if (rssi >= -70) return 'Fair';
    return 'Weak';
  }

  bool get isSignalWeak => rssi < -70;
  bool get isSignalGood => rssi >= -60;

  Map<String, dynamic> toJson() {
    return {
      'device_id': deviceId,
      'battery': battery,
      'rssi': rssi,
      'is_connected': isConnected,
      'last_update': lastUpdate.toIso8601String(),
    };
  }

  factory DeviceStatus.fromJson(Map<String, dynamic> json) {
    return DeviceStatus(
      deviceId: json['device_id'] as String,
      battery: json['battery'] as int,
      rssi: json['rssi'] as int,
      isConnected: json['is_connected'] as bool,
      lastUpdate: json['last_update'] != null
          ? DateTime.parse(json['last_update'])
          : null,
    );
  }

  DeviceStatus copyWith({
    String? deviceId,
    int? battery,
    int? rssi,
    bool? isConnected,
    DateTime? lastUpdate,
  }) {
    return DeviceStatus(
      deviceId: deviceId ?? this.deviceId,
      battery: battery ?? this.battery,
      rssi: rssi ?? this.rssi,
      isConnected: isConnected ?? this.isConnected,
      lastUpdate: lastUpdate ?? this.lastUpdate,
    );
  }
}
