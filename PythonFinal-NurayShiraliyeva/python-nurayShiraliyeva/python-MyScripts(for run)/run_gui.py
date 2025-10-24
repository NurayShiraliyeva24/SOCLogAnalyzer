#!/usr/bin/env python3
"""
Security Analysis GUI Launcher
A modern Python GUI for security log analysis with AI-powered threat detection
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    from simple_gui import ModernSecurityGUI
    
    print("🛡️  Starting Advanced Security Intelligence Platform...")
    print("📊 Enhanced Features:")
    print("   • Modern sidebar navigation interface")
    print("   • Drag-and-drop file upload")
    print("   • Real-time analysis progress")
    print("   • Comprehensive threat analysis")
    print("   • AI-powered insights with Mistral AI")
    print("   • IP Intelligence & Geolocation")
    print("   • Advanced reporting & analytics")
    print("   • Professional dashboard design")
    print("\n🚀 Launching application...")
    
    # Check for AI mode argument
    ai_mode = any(arg.lower() == "ai" for arg in sys.argv[1:])
    if ai_mode:
        print("🤖 AI Enhanced Mode activated!")
    
    root = tk.Tk()
    app = ModernSecurityGUI(root, ai_mode)
    root.mainloop()
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("📦 Please install required packages:")
    print("   pip install -r requirements_gui.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1)
