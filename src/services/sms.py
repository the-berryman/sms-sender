# src/services/sms.py
"""
Service class for handling SMS-related operations including API interactions.
"""

import requests
import xml.etree.ElementTree as ET
from src.utils.xml_builder import XMLBuilder


class SMSService:
    """Handles all SMS-related operations and API interactions"""

    def __init__(self):
        self.xml_builder = XMLBuilder()

    def send_sms(self, data):
        """
        Send an SMS using the IOVOX API

        Args:
            data (dict): Dictionary containing all necessary SMS data

        Returns:
            dict: Response data including SMS ID

        Raises:
            Exception: If API request fails or returns an error
        """
        # Determine API URL based on environment
        base_url = "sandboxapi.iovox.com" if data['environment'] == "sandbox" else "api.iovox.com"
        url = f"https://{base_url}:444/SMS?v=3&method=sendSms"

        # Prepare request headers
        headers = {
            'username': data['username'],
            'secureKey': data['secure_key'],
            'Content-Type': 'application/xml'
        }

        # Create XML payload
        payload = self.xml_builder.create_sms_payload(data)

        try:
            # Send request to API
            response = requests.post(url, data=payload, headers=headers)

            # Handle successful response
            if response.status_code == 201:
                tree = ET.fromstring(response.content)
                sms_id = tree.find('sms_activity_id').text
                return {'sms_id': sms_id}

            # Handle error response
            else:
                tree = ET.fromstring(response.content)
                error = tree.find('error').text
                raise Exception(f"API Error: {error}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")