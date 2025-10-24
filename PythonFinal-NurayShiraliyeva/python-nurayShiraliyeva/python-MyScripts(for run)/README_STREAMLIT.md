# 🛡️ Advanced Security Intelligence Platform - Streamlit Edition

A modern, web-based security log analysis platform with AI-powered threat detection, interactive visualizations, and comprehensive reporting capabilities.

## ✨ Features

### 🎨 Modern Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Dashboards**: Real-time data visualization with Plotly charts
- **Professional UI**: Modern gradient designs and smooth animations
- **Sidebar Navigation**: Easy access to all features

### 📊 Advanced Analytics
- **Interactive Charts**: Pie charts, histograms, and distribution plots
- **Real-time Metrics**: Live updating statistics and KPIs
- **Risk Assessment**: Color-coded risk levels and threat indicators
- **Geographic Visualization**: IP geolocation and country-based analysis

### 🤖 AI-Powered Features
- **Smart Threat Detection**: AI-enhanced analysis using Mistral AI
- **Automated Insights**: Intelligent recommendations and alerts
- **Pattern Recognition**: Advanced behavioral analysis
- **Risk Scoring**: Dynamic threat level assessment

### 📁 File Management & Analysis
- **Drag & Drop Upload**: Easy file upload interface
- **Multiple Formats**: Support for .log and .txt files
- **Progress Tracking**: Real-time analysis progress indicators
- **Advanced Log Browser**: Comprehensive log analysis with filtering and search
- **Attack Pattern Detection**: Automatic detection of SQL injection, XSS, directory traversal
- **User Behavior Analysis**: Session analysis and anomaly detection
- **Time-Based Analysis**: Hourly and daily request distribution charts
- **Export Options**: Enhanced CSV, Markdown, and JSON export formats

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Launch Application**
   
   **Option 1: Using Python**
   ```bash
   python run_streamlit.py
   ```
   
   **Option 2: Using Batch File (Windows)**
   ```bash
   launch_streamlit.bat
   ```
   
   **Option 3: Direct Streamlit**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

3. **Access Application**
   - Open your web browser
   - Navigate to: `http://localhost:8501`
   - The application will load automatically

## 📱 Usage Guide

### 1. Dashboard
- **Overview**: Main landing page with key metrics
- **Quick Stats**: Summary of analysis results
- **Navigation**: Easy access to all features

### 2. Upload & Analysis
- **File Upload**: Drag and drop your log files
- **Analysis Options**: Configure real-time monitoring and deep analysis
- **Progress Tracking**: Watch real-time analysis progress
- **Results Display**: Comprehensive analysis results

### 3. IP Intelligence
- **Detailed Analysis**: In-depth IP threat assessment
- **CTI Data**: Comprehensive threat intelligence
- **Geolocation**: Country and region information
- **Risk Scoring**: Dynamic risk level assessment

### 4. AI Insights
- **Smart Analysis**: AI-powered threat detection
- **Recommendations**: Automated security suggestions
- **Pattern Recognition**: Advanced behavioral analysis
- **Risk Assessment**: Intelligent threat evaluation

### 5. Reports
- **Export Options**: Multiple format support
- **Custom Reports**: Tailored analysis reports
- **Data Visualization**: Interactive charts and graphs
- **Sharing**: Easy report distribution

### 6. Settings
- **Configuration**: Customize analysis parameters
- **API Keys**: Configure external service access
- **Preferences**: Personalize your experience
- **Security**: Manage authentication and access

## 🔧 Configuration

### API Keys
Configure the following API keys in the Settings section:

- **AbuseIPDB**: For IP reputation checking
- **VirusTotal**: For malware detection
- **Mistral AI**: For AI-powered analysis

### Analysis Settings
- **Risk Threshold**: Adjust sensitivity levels
- **Rate Limits**: Configure request limits
- **Monitoring**: Enable real-time features
- **AI Mode**: Toggle enhanced AI features

## 📊 Supported File Formats

- **Log Files**: `.log` extension
- **Text Files**: `.txt` extension
- **JSON Logs**: Structured log formats
- **CSV Logs**: Comma-separated log data

## 🌐 Browser Compatibility

- **Chrome**: Recommended (best performance)
- **Firefox**: Fully supported
- **Safari**: Supported
- **Edge**: Supported
- **Mobile Browsers**: Responsive design

## 🚀 Deployment Options

### Local Development
```bash
python -m streamlit run streamlit_app.py --server.port 8501
```

### Production Deployment
```bash
python -m streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements_streamlit.txt
EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## 🔒 Security Features

- **Input Validation**: Secure file upload handling
- **Data Protection**: Encrypted data transmission
- **Access Control**: Configurable user permissions
- **Audit Logging**: Comprehensive activity tracking
- **Threat Detection**: Real-time security monitoring

## 📈 Performance

- **Fast Loading**: Optimized for quick startup
- **Real-time Updates**: Live data refresh
- **Efficient Processing**: Optimized analysis algorithms
- **Scalable Architecture**: Handles large log files
- **Memory Management**: Efficient resource usage

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   python -m streamlit run streamlit_app.py --server.port 8502
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

3. **File Upload Issues**
   - Check file format (.log or .txt)
   - Ensure file size is reasonable
   - Verify file permissions

4. **API Connection Issues**
   - Verify API keys in Settings
   - Check internet connectivity
   - Review API rate limits

### Support

For technical support or feature requests:
- Check the documentation
- Review error messages
- Verify configuration settings
- Test with sample data

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Contact

For questions or support, please contact the development team.

---

**🛡️ Advanced Security Intelligence Platform** - Protecting your infrastructure with AI-powered threat detection.
