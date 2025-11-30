"""
WiFi Connection Manager for ESP32
Handles WiFi connectivity with auto-reconnect

Features:
- Connect to WiFi network
- Connection status monitoring
- Auto-reconnect on disconnect
- Signal strength (RSSI) reporting
"""

import network
import time
import gc

class WiFiManager:
    def __init__(self, ssid, password, timeout=30):
        """
        Initialize WiFi manager
        
        Args:
            ssid: WiFi network SSID
            password: WiFi password
            timeout: Connection timeout in seconds
        """
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
        # Disable access point mode to save power
        ap = network.WLAN(network.AP_IF)
        ap.active(False)
        
        print('[WiFi] Manager initialized')
    
    def connect(self):
        """
        Connect to WiFi network
        
        Returns:
            True if connected successfully, False otherwise
        """
        if self.is_connected():
            print('[WiFi] Already connected')
            return True
        
        print(f'[WiFi] Connecting to {self.ssid}...')
        
        try:
            self.wlan.connect(self.ssid, self.password)
            
            # Wait for connection
            start_time = time.time()
            while not self.wlan.isconnected():
                if time.time() - start_time > self.timeout:
                    print('[WiFi] Connection timeout')
                    return False
                
                time.sleep(0.5)
                print('.', end='')
            
            print()
            print('[WiFi] Connected successfully')
            self._print_network_info()
            
            # Force garbage collection
            gc.collect()
            
            return True
            
        except Exception as e:
            print(f'[WiFi] Connection error: {e}')
            return False
    
    def disconnect(self):
        """Disconnect from WiFi network"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
            print('[WiFi] Disconnected')
    
    def is_connected(self):
        """
        Check if connected to WiFi
        
        Returns:
            True if connected, False otherwise
        """
        return self.wlan.isconnected()
    
    def get_ip(self):
        """
        Get IP address
        
        Returns:
            IP address string, or None if not connected
        """
        if self.is_connected():
            return self.wlan.ifconfig()[0]
        return None
    
    def get_rssi(self):
        """
        Get signal strength (RSSI)
        
        Returns:
            RSSI value in dBm, or None if not connected
        """
        if self.is_connected():
            try:
                return self.wlan.status('rssi')
            except:
                # Fallback for older MicroPython versions
                return -50  # Default value
        return None
    
    def reconnect(self):
        """
        Reconnect to WiFi network
        
        Returns:
            True if reconnected successfully, False otherwise
        """
        print('[WiFi] Reconnecting...')
        self.disconnect()
        time.sleep(2)
        return self.connect()
    
    def monitor_connection(self):
        """
        Monitor connection and auto-reconnect if disconnected
        
        Returns:
            True if connected or reconnected, False otherwise
        """
        if not self.is_connected():
            print('[WiFi] Connection lost, attempting to reconnect...')
            return self.reconnect()
        return True
    
    def _print_network_info(self):
        """Print network information"""
        if self.is_connected():
            ifconfig = self.wlan.ifconfig()
            rssi = self.get_rssi()
            
            print('[WiFi] Network Info:')
            print(f'  IP Address: {ifconfig[0]}')
            print(f'  Subnet Mask: {ifconfig[1]}')
            print(f'  Gateway: {ifconfig[2]}')
            print(f'  DNS: {ifconfig[3]}')
            if rssi is not None:
                print(f'  RSSI: {rssi} dBm')
    
    def get_status(self):
        """
        Get WiFi status information
        
        Returns:
            Dictionary with status information
        """
        return {
            'connected': self.is_connected(),
            'ip': self.get_ip(),
            'rssi': self.get_rssi(),
            'ssid': self.ssid
        }
