import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from datetime import datetime
from main import (
    parse_log_file, get_cti_data, analyze_stats, 
    analyze_user_agents, ai_note, advanced_ai_analysis
)

# Modern color scheme
COLORS = {
    'primary': '#2563eb',  # Blue
    'secondary': '#64748b',  # Slate
    'success': '#10b981',  # Emerald
    'warning': '#f59e0b',  # Amber
    'danger': '#ef4444',  # Red
    'dark': '#1e293b',  # Dark slate
    'light': '#f8fafc',  # Light gray
    'white': '#ffffff',
    'border': '#e2e8f0'  # Light border
}

class ModernSecurityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Security Analysis Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['light'])
        
        self.setup_modern_style()
        self.log_file_path = tk.StringVar()
        self.analysis_data = None
        self.create_widgets()
        
    def setup_modern_style(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button style
        style.configure('Modern.TButton', 
                        background=COLORS['primary'], 
                        foreground=COLORS['white'], 
                        borderwidth=0, 
                        padding=(20, 10), 
                        font=('Segoe UI', 10, 'bold'))
        style.map('Modern.TButton', 
                  background=[('active', '#1d4ed8'), ('pressed', '#1e40af')])
        
        # Frame style
        style.configure('Modern.TFrame', 
                        background=COLORS['white'], 
                        borderwidth=1, 
                        relief='solid')
        
        # Label Frame style
        style.configure('Modern.TLabelframe', 
                        background=COLORS['white'], 
                        borderwidth=1, 
                        relief='solid', 
                        bordercolor=COLORS['border'])
        style.configure('Modern.TLabelframe.Label', 
                        background=COLORS['white'], 
                        foreground=COLORS['dark'], 
                        font=('Segoe UI', 11, 'bold'))
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = tk.Label(header_frame, 
                               text="🛡️ Security Analysis Dashboard", 
                               font=('Segoe UI', 24, 'bold'), 
                               fg=COLORS['dark'], 
                               bg=COLORS['white'])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(header_frame, 
                                  text="AI-Powered Threat Detection & Analysis", 
                                  font=('Segoe UI', 12), 
                                  fg=COLORS['secondary'], 
                                  bg=COLORS['white'])
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # File section
        self.create_file_section(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)

    def create_file_section(self, parent):
        """Create file upload section"""
        file_frame = ttk.LabelFrame(parent, text="📁 Upload Log File", style='Modern.TLabelframe', padding="25")
        file_frame.pack(fill=tk.X, pady=(0, 25))
        
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X)
        
        file_label = tk.Label(input_frame, text="Select Log File:", 
                              font=('Segoe UI', 10, 'bold'), 
                              fg=COLORS['dark'], 
                              bg=COLORS['white'])
        file_label.pack(anchor=tk.W, pady=(0, 8))
        
        file_row = ttk.Frame(input_frame)
        file_row.pack(fill=tk.X)
        
        self.file_entry = tk.Entry(file_row, 
                                   textvariable=self.log_file_path, 
                                   font=('Segoe UI', 10), 
                                   relief='solid', 
                                   borderwidth=1, 
                                   bg=COLORS['white'], 
                                   fg=COLORS['dark'], 
                                   insertbackground=COLORS['primary'])
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
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
        
        self.analyze_btn.config(state='disabled')
        self.show_progress()
        
        thread = threading.Thread(target=self.perform_analysis)
        thread.daemon = True
        thread.start()

    def show_progress(self):
        """Show progress section"""
        self.progress_frame.pack(fill=tk.X, pady=(0, 25))
        self.progress.start()
        self.status_label.config(text="Parsing log file...")
        
    def hide_progress(self):
        """Hide progress section"""
        self.progress.stop()
        self.progress_frame.pack_forget()

    def perform_analysis(self):
        try:
            logs = parse_log_file(self.log_file_path.get())
            unique_ips = set(l["ip"] for l in logs if l["ip"] != "-")
            high_risk_ips = []
            ip_cti_mapping = {}
            
            for ip in unique_ips:
                cti = get_cti_data(ip)
                ip_cti_mapping[ip] = cti
                if (cti['abuse_score'] and cti['abuse_score'] > 50) or cti['web_reputation'] in ['Untrusted', 'Questionable']:
                    high_risk_ips.append(ip)
            
            stats, overall = analyze_stats(logs, high_risk_ips)
            ua_stats = analyze_user_agents(logs, high_risk_ips)
            
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
            
            self.analysis_data = final_data
            self.root.after(0, self.display_results)
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Analysis failed: {str(e)}"))

    def display_results(self):
        """Display analysis results"""
        self.hide_progress()
        self.analyze_btn.config(state='normal')
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        self.results_title.config(text=f"Analysis Complete - {len(self.analysis_data['ips'])} High-Risk IPs Found")
        self.export_btn.pack(side=tk.RIGHT)
        
        self.populate_summary_tab()
        self.populate_ip_tab()
        self.populate_ai_tab()

    def populate_summary_tab(self):
        # Populate summary tab here
        pass
        
    def populate_ip_tab(self):
        # Populate IP analysis tab here
        pass

    def populate_ai_tab(self):
        # Populate AI analysis tab here
        pass

    def export_report(self):
        # Export report here
        pass

def main():
    root = tk.Tk()
    app = ModernSecurityGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
