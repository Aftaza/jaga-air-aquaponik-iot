"""
MQTT Client for ThingSpeak with TLS/SSL Support
Handles MQTT connection and data publishing to ThingSpeak

Features:
- Connect to ThingSpeak MQTT broker with TLS/SSL encryption
- Publish sensor data
- Subscribe to control commands
- Auto-reconnect on disconnect
- Secure communication using SSL/TLS
"""

from umqtt.simple import MQTTClient
import json
import time
import ussl

class ThingSpeakMQTT:
    def __init__(self, broker, port, username, password, client_id, channel_id, use_ssl=True):
        """
        Initialize MQTT client for ThingSpeak with SSL/TLS support
        
        Args:
            broker: MQTT broker address
            port: MQTT broker port (8883 for SSL, 1883 for non-SSL)
            username: MQTT username
            password: MQTT password (API key)
            client_id: Client ID
            channel_id: ThingSpeak channel ID
            use_ssl: Enable SSL/TLS encryption (default: True)
        """
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.channel_id = channel_id
        self.use_ssl = use_ssl
        
        self.client = None
        self.connected = False
        self.publish_topic = f'channels/{channel_id}/publish'
        
        print('[MQTT] Client initialized')
        print(f'  Broker: {broker}:{port}')
        print(f'  SSL/TLS: {"Enabled" if use_ssl else "Disabled"}')
        print(f'  Channel: {channel_id}')
    
    def connect(self):
        """
        Connect to MQTT broker with optional SSL/TLS encryption
        
        Returns:
            True if connected successfully, False otherwise
        """
        if self.connected:
            print('[MQTT] Already connected')
            return True
        
        try:
            print('[MQTT] Connecting to broker...')
            
            # Create MQTT client with SSL/TLS support if enabled
            if self.use_ssl:
                print('[MQTT] Using SSL/TLS encryption')
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
                print('[MQTT] Using non-encrypted connection')
                self.client = MQTTClient(
                    client_id=self.client_id,
                    server=self.broker,
                    port=self.port,
                    user=self.username,
                    password=self.password,
                    keepalive=60
                )
            
            self.client.connect()
            self.connected = True
            
            print('[MQTT] Connected successfully')
            return True
            
        except Exception as e:
            print(f'[MQTT] Connection error: {e}')
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client and self.connected:
            try:
                self.client.disconnect()
                print('[MQTT] Disconnected')
            except:
                pass
            finally:
                self.connected = False
    
    def publish_sensor_data(self, temperature, ph, tds, water_level, pump_status, light_status):
        """
        Publish sensor data to ThingSpeak
        
        ThingSpeak field mapping:
        - field1: temperature
        - field2: ph
        - field3: tds
        - field4: water_level (1=normal, 0=low)
        - field5: pump_status (1=on, 0=off)
        - field6: light_status (1=on, 0=off)
        
        Args:
            temperature: Temperature in °C
            ph: pH value
            tds: TDS in ppm
            water_level: Water level (True/False)
            pump_status: Pump status (True/False)
            light_status: Light status (True/False)
            
        Returns:
            True if published successfully, False otherwise
        """
        if not self.connected:
            print('[MQTT] Not connected, attempting to connect...')
            if not self.connect():
                return False
        
        try:
            # Format payload for ThingSpeak
            # Using field1=value&field2=value format
            payload = (
                f'field1={temperature:.2f}&'
                f'field2={ph:.2f}&'
                f'field3={tds}&'
                f'field4={1 if water_level else 0}&'
                f'field5={1 if pump_status else 0}&'
                f'field6={1 if light_status else 0}'
            )
            
            print(f'[MQTT] Publishing: {payload}')
            self.client.publish(self.publish_topic.encode(), payload.encode())
            
            return True
            
        except Exception as e:
            print(f'[MQTT] Publish error: {e}')
            self.connected = False
            return False
    
    def publish_status(self, battery, rssi):
        """
        Publish device status (battery and RSSI)
        
        Args:
            battery: Battery percentage (0-100)
            rssi: Signal strength in dBm
            
        Returns:
            True if published successfully, False otherwise
        """
        if not self.connected:
            if not self.connect():
                return False
        
        try:
            payload = f'field7={battery}&field8={rssi}'
            
            print(f'[MQTT] Publishing status: {payload}')
            self.client.publish(self.publish_topic.encode(), payload.encode())
            
            return True
            
        except Exception as e:
            print(f'[MQTT] Status publish error: {e}')
            self.connected = False
            return False
    
    def check_messages(self):
        """
        Check for incoming MQTT messages (non-blocking)
        
        Returns:
            True if check was successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            self.client.check_msg()
            return True
        except Exception as e:
            print(f'[MQTT] Check messages error: {e}')
            self.connected = False
            return False
    
    def is_connected(self):
        """Check if MQTT client is connected"""
        return self.connected
    
    def reconnect(self):
        """
        Reconnect to MQTT broker
        
        Returns:
            True if reconnected successfully, False otherwise
        """
        print('[MQTT] Reconnecting...')
        self.disconnect()
        time.sleep(2)
        return self.connect()
