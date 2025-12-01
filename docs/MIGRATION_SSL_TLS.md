# Migration Guide: SSL/TLS MQTT Update

## Overview

Sistem IoT Aquaponik Mini telah diupdate untuk menggunakan koneksi MQTT terenkripsi dengan TLS/SSL. Dokumen ini menjelaskan perubahan yang dilakukan dan langkah-langkah untuk mengupdate sistem yang sudah ada.

## 🔄 Perubahan Utama

### 1. File yang Dimodifikasi

#### `scripts/config.py`
**Perubahan:**
- Port MQTT diubah dari `1883` (non-SSL) ke `8883` (SSL/TLS)
- Ditambahkan flag `THINGSPEAK_USE_SSL = True`

**Before:**
```python
THINGSPEAK_MQTT_PORT = 1883  # Use 8883 for SSL
```

**After:**
```python
THINGSPEAK_MQTT_PORT = 8883  # TLS/SSL port (use 1883 for non-SSL)
THINGSPEAK_USE_SSL = True    # Enable TLS/SSL encryption
```

#### `scripts/mqtt_client.py`
**Perubahan:**
- Import module `ussl` untuk SSL support
- Tambah parameter `use_ssl` di constructor
- Update method `connect()` untuk support SSL/TLS
- Tambah conditional logic untuk SSL vs non-SSL connection

**Key Changes:**
```python
import ussl  # New import

class ThingSpeakMQTT:
    def __init__(self, ..., use_ssl=True):  # New parameter
        self.use_ssl = use_ssl
        
    def connect(self):
        if self.use_ssl:
            # SSL/TLS connection
            self.client = MQTTClient(
                ...,
                ssl=True,
                ssl_params={'server_hostname': self.broker}
            )
        else:
            # Non-SSL connection
            self.client = MQTTClient(...)
```

#### `scripts/main.py`
**Perubahan:**
- Update inisialisasi MQTT client untuk pass parameter `use_ssl`

**Before:**
```python
self.mqtt = ThingSpeakMQTT(
    broker=config.THINGSPEAK_MQTT_BROKER,
    port=config.THINGSPEAK_MQTT_PORT,
    username=config.THINGSPEAK_MQTT_USERNAME,
    password=config.THINGSPEAK_MQTT_PASSWORD,
    client_id=config.THINGSPEAK_CLIENT_ID,
    channel_id=config.THINGSPEAK_CHANNEL_ID
)
```

**After:**
```python
self.mqtt = ThingSpeakMQTT(
    broker=config.THINGSPEAK_MQTT_BROKER,
    port=config.THINGSPEAK_MQTT_PORT,
    username=config.THINGSPEAK_MQTT_USERNAME,
    password=config.THINGSPEAK_MQTT_PASSWORD,
    client_id=config.THINGSPEAK_CLIENT_ID,
    channel_id=config.THINGSPEAK_CHANNEL_ID,
    use_ssl=config.THINGSPEAK_USE_SSL  # New parameter
)
```

### 2. Dokumentasi yang Diupdate

#### Updated Files:
- ✅ `docs/README.md` - Added SSL/TLS features dan security notes
- ✅ `docs/ESP32_SETUP.md` - Updated configuration dan troubleshooting
- ✅ `docs/THINGSPEAK_SETUP.md` - Updated MQTT configuration dengan SSL/TLS

#### New Files:
- ✅ `docs/MQTT_SSL_SECURITY.md` - Comprehensive SSL/TLS security guide
- ✅ `docs/MIGRATION_SSL_TLS.md` - This migration guide

## 📋 Langkah-langkah Update

### Untuk Sistem Baru (Fresh Install)

1. **Flash MicroPython** (pastikan versi terbaru dengan SSL support):
   ```bash
   esptool.py --chip esp32 --port COM3 erase_flash
   esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-latest.bin
   ```

2. **Configure settings** di `scripts/config.py`:
   ```python
   THINGSPEAK_MQTT_PORT = 8883
   THINGSPEAK_USE_SSL = True
   # ... other settings
   ```

3. **Upload semua files** ke ESP32:
   ```bash
   cd scripts
   ampy --port COM3 put config.py
   ampy --port COM3 put mqtt_client.py
   ampy --port COM3 put main.py
   ampy --port COM3 put wifi_manager.py
   ampy --port COM3 put boot.py
   ampy --port COM3 put sensors sensors
   ampy --port COM3 put actuators actuators
   ```

4. **Reset ESP32** dan verify connection

### Untuk Sistem yang Sudah Ada (Update)

#### Option 1: Full Update (Recommended)

1. **Backup existing config**:
   ```bash
   ampy --port COM3 get config.py config.py.backup
   ```

2. **Update files** satu per satu:
   ```bash
   ampy --port COM3 put config.py
   ampy --port COM3 put mqtt_client.py
   ampy --port COM3 put main.py
   ```

