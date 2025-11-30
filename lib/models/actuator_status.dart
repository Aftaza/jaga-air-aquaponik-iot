class ActuatorStatus {
  final bool pumpStatus;
  final bool lightStatus;
  final DateTime timestamp;

  ActuatorStatus({
    required this.pumpStatus,
    required this.lightStatus,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toJson() {
    return {
      'pump_status': pumpStatus,
      'light_status': lightStatus,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  factory ActuatorStatus.fromJson(Map<String, dynamic> json) {
    return ActuatorStatus(
      pumpStatus: json['pump_status'] as bool,
      lightStatus: json['light_status'] as bool,
      timestamp: json['timestamp'] != null
          ? DateTime.parse(json['timestamp'])
          : null,
    );
  }

  ActuatorStatus copyWith({
    bool? pumpStatus,
    bool? lightStatus,
    DateTime? timestamp,
  }) {
    return ActuatorStatus(
      pumpStatus: pumpStatus ?? this.pumpStatus,
      lightStatus: lightStatus ?? this.lightStatus,
      timestamp: timestamp ?? this.timestamp,
    );
  }
}
