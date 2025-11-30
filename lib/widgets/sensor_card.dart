import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SensorCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final String value;
  final String unit;
  final bool isNormal;
  final bool isWarning;
  final bool isCritical;
  final Color sensorColor;

  const SensorCard({
    super.key,
    required this.title,
    required this.icon,
    required this.value,
    required this.unit,
    required this.isNormal,
    required this.isWarning,
    required this.isCritical,
    required this.sensorColor,
  });

  @override
  Widget build(BuildContext context) {
    final statusColor = AppTheme.getStatusColor(isNormal, isWarning, isCritical);
    final statusText = isCritical ? 'Critical' : (isWarning ? 'Warning' : 'Normal');
    final statusIcon = isCritical
        ? Icons.error
        : (isWarning ? Icons.warning : Icons.check_circle);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: sensorColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    icon,
                    color: sensorColor,
                    size: 24,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Icon(
                            statusIcon,
                            color: statusColor,
                            size: 16,
                          ),
                          const SizedBox(width: 4),
                          Text(
                            statusText,
                            style: TextStyle(
                              color: statusColor,
                              fontSize: 12,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  value,
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: sensorColor,
                        fontWeight: FontWeight.bold,
                      ),
                ),
                const SizedBox(width: 8),
                Padding(
                  padding: const EdgeInsets.only(bottom: 4.0),
                  child: Text(
                    unit,
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          color: AppTheme.textSecondary,
                        ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
