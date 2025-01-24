# src/services/sms.py
"""
Service class for handling SMS-related operations including API interactions.
"""

import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ..utils.xml_builder import XMLBuilder
from ..utils.logger import setup_logger, log_api_interaction


class SMSService:
    """Handles all SMS-related operations and API interactions"""

    def __init__(self):
        self.xml_builder = XMLBuilder()
        self.logger = setup_logger()

    def _pretty_print_xml(self, xml_string):
        """Format XML string for better readability in logs"""
        parsed = minidom.parseString(xml_string)
        return parsed.toprettyxml(indent="  ")

    def _log_simple(self, message, level='info'):
        """Log a simple message without detailed formatting"""
        # Add empty details to satisfy the formatter
        getattr(self.logger, level)(message, extra={'details': ''})

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
        try:
            # Determine API URL based on environment
            base_url = "sandboxapi.iovox.com" if data['environment'] == "sandbox" else "api.iovox.com"
            url = f"https://{base_url}:444/SMS?v=3&method=sendSms"

            # Prepare request headers with sensitive information masked
            headers = {
                'username': data['username'],
                'secureKey': '***masked***',  # Mask the secure key in logs
                'Content-Type': 'application/xml'
            }

            # Create XML payload
            payload = self.xml_builder.create_sms_payload(data)

            # Log the outgoing request
            log_api_interaction(
                self.logger,
                'SENT',
                self._pretty_print_xml(payload.decode('utf-8')),
                f"URL: {url}\nHeaders: {headers}"
            )

            # Prepare the actual headers for the request
            request_headers = headers.copy()
            request_headers['secureKey'] = data['secure_key']  # Use actual secure key

            # Send request to API
            response = requests.post(url, data=payload, headers=request_headers)

            # Log the response
            response_content = response.content.decode('utf-8') if response.content else "No response content"
            log_api_interaction(
                self.logger,
                'RECEIVED',
                self._pretty_print_xml(response_content) if response_content else "No content",
                f"Status Code: {response.status_code}\nHeaders: {dict(response.headers)}"
            )

            # Handle successful response
            if response.status_code == 201:
                tree = ET.fromstring(response.content)
                sms_id = tree.find('sms_activity_id').text
                self._log_simple(f"SMS sent successfully with ID: {sms_id}")
                return {'sms_id': sms_id}

            # Handle error response
            else:
                tree = ET.fromstring(response.content)
                error = tree.find('error').text
                error_message = f"API Error: {error}"
                self._log_simple(error_message, 'error')
                raise Exception(error_message)

        except requests.exceptions.RequestException as e:
            error_message = f"Network error: {str(e)}"
            self._log_simple(error_message, 'error')
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            self._log_simple(error_message, 'error')
            raise