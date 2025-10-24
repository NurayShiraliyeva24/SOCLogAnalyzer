#!/usr/bin/env python3
"""
Streamlit Security Intelligence Platform Launcher
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application"""
    
    print("🛡️  Starting Advanced Security Intelligence Platform...")
    print("📊 Enhanced Features:")
    print("   • Modern web-based interface")
    print("   • Interactive dashboards and visualizations")
    print("   • Real-time file upload and analysis")
    print("   • AI-powered threat detection")
    print("   • IP Intelligence & Geolocation")
    print("   • Advanced reporting & analytics")
    print("   • Professional web design")
    print("\n🚀 Launching Streamlit application...")
    print("📱 The application will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("\n" + "="*60)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        print("📦 Please install required packages:")
        print("   pip install -r requirements_streamlit.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()

