import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
import time
from datetime import datetime, timedelta
from main import (
    parse_log_file, get_cti_data, analyze_stats, 
    analyze_user_agents, ai_note, advanced_ai_analysis
)

# Enhanced Modern Color Scheme
COLORS = {
    'primary': '#3b82f6',      # Modern Blue
    'primary_dark': '#1e40af', # Dark Blue
    'secondary': '#64748b',    # Slate
    'secondary_dark': '#334155', # Dark Slate
    'success': '#10b981',      # Emerald
    'success_dark': '#059669', # Dark Emerald
    'warning': '#f59e0b',      # Amber
    'warning_dark': '#d97706', # Dark Amber
    'danger': '#ef4444',       # Red
    'danger_dark': '#dc2626',  # Dark Red
    'info': '#06b6d4',         # Cyan
    'info_dark': '#0891b2',    # Dark Cyan
    'dark': '#0f172a',         # Very Dark
    'dark_secondary': '#1e293b', # Dark Secondary
    'light': '#f1f5f9',        # Light Gray
    'light_secondary': '#e2e8f0', # Light Secondary
    'white': '#ffffff',
    'border': '#cbd5e1',       # Border
    'text_primary': '#0f172a', # Primary Text
    'text_secondary': '#64748b', # Secondary Text
    'background': '#f8fafc',   # Background
    'card_background': '#ffffff', # Card Background
    'hover': '#f1f5f9',        # Hover State
    'gradient_start': '#3b82f6', # Gradient Start
    'gradient_end': '#1e40af'   # Gradient End
}

