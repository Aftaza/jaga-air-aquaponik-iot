import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  // WiFi settings
  String _wifiSsid = 'HomeAquaponik';
  String _wifiPassword = '********';

  // ThingSpeak settings
  String _channelId = '1234567';
  String _readApiKey = '****************';
  String _writeApiKey = '****************';
  String _mqttUsername = 'aquaponik_user';

  // Threshold settings
  double _tempMin = 22.0;
  double _tempMax = 30.0;
  double _phMin = 6.5;
  double _phMax = 7.5;
  int _tdsMin = 300;
  int _tdsMax = 600;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        children: [
          // WiFi Configuration Section
          _buildSectionHeader('WiFi Configuration'),
          _buildListTile(
            icon: Icons.wifi,
            title: 'WiFi SSID',
            subtitle: _wifiSsid,
            onTap: () => _showEditDialog(
              'WiFi SSID',
              _wifiSsid,
              (value) => setState(() => _wifiSsid = value),
            ),
          ),
          _buildListTile(
            icon: Icons.lock,
            title: 'WiFi Password',
            subtitle: _wifiPassword,
            onTap: () => _showEditDialog(
              'WiFi Password',
              '',
              (value) => setState(() => _wifiPassword = value),
              obscureText: true,
            ),
          ),

          const Divider(height: 32),

          // ThingSpeak Configuration Section
          _buildSectionHeader('ThingSpeak Configuration'),
          _buildListTile(
            icon: Icons.cloud,
            title: 'Channel ID',
            subtitle: _channelId,
            onTap: () => _showEditDialog(
              'Channel ID',
              _channelId,
              (value) => setState(() => _channelId = value),
            ),
          ),
          _buildListTile(
            icon: Icons.vpn_key,
            title: 'Read API Key',
            subtitle: _readApiKey,
            onTap: () => _showEditDialog(
              'Read API Key',
              '',
              (value) => setState(() => _readApiKey = value),
              obscureText: true,
            ),
          ),
          _buildListTile(
            icon: Icons.vpn_key,
            title: 'Write API Key',
            subtitle: _writeApiKey,
            onTap: () => _showEditDialog(
              'Write API Key',
              '',
              (value) => setState(() => _writeApiKey = value),
              obscureText: true,
            ),
          ),
          _buildListTile(
            icon: Icons.person,
            title: 'MQTT Username',
            subtitle: _mqttUsername,
            onTap: () => _showEditDialog(
              'MQTT Username',
              _mqttUsername,
              (value) => setState(() => _mqttUsername = value),
            ),
          ),

          const Divider(height: 32),

          // Threshold Settings Section
          _buildSectionHeader('Parameter Thresholds'),
          _buildThresholdCard(
            'Temperature',
            Icons.thermostat,
            AppTheme.temperature,
            _tempMin,
            _tempMax,
            '°C',
            (min, max) {
              setState(() {
                _tempMin = min;
                _tempMax = max;
              });
            },
            minRange: 0,
            maxRange: 50,
          ),
          _buildThresholdCard(
            'pH Level',
            Icons.science,
            AppTheme.ph,
            _phMin,
            _phMax,
            'pH',
            (min, max) {
              setState(() {
                _phMin = min;
                _phMax = max;
              });
            },
            minRange: 0,
            maxRange: 14,
            decimals: 1,
          ),
          Card(
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
                          color: AppTheme.tds.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Icon(
                          Icons.water_drop,
                          color: AppTheme.tds,
                        ),
                      ),
                      const SizedBox(width: 12),
                      const Text(
                        'TDS',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          decoration: const InputDecoration(
                            labelText: 'Min',
                            suffixText: 'ppm',
                            border: OutlineInputBorder(),
                          ),
                          keyboardType: TextInputType.number,
                          controller: TextEditingController(
                            text: _tdsMin.toString(),
                          ),
                          onSubmitted: (value) {
                            setState(() {
                              _tdsMin = int.tryParse(value) ?? _tdsMin;
                            });
                          },
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: TextField(
                          decoration: const InputDecoration(
                            labelText: 'Max',
                            suffixText: 'ppm',
                            border: OutlineInputBorder(),
                          ),
                          keyboardType: TextInputType.number,
                          controller: TextEditingController(
                            text: _tdsMax.toString(),
                          ),
                          onSubmitted: (value) {
                            setState(() {
                              _tdsMax = int.tryParse(value) ?? _tdsMax;
                            });
                          },
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),

          const Divider(height: 32),

          // Device Info Section
          _buildSectionHeader('Device Information'),
          _buildListTile(
            icon: Icons.devices,
            title: 'Device ID',
            subtitle: 'AQP-001',
            trailing: const SizedBox(),
          ),
          _buildListTile(
            icon: Icons.memory,
            title: 'Firmware Version',
            subtitle: 'v1.0.0',
            trailing: const SizedBox(),
          ),
          _buildListTile(
            icon: Icons.info,
            title: 'About',
            subtitle: 'IoT Aquaponik Mini v1.0',
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _showAboutDialog(),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.bold,
          color: AppTheme.primary,
        ),
      ),
    );
  }

  Widget _buildListTile({
    required IconData icon,
    required String title,
    required String subtitle,
    VoidCallback? onTap,
    Widget? trailing,
  }) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primary),
      title: Text(title),
      subtitle: Text(subtitle),
      trailing: trailing ?? const Icon(Icons.chevron_right),
      onTap: onTap,
    );
  }

  Widget _buildThresholdCard(
    String title,
    IconData icon,
    Color color,
    double minValue,
    double maxValue,
    String unit,
    Function(double, double) onChanged, {
    double minRange = 0,
    double maxRange = 100,
    int decimals = 0,
  }) {
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
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(icon, color: color),
                ),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    decoration: InputDecoration(
                      labelText: 'Min',
                      suffixText: unit,
                      border: const OutlineInputBorder(),
                    ),
                    keyboardType: const TextInputType.numberWithOptions(
                      decimal: true,
                    ),
                    controller: TextEditingController(
                      text: minValue.toStringAsFixed(decimals),
                    ),
                    onSubmitted: (value) {
                      final newMin = double.tryParse(value) ?? minValue;
                      onChanged(newMin, maxValue);
                    },
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: TextField(
                    decoration: InputDecoration(
                      labelText: 'Max',
                      suffixText: unit,
                      border: const OutlineInputBorder(),
                    ),
                    keyboardType: const TextInputType.numberWithOptions(
                      decimal: true,
                    ),
                    controller: TextEditingController(
                      text: maxValue.toStringAsFixed(decimals),
                    ),
                    onSubmitted: (value) {
                      final newMax = double.tryParse(value) ?? maxValue;
                      onChanged(minValue, newMax);
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  void _showEditDialog(
    String title,
    String initialValue,
    Function(String) onSave, {
    bool obscureText = false,
  }) {
    final controller = TextEditingController(text: initialValue);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Edit $title'),
        content: TextField(
          controller: controller,
          obscureText: obscureText,
          decoration: InputDecoration(
            labelText: title,
            border: const OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              onSave(controller.text);
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('$title updated')),
              );
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showAboutDialog() {
    showAboutDialog(
      context: context,
      applicationName: 'IoT Aquaponik',
      applicationVersion: 'v1.0.0',
      applicationIcon: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          color: AppTheme.primary,
          borderRadius: BorderRadius.circular(12),
        ),
        child: const Icon(
          Icons.water_drop,
          color: Colors.white,
          size: 40,
        ),
      ),
      children: const [
        Text('IoT Aquaponik Mini Monitoring System'),
        SizedBox(height: 8),
        Text('A smart monitoring solution for aquaponic systems.'),
      ],
    );
  }
}
