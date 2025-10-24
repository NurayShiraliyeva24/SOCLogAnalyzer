#!/usr/bin/env python3
"""
Modern Security Analysis GUI Demo
Showcases the new modern design features
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_gui import ModernSecurityGUI, COLORS
    
    def create_demo():
        """Create a demo window showing the modern design"""
        root = tk.Tk()
        root.title("🛡️ Modern Security Dashboard - Demo")
        root.geometry("1000x600")
        root.configure(bg=COLORS['light'])
        
        # Demo header
        header_frame = tk.Frame(root, bg=COLORS['white'], height=100)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🛡️ Modern Security Analysis Dashboard",
                              font=('Segoe UI', 24, 'bold'),
                              fg=COLORS['dark'],
                              bg=COLORS['white'])
        title_label.pack(pady=20)
        
        # Demo features
        features_frame = tk.Frame(root, bg=COLORS['light'])
        features_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Feature cards
        features = [
            ("🎨", "Modern Design", "Clean, contemporary interface with card-based layout"),
            ("🎯", "Smart Analysis", "AI-powered threat detection with concise insights"),
            ("📊", "Visual Data", "Beautiful statistics cards and risk indicators"),
            ("⚡", "Fast Performance", "Optimized for speed and responsiveness")
        ]
        
        for i, (icon, title, desc) in enumerate(features):
            card = tk.Frame(features_frame, bg=COLORS['white'], relief='solid', borderwidth=1)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            # Icon
            icon_label = tk.Label(card, text=icon, font=('Segoe UI', 32), 
                                 bg=COLORS['white'], fg=COLORS['primary'])
            icon_label.pack(pady=(20, 10))
            
            # Title
            title_label = tk.Label(card, text=title, font=('Segoe UI', 14, 'bold'),
                                  bg=COLORS['white'], fg=COLORS['dark'])
            title_label.pack()
            
            # Description
            desc_label = tk.Label(card, text=desc, font=('Segoe UI', 10),
                                 bg=COLORS['white'], fg=COLORS['secondary'],
                                 wraplength=200)
            desc_label.pack(pady=(5, 20))
        
        # Configure grid
        features_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(1, weight=1)
        
        # Launch button
        launch_frame = tk.Frame(root, bg=COLORS['light'])
        launch_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        launch_btn = tk.Button(launch_frame,
                              text="🚀 Launch Security Dashboard",
                              command=lambda: launch_main_app(root),
                              font=('Segoe UI', 12, 'bold'),
                              bg=COLORS['primary'],
                              fg=COLORS['white'],
                              relief='flat',
                              borderwidth=0,
                              padx=30,
                              pady=12,
                              cursor='hand2')
        launch_btn.pack()
        
        # Add hover effect
        def on_enter(e):
            launch_btn.config(bg='#1d4ed8')
        def on_leave(e):
            launch_btn.config(bg=COLORS['primary'])
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
        
        return root
    
    def launch_main_app(demo_root):
        """Launch the main application"""
        demo_root.destroy()
        main_root = tk.Tk()
        app = ModernSecurityGUI(main_root)
        main_root.mainloop()
    
    if __name__ == "__main__":
        print("🎨 Launching Modern Security Dashboard Demo...")
        print("✨ Features:")
        print("   • Modern card-based design")
        print("   • Contemporary color scheme")
        print("   • Smooth hover effects")
        print("   • Professional typography")
        print("   • Responsive layout")
        print("\n🚀 Starting demo...")
        
        root = create_demo()
        root.mainloop()
        
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("📦 Please ensure simple_gui.py is in the same directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting demo: {e}")
    sys.exit(1)
