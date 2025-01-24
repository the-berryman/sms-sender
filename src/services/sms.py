# src/services/sms.py
"""
Service class for handling SMS-related operations including API interactions.
"""

import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from ..utils.xml_builder import XMLBuilder
from ..utils.logger import logger  # Import the singleton logger instance


class SMSService:
    def __init__(self):
        self.xml_builder = XMLBuilder()

    def _pretty_print_xml(self, xml_string):
        """Format XML string for better readability in logs"""
        parsed = minidom.parseString(xml_string)
        return parsed.toprettyxml(indent="  ")

    def send_sms(self, data):
        """Send SMS using the IOVOX API"""
        try:
            # Determine API URL based on environment
            base_url = "sandboxapi.iovox.com" if data['environment'] == "sandbox" else "api.iovox.com"
            url = f"https://{base_url}:444/SMS?v=3&method=sendSms"

            # Prepare request headers (mask sensitive data for logging)
            headers = {
                'username': data['username'],
                'secureKey': data['secure_key'],
                'Content-Type': 'application/xml'
            }

            log_headers = headers.copy()
            log_headers['secureKey'] = '***masked***'

            # Create XML payload
            payload = self.xml_builder.create_sms_payload(data)

            # Log the outgoing request
            logger.log_api_interaction(
                'SENT',
                self._pretty_print_xml(payload.decode('utf-8')),
                f"URL: {url}\nHeaders: {log_headers}"
            )

            # Send request to API
            response = requests.post(url, data=payload, headers=headers)

            # Log the response
            response_content = response.content.decode('utf-8') if response.content else "No response content"
            logger.log_api_interaction(
                'RECEIVED',
                self._pretty_print_xml(response_content) if response_content else "No content",
                f"Status Code: {response.status_code}\nHeaders: {dict(response.headers)}"
            )

            # Handle successful response
            if response.status_code == 201:
                tree = ET.fromstring(response.content)
                sms_id = tree.find('sms_activity_id').text
                logger.info(f"SMS sent successfully with ID: {sms_id}")
                return {'sms_id': sms_id}

            # Handle error response
            tree = ET.fromstring(response.content)
            error = tree.find('error').text
            error_message = f"API Error: {error}"
            logger.error(error_message)
            raise Exception(error_message)

        except requests.exceptions.RequestException as e:
            error_message = f"Network error: {str(e)}"
            logger.error(error_message, exc_info=True)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            logger.error(error_message, exc_info=True)
            raise