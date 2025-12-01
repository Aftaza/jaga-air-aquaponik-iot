# MQTT SSL/TLS Security Guide

## Overview

Sistem IoT Aquaponik Mini menggunakan koneksi MQTT terenkripsi dengan TLS/SSL untuk memastikan keamanan data sensor yang dikirim ke ThingSpeak. Dokumen ini menjelaskan implementasi, konfigurasi, dan best practices untuk keamanan MQTT.

## 🔒 Mengapa SSL/TLS Penting?

### Tanpa Enkripsi (Port 1883)
- ❌ Data dikirim dalam **plain text**
- ❌ Credentials (username/password) dapat di-intercept
- ❌ Rentan terhadap **man-in-the-middle attacks**
- ❌ Data sensor dapat dimodifikasi oleh pihak ketiga
- ❌ Tidak ada verifikasi identitas server

### Dengan SSL/TLS (Port 8883)
- ✅ **Enkripsi end-to-end** untuk semua data
- ✅ Credentials dikirim secara terenkripsi
- ✅ **Certificate-based authentication** untuk verifikasi server
- ✅ Proteksi terhadap man-in-the-middle attacks
- ✅ Data integrity - tidak dapat dimodifikasi tanpa terdeteksi

## 📋 Implementasi di MicroPython

### 1. Konfigurasi SSL/TLS

Edit `scripts/config.py`:

```python
# ThingSpeak MQTT Configuration with TLS/SSL
THINGSPEAK_MQTT_BROKER = 'mqtt3.thingspeak.com'
THINGSPEAK_MQTT_PORT = 8883  # TLS/SSL port
THINGSPEAK_USE_SSL = True    # Enable TLS/SSL encryption
THINGSPEAK_CHANNEL_ID = 'YOUR_CHANNEL_ID'
THINGSPEAK_WRITE_API_KEY = 'YOUR_WRITE_API_KEY'
THINGSPEAK_MQTT_USERNAME = 'YOUR_MQTT_USERNAME'
THINGSPEAK_MQTT_PASSWORD = 'YOUR_MQTT_PASSWORD'
THINGSPEAK_CLIENT_ID = 'YOUR_CLIENT_ID'
```

### 2. MQTT Client dengan SSL Support

File `mqtt_client.py` telah diupdate untuk support SSL/TLS:

```python
import ussl
from umqtt.simple import MQTTClient

class ThingSpeakMQTT:
    def __init__(self, broker, port, username, password, client_id, channel_id, use_ssl=True):
        self.use_ssl = use_ssl
        # ... other initialization
    
    def connect(self):
        if self.use_ssl:
            # Create SSL/TLS connection
            self.client = MQTTClient(
                client_id=self.client_id,
                server=self.broker,
                port=self.port,
                user=self.username,
                password=self.password,
                keepalive=60,
                ssl=True,
                ssl_params={'server_hostname': self.broker}
            )
        else:
            # Non-SSL connection (not recommended)
            self.client = MQTTClient(...)
```

### 3. SSL Parameters

**server_hostname**: Digunakan untuk Server Name Indication (SNI), memungkinkan server untuk menyajikan sertifikat yang benar.

```python
ssl_params={'server_hostname': self.broker}
```

## 🔧 Persyaratan Teknis

### MicroPython Firmware
- **Minimum Version**: v1.20 atau lebih baru
- **SSL Support**: Pastikan firmware di-compile dengan SSL support
- **Verify SSL**: Test di REPL:
  ```python
  >>> import ussl
  >>> # Jika tidak ada error, SSL supported
  ```

### Memory Requirements
- **Non-SSL**: ~30-40 KB free memory
- **SSL/TLS**: ~50-70 KB free memory
- **Check Memory**:
  ```python
  >>> import gc
  >>> gc.collect()
  >>> gc.mem_free()
  110000  # Should be > 50000 for SSL
  ```

### System Time
SSL/TLS memerlukan waktu sistem yang akurat untuk validasi sertifikat:

```python
>>> import time
>>> time.localtime()
(2025, 12, 1, 12, 30, 45, 0, 335)  # Should show current time
```

Jika waktu tidak akurat, set menggunakan NTP:
```python
import ntptime
ntptime.settime()
```

## 🛠️ Troubleshooting SSL/TLS

### Error: "SSL handshake failed"

**Penyebab Umum:**
1. Waktu sistem tidak akurat
2. Memory tidak cukup
3. Firmware tidak support SSL
4. Server certificate validation failed

**Solusi:**

