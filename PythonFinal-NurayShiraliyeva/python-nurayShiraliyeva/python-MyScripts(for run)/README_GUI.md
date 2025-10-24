# 🛡️ Security Analysis Dashboard - GUI Version

A modern Python GUI application for comprehensive security log analysis with AI-powered threat detection using Mistral AI.

## ✨ Features

- **Modern GUI Interface**: Clean, intuitive tkinter-based interface
- **File Browser**: Easy log file selection with drag-and-drop support
- **Real-time Analysis**: Progress tracking during analysis
- **Comprehensive Analysis**: 
  - CTI (Cyber Threat Intelligence) integration
  - Statistical analysis
  - User-agent correlation
  - AI-powered threat assessment
- **Visual Results**: Organized tabs for different analysis aspects
- **Export Functionality**: Save reports in Markdown format
- **Risk Visualization**: Color-coded risk levels (High/Medium/Low)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_gui.txt
```

### 2. Run the Application
```bash
python run_gui.py
```
or
```bash
python gui_app.py
```

## 📋 How to Use

1. **Launch the Application**: Run the GUI application
2. **Select Log File**: Click "Browse" to select your access log file
3. **Start Analysis**: Click "🔍 Analyze Logs" to begin analysis
4. **View Results**: 
   - **Summary Tab**: Overall statistics and high-risk IPs
   - **IP Analysis Tab**: Detailed analysis for each high-risk IP
   - **AI Analysis Tab**: AI-powered insights and recommendations
5. **Export Report**: Click "📄 Export Report" to save analysis results

## 🔧 Configuration

The application uses the following APIs (configured in `main.py`):
- **Mistral AI**: For AI-powered analysis
- **AbuseIPDB**: For IP reputation data
- **VirusTotal**: For malware detection
- **Talos Intelligence**: For web reputation

## 📊 Analysis Features

### CTI Integration
- AbuseIPDB reputation scores
- VirusTotal malicious vendor detection
- Talos web reputation analysis
- Geographic information

### Statistical Analysis
- Request patterns
- Error rate analysis
- User-agent correlation
- Suspicious activity detection

### AI Analysis
- Risk assessment summaries
- Pattern recognition
- Coordinated attack detection
- Non-technical explanations

## 🎨 Interface Overview

- **File Selection**: Browse and select log files
- **Progress Tracking**: Real-time analysis progress
- **Results Display**: Tabbed interface for different analysis aspects
- **Export Options**: Save comprehensive reports

## 📁 File Structure

```
python_project/
├── gui_app.py              # Main GUI application
├── run_gui.py              # Application launcher
├── main.py                 # Core analysis functions
├── requirements_gui.txt    # GUI dependencies
├── README_GUI.md          # This file
└── data/
    └── access.log         # Sample log file
```

## 🔍 Supported Log Formats

The application supports standard web server access logs in JSON format with the following fields:
- `timestamp`: Request timestamp
- `remote_addr`: Client IP address
- `method`: HTTP method
- `uri`: Request URI
- `status`: HTTP status code
- `user_agent`: Client user agent

## ⚠️ Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Internet connection for API calls
- Valid API keys for external services

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Install required packages with `pip install -r requirements_gui.txt`
2. **API Errors**: Check internet connection and API key validity
3. **File Format**: Ensure log file is in supported JSON format
4. **Memory Issues**: Large log files may require more system memory

### Performance Tips

- For large log files (>100MB), consider splitting into smaller chunks
- Ensure stable internet connection for API calls
- Close other applications to free up system resources

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Verify API keys are correctly configured
3. Ensure log file format matches expected structure
4. Check internet connectivity for external API calls

---

**Note**: This GUI version provides the same powerful analysis capabilities as the command-line version but with an intuitive graphical interface for easier use and better visualization of results.
