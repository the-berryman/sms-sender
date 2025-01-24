# src/utils/xml_builder.py
"""
Utility class for building XML payloads for the IOVOX API.
"""

import xml.etree.ElementTree as ET


class XMLBuilder:
    """Handles creation of XML payloads for various API requests"""

    def create_sms_payload(self, data):
        """
        Create XML payload for sending SMS

        Args:
            data (dict): Dictionary containing SMS data

        Returns:
            bytes: UTF-8 encoded XML payload
        """
        # Create root element
        root = ET.Element("request")

        # Add required fields
        ET.SubElement(root, "origin").text = data['origin']
        ET.SubElement(root, "destination").text = data['destination']
        ET.SubElement(root, "message").text = data['message']

        # Add optional fields if provided
        if data.get('callback_url'):
            ET.SubElement(root, "callback_url").text = data['callback_url']

        if data.get('expiry'):
            ET.SubElement(root, "expiry").text = data['expiry']

        # Return XML as UTF-8 encoded bytes
        return ET.tostring(root, encoding='utf-8', xml_declaration=True)