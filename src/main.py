# src/main.py
"""
Entry point for the SMS Sender application.
This file is responsible for launching the main application window.
"""

import tkinter as tk
from .gui.app import SMSSenderApp

def main():
    """Initialize and start the SMS Sender application"""
    root = tk.Tk()
    app = SMSSenderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()