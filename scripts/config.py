# Configuration for IoT Aquaponik ESP32
# =====================================

# WiFi Settings
WIFI_SSID = 'YOUR_WIFI_SSID'
WIFI_PASSWORD = 'YOUR_WIFI_PASSWORD'

# ThingSpeak MQTT Configuration with TLS/SSL
THINGSPEAK_MQTT_BROKER = 'mqtt3.thingspeak.com'
THINGSPEAK_MQTT_PORT = 8883  # TLS/SSL port (use 1883 for non-SSL)
THINGSPEAK_USE_SSL = True    # Enable TLS/SSL encryption
THINGSPEAK_CHANNEL_ID = 'YOUR_CHANNEL_ID'
THINGSPEAK_WRITE_API_KEY = 'YOUR_WRITE_API_KEY'
THINGSPEAK_READ_API_KEY = 'YOUR_READ_API_KEY'
THINGSPEAK_MQTT_USERNAME = 'YOUR_MQTT_USERNAME'
THINGSPEAK_MQTT_PASSWORD = 'YOUR_MQTT_PASSWORD'
THINGSPEAK_CLIENT_ID = 'YOUR_MQTT_CLIENT_ID'

# Device Configuration
DEVICE_ID = 'AQP-001'

# Pin Configuration
PIN_DS18B20 = 25          # OneWire temperature sensor
PIN_PH_SENSOR = 34        # ADC1 Channel 6 (Analog pH sensor)
PIN_TDS_SENSOR = 32       # ADC1 Channel 4 (Analog TDS sensor)
PIN_FLOAT_SWITCH = 27     # Digital input (water level)
PIN_RELAY_PUMP = 16       # Digital output (pump control)
PIN_RELAY_LIGHT = 17      # Digital output (light control)

# Sensor Configuration
PH_VOLTAGE_CALIBRATION = 2.5  # Bias voltage for pH sensor
TDS_VREF = 3.3                # Reference voltage for TDS sensor
ADC_RESOLUTION = 4095.0       # 12-bit ADC resolution

# Temperature Thresholds (°C)
TEMP_MIN = 22.0
TEMP_MAX = 30.0
TEMP_CRITICAL_MIN = 20.0
TEMP_CRITICAL_MAX = 32.0

# pH Thresholds
PH_MIN = 6.5
PH_MAX = 7.5
PH_CRITICAL_MIN = 6.0
PH_CRITICAL_MAX = 8.0

# TDS Thresholds (ppm)
TDS_MIN = 300
TDS_MAX = 600
TDS_CRITICAL_MIN = 200
TDS_CRITICAL_MAX = 800

# Update Intervals (seconds)
SENSOR_READ_INTERVAL = 10     # Temperature reading interval (faster for 15s publish)
PH_READ_INTERVAL = 15         # pH reading interval (match MQTT interval)
TDS_READ_INTERVAL = 15        # TDS reading interval (match MQTT interval)
MQTT_PUBLISH_INTERVAL = 15    # MQTT publish interval (every 15 seconds)
STATUS_UPDATE_INTERVAL = 3600 # Battery/RSSI update (1 hour)

# MQTT Topics
MQTT_TOPIC_PUBLISH = f'channels/{THINGSPEAK_CHANNEL_ID}/publish'
MQTT_TOPIC_STATUS = f'aquaponik/{DEVICE_ID}/status'
MQTT_TOPIC_CONTROL = f'aquaponik/{DEVICE_ID}/control'
MQTT_TOPIC_ALERT = f'aquaponik/{DEVICE_ID}/alert'

# Watchdog Configuration
WATCHDOG_TIMEOUT = 120  # seconds

# Debug Mode
DEBUG = True
