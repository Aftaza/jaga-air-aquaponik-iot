import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ActuatorCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final bool isActive;
  final Function(bool) onToggle;
  final String activeLabel;
  final String inactiveLabel;

  const ActuatorCard({
    super.key,
    required this.title,
    required this.icon,
    required this.isActive,
    required this.onToggle,
    this.activeLabel = 'ON',
    this.inactiveLabel = 'OFF',
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isActive
                    ? AppTheme.primary.withOpacity(0.1)
                    : Colors.grey.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(
                icon,
                color: isActive ? AppTheme.primary : Colors.grey,
                size: 28,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    isActive ? activeLabel : inactiveLabel,
                    style: TextStyle(
                      color: isActive ? AppTheme.success : AppTheme.textSecondary,
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
            Switch(
              value: isActive,
              onChanged: onToggle,
            ),
          ],
        ),
      ),
    );
  }
}