1. **Set waktu dengan NTP:**
   ```python
   import ntptime
   import time
   ntptime.settime()
   print(time.localtime())
   ```

2. **Free up memory:**
   ```python
   import gc
   gc.collect()
   print(f"Free memory: {gc.mem_free()} bytes")
   ```

3. **Update firmware:**
   - Download latest MicroPython firmware dengan SSL support
   - Flash ulang ESP32

4. **Temporary: Disable certificate verification** (not recommended for production):
   ```python
   ssl_params={'server_hostname': self.broker, 'cert_reqs': 0}
   ```

### Error: "Connection timeout"

**Solusi:**
1. Check WiFi connection stability
2. Verify broker address dan port
3. Test dengan non-SSL terlebih dahulu:
   ```python
   THINGSPEAK_USE_SSL = False
   THINGSPEAK_MQTT_PORT = 1883
   ```
4. Check firewall tidak memblokir port 8883

### Error: "Out of memory"

**Solusi:**
1. Reduce sensor reading frequency
2. Optimize code untuk reduce memory usage
3. Call `gc.collect()` lebih sering
4. Consider non-SSL jika memory sangat terbatas

## 🔐 Best Practices

### 1. Always Use SSL/TLS in Production
```python
# PRODUCTION - Always use SSL
THINGSPEAK_USE_SSL = True
THINGSPEAK_MQTT_PORT = 8883
```

### 2. Keep Credentials Secure
- Jangan commit `config.py` dengan credentials ke Git
- Gunakan `.gitignore` untuk exclude config files
- Rotate MQTT API keys secara berkala

### 3. Monitor Memory Usage
```python
import gc

def check_memory():
    gc.collect()
    free = gc.mem_free()
    print(f"Free memory: {free} bytes")
    if free < 50000:
        print("WARNING: Low memory for SSL!")
    return free
```

### 4. Implement Retry Logic
```python
def connect_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            if mqtt.connect():
                return True
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(5)
    return False
```

### 5. Regular Firmware Updates
- Update MicroPython firmware untuk security patches
- Check release notes untuk SSL/TLS improvements

## 📊 Performance Impact

### Connection Time
- **Non-SSL**: ~1-2 seconds
- **SSL/TLS**: ~3-5 seconds (due to handshake)

### Memory Usage
- **Non-SSL**: ~30 KB
- **SSL/TLS**: ~50-60 KB

### Data Throughput
- Minimal impact pada data rate
- SSL overhead: ~5-10% untuk small payloads

## 🔍 Verification

### Test SSL Connection

```python
from mqtt_client import ThingSpeakMQTT
import config

# Initialize with SSL
mqtt = ThingSpeakMQTT(
    broker=config.THINGSPEAK_MQTT_BROKER,
    port=config.THINGSPEAK_MQTT_PORT,
    username=config.THINGSPEAK_MQTT_USERNAME,
    password=config.THINGSPEAK_MQTT_PASSWORD,
    client_id=config.THINGSPEAK_CLIENT_ID,
    channel_id=config.THINGSPEAK_CHANNEL_ID,
    use_ssl=True
)

# Connect and verify
if mqtt.connect():
    print("✅ SSL/TLS connection successful!")
    print(f"  Broker: {config.THINGSPEAK_MQTT_BROKER}:{config.THINGSPEAK_MQTT_PORT}")
    print(f"  SSL: Enabled")
else:
    print("❌ Connection failed")
```

Expected output:
```
[MQTT] Client initialized
  Broker: mqtt3.thingspeak.com:8883
  SSL/TLS: Enabled
  Channel: 1234567
[MQTT] Connecting to broker...
[MQTT] Using SSL/TLS encryption
[MQTT] Connected successfully
✅ SSL/TLS connection successful!
  Broker: mqtt3.thingspeak.com:8883
  SSL: Enabled
```

## 📚 Additional Resources

- **MicroPython SSL Documentation**: https://docs.micropython.org/en/latest/library/ussl.html
- **ThingSpeak MQTT API**: https://www.mathworks.com/help/thingspeak/mqtt-api.html
- **MQTT Security Best Practices**: https://mqtt.org/mqtt-security-best-practices/
- **TLS/SSL Overview**: https://en.wikipedia.org/wiki/Transport_Layer_Security

## 🆘 Support

Jika mengalami masalah dengan SSL/TLS:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Verify semua persyaratan di dokumen ini
3. Test dengan non-SSL untuk isolate masalah
4. Check MicroPython forum untuk known issues

---

**Last Updated**: 2025-12-01  
**Version**: 1.0 (SSL/TLS Enabled)