3. **Reset ESP32** dan test

#### Option 2: Manual Update

1. **Connect to ESP32 REPL**:
   ```bash
   screen /dev/ttyUSB0 115200
   # atau
   picocom COM3 -b115200
   ```

2. **Edit config.py** via REPL atau file editor:
   ```python
   # Add these lines to config.py
   THINGSPEAK_MQTT_PORT = 8883
   THINGSPEAK_USE_SSL = True
   ```

3. **Replace mqtt_client.py** dengan versi baru

4. **Update main.py** untuk pass `use_ssl` parameter

5. **Soft reset**:
   ```python
   >>> import machine
   >>> machine.soft_reset()
   ```

## ✅ Verification

### 1. Check SSL Support

```python
>>> import ussl
>>> # No error = SSL supported
```

### 2. Check Memory

```python
>>> import gc
>>> gc.collect()
>>> gc.mem_free()
110000  # Should be > 50000
```

### 3. Test Connection

Expected output:
```
[MQTT] Client initialized
  Broker: mqtt3.thingspeak.com:8883
  SSL/TLS: Enabled
  Channel: 1234567
[MQTT] Connecting to broker...
[MQTT] Using SSL/TLS encryption
[MQTT] Connected successfully
```

### 4. Verify Data Publishing

Check ThingSpeak channel untuk confirm data masih diterima.

## 🔧 Troubleshooting

### Issue: "SSL handshake failed"

**Solution:**
1. Update MicroPython firmware ke versi terbaru
2. Set system time dengan NTP:
   ```python
   import ntptime
   ntptime.settime()
   ```
3. Check memory: `gc.mem_free()` > 50000

### Issue: "Connection timeout"

**Solution:**
1. Verify WiFi connection
2. Test dengan non-SSL first:
   ```python
   THINGSPEAK_USE_SSL = False
   THINGSPEAK_MQTT_PORT = 1883
   ```
3. Check firewall tidak block port 8883

### Issue: "Out of memory"

**Solution:**
1. Free memory: `gc.collect()`
2. Reduce sensor reading frequency
3. Consider non-SSL jika memory sangat terbatas

## 🔙 Rollback (Jika Diperlukan)

Jika mengalami masalah dengan SSL/TLS, rollback ke non-SSL:

### Quick Rollback

Edit `config.py`:
```python
THINGSPEAK_MQTT_PORT = 1883
THINGSPEAK_USE_SSL = False
```

Reset ESP32. Sistem akan menggunakan non-SSL connection.

### Full Rollback

1. Restore backup config:
   ```bash
   ampy --port COM3 put config.py.backup config.py
   ```

2. Use old version of mqtt_client.py (without SSL support)

3. Reset ESP32

## 📊 Comparison

| Feature | Non-SSL (Old) | SSL/TLS (New) |
|---------|---------------|---------------|
| Port | 1883 | 8883 |
| Encryption | ❌ No | ✅ Yes |
| Security | Low | High |
| Memory Usage | ~30 KB | ~50-60 KB |
| Connection Time | ~1-2s | ~3-5s |
| Certificate Validation | N/A | ✅ Yes |
| Recommended | ❌ No | ✅ Yes |

## 🎯 Recommendations

### Production Deployment
- ✅ **Always use SSL/TLS** (port 8883)
- ✅ Keep firmware updated
- ✅ Monitor memory usage
- ✅ Implement retry logic
- ✅ Regular security audits

### Development/Testing
- Use SSL/TLS by default
- Non-SSL only untuk debugging specific issues
- Test both modes untuk ensure compatibility

### Memory-Constrained Devices
- Optimize code untuk reduce memory usage
- Consider firmware dengan smaller footprint
- Monitor `gc.mem_free()` regularly
- Implement memory cleanup routines

## 📚 Additional Resources

- [MQTT_SSL_SECURITY.md](MQTT_SSL_SECURITY.md) - Detailed SSL/TLS guide
- [ESP32_SETUP.md](ESP32_SETUP.md) - Complete setup guide
- [THINGSPEAK_SETUP.md](THINGSPEAK_SETUP.md) - ThingSpeak configuration
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

## 📝 Changelog

### Version 1.1 (2025-12-01)
- ✅ Added SSL/TLS support untuk MQTT
- ✅ Updated default port to 8883
- ✅ Added `THINGSPEAK_USE_SSL` configuration flag
- ✅ Updated mqtt_client.py dengan SSL support
- ✅ Updated all documentation
- ✅ Added MQTT_SSL_SECURITY.md
- ✅ Added migration guide

### Version 1.0 (Previous)
- Basic MQTT support (non-SSL)
- Port 1883
- No encryption

---

**Last Updated**: 2025-12-01  
**Migration Version**: 1.0 → 1.1 (SSL/TLS)
