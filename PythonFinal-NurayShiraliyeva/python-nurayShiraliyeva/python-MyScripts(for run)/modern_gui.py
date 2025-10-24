#!/usr/bin/env python3
"""
Entry point to launch the Modern Security GUI.
Usage:
  python modern_gui.py [ai]

The optional "ai" argument is accepted for compatibility and may be used by
future versions to toggle AI-related features. It is currently informational.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ensure local imports resolve when launched directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_gui import ModernSecurityGUI  # Import GUI class
except Exception as import_error:
    print(f"❌ Error importing GUI: {import_error}")
    print("📦 Make sure 'simple_gui.py' exists in this directory.")
    sys.exit(1)

def main():
    # Accept optional "ai" argument for AI-related features
    enable_ai_flag = any(arg.lower() == "ai" for arg in sys.argv[1:])
    
    # Display AI mode information if the flag is provided
    if enable_ai_flag:
        print("🤖 AI mode flag detected. Launching GUI with AI features enabled...")
    else:
        print("🔒 Launching GUI in normal mode...")

    # Create the Tkinter root window
    root = tk.Tk()
    root.title("🛡️ Modern Security Dashboard")  # Set the window title
    root.geometry("1200x800")  # Set a fixed window size
    root.configure(bg="#f0f0f0")  # Set background color for window

    # Center the window on the screen
    window_width = 1200
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    try:
        # Create the application (GUI) instance and pass the root window
        _app = ModernSecurityGUI(root, enable_ai_flag)
    except Exception as e:
        print(f"❌ Error initializing GUI: {e}")
        messagebox.showerror("Error", "An error occurred while initializing the GUI.")
        sys.exit(1)

    # Start the Tkinter main loop to display the window
    root.mainloop()

if __name__ == "__main__":
    main()
