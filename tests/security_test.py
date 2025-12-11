import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, allowed_file

class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
    def test_lfi_prevention(self):
        """Test that file download endpoint rejects non-PCAP files"""
        # Attempt to download this test file itself (ends in .py)
        path = os.path.abspath(__file__)
        response = self.client.get(f'/flipper/download?path={path}')
        
        # Debugging output if verification fails
        if response.status_code != 403:
            print(f"\nDEBUG: Status: {response.status_code}")
            print(f"DEBUG: Data: {response.data.decode('utf-8')}")
        
        # Should be forbidden (403)
        self.assertEqual(response.status_code, 403, f"Expected 403, got {response.status_code}. Body: {response.data}")
        self.assertIn(b"Security error", response.data)
        
    def test_allowed_file(self):
        """Test the file extension checker"""
        self.assertTrue(allowed_file('test.pcap', 'pcap'))
        self.assertTrue(allowed_file('test.cap', 'pcap'))
        self.assertTrue(allowed_file('test.pcapng', 'pcap'))
        self.assertFalse(allowed_file('test.exe', 'pcap'))
        self.assertFalse(allowed_file('test.py', 'pcap'))

if __name__ == '__main__':
    unittest.main()
