import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../models/sensor_data.dart';
import '../services/mock_data_service.dart';
import '../theme/app_theme.dart';

enum TimeRange {
  last24Hours('Last 24 Hours'),
  last7Days('Last 7 Days'),
  last30Days('Last 30 Days');

  const TimeRange(this.label);
  final String label;
}

class ChartScreen extends StatefulWidget {
  const ChartScreen({super.key});

  @override
  State<ChartScreen> createState() => _ChartScreenState();
}

class _ChartScreenState extends State<ChartScreen> {
  final MockDataService _dataService = MockDataService();
  TimeRange _selectedRange = TimeRange.last24Hours;
  List<SensorData> _data = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    setState(() {
      _isLoading = true;
    });

    // Simulate loading delay
    Future.delayed(const Duration(milliseconds: 500), () {
      setState(() {
        switch (_selectedRange) {
          case TimeRange.last24Hours:
            _data = _dataService.last24Hours;
            break;
          case TimeRange.last7Days:
            _data = _dataService.last7Days;
            break;
          case TimeRange.last30Days:
            _data = _dataService.last30Days;
            break;
        }
        _isLoading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Historical Data'),
        actions: [
          PopupMenuButton<TimeRange>(
            initialValue: _selectedRange,
            icon: const Icon(Icons.access_time),
            onSelected: (TimeRange range) {
              setState(() {
                _selectedRange = range;
              });
              _loadData();
            },
            itemBuilder: (BuildContext context) {
              return TimeRange.values.map((TimeRange range) {
                return PopupMenuItem<TimeRange>(
                  value: range,
                  child: Text(range.label),
                );
              }).toList();
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16.0),
              children: [
                _buildChartCard(
                  'Temperature',
                  '°C',
                  AppTheme.temperature,
                  _data.map((d) => d.temperature).toList(),
                  minY: 20,
                  maxY: 35,
                  thresholdMin: 22,
                  thresholdMax: 30,
                ),
                const SizedBox(height: 16),
                _buildChartCard(
                  'pH Level',
                  'pH',
                  AppTheme.ph,
                  _data.map((d) => d.ph).toList(),
                  minY: 6,
                  maxY: 8,
                  thresholdMin: 6.5,
                  thresholdMax: 7.5,
                ),
                const SizedBox(height: 16),
                _buildChartCard(
                  'TDS',
                  'ppm',
                  AppTheme.tds,
                  _data.map((d) => d.tds.toDouble()).toList(),
                  minY: 0,
                  maxY: 1000,
                  thresholdMin: 300,
                  thresholdMax: 600,
                ),
              ],
            ),
    );
  }

  Widget _buildChartCard(
    String title,
    String unit,
    Color color,
    List<double> values, {
    required double minY,
    required double maxY,
    double? thresholdMin,
    double? thresholdMax,
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
                  width: 4,
                  height: 20,
                  decoration: BoxDecoration(
                    color: color,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const Spacer(),
                Text(
                  _selectedRange.label,
                  style: const TextStyle(
                    color: AppTheme.textSecondary,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(
                    show: true,
                    drawVerticalLine: false,
                    horizontalInterval: (maxY - minY) / 5,
                    getDrawingHorizontalLine: (value) {
                      return FlLine(
                        color: Colors.grey.withOpacity(0.2),
                        strokeWidth: 1,
                      );
                    },
                  ),
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 40,
                        getTitlesWidget: (value, meta) {
                          return Text(
                            value.toStringAsFixed(0),
                            style: const TextStyle(
                              fontSize: 10,
                              color: AppTheme.textSecondary,
                            ),
                          );
                        },
                      ),
                    ),
                    rightTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    topTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 30,
                        getTitlesWidget: (value, meta) {
                          final index = value.toInt();
                          if (index < 0 || index >= _data.length) {
                            return const SizedBox();
                          }
                          
                          // Show fewer labels based on data size
                          final showEvery = (_data.length / 6).ceil();
                          if (index % showEvery != 0) {
                            return const SizedBox();
                          }

                          final time = _data[index].timestamp;
                          String label;
                          
                          if (_selectedRange == TimeRange.last24Hours) {
                            label = '${time.hour}:${time.minute.toString().padLeft(2, '0')}';
                          } else if (_selectedRange == TimeRange.last7Days) {
                            label = '${time.day}/${time.month}';
                          } else {
                            label = '${time.day}/${time.month}';
                          }

                          return SideTitleWidget(
                            axisSide: meta.axisSide,
                            child: Text(
                              label,
                              style: const TextStyle(
                                fontSize: 9,
                                color: AppTheme.textSecondary,
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  ),
                  borderData: FlBorderData(show: false),
                  minY: minY,
                  maxY: maxY,
                  lineBarsData: [
                    LineChartBarData(
                      spots: values.asMap().entries.map((e) {
                        return FlSpot(e.key.toDouble(), e.value);
                      }).toList(),
                      isCurved: true,
                      color: color,
                      barWidth: 2,
                      isStrokeCapRound: true,
                      dotData: const FlDotData(show: false),
                      belowBarData: BarAreaData(
                        show: true,
                        color: color.withOpacity(0.1),
                      ),
                    ),
                  ],
                  lineTouchData: LineTouchData(
                    touchTooltipData: LineTouchTooltipData(
                      getTooltipItems: (touchedSpots) {
                        return touchedSpots.map((spot) {
                          return LineTooltipItem(
                            '${spot.y.toStringAsFixed(1)} $unit',
                            const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          );
                        }).toList();
                      },
                    ),
                  ),
                  extraLinesData: ExtraLinesData(
                    horizontalLines: [
                      if (thresholdMin != null)
                        HorizontalLine(
                          y: thresholdMin,
                          color: AppTheme.warning.withOpacity(0.6),
                          strokeWidth: 1,
                          dashArray: [5, 5],
                          label: HorizontalLineLabel(
                            show: true,
                            alignment: Alignment.topRight,
                            style: const TextStyle(
                              fontSize: 10,
                              color: AppTheme.warning,
                            ),
                            labelResolver: (line) => 'Min',
                          ),
                        ),
                      if (thresholdMax != null)
                        HorizontalLine(
                          y: thresholdMax,
                          color: AppTheme.warning.withOpacity(0.6),
                          strokeWidth: 1,
                          dashArray: [5, 5],
                          label: HorizontalLineLabel(
                            show: true,
                            alignment: Alignment.bottomRight,
                            style: const TextStyle(
                              fontSize: 10,
                              color: AppTheme.warning,
                            ),
                            labelResolver: (line) => 'Max',
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
