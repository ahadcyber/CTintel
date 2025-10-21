"""VirusTotal API Integration for Threat Lookup"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VirusTotalChecker:
    """VirusTotal API client for threat verification"""
    
    def __init__(self):
        self.api_key = os.getenv('VIRUSTOTAL_API_KEY', '')
        self.base_url = 'https://www.virustotal.com/api/v3'
        self.headers = {'x-apikey': self.api_key} if self.api_key else {}
    
    def check_ip(self, ip_address):
        """Check IP address reputation"""
        if not self.api_key:
            return {'error': 'VirusTotal API key not configured'}
        
        try:
            url = f'{self.base_url}/ip_addresses/{ip_address}'
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                
                return {
                    'ip': ip_address,
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                    'threat_level': self._calculate_threat_level(stats),
                    'source': 'VirusTotal'
                }
            else:
                return {'error': f'API returned status {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def check_domain(self, domain):
        """Check domain reputation"""
        if not self.api_key:
            return {'error': 'VirusTotal API key not configured'}
        
        try:
            url = f'{self.base_url}/domains/{domain}'
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                
                return {
                    'domain': domain,
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                    'threat_level': self._calculate_threat_level(stats),
                    'source': 'VirusTotal'
                }
            else:
                return {'error': f'API returned status {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def check_url(self, url):
        """Check URL reputation"""
        if not self.api_key:
            return {'error': 'VirusTotal API key not configured'}
        
        try:
            import base64
            # URL needs to be base64 encoded without padding
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            
            api_url = f'{self.base_url}/urls/{url_id}'
            response = requests.get(api_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                
                return {
                    'url': url,
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                    'threat_level': self._calculate_threat_level(stats),
                    'source': 'VirusTotal'
                }
            else:
                return {'error': f'API returned status {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def check_hash(self, file_hash):
        """Check file hash reputation"""
        if not self.api_key:
            return {'error': 'VirusTotal API key not configured'}
        
        try:
            url = f'{self.base_url}/files/{file_hash}'
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                
                return {
                    'hash': file_hash,
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                    'threat_level': self._calculate_threat_level(stats),
                    'source': 'VirusTotal'
                }
            else:
                return {'error': f'API returned status {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_threat_level(self, stats):
        """Calculate threat level based on detection stats"""
        malicious = stats.get('malicious', 0)
        suspicious = stats.get('suspicious', 0)
        
        total_detections = malicious + suspicious
        
        if total_detections == 0:
            return 'Clean'
        elif total_detections <= 2:
            return 'Low'
        elif total_detections <= 5:
            return 'Medium'
        elif total_detections <= 10:
            return 'High'
        else:
            return 'Critical'


# Singleton instance
vt_checker = VirusTotalChecker()