class ModernSecurityGUI:
    def __init__(self, root, ai_mode=False):
        self.root = root
        self.ai_mode = ai_mode
        self.root.title("🛡️ Advanced Security Intelligence Platform" + (" - AI Enhanced" if ai_mode else ""))
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['background'])
        self.root.minsize(1200, 800)
        
        # Enhanced variables
        self.log_file_path = tk.StringVar()
        self.analysis_data = None
        self.current_tab = tk.StringVar(value="dashboard")
        self.notifications = []
        self.real_time_mode = False
        
        # Configure enhanced modern styling
        self.setup_enhanced_modern_style()
        
        # Create main interface with new layout
        self.create_enhanced_layout()
        
        # Initialize real-time monitoring if AI mode
        if self.ai_mode:
            self.initialize_ai_features()
        
    def setup_enhanced_modern_style(self):
        """Setup enhanced modern ttk styles with advanced theming"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Enhanced button styles
        style.configure('Primary.TButton',
                       background=COLORS['primary'],
                       foreground=COLORS['white'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat')
        style.map('Primary.TButton',
                 background=[('active', COLORS['primary_dark']),
                           ('pressed', COLORS['primary_dark'])])
        
        style.configure('Secondary.TButton',
                       background=COLORS['secondary'],
                       foreground=COLORS['white'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Secondary.TButton',
                 background=[('active', COLORS['secondary_dark']),
                           ('pressed', COLORS['secondary_dark'])])
        
        style.configure('Success.TButton',
                       background=COLORS['success'],
                       foreground=COLORS['white'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Success.TButton',
                 background=[('active', COLORS['success_dark']),
                           ('pressed', COLORS['success_dark'])])
        
        style.configure('Danger.TButton',
                       background=COLORS['danger'],
                       foreground=COLORS['white'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Danger.TButton',
                 background=[('active', COLORS['danger_dark']),
                           ('pressed', COLORS['danger_dark'])])
        
        # Enhanced frame styles
        style.configure('Card.TFrame',
                       background=COLORS['card_background'],
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Sidebar.TFrame',
                       background=COLORS['dark_secondary'],
                       borderwidth=0)
        
        style.configure('Header.TFrame',
                       background=COLORS['white'],
                       borderwidth=0)
        
        # Enhanced label frame styles
        style.configure('Modern.TLabelframe',
                       background=COLORS['card_background'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=COLORS['border'])
        style.configure('Modern.TLabelframe.Label',
                       background=COLORS['card_background'],
                       foreground=COLORS['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        # Enhanced notebook styles
        style.configure('Modern.TNotebook',
                       background=COLORS['background'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=COLORS['light_secondary'],
                       foreground=COLORS['text_primary'],
                       padding=(25, 12),
                       font=('Segoe UI', 11, 'bold'))
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', COLORS['card_background']),
                           ('active', COLORS['hover'])])
        
        # Enhanced progress bar styles
        style.configure('Primary.Horizontal.TProgressbar',
                       background=COLORS['primary'],
                       troughcolor=COLORS['light_secondary'],
                       borderwidth=0,
                       lightcolor=COLORS['primary'],
                       darkcolor=COLORS['primary'])
        
        style.configure('Success.Horizontal.TProgressbar',
                       background=COLORS['success'],
                       troughcolor=COLORS['light_secondary'],
                       borderwidth=0,
                       lightcolor=COLORS['success'],
                       darkcolor=COLORS['success'])
        
        style.configure('Danger.Horizontal.TProgressbar',
                       background=COLORS['danger'],
                       troughcolor=COLORS['light_secondary'],
                       borderwidth=0,
                       lightcolor=COLORS['danger'],
                       darkcolor=COLORS['danger'])
        
        # Enhanced entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=COLORS['card_background'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=COLORS['border'],
                       font=('Segoe UI', 10))
        
        # Enhanced combobox styles
        style.configure('Modern.TCombobox',
                       fieldbackground=COLORS['card_background'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=COLORS['border'],
                       font=('Segoe UI', 10))
        
    def create_enhanced_layout(self):
        """Create the enhanced modern layout with sidebar navigation"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=COLORS['background'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar navigation
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Create notification system
        self.create_notification_system()
    
    def create_sidebar(self):
        """Create modern sidebar navigation"""
        self.sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        self.sidebar.pack_propagate(False)
        
        # Sidebar header
        sidebar_header = tk.Frame(self.sidebar, bg=COLORS['dark_secondary'], height=80)
        sidebar_header.pack(fill=tk.X, padx=0, pady=0)
        sidebar_header.pack_propagate(False)
        
        # Logo and title
        logo_frame = tk.Frame(sidebar_header, bg=COLORS['dark_secondary'])
        logo_frame.pack(expand=True, fill=tk.BOTH)
        
        logo_label = tk.Label(logo_frame, 
                             text="🛡️",
                             font=('Segoe UI', 24),
                             bg=COLORS['dark_secondary'],
                             fg=COLORS['white'])
        logo_label.pack(pady=(15, 5))
        
        title_label = tk.Label(logo_frame,
                              text="Security Intel",
                              font=('Segoe UI', 14, 'bold'),
                              bg=COLORS['dark_secondary'],
                              fg=COLORS['white'])
        title_label.pack()
        
        # Navigation menu
        nav_frame = tk.Frame(self.sidebar, bg=COLORS['dark_secondary'])
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Navigation items
        nav_items = [
            ("📊", "Dashboard", "dashboard"),
            ("📁", "File Upload", "upload"),
            ("🔍", "Analysis", "analysis"),
            ("🌐", "IP Intelligence", "ip_intel"),
            ("🤖", "AI Insights", "ai_insights"),
            ("📈", "Reports", "reports"),
            ("⚙️", "Settings", "settings")
        ]
        
        self.nav_buttons = {}
        for icon, text, command in nav_items:
            btn = tk.Button(nav_frame,
                           text=f"{icon} {text}",
                           command=lambda cmd=command: self.switch_tab(cmd),
                           font=('Segoe UI', 11),
                           bg=COLORS['dark_secondary'],
                           fg=COLORS['white'],
                           relief='flat',
                           anchor='w',
                           padx=15,
                           pady=12,
                           cursor='hand2')
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons[command] = btn
            
            # Add hover effect
            self.add_sidebar_hover_effect(btn)
        
        # AI mode indicator
        if self.ai_mode:
            ai_frame = tk.Frame(self.sidebar, bg=COLORS['primary'], height=50)
            ai_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 20))
            ai_frame.pack_propagate(False)
            
            ai_label = tk.Label(ai_frame,
                               text="🤖 AI Enhanced Mode",
                               font=('Segoe UI', 10, 'bold'),
                               bg=COLORS['primary'],
                               fg=COLORS['white'])
            ai_label.pack(expand=True)
    
    def create_main_content(self):
        """Create main content area with tabbed interface"""
        self.content_frame = tk.Frame(self.main_container, bg=COLORS['background'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Header bar
        self.create_header_bar()
        
        # Main content area
        self.main_content = tk.Frame(self.content_frame, bg=COLORS['background'])
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tab content
        self.create_tab_content()
    
    def create_header_bar(self):
        """Create modern header bar"""
        header = ttk.Frame(self.content_frame, style='Header.TFrame', height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Left side - breadcrumbs and title
        left_frame = tk.Frame(header, bg=COLORS['white'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=15)
        
        # Breadcrumb
        breadcrumb_label = tk.Label(left_frame,
                                   text="Dashboard > Security Analysis",
                                   font=('Segoe UI', 10),
                                   bg=COLORS['white'],
                                   fg=COLORS['text_secondary'])
        breadcrumb_label.pack(anchor=tk.W)
        
        # Page title
        self.page_title = tk.Label(left_frame,
                                  text="Security Analysis Dashboard",
                                  font=('Segoe UI', 18, 'bold'),
                                  bg=COLORS['white'],
                                  fg=COLORS['text_primary'])
        self.page_title.pack(anchor=tk.W, pady=(5, 0))
        
        # Right side - actions and status
        right_frame = tk.Frame(header, bg=COLORS['white'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=15)
        
        # Status indicator
        self.status_frame = tk.Frame(right_frame, bg=COLORS['white'])
        self.status_frame.pack(side=tk.RIGHT, padx=(0, 20))
        
        self.status_indicator = tk.Label(self.status_frame,
                                        text="● Ready",
                                        font=('Segoe UI', 10),
                                        bg=COLORS['white'],
                                        fg=COLORS['success'])
        self.status_indicator.pack()
        
        # Quick actions
        actions_frame = tk.Frame(right_frame, bg=COLORS['white'])
        actions_frame.pack(side=tk.RIGHT)
        
        refresh_btn = tk.Button(actions_frame,
                               text="🔄 Refresh",
                               command=self.refresh_data,
                               font=('Segoe UI', 10),
                               bg=COLORS['light_secondary'],
                               fg=COLORS['text_primary'],
                               relief='flat',
                               padx=15,
                               pady=8,
                               cursor='hand2')
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = tk.Button(actions_frame,
                              text="📄 Export",
                              command=self.quick_export,
                              font=('Segoe UI', 10),
                              bg=COLORS['primary'],
                              fg=COLORS['white'],
                              relief='flat',
                              padx=15,
                              pady=8,
                              cursor='hand2')
        export_btn.pack(side=tk.LEFT)
    
    def create_tab_content(self):
        """Create tabbed content areas"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_content, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tab frames
        self.tab_frames = {}
        
        # Dashboard tab
        self.tab_frames['dashboard'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['dashboard'], text="📊 Dashboard")
        self.create_dashboard_tab()
        
        # Upload tab
        self.tab_frames['upload'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['upload'], text="📁 Upload")
        self.create_upload_tab()
        
        # Analysis tab
        self.tab_frames['analysis'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['analysis'], text="🔍 Analysis")
        self.create_analysis_tab()
        
        # IP Intelligence tab
        self.tab_frames['ip_intel'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['ip_intel'], text="🌐 IP Intel")
        self.create_ip_intel_tab()
        
        # AI Insights tab
        self.tab_frames['ai_insights'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['ai_insights'], text="🤖 AI Insights")
        self.create_ai_insights_tab()
        
        # Reports tab
        self.tab_frames['reports'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['reports'], text="📈 Reports")
        self.create_reports_tab()
        
        # Settings tab
        self.tab_frames['settings'] = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(self.tab_frames['settings'], text="⚙️ Settings")
        self.create_settings_tab()
    
    def create_notification_system(self):
        """Create notification system"""
        self.notification_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.notification_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)
    
    def switch_tab(self, tab_name):
        """Switch to specified tab"""
        self.current_tab.set(tab_name)
        
        # Update navigation button states
        for name, btn in self.nav_buttons.items():
            if name == tab_name:
                btn.config(bg=COLORS['primary'], fg=COLORS['white'])
            else:
                btn.config(bg=COLORS['dark_secondary'], fg=COLORS['white'])
        
        # Update page title
        titles = {
            'dashboard': 'Security Analysis Dashboard',
            'upload': 'File Upload & Configuration',
            'analysis': 'Threat Analysis & Detection',
            'ip_intel': 'IP Intelligence & Geolocation',
            'ai_insights': 'AI-Powered Security Insights',
            'reports': 'Reports & Analytics',
            'settings': 'System Settings & Configuration'
        }
        self.page_title.config(text=titles.get(tab_name, 'Security Analysis'))
        
        # Switch notebook tab
        tab_index = list(self.tab_frames.keys()).index(tab_name)
        self.notebook.select(tab_index)
    
    def add_sidebar_hover_effect(self, widget):
        """Add hover effect to sidebar buttons"""
        def on_enter(e):
            if widget.cget('bg') != COLORS['primary']:
                widget.config(bg=COLORS['hover'])
        def on_leave(e):
            if widget.cget('bg') != COLORS['primary']:
                widget.config(bg=COLORS['dark_secondary'])
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        # Dashboard content will be populated when analysis is complete
        dashboard_frame = tk.Frame(self.tab_frames['dashboard'], bg=COLORS['card_background'])
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(dashboard_frame,
                                text="🛡️ Welcome to Advanced Security Intelligence Platform",
                              font=('Segoe UI', 24, 'bold'),
                                bg=COLORS['card_background'],
                                fg=COLORS['text_primary'])
        welcome_label.pack(pady=(50, 20))
        
        # Instructions
        instructions = tk.Label(dashboard_frame,
                               text="Upload a log file to begin security analysis and threat detection",
                               font=('Segoe UI', 14),
                               bg=COLORS['card_background'],
                               fg=COLORS['text_secondary'])
        instructions.pack(pady=(0, 50))
        
        # Quick start button
        quick_start_btn = tk.Button(dashboard_frame,
                                   text="🚀 Start Analysis",
                                   command=lambda: self.switch_tab('upload'),
                                   font=('Segoe UI', 14, 'bold'),
                                   bg=COLORS['primary'],
                                   fg=COLORS['white'],
                                   relief='flat',
                                   padx=30,
                                   pady=15,
                                   cursor='hand2')
        quick_start_btn.pack()
    
    def create_upload_tab(self):
        """Create the file upload tab with drag-and-drop interface"""
        upload_frame = tk.Frame(self.tab_frames['upload'], bg=COLORS['card_background'])
        upload_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Upload section
        upload_section = ttk.LabelFrame(upload_frame, text="📁 File Upload", 
                                       style='Modern.TLabelframe', padding="30")
        upload_section.pack(fill=tk.X, pady=(0, 20))
        
        # Drag and drop area
        drop_frame = tk.Frame(upload_section, bg=COLORS['light_secondary'], 
                             relief='solid', borderwidth=2, height=200)
        drop_frame.pack(fill=tk.X, pady=(0, 20))
        drop_frame.pack_propagate(False)
        
        # Drop area content
        drop_content = tk.Frame(drop_frame, bg=COLORS['light_secondary'])
        drop_content.pack(expand=True, fill=tk.BOTH)
        
        drop_icon = tk.Label(drop_content, text="📁", font=('Segoe UI', 48),
                            bg=COLORS['light_secondary'], fg=COLORS['text_secondary'])
        drop_icon.pack(pady=(20, 10))
        
        drop_text = tk.Label(drop_content,
                            text="Drag and drop your log file here\nor click to browse",
                            font=('Segoe UI', 14),
                            bg=COLORS['light_secondary'],
                            fg=COLORS['text_secondary'])
        drop_text.pack()
        
        # File input
        file_input_frame = tk.Frame(upload_section, bg=COLORS['card_background'])
        file_input_frame.pack(fill=tk.X, pady=(0, 20))
        
        file_label = tk.Label(file_input_frame, text="Selected File:",
                             font=('Segoe UI', 12, 'bold'),
                             bg=COLORS['card_background'],
                             fg=COLORS['text_primary'])
        file_label.pack(anchor=tk.W, pady=(0, 10))
        
        file_entry_frame = tk.Frame(file_input_frame, bg=COLORS['card_background'])
        file_entry_frame.pack(fill=tk.X)
        
        self.file_entry = ttk.Entry(file_entry_frame, textvariable=self.log_file_path,
                                   style='Modern.TEntry', font=('Segoe UI', 11))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        browse_btn = ttk.Button(file_entry_frame, text="📁 Browse",
                               command=self.browse_file, style='Secondary.TButton')
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.analyze_btn = ttk.Button(file_entry_frame, text="🔍 Analyze",
                                     command=self.start_analysis, style='Primary.TButton')
        self.analyze_btn.pack(side=tk.LEFT)
        
        # Analysis options
        options_section = ttk.LabelFrame(upload_frame, text="⚙️ Analysis Options", 
                                        style='Modern.TLabelframe', padding="20")
        options_section.pack(fill=tk.X, pady=(0, 20))
        
        options_frame = tk.Frame(options_section, bg=COLORS['card_background'])
        options_frame.pack(fill=tk.X)
        
        # Real-time monitoring option
        self.real_time_var = tk.BooleanVar()
        real_time_check = tk.Checkbutton(options_frame,
                                        text="Enable Real-time Monitoring",
                                        variable=self.real_time_var,
                                        font=('Segoe UI', 11),
                                        bg=COLORS['card_background'],
                                        fg=COLORS['text_primary'])
        real_time_check.pack(anchor=tk.W, pady=5)
        
        # Deep analysis option
        self.deep_analysis_var = tk.BooleanVar(value=True)
        deep_analysis_check = tk.Checkbutton(options_frame,
                                            text="Enable Deep Analysis (AI Enhanced)",
                                            variable=self.deep_analysis_var,
                                            font=('Segoe UI', 11),
                                            bg=COLORS['card_background'],
                                            fg=COLORS['text_primary'])
        deep_analysis_check.pack(anchor=tk.W, pady=5)
        
        # Progress section
        self.progress_section = ttk.LabelFrame(upload_frame, text="⏳ Analysis Progress", 
                                              style='Modern.TLabelframe', padding="20")
        self.progress_section.pack(fill=tk.X)
        self.progress_section.pack_forget()  # Initially hidden
        
        # Progress bar
        self.progress = ttk.Progressbar(self.progress_section, 
                                      mode='indeterminate',
                                      style='Primary.Horizontal.TProgressbar')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(self.progress_section,
                                    text="Ready to analyze...",
                                    font=('Segoe UI', 11),
                                    bg=COLORS['card_background'],
                                    fg=COLORS['text_secondary'])
        self.status_label.pack(anchor=tk.W)
    
    def create_analysis_tab(self):
        """Create the analysis results tab"""
        analysis_frame = tk.Frame(self.tab_frames['analysis'], bg=COLORS['card_background'])
        analysis_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Analysis content will be populated after analysis
        self.analysis_content = tk.Frame(analysis_frame, bg=COLORS['card_background'])
        self.analysis_content.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder
        placeholder = tk.Label(self.analysis_content,
                              text="Analysis results will appear here after processing",
                              font=('Segoe UI', 16),
                              bg=COLORS['card_background'],
                              fg=COLORS['text_secondary'])
        placeholder.pack(expand=True)
    
    def create_ip_intel_tab(self):
        """Create the IP intelligence tab"""
        ip_frame = tk.Frame(self.tab_frames['ip_intel'], bg=COLORS['card_background'])
        ip_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # IP intelligence content
        self.ip_intel_content = tk.Frame(ip_frame, bg=COLORS['card_background'])
        self.ip_intel_content.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder
        placeholder = tk.Label(self.ip_intel_content,
                              text="IP Intelligence data will appear here",
                              font=('Segoe UI', 16),
                              bg=COLORS['card_background'],
                              fg=COLORS['text_secondary'])
        placeholder.pack(expand=True)
    
    def create_ai_insights_tab(self):
        """Create the AI insights tab"""
        ai_frame = tk.Frame(self.tab_frames['ai_insights'], bg=COLORS['card_background'])
        ai_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # AI insights content
        self.ai_insights_content = tk.Frame(ai_frame, bg=COLORS['card_background'])
        self.ai_insights_content.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder
        placeholder = tk.Label(self.ai_insights_content,
                              text="AI-powered insights will appear here",
                              font=('Segoe UI', 16),
                              bg=COLORS['card_background'],
                              fg=COLORS['text_secondary'])
        placeholder.pack(expand=True)
    
    def create_reports_tab(self):
        """Create the reports tab"""
        reports_frame = tk.Frame(self.tab_frames['reports'], bg=COLORS['card_background'])
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Reports content
        self.reports_content = tk.Frame(reports_frame, bg=COLORS['card_background'])
        self.reports_content.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder
        placeholder = tk.Label(self.reports_content,
                              text="Reports and analytics will appear here",
                              font=('Segoe UI', 16),
                              bg=COLORS['card_background'],
                              fg=COLORS['text_secondary'])
        placeholder.pack(expand=True)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = tk.Frame(self.tab_frames['settings'], bg=COLORS['card_background'])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Settings content
        self.settings_content = tk.Frame(settings_frame, bg=COLORS['card_background'])
        self.settings_content.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder
        placeholder = tk.Label(self.settings_content,
                              text="System settings and configuration options",
                              font=('Segoe UI', 16),
                              bg=COLORS['card_background'],
                              fg=COLORS['text_secondary'])
        placeholder.pack(expand=True)
    
    def initialize_ai_features(self):
        """Initialize AI-specific features"""
        # This will be expanded with AI-specific functionality
        pass
    
    def refresh_data(self):
        """Refresh data and update display"""
        # Implementation for data refresh
        pass
    
    def quick_export(self):
        """Quick export functionality"""
        # Implementation for quick export
        pass
    
    def browse_file(self):
        """Open file dialog to select log file"""
        file_path = filedialog.askopenfilename(
            title="Select Log File",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.log_file_path.set(file_path)
    
    def start_analysis(self):
        """Start the analysis process"""
        if not self.log_file_path.get():
            messagebox.showerror("Error", "Please select a log file first!")
            return
            
        if not os.path.exists(self.log_file_path.get()):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
        
        # Disable analyze button and show progress
        self.analyze_btn.config(state='disabled')
        self.progress_section.pack(fill=tk.X, pady=(20, 0))
        self.progress.start()
        self.status_label.config(text="Starting analysis...")
        
        # Start analysis in separate thread
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()
    
    def perform_analysis(self):
        """Perform the security analysis"""
        try:
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Parsing log file..."))
            
            # Parse logs
            logs = parse_log_file(self.log_file_path.get())
            unique_ips = set(l["ip"] for l in logs if l["ip"] != "-")
            
            self.root.after(0, lambda: self.status_label.config(text="Performing CTI lookups..."))
            
            # High-Risk IP Detection
            high_risk_ips = []
            ip_cti_mapping = {}
            for ip in unique_ips:
                cti = get_cti_data(ip)
                ip_cti_mapping[ip] = cti
                if (cti['abuse_score'] and cti['abuse_score'] > 50) or cti['web_reputation'] in ['Untrusted', 'Questionable']:
                    high_risk_ips.append(ip)
            
            self.root.after(0, lambda: self.status_label.config(text="Analyzing statistics..."))
            
            # Analysis
            stats, overall = analyze_stats(logs, high_risk_ips)
            ua_stats = analyze_user_agents(logs, high_risk_ips)
            
            self.root.after(0, lambda: self.status_label.config(text="Generating AI analysis..."))
            
            # Prepare final data
            final_data = {"ips": {}, "overall": {}, "advanced_ai": ""}
            
            for ip in high_risk_ips:
                cti = ip_cti_mapping[ip]
                final_data["ips"][ip] = {
                    "cti": cti,
                    "stats": stats[ip],
                    "ai_note": ai_note(ip, cti, stats[ip]),
                    "user_agents": ua_stats[ip]
                }
            
            final_data["overall"] = overall
            final_data["advanced_ai"] = advanced_ai_analysis(overall, high_risk_ips)
            
            # Store analysis data
            self.analysis_data = {
                'data': final_data,
                'summary': {
                    'total_logs': len(logs),
                    'unique_ips': len(unique_ips),
                    'high_risk_ips': len(high_risk_ips),
                    'high_risk_list': high_risk_ips
                }
            }
            
            # Update UI on main thread
            self.root.after(0, self.analysis_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Analysis failed: {str(e)}"))
    
    def analysis_complete(self):
        """Handle analysis completion"""
        # Hide progress and re-enable button
        self.progress.stop()
        self.progress_section.pack_forget()
        self.analyze_btn.config(state='normal')
        
        # Update status
        self.status_indicator.config(text="● Analysis Complete", fg=COLORS['success'])
        
        # Switch to analysis tab
        self.switch_tab('analysis')
        
        # Populate analysis results
        self.populate_analysis_results()
    
    def populate_analysis_results(self):
        """Populate the analysis results in the analysis tab"""
        # Clear existing content
        for widget in self.analysis_content.winfo_children():
            widget.destroy()
        
        # Create analysis results display
        if self.analysis_data:
            summary = self.analysis_data['summary']
            data = self.analysis_data['data']
            
            # Create results header
            header_frame = tk.Frame(self.analysis_content, bg=COLORS['card_background'])
            header_frame.pack(fill=tk.X, padx=20, pady=20)
            
            title_label = tk.Label(header_frame,
                                  text=f"🔍 Analysis Complete - {summary['high_risk_ips']} High-Risk IPs Found",
                                  font=('Segoe UI', 18, 'bold'),
                                  bg=COLORS['card_background'],
                                  fg=COLORS['text_primary'])
            title_label.pack(anchor=tk.W)
            
            # Create summary cards
            cards_frame = tk.Frame(self.analysis_content, bg=COLORS['card_background'])
            cards_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            # Summary statistics
            stats_data = [
                ("📄", "Total Log Entries", summary['total_logs'], COLORS['primary']),
                ("🌐", "Unique IPs", summary['unique_ips'], COLORS['secondary']),
                ("⚠️", "High-Risk IPs", summary['high_risk_ips'], COLORS['danger']),
                ("📈", "Total Requests", data['overall']['total_requests'], COLORS['success'])
            ]
            
            for i, (icon, label, value, color) in enumerate(stats_data):
                card = self.create_simple_stat_card(cards_frame, icon, label, value, color)
                card.grid(row=0, column=i, padx=10, sticky='ew')
            
            # Configure grid weights
            for i in range(len(stats_data)):
                cards_frame.columnconfigure(i, weight=1)
            
            # High-risk IPs list
            if summary['high_risk_list']:
                risk_frame = tk.Frame(self.analysis_content, bg=COLORS['card_background'])
                risk_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
                
                risk_header = tk.Label(risk_frame,
                                      text="🚨 High-Risk IP Addresses",
                                      font=('Segoe UI', 14, 'bold'),
                                      bg=COLORS['card_background'],
                                      fg=COLORS['text_primary'])
                risk_header.pack(anchor=tk.W, pady=(0, 15))
                
                # Create scrollable list
                canvas = tk.Canvas(risk_frame, bg=COLORS['light_secondary'], highlightthickness=0)
                scrollbar = ttk.Scrollbar(risk_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=COLORS['light_secondary'])
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Add IP cards
                for ip in summary['high_risk_list']:
                    ip_data = data['ips'][ip]
                    risk_level = "HIGH" if ip_data['cti']['abuse_score'] >= 75 else "MEDIUM"
                    risk_color = COLORS['danger'] if risk_level == "HIGH" else COLORS['warning']
                    
                    ip_card = self.create_simple_ip_card(scrollable_frame, ip, risk_level, 
                                                        ip_data['cti']['abuse_score'], risk_color)
                    ip_card.pack(fill=tk.X, pady=(0, 8))
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
    
    def create_simple_stat_card(self, parent, icon, label, value, color):
        """Create a simple statistics card"""
        card = tk.Frame(parent, bg=COLORS['card_background'], relief='solid', borderwidth=1, padx=15, pady=15)
        
        # Icon
        icon_label = tk.Label(card, text=icon, font=('Segoe UI', 20), 
                             bg=COLORS['card_background'], fg=color)
        icon_label.pack(pady=(0, 8))
        
        # Value
        value_label = tk.Label(card, text=str(value), font=('Segoe UI', 16, 'bold'),
                              bg=COLORS['card_background'], fg=COLORS['text_primary'])
        value_label.pack()
        
        # Label
        label_label = tk.Label(card, text=label, font=('Segoe UI', 10),
                              bg=COLORS['card_background'], fg=COLORS['text_secondary'])
        label_label.pack(pady=(5, 0))
        
        return card
    
    def create_simple_ip_card(self, parent, ip, risk_level, score, color):
        """Create a simple IP card"""
        card = tk.Frame(parent, bg=COLORS['card_background'], relief='solid', borderwidth=1, padx=15, pady=12)
        
        # Header with IP and risk level
        header_frame = tk.Frame(card, bg=COLORS['card_background'])
        header_frame.pack(fill=tk.X)
        
        ip_label = tk.Label(header_frame, text=f"🌐 {ip}", 
                           font=('Segoe UI', 12, 'bold'),
                           bg=COLORS['card_background'], fg=COLORS['text_primary'])
        ip_label.pack(side=tk.LEFT)
        
        risk_badge = tk.Label(header_frame, text=risk_level,
                             font=('Segoe UI', 9, 'bold'),
                             bg=color, fg=COLORS['white'],
                             padx=8, pady=2)
        risk_badge.pack(side=tk.RIGHT)
        
        # Score
        score_label = tk.Label(card, text=f"Abuse Score: {score}",
                              font=('Segoe UI', 10),
                              bg=COLORS['card_background'], fg=COLORS['text_secondary'])
        score_label.pack(anchor=tk.W, pady=(8, 0))
        
        return card
    
    def show_error(self, message):
        """Show error message"""
        self.progress.stop()
        self.progress_section.pack_forget()
        self.analyze_btn.config(state='normal')
        self.status_indicator.config(text="● Error", fg=COLORS['danger'])
        messagebox.showerror("Error", message)
        
    def create_file_section(self, parent):
        """Create modern file selection section"""
        file_frame = ttk.LabelFrame(parent, text="📁 Upload Log File", 
                                   style='Modern.TLabelframe', padding="25")
        file_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Modern file input area
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X)
        
        # File path label
        file_label = tk.Label(input_frame, text="Select Log File:", 
                             font=('Segoe UI', 10, 'bold'),
                             fg=COLORS['dark'],
                             bg=COLORS['white'])
        file_label.pack(anchor=tk.W, pady=(0, 8))
        
        # File input row
        file_row = ttk.Frame(input_frame)
        file_row.pack(fill=tk.X)
        
        # Modern entry with placeholder
        self.file_entry = tk.Entry(file_row, 
                                  textvariable=self.log_file_path,
                                  font=('Segoe UI', 10),
                                  relief='solid',
                                  borderwidth=1,
                                  bg=COLORS['white'],
                                  fg=COLORS['dark'],
                                  insertbackground=COLORS['primary'])
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Modern buttons
        browse_btn = tk.Button(file_row, 
                              text="📁 Browse",
                              command=self.browse_file,
                              font=('Segoe UI', 10, 'bold'),
                              bg=COLORS['secondary'],
                              fg=COLORS['white'],
                              relief='flat',
                              borderwidth=0,
                              padx=20,
                              pady=8,
                              cursor='hand2')
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.analyze_btn = tk.Button(file_row, 
                                    text="🔍 Analyze",
                                    command=self.start_analysis,
                                    font=('Segoe UI', 10, 'bold'),
                                    bg=COLORS['primary'],
                                    fg=COLORS['white'],
                                    relief='flat',
                                    borderwidth=0,
                                    padx=25,
                                    pady=8,
                                    cursor='hand2')
        self.analyze_btn.pack(side=tk.LEFT)
        
        # Add hover effects
        self.add_hover_effect(browse_btn, COLORS['secondary'], '#475569')
        self.add_hover_effect(self.analyze_btn, COLORS['primary'], '#1d4ed8')
        
    def add_hover_effect(self, widget, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            widget.config(bg=hover_color)
        def on_leave(e):
            widget.config(bg=normal_color)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
    def create_progress_section(self, parent):
        """Create modern progress section"""
        self.progress_frame = ttk.LabelFrame(parent, text="⏳ Analysis Progress", 
                                           style='Modern.TLabelframe', padding="25")
        self.progress_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Progress container
        progress_container = ttk.Frame(self.progress_frame)
        progress_container.pack(fill=tk.X)
        
        # Modern progress bar
        self.progress = ttk.Progressbar(progress_container, 
                                      mode='indeterminate',
                                      style='Modern.Horizontal.TProgressbar')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # Status label with modern styling
        self.status_label = tk.Label(progress_container, 
                                    text="Ready to analyze log files...",
                                    font=('Segoe UI', 10),
                                    fg=COLORS['secondary'],
                                    bg=COLORS['white'])
        self.status_label.pack(anchor=tk.W)
        
        # Initially hide progress
        self.progress_frame.pack_forget()
        
    def create_results_section(self, parent):
        """Create modern results display section"""
        self.results_frame = ttk.LabelFrame(parent, text="📊 Analysis Results", 
                                          style='Modern.TLabelframe', padding="25")
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern results header
        header_frame = ttk.Frame(self.results_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Results title with modern styling
        self.results_title = tk.Label(header_frame, 
                                     text="No analysis performed yet", 
                                     font=('Segoe UI', 14, 'bold'),
                                     fg=COLORS['dark'],
                                     bg=COLORS['white'])
        self.results_title.pack(side=tk.LEFT)
        
        # Modern export button
        self.export_btn = tk.Button(header_frame, 
                                   text="📄 Export Report",
                                   command=self.export_report,
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=COLORS['success'],
                                   fg=COLORS['white'],
                                   relief='flat',
                                   borderwidth=0,
                                   padx=20,
                                   pady=8,
                                   cursor='hand2')
        self.export_btn.pack(side=tk.RIGHT)
        self.export_btn.pack_forget()  # Initially hidden
        self.add_hover_effect(self.export_btn, COLORS['success'], '#059669')
        
        # Modern notebook for tabs
        self.notebook = ttk.Notebook(self.results_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.summary_frame, text="📈 Summary")
        
        # IP Analysis tab
        self.ip_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.ip_frame, text="🌐 IP Analysis")
        
        # AI Analysis tab
        self.ai_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.ai_frame, text="🤖 AI Analysis")
        
        # Initially hide results
        self.results_frame.pack_forget()
        
    def browse_file(self):
        """Open file dialog to select log file"""
        file_path = filedialog.askopenfilename(
            title="Select Log File",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.log_file_path.set(file_path)
            
    def start_analysis(self):
        """Start the analysis in a separate thread"""
        if not self.log_file_path.get():
            messagebox.showerror("Error", "Please select a log file first!")
            return
            
        if not os.path.exists(self.log_file_path.get()):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
            
        # Disable analyze button and show progress
        self.analyze_btn.config(state='disabled')
        self.progress_section.pack(fill=tk.X, pady=(20, 0))
        self.progress.start()
        self.status_label.config(text="Starting analysis...")
        
        # Start analysis in separate thread
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()
        
    def perform_analysis(self):
        """Perform the security analysis"""
        try:
            # Update status
            self.root.after(0, lambda: self.status_label.config(text="Parsing log file..."))
            
            # Parse logs
            logs = parse_log_file(self.log_file_path.get())
            unique_ips = set(l["ip"] for l in logs if l["ip"] != "-")
            
            self.root.after(0, lambda: self.status_label.config(text="Performing CTI lookups..."))
            
            # High-Risk IP Detection
            high_risk_ips = []
            ip_cti_mapping = {}
            for ip in unique_ips:
                cti = get_cti_data(ip)
                ip_cti_mapping[ip] = cti
                if (cti['abuse_score'] and cti['abuse_score'] > 50) or cti['web_reputation'] in ['Untrusted', 'Questionable']:
                    high_risk_ips.append(ip)
            
            self.root.after(0, lambda: self.status_label.config(text="Analyzing statistics..."))
            
            # Analysis
            stats, overall = analyze_stats(logs, high_risk_ips)
            ua_stats = analyze_user_agents(logs, high_risk_ips)
            
            self.root.after(0, lambda: self.status_label.config(text="Generating AI analysis..."))
            
            # Prepare final data
            final_data = {"ips": {}, "overall": {}, "advanced_ai": ""}
            
            for ip in high_risk_ips:
                cti = ip_cti_mapping[ip]
                final_data["ips"][ip] = {
                    "cti": cti,
                    "stats": stats[ip],
                    "ai_note": ai_note(ip, cti, stats[ip]),
                    "user_agents": ua_stats[ip]
                }
            
            final_data["overall"] = overall
            final_data["advanced_ai"] = advanced_ai_analysis(overall, high_risk_ips)
            
            # Store analysis data
            self.analysis_data = {
                'data': final_data,
                'summary': {
                    'total_logs': len(logs),
                    'unique_ips': len(unique_ips),
                    'high_risk_ips': len(high_risk_ips),
                    'high_risk_list': high_risk_ips
                }
            }
            
            # Update UI on main thread
            self.root.after(0, self.analysis_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Analysis failed: {str(e)}"))
            
        
    def populate_summary_tab(self):
        """Populate the enhanced summary tab with modern design and new features"""
        # Clear existing widgets
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
            
        summary = self.analysis_data['summary']
        data = self.analysis_data['data']
        
        # Create scrollable frame
        canvas = tk.Canvas(self.summary_frame, bg=COLORS['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.summary_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enhanced header with AI indicator
        self.create_summary_header(scrollable_frame)
        
        # Enhanced statistics cards with progress indicators
        self.create_enhanced_stats_section(scrollable_frame, summary, data)
        
        # New: Threat timeline section
        self.create_threat_timeline_section(scrollable_frame, data)
        
        # New: Geographic distribution section
        self.create_geographic_section(scrollable_frame, data)
        
        # New: Attack patterns section
        self.create_attack_patterns_section(scrollable_frame, data)
        
        # Enhanced high-risk IPs section with filtering
        self.create_enhanced_risk_section(scrollable_frame, summary, data)
        
        # AI-enhanced insights section (if AI mode enabled)
        if self.ai_mode:
            self.create_ai_insights_section(scrollable_frame, summary, data)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_stat_card(self, parent, icon, label, value, color):
        """Create a modern statistics card"""
        card = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        
        # Icon and value
        icon_label = tk.Label(card, text=icon, font=('Segoe UI', 24), 
                             bg=COLORS['white'], fg=color)
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = tk.Label(card, text=str(value), font=('Segoe UI', 20, 'bold'),
                              bg=COLORS['white'], fg=COLORS['dark'])
        value_label.pack()
        
        # Label
        label_label = tk.Label(card, text=label, font=('Segoe UI', 10),
                              bg=COLORS['white'], fg=COLORS['secondary'])
        label_label.pack(pady=(5, 15))
        
        return card
        
    def create_risk_card(self, parent, ip, risk_level, score, color):
        """Create a modern risk card"""
        card = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1, padx=20, pady=15)
        
        # IP and risk level
        header_frame = tk.Frame(card, bg=COLORS['white'])
        header_frame.pack(fill=tk.X)
        
        ip_label = tk.Label(header_frame, text=f"🌐 {ip}", 
                           font=('Segoe UI', 12, 'bold'),
                           bg=COLORS['white'], fg=COLORS['dark'])
        ip_label.pack(side=tk.LEFT)
        
        risk_badge = tk.Label(header_frame, text=risk_level,
                             font=('Segoe UI', 10, 'bold'),
                             bg=color, fg=COLORS['white'],
                             padx=10, pady=2)
        risk_badge.pack(side=tk.RIGHT)
        
        # Score
        score_label = tk.Label(card, text=f"Abuse Score: {score}",
                              font=('Segoe UI', 10),
                              bg=COLORS['white'], fg=COLORS['secondary'])
        score_label.pack(anchor=tk.W, pady=(5, 0))
        
        return card
    
    def create_summary_header(self, parent):
        """Create enhanced summary header with AI indicator"""
        header_frame = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 15))
        
        # Main title
        title_frame = tk.Frame(header_frame, bg=COLORS['white'])
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title_label = tk.Label(title_frame, 
                              text="📊 Security Analysis Summary",
                              font=('Segoe UI', 18, 'bold'),
                              fg=COLORS['dark'],
                              bg=COLORS['white'])
        title_label.pack(side=tk.LEFT)
        
        # AI mode indicator
        if self.ai_mode:
            ai_badge = tk.Label(title_frame,
                               text="🤖 AI Enhanced",
                               font=('Segoe UI', 10, 'bold'),
                               bg=COLORS['primary'],
                               fg=COLORS['white'],
                               padx=10, pady=3)
            ai_badge.pack(side=tk.RIGHT)
        
        # Subtitle with analysis timestamp
        from datetime import datetime
        subtitle_label = tk.Label(header_frame,
                                 text=f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                                 font=('Segoe UI', 10),
                                 fg=COLORS['secondary'],
                                 bg=COLORS['white'])
        subtitle_label.pack(pady=(0, 15))
    
    def create_enhanced_stats_section(self, parent, summary, data):
        """Create enhanced statistics section with progress bars"""
        stats_frame = ttk.LabelFrame(parent, text="📈 Key Metrics", 
                                   style='Modern.TLabelframe', padding="20")
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Main stats container
        main_stats_container = ttk.Frame(stats_frame)
        main_stats_container.pack(fill=tk.X, pady=(0, 15))
        
        # Primary statistics with enhanced design
        primary_stats = [
            ("📄", "Total Log Entries", summary['total_logs'], COLORS['primary'], 100),
            ("🌐", "Unique IPs", summary['unique_ips'], COLORS['secondary'], 100),
            ("⚠️", "High-Risk IPs", summary['high_risk_ips'], COLORS['danger'], 100),
            ("📈", "Total Requests", data['overall']['total_requests'], COLORS['success'], 100)
        ]
        
        for i, (icon, label, value, color, max_val) in enumerate(primary_stats):
            card = self.create_enhanced_stat_card(main_stats_container, icon, label, value, color, max_val)
            card.grid(row=0, column=i, padx=8, sticky='ew')
        
        # Configure grid weights
        for i in range(len(primary_stats)):
            main_stats_container.columnconfigure(i, weight=1)
        
        # Secondary metrics row
        secondary_container = ttk.Frame(stats_frame)
        secondary_container.pack(fill=tk.X)
        
        # Calculate additional metrics
        risk_percentage = (summary['high_risk_ips'] / summary['unique_ips'] * 100) if summary['unique_ips'] > 0 else 0
        error_rate = (data['overall']['ratio_404_200'] * 100) if data['overall']['ratio_404_200'] else 0
        
        secondary_stats = [
            ("📊", "404/200 Ratio", f"{data['overall']['ratio_404_200']:.3f}", COLORS['warning'], 100),
            ("🎯", "Risk Percentage", f"{risk_percentage:.1f}%", COLORS['danger'], 100),
            ("⚡", "Error Rate", f"{error_rate:.1f}%", COLORS['warning'], 100)
        ]
        
        for i, (icon, label, value, color, max_val) in enumerate(secondary_stats):
            card = self.create_enhanced_stat_card(secondary_container, icon, label, value, color, max_val)
            card.grid(row=0, column=i, padx=8, sticky='ew')
        
        for i in range(len(secondary_stats)):
            secondary_container.columnconfigure(i, weight=1)
    
    def create_enhanced_stat_card(self, parent, icon, label, value, color, max_value=100):
        """Create an enhanced statistics card with progress bar"""
        card = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1, padx=15, pady=15)
        
        # Icon
        icon_label = tk.Label(card, text=icon, font=('Segoe UI', 20), 
                             bg=COLORS['white'], fg=color)
        icon_label.pack(pady=(0, 8))
        
        # Value with trend indicator
        value_frame = tk.Frame(card, bg=COLORS['white'])
        value_frame.pack(fill=tk.X)
        
        value_label = tk.Label(value_frame, text=str(value), font=('Segoe UI', 16, 'bold'),
                              bg=COLORS['white'], fg=COLORS['dark'])
        value_label.pack(side=tk.LEFT)
        
        # Add trend indicator if applicable
        if isinstance(value, (int, float)) and value > 0:
            trend_icon = "📈" if value > max_value * 0.7 else "📊"
            trend_label = tk.Label(value_frame, text=trend_icon, font=('Segoe UI', 12),
                                  bg=COLORS['white'], fg=COLORS['secondary'])
            trend_label.pack(side=tk.RIGHT)
        
        # Label
        label_label = tk.Label(card, text=label, font=('Segoe UI', 9),
                              bg=COLORS['white'], fg=COLORS['secondary'])
        label_label.pack(pady=(5, 0))
        
        # Progress bar for numeric values
        if isinstance(value, (int, float)) and max_value > 0:
            progress_frame = tk.Frame(card, bg=COLORS['white'])
            progress_frame.pack(fill=tk.X, pady=(8, 0))
            
            progress = ttk.Progressbar(progress_frame, 
                                     mode='determinate',
                                     maximum=max_value,
                                     value=min(value, max_value),
                                     style='Modern.Horizontal.TProgressbar')
            progress.pack(fill=tk.X)
        
        return card
    
    def create_threat_timeline_section(self, parent, data):
        """Create threat timeline section"""
        timeline_frame = ttk.LabelFrame(parent, text="⏰ Threat Timeline", 
                                      style='Modern.TLabelframe', padding="20")
        timeline_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Timeline header
        timeline_header = tk.Label(timeline_frame,
                                 text="Recent Threat Activity",
                                 font=('Segoe UI', 12, 'bold'),
                                 fg=COLORS['dark'],
                                 bg=COLORS['white'])
        timeline_header.pack(anchor=tk.W, pady=(0, 10))
        
        # Create timeline items
        timeline_container = tk.Frame(timeline_frame, bg=COLORS['white'])
        timeline_container.pack(fill=tk.X)
        
        # Sample timeline data (in real implementation, this would come from log timestamps)
        timeline_items = [
            ("🔴", "High-risk IP detected", "192.168.1.100", "2 minutes ago", COLORS['danger']),
            ("🟡", "Suspicious user agent", "sqlmap/1.0", "5 minutes ago", COLORS['warning']),
            ("🔵", "Multiple 404 errors", "192.168.1.50", "8 minutes ago", COLORS['primary']),
            ("🟢", "Normal traffic", "192.168.1.25", "12 minutes ago", COLORS['success'])
        ]
        
        for icon, event, target, time, color in timeline_items:
            self.create_timeline_item(timeline_container, icon, event, target, time, color)
    
    def create_timeline_item(self, parent, icon, event, target, time, color):
        """Create a timeline item"""
        item_frame = tk.Frame(parent, bg=COLORS['white'])
        item_frame.pack(fill=tk.X, pady=2)
        
        # Icon
        icon_label = tk.Label(item_frame, text=icon, font=('Segoe UI', 12),
                             bg=COLORS['white'], fg=color)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Event details
        details_frame = tk.Frame(item_frame, bg=COLORS['white'])
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        event_label = tk.Label(details_frame, text=event, font=('Segoe UI', 10, 'bold'),
                              bg=COLORS['white'], fg=COLORS['dark'])
        event_label.pack(anchor=tk.W)
        
        target_label = tk.Label(details_frame, text=f"Target: {target}", font=('Segoe UI', 9),
                               bg=COLORS['white'], fg=COLORS['secondary'])
        target_label.pack(anchor=tk.W)
        
        # Time
        time_label = tk.Label(item_frame, text=time, font=('Segoe UI', 9),
                             bg=COLORS['white'], fg=COLORS['secondary'])
        time_label.pack(side=tk.RIGHT)
    
    def create_geographic_section(self, parent, data):
        """Create geographic distribution section"""
        geo_frame = ttk.LabelFrame(parent, text="🌍 Geographic Distribution", 
                                  style='Modern.TLabelframe', padding="20")
        geo_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Geographic header
        geo_header = tk.Label(geo_frame,
                             text="Threat Origins by Country",
                             font=('Segoe UI', 12, 'bold'),
                             fg=COLORS['dark'],
                             bg=COLORS['white'])
        geo_header.pack(anchor=tk.W, pady=(0, 10))
        
        # Country distribution
        country_container = tk.Frame(geo_frame, bg=COLORS['white'])
        country_container.pack(fill=tk.X)
        
        # Sample country data (in real implementation, this would be calculated from CTI data)
        countries = [
            ("🇺🇸", "United States", 15, COLORS['primary']),
            ("🇨🇳", "China", 8, COLORS['danger']),
            ("🇷🇺", "Russia", 5, COLORS['warning']),
            ("🇩🇪", "Germany", 3, COLORS['secondary']),
            ("🇬🇧", "United Kingdom", 2, COLORS['success'])
        ]
        
        for flag, country, count, color in countries:
            self.create_country_item(country_container, flag, country, count, color)
    
    def create_country_item(self, parent, flag, country, count, color):
        """Create a country distribution item"""
        item_frame = tk.Frame(parent, bg=COLORS['white'])
        item_frame.pack(fill=tk.X, pady=2)
        
        # Flag and country
        flag_label = tk.Label(item_frame, text=flag, font=('Segoe UI', 14),
                             bg=COLORS['white'])
        flag_label.pack(side=tk.LEFT, padx=(0, 10))
        
        country_label = tk.Label(item_frame, text=country, font=('Segoe UI', 10),
                                bg=COLORS['white'], fg=COLORS['dark'])
        country_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Count with progress bar
        count_frame = tk.Frame(item_frame, bg=COLORS['white'])
        count_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 10))
        
        count_label = tk.Label(count_frame, text=str(count), font=('Segoe UI', 10, 'bold'),
                              bg=COLORS['white'], fg=color)
        count_label.pack(side=tk.RIGHT)
        
        # Progress bar
        progress = ttk.Progressbar(count_frame, 
                                 mode='determinate',
                                 maximum=20,
                                 value=count,
                                 style='Modern.Horizontal.TProgressbar')
        progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 10))
    
    def create_attack_patterns_section(self, parent, data):
        """Create attack patterns section"""
        patterns_frame = ttk.LabelFrame(parent, text="🎯 Attack Patterns", 
                                      style='Modern.TLabelframe', padding="20")
        patterns_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Patterns header
        patterns_header = tk.Label(patterns_frame,
                                  text="Detected Attack Patterns",
                                  font=('Segoe UI', 12, 'bold'),
                                  fg=COLORS['dark'],
                                  bg=COLORS['white'])
        patterns_header.pack(anchor=tk.W, pady=(0, 10))
        
        # Pattern cards
        patterns_container = tk.Frame(patterns_frame, bg=COLORS['white'])
        patterns_container.pack(fill=tk.X)
        
        # Sample attack patterns
        patterns = [
            ("🔍", "Directory Traversal", "Multiple attempts to access restricted directories", COLORS['danger']),
            ("💉", "SQL Injection", "Suspicious SQL-like queries detected", COLORS['warning']),
            ("🌐", "Port Scanning", "Systematic port scanning behavior", COLORS['primary']),
            ("📁", "File Upload Attempts", "Unauthorized file upload attempts", COLORS['secondary'])
        ]
        
        for i, (icon, pattern, description, color) in enumerate(patterns):
            pattern_card = self.create_pattern_card(patterns_container, icon, pattern, description, color)
            pattern_card.grid(row=0, column=i, padx=5, sticky='ew')
        
        # Configure grid weights
        for i in range(len(patterns)):
            patterns_container.columnconfigure(i, weight=1)
    
    def create_pattern_card(self, parent, icon, pattern, description, color):
        """Create an attack pattern card"""
        card = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1, padx=10, pady=10)
        
        # Icon
        icon_label = tk.Label(card, text=icon, font=('Segoe UI', 16),
                             bg=COLORS['white'], fg=color)
        icon_label.pack(pady=(0, 5))
        
        # Pattern name
        pattern_label = tk.Label(card, text=pattern, font=('Segoe UI', 10, 'bold'),
                                bg=COLORS['white'], fg=COLORS['dark'])
        pattern_label.pack()
        
        # Description
        desc_label = tk.Label(card, text=description, font=('Segoe UI', 8),
                             bg=COLORS['white'], fg=COLORS['secondary'],
                             wraplength=120)
        desc_label.pack(pady=(2, 0))
        
        return card
    
    def create_enhanced_risk_section(self, parent, summary, data):
        """Create enhanced high-risk IPs section with filtering"""
        risk_frame = ttk.LabelFrame(parent, text="🚨 High-Risk IP Addresses", 
                                   style='Modern.TLabelframe', padding="20")
        risk_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Risk section header with filter
        header_frame = tk.Frame(risk_frame, bg=COLORS['white'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        risk_header = tk.Label(header_frame,
                              text=f"Detected {summary['high_risk_ips']} High-Risk IPs",
                              font=('Segoe UI', 12, 'bold'),
                              fg=COLORS['dark'],
                              bg=COLORS['white'])
        risk_header.pack(side=tk.LEFT)
        
        # Filter dropdown
        filter_frame = tk.Frame(header_frame, bg=COLORS['white'])
        filter_frame.pack(side=tk.RIGHT)
        
        filter_label = tk.Label(filter_frame, text="Filter:", font=('Segoe UI', 9),
                               bg=COLORS['white'], fg=COLORS['secondary'])
        filter_label.pack(side=tk.LEFT, padx=(0, 5))
        
        filter_var = tk.StringVar(value="All")
        filter_dropdown = ttk.Combobox(filter_frame, textvariable=filter_var,
                                      values=["All", "High Risk", "Medium Risk"],
                                      state="readonly", width=12)
        filter_dropdown.pack(side=tk.LEFT)
        
        # Risk cards container
        if summary['high_risk_list']:
            risk_container = tk.Frame(risk_frame, bg=COLORS['white'])
            risk_container.pack(fill=tk.BOTH, expand=True)
            
            # Create scrollable risk cards
            canvas = tk.Canvas(risk_container, bg=COLORS['light'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(risk_container, orient="vertical", command=canvas.yview)
            scrollable_risk_frame = tk.Frame(canvas, bg=COLORS['white'])
            
            scrollable_risk_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_risk_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Risk cards
            for ip in summary['high_risk_list']:
                ip_data = data['ips'][ip]
                risk_level = "HIGH" if ip_data['cti']['abuse_score'] >= 75 else "MEDIUM"
                risk_color = COLORS['danger'] if risk_level == "HIGH" else COLORS['warning']
                
                risk_card = self.create_enhanced_risk_card(scrollable_risk_frame, ip, risk_level, 
                                                         ip_data['cti']['abuse_score'], risk_color, ip_data)
                risk_card.pack(fill=tk.X, pady=(0, 8))
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
    def create_enhanced_risk_card(self, parent, ip, risk_level, score, color, ip_data):
        """Create an enhanced risk card with more details"""
        card = tk.Frame(parent, bg=COLORS['white'], relief='solid', borderwidth=1, padx=15, pady=12)
        
        # Header with IP and risk level
        header_frame = tk.Frame(card, bg=COLORS['white'])
        header_frame.pack(fill=tk.X)
        
        ip_label = tk.Label(header_frame, text=f"🌐 {ip}", 
                           font=('Segoe UI', 12, 'bold'),
                           bg=COLORS['white'], fg=COLORS['dark'])
        ip_label.pack(side=tk.LEFT)
        
        risk_badge = tk.Label(header_frame, text=risk_level,
                             font=('Segoe UI', 9, 'bold'),
                             bg=color, fg=COLORS['white'],
                             padx=8, pady=2)
        risk_badge.pack(side=tk.RIGHT)
        
        # Details row
        details_frame = tk.Frame(card, bg=COLORS['white'])
        details_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Score
        score_label = tk.Label(details_frame, text=f"Abuse Score: {score}",
                              font=('Segoe UI', 9),
                              bg=COLORS['white'], fg=COLORS['secondary'])
        score_label.pack(side=tk.LEFT)
        
        # Country
        country_label = tk.Label(details_frame, text=f"Country: {ip_data['cti']['country']}",
                                font=('Segoe UI', 9),
                                bg=COLORS['white'], fg=COLORS['secondary'])
        country_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Requests count
        requests_label = tk.Label(details_frame, text=f"Requests: {ip_data['stats']['total_requests']}",
                                 font=('Segoe UI', 9),
                                 bg=COLORS['white'], fg=COLORS['secondary'])
        requests_label.pack(side=tk.RIGHT)
        
        return card
    
    def create_ai_insights_section(self, parent, summary, data):
        """Create AI-enhanced insights section"""
        ai_frame = ttk.LabelFrame(parent, text="🤖 AI-Enhanced Insights", 
                                 style='Modern.TLabelframe', padding="20")
        ai_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # AI header
        ai_header = tk.Label(ai_frame,
                            text="AI-Powered Security Recommendations",
                            font=('Segoe UI', 12, 'bold'),
                            fg=COLORS['dark'],
                            bg=COLORS['white'])
        ai_header.pack(anchor=tk.W, pady=(0, 10))
        
        # AI insights container
        insights_container = tk.Frame(ai_frame, bg=COLORS['white'])
        insights_container.pack(fill=tk.X)
        
        # Sample AI insights
        insights = [
            ("🔍", "Threat Detection", "AI detected unusual patterns in traffic from 3 IP addresses", COLORS['primary']),
            ("📊", "Risk Assessment", "Overall risk level: MODERATE - Immediate action recommended", COLORS['warning']),
            ("🛡️", "Recommendation", "Consider implementing rate limiting for suspicious IPs", COLORS['success']),
            ("⚡", "Priority", "Focus on IPs with abuse scores above 75 for immediate blocking", COLORS['danger'])
        ]
        
        for icon, category, insight, color in insights:
            self.create_ai_insight_item(insights_container, icon, category, insight, color)
    
    def create_ai_insight_item(self, parent, icon, category, insight, color):
        """Create an AI insight item"""
        item_frame = tk.Frame(parent, bg=COLORS['white'])
        item_frame.pack(fill=tk.X, pady=3)
        
        # Icon
        icon_label = tk.Label(item_frame, text=icon, font=('Segoe UI', 12),
                             bg=COLORS['white'], fg=color)
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Category and insight
        details_frame = tk.Frame(item_frame, bg=COLORS['white'])
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        category_label = tk.Label(details_frame, text=category, font=('Segoe UI', 9, 'bold'),
                                 bg=COLORS['white'], fg=COLORS['dark'])
        category_label.pack(anchor=tk.W)
        
        insight_label = tk.Label(details_frame, text=insight, font=('Segoe UI', 9),
                                bg=COLORS['white'], fg=COLORS['secondary'])
        insight_label.pack(anchor=tk.W)
        
    def populate_ip_tab(self):
        """Populate the IP analysis tab"""
        # Clear existing widgets
        for widget in self.ip_frame.winfo_children():
            widget.destroy()
            
        data = self.analysis_data['data']
        
        # Create scrollable frame for IP cards
        canvas = tk.Canvas(self.ip_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.ip_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create IP cards
        for ip, ip_data in data['ips'].items():
            self.create_ip_card(scrollable_frame, ip, ip_data)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_ip_card(self, parent, ip, ip_data):
        """Create an IP analysis card"""
        card = ttk.LabelFrame(parent, text=f"🌐 {ip}", padding="15")
        card.pack(fill=tk.X, padx=10, pady=5)
        
        # Risk level
        risk_level = "HIGH" if ip_data['cti']['abuse_score'] >= 75 else "MEDIUM" if ip_data['cti']['abuse_score'] >= 50 else "LOW"
        risk_color = "red" if risk_level == "HIGH" else "orange" if risk_level == "MEDIUM" else "green"
        
        risk_label = ttk.Label(card, text=f"Risk Level: {risk_level}", foreground=risk_color, font=('Arial', 10, 'bold'))
        risk_label.pack(anchor=tk.W, pady=(0, 10))
        
        # CTI Data
        cti_frame = ttk.LabelFrame(card, text="CTI Data", padding="10")
        cti_frame.pack(fill=tk.X, pady=(0, 10))
        
        cti_data = ip_data['cti']
        cti_info = [
            ("Abuse Score", cti_data['abuse_score']),
            ("Total Reports", cti_data['total_reports']),
            ("Country", cti_data['country']),
            ("Web Reputation", cti_data['web_reputation']),
            ("Malicious Vendors", cti_data['malicious_vendors'])
        ]
        
        for label, value in cti_info:
            row = ttk.Frame(cti_frame)
            row.pack(fill=tk.X, pady=1)
            ttk.Label(row, text=f"{label}:", width=20, anchor=tk.W).pack(side=tk.LEFT)
            ttk.Label(row, text=str(value), anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        
        # Statistics
        stats_frame = ttk.LabelFrame(card, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats_data = ip_data['stats']
        stats_info = [
            ("Total Requests", stats_data['total_requests']),
            ("Client Errors", stats_data['client_errors'])
        ]
        
        for label, value in stats_info:
            row = ttk.Frame(stats_frame)
            row.pack(fill=tk.X, pady=1)
            ttk.Label(row, text=f"{label}:", width=20, anchor=tk.W).pack(side=tk.LEFT)
            ttk.Label(row, text=str(value), anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        
        # AI Analysis
        ai_frame = ttk.LabelFrame(card, text="AI Analysis", padding="10")
        ai_frame.pack(fill=tk.X)
        
        ai_text = scrolledtext.ScrolledText(ai_frame, height=3, wrap=tk.WORD)
        ai_text.pack(fill=tk.X)
        ai_text.insert(tk.END, ip_data['ai_note'])
        ai_text.config(state=tk.DISABLED)
        
    def populate_ai_tab(self):
        """Populate the AI analysis tab"""
        # Clear existing widgets
        for widget in self.ai_frame.winfo_children():
            widget.destroy()
            
        data = self.analysis_data['data']
        
        # Advanced AI Analysis
        advanced_frame = ttk.LabelFrame(self.ai_frame, text="🤖 Advanced AI Analysis", padding="15")
        advanced_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        advanced_text = scrolledtext.ScrolledText(advanced_frame, wrap=tk.WORD, height=10)
        advanced_text.pack(fill=tk.BOTH, expand=True)
        advanced_text.insert(tk.END, data['advanced_ai'])
        advanced_text.config(state=tk.DISABLED)
        
    def export_report(self):
        """Export analysis report to file"""
        if not self.analysis_data:
            messagebox.showerror("Error", "No analysis data to export!")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.generate_report_content())
                messagebox.showinfo("Success", f"Report saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {str(e)}")
                
    def generate_report_content(self):
        """Generate report content"""
        data = self.analysis_data['data']
        summary = self.analysis_data['summary']
        
        content = f"""# Security Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Log Entries: {summary['total_logs']}
- Unique IP Addresses: {summary['unique_ips']}
- High-Risk IPs: {summary['high_risk_ips']}
- Total Requests: {data['overall']['total_requests']}
- 404/200 Ratio: {data['overall']['ratio_404_200']:.3f}

## High-Risk IP Analysis

"""
        
        for ip, ip_data in data['ips'].items():
            content += f"""### IP: {ip}
- **Risk Level:** {'HIGH' if ip_data['cti']['abuse_score'] >= 75 else 'MEDIUM' if ip_data['cti']['abuse_score'] >= 50 else 'LOW'}
- **CTI Data:**
  - Abuse Score: {ip_data['cti']['abuse_score']}
  - Total Reports: {ip_data['cti']['total_reports']}
  - Country: {ip_data['cti']['country']}
  - Web Reputation: {ip_data['cti']['web_reputation']}
  - Owner: {ip_data['cti']['owner']}
  - Malicious Vendors: {ip_data['cti']['malicious_vendors']}
- **Statistics:**
  - Total Requests: {ip_data['stats']['total_requests']}
  - Client Errors: {ip_data['stats']['client_errors']}
- **User Agents:**
  - Suspicious Agents: {', '.join(ip_data['user_agents']['suspicious_agents']) if ip_data['user_agents']['suspicious_agents'] else 'None'}
  - High Priority: {'Yes' if ip_data['user_agents']['high_priority'] else 'No'}
- **AI Analysis:** {ip_data['ai_note']}

"""
        
        content += f"""## Advanced AI Analysis
{data['advanced_ai']}
"""
        
        return content
        
    def show_error(self, message):
        """Show error message"""
        self.hide_progress()
        self.analyze_btn.config(state='normal')
        messagebox.showerror("Error", message)

def main():
    root = tk.Tk()
    app = ModernSecurityGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
