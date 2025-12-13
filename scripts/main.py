"""
Main application for IoT Aquaponik ESP32
Monitors sensors and publishes data to ThingSpeak via MQTT

Features:
- Multi-sensor monitoring (Temperature, pH, TDS, Water Level)
- Actuator control (Pump, Light)
- MQTT data publishing to ThingSpeak every 15 seconds
- Automatic dummy data generation when sensors unavailable
- WiFi auto-reconnect
- Watchdog timer
"""

import time
import gc
import machine
from machine import WDT

# Import configuration
import config

# Import WiFi manager
from wifi_manager import WiFiManager

# Import MQTT client
from mqtt_client import ThingSpeakMQTT

# Import sensor drivers
from sensors.ds18b20 import DS18B20Sensor
from sensors.ph_sensor import PHSensor
from sensors.tds_sensor import TDSSensor
from sensors.float_switch import FloatSwitch

# Import actuator drivers
from actuators.relay import RelayController

class AquaponikSystem:
    def __init__(self):
        """Initialize the aquaponik monitoring system"""
        print('[System] Initializing...')
        
        # Initialize WiFi
        self.wifi = WiFiManager(config.WIFI_SSID, config.WIFI_PASSWORD)
        
        # Initialize MQTT client with SSL/TLS support
        self.mqtt = ThingSpeakMQTT(
            broker=config.THINGSPEAK_MQTT_BROKER,
            port=config.THINGSPEAK_MQTT_PORT,
            username=config.THINGSPEAK_MQTT_USERNAME,
            password=config.THINGSPEAK_MQTT_PASSWORD,
            client_id=config.THINGSPEAK_CLIENT_ID,
            channel_id=config.THINGSPEAK_CHANNEL_ID,
            use_ssl=config.THINGSPEAK_USE_SSL
        )
        
        # Initialize sensors with dummy data enabled
        print('[System] Initializing sensors...')
        self.temp_sensor = DS18B20Sensor(config.PIN_DS18B20, enable_dummy=True)
        self.ph_sensor = PHSensor(config.PIN_PH_SENSOR, 
                                   voltage_calibration=config.PH_VOLTAGE_CALIBRATION,
                                   enable_dummy=True)
        self.tds_sensor = TDSSensor(config.PIN_TDS_SENSOR, 
                                     vref=config.TDS_VREF,
                                     enable_dummy=True)
        self.float_switch = FloatSwitch(config.PIN_FLOAT_SWITCH, enable_dummy=True)
        
        # Log sensor availability status
        self._log_sensor_status()
        
        # Initialize actuators
        print('[System] Initializing actuators...')
        self.relay = RelayController(config.PIN_RELAY_PUMP, 
                                     config.PIN_RELAY_LIGHT)
        
        # Sensor data (will always have values due to dummy data)
        self.temperature = None
        self.ph = None
        self.tds = None
        self.water_level = None
        
        # Timing
        self.last_sensor_read = 0
        self.last_ph_read = 0
        self.last_tds_read = 0
        self.last_mqtt_publish = 0
        self.last_status_update = 0
        
        # Watchdog timer (2 minutes)
        if hasattr(machine, 'WDT'):
            try:
                self.wdt = WDT(timeout=config.WATCHDOG_TIMEOUT * 1000)
                print('[System] Watchdog enabled')
            except:
                self.wdt = None
                print('[System] Watchdog not available')
        else:
            self.wdt = None
        
        print('[System] Initialization complete')
        print(f'[System] MQTT publish interval: {config.MQTT_PUBLISH_INTERVAL} seconds')
    
    def _log_sensor_status(self):
        """Log the availability status of all sensors"""
        print('[System] Sensor Status:')
        print(f'  - DS18B20 Temperature: {"Available" if self.temp_sensor.is_available() else "Not found (using dummy)"}')
        print(f'  - pH Sensor: {"Available" if self.ph_sensor.is_available() else "Not found (using dummy)"}')
        print(f'  - TDS Sensor: {"Available" if self.tds_sensor.is_available() else "Not found (using dummy)"}')
        print(f'  - Float Switch: {"Available" if self.float_switch.is_available() else "Not found (using dummy)"}')
    
    def connect_network(self):
        """Connect to WiFi and MQTT"""
        # Connect to WiFi
        if not self.wifi.connect():
            print('[System] Failed to connect to WiFi')
            return False
        
        # Connect to MQTT
        if not self.mqtt.connect():
            print('[System] Failed to connect to MQTT')
            return False
        
        return True
    
    def read_sensors(self):
        """Read all sensors with appropriate intervals"""
        current_time = time.time()
        
        # Read temperature (every SENSOR_READ_INTERVAL seconds)
        if current_time - self.last_sensor_read >= config.SENSOR_READ_INTERVAL:
            self.temperature = self.temp_sensor.read_temperature()
            self.water_level = self.float_switch.is_water_level_normal()
            self.last_sensor_read = current_time
            
            if config.DEBUG:
                print(f'[Sensors] Temp: {self.temperature}°C, Water: {"OK" if self.water_level else "LOW"}')
        
        # Read pH (every PH_READ_INTERVAL seconds)
        if current_time - self.last_ph_read >= config.PH_READ_INTERVAL:
            self.ph = self.ph_sensor.read_ph()
            self.last_ph_read = current_time
            
            if config.DEBUG:
                print(f'[Sensors] pH: {self.ph}')
        
        # Read TDS (every TDS_READ_INTERVAL seconds, with temperature compensation)
        if current_time - self.last_tds_read >= config.TDS_READ_INTERVAL:
            if self.temperature is not None:
                self.tds = self.tds_sensor.read_tds(temperature=self.temperature)
            else:
                self.tds = self.tds_sensor.read_tds()
            self.last_tds_read = current_time
            
            if config.DEBUG:
                print(f'[Sensors] TDS: {self.tds} ppm')
    
    def check_thresholds(self):
        """Check sensor values against thresholds and trigger alerts"""
        alerts = []
        
        # Check temperature
        if self.temperature is not None:
            if self.temperature < config.TEMP_CRITICAL_MIN or self.temperature > config.TEMP_CRITICAL_MAX:
                alerts.append(f'CRITICAL: Temperature {self.temperature}°C out of range')
            elif self.temperature < config.TEMP_MIN or self.temperature > config.TEMP_MAX:
                alerts.append(f'WARNING: Temperature {self.temperature}°C near threshold')
        
        # Check pH
        if self.ph is not None:
            if self.ph < config.PH_CRITICAL_MIN or self.ph > config.PH_CRITICAL_MAX:
                alerts.append(f'CRITICAL: pH {self.ph} out of range')
            elif self.ph < config.PH_MIN or self.ph > config.PH_MAX:
                alerts.append(f'WARNING: pH {self.ph} near threshold')
        
        # Check TDS
        if self.tds is not None:
            if self.tds < config.TDS_CRITICAL_MIN or self.tds > config.TDS_CRITICAL_MAX:
                alerts.append(f'CRITICAL: TDS {self.tds} ppm out of range')
            elif self.tds < config.TDS_MIN or self.tds > config.TDS_MAX:
                alerts.append(f'WARNING: TDS {self.tds} ppm near threshold')
        
        # Check water level
        if self.water_level is not None and not self.water_level:
            alerts.append('CRITICAL: Water level LOW!')
        
        # Print alerts
        for alert in alerts:
            print(f'[Alert] {alert}')
        
        return alerts
    
    def publish_data(self):
        """Publish sensor data to ThingSpeak via MQTT every 15 seconds"""
        current_time = time.time()
        
        if current_time - self.last_mqtt_publish >= config.MQTT_PUBLISH_INTERVAL:
            # Always publish data - sensors with dummy enabled will provide values
            # Use default/fallback values if any sensor still returns None
            temp = self.temperature if self.temperature is not None else 25.0
            ph = self.ph if self.ph is not None else 7.0
            tds = self.tds if self.tds is not None else 450
            water_level = self.water_level if self.water_level is not None else True
            
            # Log what we're sending
            if config.DEBUG:
                print(f'[MQTT] Publishing data:')
                print(f'  Temp: {temp}°C {"(dummy)" if self.temperature is None else ""}')
                print(f'  pH: {ph} {"(dummy)" if self.ph is None else ""}')
                print(f'  TDS: {tds} ppm {"(dummy)" if self.tds is None else ""}')
                print(f'  Water: {"OK" if water_level else "LOW"} {"(dummy)" if self.water_level is None else ""}')
            
            success = self.mqtt.publish_sensor_data(
                temperature=temp,
                ph=ph,
                tds=tds,
                water_level=water_level,
                pump_status=self.relay.get_pump_status(),
                light_status=self.relay.get_light_status()
            )
            
            if success:
                print('[MQTT] Data published successfully')
            else:
                print('[MQTT] Failed to publish data')
            
            self.last_mqtt_publish = current_time
        
        # Publish status (battery and RSSI) less frequently
        if current_time - self.last_status_update >= config.STATUS_UPDATE_INTERVAL:
            rssi = self.wifi.get_rssi()
            if rssi is not None:
                # For demo purposes, use a mock battery value
                # In real implementation, you would read from a battery monitoring circuit
                battery = 100
                self.mqtt.publish_status(battery, rssi)
                self.last_status_update = current_time
    
    def run(self):
        """Main application loop"""
        print('[System] Starting main loop...')
        
        # Initial network connection
        if not self.connect_network():
            print('[System] Network connection failed, retrying in 10 seconds...')
            time.sleep(10)
            return
        
        # Main loop
        while True:
            try:
                # Feed watchdog
                if self.wdt:
                    self.wdt.feed()
                
                # Monitor WiFi connection
                if not self.wifi.monitor_connection():
                    print('[System] WiFi reconnection failed')
                    time.sleep(5)
                    continue
                
                # Monitor MQTT connection
                if not self.mqtt.is_connected():
                    print('[System] MQTT disconnected, reconnecting...')
                    self.mqtt.reconnect()
                
                # Read sensors
                self.read_sensors()
                
                # Check thresholds
                self.check_thresholds()
                
                # Publish data
                self.publish_data()
                
                # Check for incoming MQTT messages
                self.mqtt.check_messages()
                
                # Garbage collection
                gc.collect()
                
                # Small delay
                time.sleep(1)
                
            except KeyboardInterrupt:
                print('[System] Interrupted by user')
                break
            except Exception as e:
                print(f'[System] Error in main loop: {e}')
                time.sleep(5)
        
        # Cleanup
        self.cleanup()
    
    def cleanup(self):
        """Cleanup before shutdown"""
        print('[System] Cleaning up...')
        self.relay.turn_all_off()
        self.mqtt.disconnect()
        self.wifi.disconnect()
        print('[System] Shutdown complete')

# Entry point
if __name__ == '__main__':
    print()
    print('=' * 50)
    print('Starting IoT Aquaponik System')
    print('=' * 50)
    print()
    
    try:
        system = AquaponikSystem()
        system.run()
    except Exception as e:
        print(f'[FATAL] System error: {e}')
        # Turn off all relays on fatal error
        try:
            relay = RelayController(config.PIN_RELAY_PUMP, config.PIN_RELAY_LIGHT)
            relay.turn_all_off()
        except:
            pass
