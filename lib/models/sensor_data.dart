class SensorData {
  final double temperature;
  final double ph;
  final int tds;
  final bool waterLevel;
  final DateTime timestamp;

  SensorData({
    required this.temperature,
    required this.ph,
    required this.tds,
    required this.waterLevel,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  // Temperature range: 0.0 - 50.0 °C
  bool get isTemperatureNormal => temperature >= 22.0 && temperature <= 30.0;
  bool get isTemperatureWarning =>
      (temperature >= 20.0 && temperature < 22.0) ||
      (temperature > 30.0 && temperature <= 32.0);
  bool get isTemperatureCritical => temperature < 20.0 || temperature > 32.0;

  // pH range: 0.0 - 14.0
  bool get isPhNormal => ph >= 6.5 && ph <= 7.5;
  bool get isPhWarning =>
      (ph >= 6.0 && ph < 6.5) || (ph > 7.5 && ph <= 8.0);
  bool get isPhCritical => ph < 6.0 || ph > 8.0;

  // TDS range: 0 - 1000 ppm
  bool get isTdsNormal => tds >= 300 && tds <= 600;
  bool get isTdsWarning =>
      (tds >= 200 && tds < 300) || (tds > 600 && tds <= 800);
  bool get isTdsCritical => tds < 200 || tds > 800;

  // Water level: true = normal, false = low
  bool get isWaterLevelNormal => waterLevel;
  bool get isWaterLevelCritical => !waterLevel;

  Map<String, dynamic> toJson() {
    return {
      'temperature': temperature,
      'ph': ph,
      'tds': tds,
      'water_level': waterLevel,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  factory SensorData.fromJson(Map<String, dynamic> json) {
    return SensorData(
      temperature: (json['temperature'] as num).toDouble(),
      ph: (json['ph'] as num).toDouble(),
      tds: json['tds'] as int,
      waterLevel: json['water_level'] as bool,
      timestamp: json['timestamp'] != null
          ? DateTime.parse(json['timestamp'])
          : null,
    );
  }

  SensorData copyWith({
    double? temperature,
    double? ph,
    int? tds,
    bool? waterLevel,
    DateTime? timestamp,
  }) {
    return SensorData(
      temperature: temperature ?? this.temperature,
      ph: ph ?? this.ph,
      tds: tds ?? this.tds,
      waterLevel: waterLevel ?? this.waterLevel,
      timestamp: timestamp ?? this.timestamp,
    );
  }
}
