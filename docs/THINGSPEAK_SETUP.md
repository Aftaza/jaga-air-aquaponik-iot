# ThingSpeak Configuration Guide

## 1. Create ThingSpeak Account

1. Go to https://thingspeak.com/
2. Sign up untuk free account
3. Verify email

## 2. Create Channel

1. Click "Channels" → "My Channels"
2. Click "New Channel"
3. Fill in channel details:
   - **Name**: IoT Aquaponik Mini
   - **Description**: Aquaponics monitoring system
   - **Field 1**: temperature
   - **Field 2**: ph
   - **Field 3**: tds
   - **Field 4**: water_level
   - **Field 5**: pump_status
   - **Field 6**: light_status
   - **Field 7**: battery
   - **Field 8**: rssi
4. Click "Save Channel"

## 3. Get API Keys

### Write API Key
1. Go to channel settings
2. Tab "API Keys"
3. Copy "Write API Key"

### Read API Key
1. Same tab "API Keys"
2. Copy "Read API Keys" (untuk Flutter app)

### Channel ID
- Visible di URL atau channel info
- Example: `https://thingspeak.com/channels/1234567`
- Channel ID = `1234567`

## 4. MQTT Configuration

### Enable MQTT
1. Go to "Account" → "My Profile"
2. Scroll to "MQTT API"
3. Click "Generate New MQTT API Key"
4. Save:
   - **Client ID**: (auto-generated)
   - **Username**: (auto-generated)
   - **Password**: (your MQTT API key)

### MQTT Credentials Format
```
Broker: mqtt3.thingspeak.com
Port: 1883 (non-SSL) or 8883 (SSL)
Client ID: <your-client-id>
Username: <your-mqtt-username>
Password: <your-mqtt-api-key>
```

## 5. Configure ESP32

Edit `scripts/config.py`:

```python
# ThingSpeak MQTT Configuration
THINGSPEAK_MQTT_BROKER = 'mqtt3.thingspeak.com'
THINGSPEAK_MQTT_PORT = 1883
THINGSPEAK_CHANNEL_ID = '1234567'  # Your channel ID
THINGSPEAK_WRITE_API_KEY = 'XXXXXXXXXXXXXXXX'  # Your Write API Key
THINGSPEAK_READ_API_KEY = 'XXXXXXXXXXXXXXXX'   # Your Read API Key
THINGSPEAK_MQTT_USERNAME = 'YourMQTTUsername'   # From MQTT settings
THINGSPEAK_MQTT_PASSWORD = 'YourMQTTPassword'   # MQTT API Key
THINGSPEAK_CLIENT_ID = 'AQP-001-CLIENT'         # Any unique ID
```

## 6. Field Mapping

| Field | Parameter | Unit | Example |
|-------|-----------|------|---------|
| Field 1 | temperature | °C | 26.5 |
| Field 2 | ph | pH | 6.8 |
| Field 3 | tds | ppm | 450 |
| Field 4 | water_level | 0/1 | 1 (normal) |
| Field 5 | pump_status | 0/1 | 0 (off) |
| Field 6 | light_status | 0/1 | 1 (on) |
| Field 7 | battery | % | 98 |
| Field 8 | rssi | dBm | -45 |

## 7. Test Connection

### Using HTTP (Manual Test)

```bash
# Replace with your API key and channel ID
curl "https://api.thingspeak.com/update?api_key=YOUR_WRITE_API_KEY&field1=26.5&field2=6.8&field3=450"
```

Expected response: Entry ID number (e.g., `123`)

### Using ESP32

Upload code dan check serial monitor:
```
[MQTT] Connected successfully
[MQTT] Publishing: field1=26.50&field2=6.80&field3=450&field4=1&field5=0&field6=1
[MQTT] Data published successfully
```

## 8. View Data

### Channel View
1. Go to "Channels" → "My Channels"
2. Click your channel name
3. See real-time charts untuk each field

### Private/Public View
- **Private**: Only you can see (default)
- **Public**: Share link dengan others
  - Channel Settings → Make Public

### Export Data
1. Channel view → "Data Export"
2. Choose format (CSV, JSON, XML)
3. Select date range
4. Download

## 9. API Rate Limits

### Free License (Non-Commercial)
- **HTTP Update**: 15 seconds minimum interval
- **MQTT Update**: 1 second minimum interval (recommended)
- **Channels**: Up to 4 channels
- **Messages/year**: Unlimited
- **Data retention**: Unlimited

### Paid Licenses
For commercial use, see ThingSpeak pricing: https://thingspeak.com/prices

## 10. Typical Payload Format

### MQTT Publish
```
Topic: channels/1234567/publish
Payload: field1=26.5&field2=6.8&field3=450&field4=1&field5=0&field6=1
```

### HTTP POST
```bash
POST https://api.thingspeak.com/update
Content-Type: application/x-www-form-urlencoded

api_key=YOUR_WRITE_API_KEY&field1=26.5&field2=6.8&field3=450
```

### JSON Format (HTTP)
```bash
POST https://api.thingspeak.com/update.json
Content-Type: application/json

{
  "api_key": "YOUR_WRITE_API_KEY",
  "field1": 26.5,
  "field2": 6.8,
  "field3": 450
}
```

## 11. Read Data (untuk Flutter App)

### Latest Entry
```
GET https://api.thingspeak.com/channels/1234567/feeds/last.json?api_key=YOUR_READ_API_KEY
```

### Multiple Entries
```
GET https://api.thingspeak.com/channels/1234567/feeds.json?api_key=YOUR_READ_API_KEY&results=100
```

### Date Range
```
GET https://api.thingspeak.com/channels/1234567/feeds.json?api_key=YOUR_READ_API_KEY&start=2025-01-01&end=2025-01-31
```

## 12. Troubleshooting

### "HTTP Error 400: Bad Request"
- Check API key is correct
- Verify field names (field1, field2, etc.)
- Check update interval (minimum 15s for HTTP)

### "Connection Timeout"
- Check internet connection
- Verify broker address (mqtt3.thingspeak.com)
- Try port 8883 (SSL) if 1883 fails

### "Unauthorized"
- Verify MQTT username/password
- Regenerate MQTT API key if needed
- Check client ID is unique

### Data Not Showing
- Wait 15-30 seconds for data to appear
- Check channel field configuration
- Verify data format matches field types

## Resources

- ThingSpeak Documentation: https://www.mathworks.com/help/thingspeak/
- MQTT Guide: https://www.mathworks.com/help/thingspeak/mqtt-api.html
- REST API: https://www.mathworks.com/help/thingspeak/rest-api.html
