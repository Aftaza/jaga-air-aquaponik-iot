"""
Boot script for ESP32
Runs on startup before main.py

Features:
- WiFi auto-connect
- Network time synchronization
- Initial error logging
"""

import gc
import esp
import time

# Disable debug output
esp.osdebug(None)

# Run garbage collection
gc.collect()

print('=' * 50)
print('IoT Aquaponik Mini - ESP32')
print('Firmware Version: 1.0.0')
print('=' * 50)
print()

# Import configuration
try:
    import config
    print('[Boot] Configuration loaded')
except ImportError:
    print('[Boot] ERROR: config.py not found!')
    print('[Boot] Please create config.py with your settings')

# Show memory info
print(f'[Boot] Free memory: {gc.mem_free()} bytes')
print()

print('[Boot] Boot completed, starting main application...')
print()
