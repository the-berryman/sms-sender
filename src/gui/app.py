# src/gui/app.py
"""
Main GUI application class for the SMS Sender.
Handles all user interface components and interactions.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.services.sms import SMSService
from src.utils.xml_builder import XMLBuilder


class SMSSenderApp:
    def __init__(self, root):
        """Initialize the application window and all its components"""
        self.root = root
        self.root.title("IOVOX SMS Sender")
        self.sms_service = SMSService()

        self._create_main_frame()
        self._create_auth_frame()
        self._create_message_frame()
        self._create_advanced_frame()
        self._create_environment_frame()
        self._create_send_button()

    def _create_main_frame(self):
        """Create and configure the main application frame"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def _create_auth_frame(self):
        """Create the authentication section of the GUI"""
        auth_frame = ttk.LabelFrame(self.main_frame, text="Authentication", padding="5")
        auth_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(auth_frame, width=40)
        self.username_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(auth_frame, text="Secure Key:").grid(row=1, column=0, sticky=tk.W)
        self.key_entry = ttk.Entry(auth_frame, width=40, show="*")
        self.key_entry.grid(row=1, column=1, padx=5, pady=2)

    def _create_message_frame(self):
        """Create the message details section of the GUI"""
        msg_frame = ttk.LabelFrame(self.main_frame, text="Message Details", padding="5")
        msg_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(msg_frame, text="Origin (Sender):").grid(row=0, column=0, sticky=tk.W)
        self.origin_entry = ttk.Entry(msg_frame, width=40)
        self.origin_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(msg_frame, text="Destination:").grid(row=1, column=0, sticky=tk.W)
        self.destination_entry = ttk.Entry(msg_frame, width=40)
        self.destination_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(msg_frame, text="Message:").grid(row=2, column=0, sticky=tk.W)
        self.message_text = tk.Text(msg_frame, width=40, height=4)
        self.message_text.grid(row=2, column=1, padx=5, pady=2)

    def _create_advanced_frame(self):
        """Create the advanced options section of the GUI"""
        adv_frame = ttk.LabelFrame(self.main_frame, text="Advanced Options", padding="5")
        adv_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(adv_frame, text="Callback URL:").grid(row=0, column=0, sticky=tk.W)
        self.callback_entry = ttk.Entry(adv_frame, width=40)
        self.callback_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(adv_frame, text="Expiry (minutes):").grid(row=1, column=0, sticky=tk.W)
        self.expiry_entry = ttk.Entry(adv_frame, width=40)
        self.expiry_entry.grid(row=1, column=1, padx=5, pady=2)

    def _create_environment_frame(self):
        """Create the environment selection section of the GUI"""
        env_frame = ttk.Frame(self.main_frame)
        env_frame.grid(row=3, column=0, columnspan=2, pady=5)

        self.env_var = tk.StringVar(value="sandbox")
        ttk.Radiobutton(env_frame, text="Sandbox", variable=self.env_var,
                        value="sandbox").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(env_frame, text="Production", variable=self.env_var,
                        value="production").grid(row=0, column=1, padx=5)

    def _create_send_button(self):
        """Create the send button and status label"""
        self.send_button = ttk.Button(self.main_frame, text="Send SMS", command=self.send_sms)
        self.send_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=5, column=0, columnspan=2)

    def _get_form_data(self):
        """Collect all form data into a dictionary"""
        return {
            'username': self.username_entry.get(),
            'secure_key': self.key_entry.get(),
            'origin': self.origin_entry.get(),
            'destination': self.destination_entry.get(),
            'message': self.message_text.get("1.0", tk.END).strip(),
            'callback_url': self.callback_entry.get(),
            'expiry': self.expiry_entry.get(),
            'environment': self.env_var.get()
        }

    def send_sms(self):
        """Handle the SMS sending process"""
        try:
            # Get all form data
            data = self._get_form_data()

            # Validate required fields
            if not all([data['username'], data['secure_key'],
                        data['origin'], data['destination'], data['message']]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Validate message length
            if len(data['message']) > 160:
                messagebox.showerror("Error", "Message must be less than 160 characters")
                return

            # Send the SMS
            result = self.sms_service.send_sms(data)

            # Handle success
            self.status_label.config(text=f"SMS sent successfully! ID: {result['sms_id']}")
            messagebox.showinfo("Success", "SMS sent successfully!")

        except Exception as e:
            # Handle any errors
            self.status_label.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")