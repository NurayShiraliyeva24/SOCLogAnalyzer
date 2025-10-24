#!/usr/bin/env python3
"""
Advanced Security Intelligence Platform - Streamlit Web Application
A modern web-based security log analysis tool with AI-powered threat detection
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import time
import json
import os
import re
import hashlib
from datetime import datetime, timedelta
import threading
from collections import Counter, defaultdict
import ipaddress
from main import (
    parse_log_file, get_cti_data, analyze_stats, 
    analyze_user_agents, ai_note, advanced_ai_analysis
)

# Page configuration
st.set_page_config(
    page_title="🛡️ Security Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    
    .risk-high {
        border-left-color: #ef4444 !important;
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
    }
    
    .risk-medium {
        border-left-color: #f59e0b !important;
        background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
    }
    
    .risk-low {
        border-left-color: #10b981 !important;
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    }
    
    .ai-badge {
        background: linear-gradient(45deg, #8b5cf6, #a855f7);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
    }
    
    .upload-section {
        border: 2px dashed #3b82f6;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        margin: 1rem 0;
    }
    
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'ai_mode' not in st.session_state:
    st.session_state.ai_mode = False
if 'raw_logs' not in st.session_state:
    st.session_state.raw_logs = []
if 'log_metadata' not in st.session_state:
    st.session_state.log_metadata = {}
if 'detailed_stats' not in st.session_state:
    st.session_state.detailed_stats = {}

def analyze_log_metadata(logs):
    """Analyze log file metadata and structure"""
    if not logs:
        return {}
    
    # Basic metadata
    total_lines = len(logs)
    unique_ips = len(set(log['ip'] for log in logs if log['ip'] != '-'))
    unique_user_agents = len(set(log.get('user_agent', '') for log in logs))
    
    # Time analysis
    timestamps = []
    for log in logs:
        try:
            if 'timestamp' in log and log['timestamp']:
                timestamps.append(datetime.strptime(log['timestamp'], '%d/%b/%Y:%H:%M:%S'))
        except:
            continue
    
    time_span = None
    if timestamps:
        time_span = {
            'start': min(timestamps),
            'end': max(timestamps),
            'duration': max(timestamps) - min(timestamps)
        }
    
    # HTTP methods analysis
    methods = Counter(log.get('method', '') for log in logs)
    
    # Status codes analysis
    status_codes = Counter(log.get('status', '') for log in logs)
    
    # File extensions analysis
    extensions = Counter()
    for log in logs:
        path = log.get('path', '')
        if '.' in path:
            ext = path.split('.')[-1].lower()
            extensions[ext] += 1
    
    # Request patterns
    paths = Counter(log.get('path', '') for log in logs)
    top_paths = paths.most_common(10)
    
    return {
        'total_lines': total_lines,
        'unique_ips': unique_ips,
        'unique_user_agents': unique_user_agents,
        'time_span': time_span,
        'http_methods': dict(methods),
        'status_codes': dict(status_codes),
        'file_extensions': dict(extensions),
        'top_paths': top_paths
    }

def generate_detailed_statistics(logs):
    """Generate comprehensive statistics from log data"""
    if not logs:
        return {}
    
    # IP analysis
    ip_stats = defaultdict(lambda: {
        'requests': 0,
        'methods': Counter(),
        'status_codes': Counter(),
        'user_agents': set(),
        'paths': Counter(),
        'first_seen': None,
        'last_seen': None,
        'bytes_sent': 0
    })
    
    # Time-based analysis
    hourly_stats = defaultdict(int)
    daily_stats = defaultdict(int)
    
    # Geographic analysis (simplified)
    country_stats = Counter()
    
    for log in logs:
        ip = log.get('ip', '-')
        if ip == '-':
            continue
            
        # IP statistics
        ip_stats[ip]['requests'] += 1
        ip_stats[ip]['methods'][log.get('method', '')] += 1
        ip_stats[ip]['status_codes'][log.get('status', '')] += 1
        ip_stats[ip]['user_agents'].add(log.get('user_agent', ''))
        ip_stats[ip]['paths'][log.get('path', '')] += 1
        
        # Time tracking
        try:
            timestamp = datetime.strptime(log['timestamp'], '%d/%b/%Y:%H:%M:%S')
            hour_key = timestamp.strftime('%Y-%m-%d %H:00')
            day_key = timestamp.strftime('%Y-%m-%d')
            
            hourly_stats[hour_key] += 1
            daily_stats[day_key] += 1
            
            if ip_stats[ip]['first_seen'] is None or timestamp < ip_stats[ip]['first_seen']:
                ip_stats[ip]['first_seen'] = timestamp
            if ip_stats[ip]['last_seen'] is None or timestamp > ip_stats[ip]['last_seen']:
                ip_stats[ip]['last_seen'] = timestamp
                
        except:
            pass
        
        # Bytes analysis
        try:
            bytes_sent = int(log.get('bytes_sent', 0))
            ip_stats[ip]['bytes_sent'] += bytes_sent
        except:
            pass
    
    # Convert sets to lists for JSON serialization
    for ip in ip_stats:
        ip_stats[ip]['user_agents'] = list(ip_stats[ip]['user_agents'])
        ip_stats[ip]['methods'] = dict(ip_stats[ip]['methods'])
        ip_stats[ip]['status_codes'] = dict(ip_stats[ip]['status_codes'])
        ip_stats[ip]['paths'] = dict(ip_stats[ip]['paths'])
    
    return {
        'ip_statistics': dict(ip_stats),
        'hourly_distribution': dict(hourly_stats),
        'daily_distribution': dict(daily_stats),
        'country_distribution': dict(country_stats)
    }

def detect_attack_patterns(logs):
    """Detect potential attack patterns in logs"""
    attack_patterns = {
        'sql_injection': [],
        'xss_attempts': [],
        'directory_traversal': [],
        'brute_force': [],
        'bot_traffic': [],
        'suspicious_paths': []
    }
    
    # SQL Injection patterns
    sql_patterns = [
        r'union\s+select', r'drop\s+table', r'insert\s+into',
        r'delete\s+from', r'update\s+set', r'exec\s*\(',
        r'xp_cmdshell', r'sp_executesql'
    ]
    
    # XSS patterns
    xss_patterns = [
        r'<script', r'javascript:', r'onload=', r'onerror=',
        r'<iframe', r'<object', r'<embed'
    ]
    
    # Directory traversal patterns
    traversal_patterns = [
        r'\.\./', r'\.\.\\', r'%2e%2e%2f', r'%2e%2e%5c'
    ]
    
    for i, log in enumerate(logs):
        path = log.get('path', '').lower()
        user_agent = log.get('user_agent', '').lower()
        
        # SQL Injection detection
        for pattern in sql_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                attack_patterns['sql_injection'].append({
                    'line': i + 1,
                    'ip': log.get('ip'),
                    'path': log.get('path'),
                    'timestamp': log.get('timestamp'),
                    'pattern': pattern
                })
        
        # XSS detection
        for pattern in xss_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                attack_patterns['xss_attempts'].append({
                    'line': i + 1,
                    'ip': log.get('ip'),
                    'path': log.get('path'),
                    'timestamp': log.get('timestamp'),
                    'pattern': pattern
                })
        
        # Directory traversal detection
        for pattern in traversal_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                attack_patterns['directory_traversal'].append({
                    'line': i + 1,
                    'ip': log.get('ip'),
                    'path': log.get('path'),
                    'timestamp': log.get('timestamp'),
                    'pattern': pattern
                })
        
        # Bot traffic detection
        bot_indicators = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
        if any(indicator in user_agent for indicator in bot_indicators):
            attack_patterns['bot_traffic'].append({
                'line': i + 1,
                'ip': log.get('ip'),
                'user_agent': log.get('user_agent'),
                'timestamp': log.get('timestamp')
            })
        
        # Suspicious paths
        suspicious_paths = ['admin', 'login', 'wp-admin', 'phpmyadmin', 'config', 'backup']
        if any(susp_path in path for susp_path in suspicious_paths):
            attack_patterns['suspicious_paths'].append({
                'line': i + 1,
                'ip': log.get('ip'),
                'path': log.get('path'),
                'timestamp': log.get('timestamp')
            })
    
    return attack_patterns

def analyze_user_behavior(logs):
    """Analyze user behavior patterns"""
    behavior_stats = {
        'session_analysis': {},
        'request_patterns': {},
        'anomaly_detection': {}
    }
    
    # Group by IP for session analysis
    ip_sessions = defaultdict(list)
    for log in logs:
        ip = log.get('ip', '-')
        if ip != '-':
            ip_sessions[ip].append(log)
    
    # Analyze each IP's behavior
    for ip, ip_logs in ip_sessions.items():
        if len(ip_logs) < 2:
            continue
            
        # Sort by timestamp
        try:
            ip_logs.sort(key=lambda x: datetime.strptime(x['timestamp'], '%d/%b/%Y:%H:%M:%S'))
        except:
            continue
        
        # Calculate session metrics
        session_duration = None
        if len(ip_logs) > 1:
            try:
                start_time = datetime.strptime(ip_logs[0]['timestamp'], '%d/%b/%Y:%H:%M:%S')
                end_time = datetime.strptime(ip_logs[-1]['timestamp'], '%d/%b/%Y:%H:%M:%S')
                session_duration = (end_time - start_time).total_seconds()
            except:
                pass
        
        # Request patterns
        methods = Counter(log.get('method', '') for log in ip_logs)
        status_codes = Counter(log.get('status', '') for log in ip_logs)
        paths = Counter(log.get('path', '') for log in ip_logs)
        
        # Calculate request rate
        request_rate = len(ip_logs) / max(session_duration / 3600, 1) if session_duration else 0
        
        behavior_stats['session_analysis'][ip] = {
            'total_requests': len(ip_logs),
            'session_duration': session_duration,
            'request_rate': request_rate,
            'methods': dict(methods),
            'status_codes': dict(status_codes),
            'unique_paths': len(paths),
            'top_paths': dict(paths.most_common(5))
        }
        
        # Anomaly detection
        anomalies = []
        if request_rate > 100:  # High request rate
            anomalies.append('High request rate')
        if len(paths) > 50:  # Many different paths
            anomalies.append('Excessive path exploration')
        if status_codes.get('404', 0) > len(ip_logs) * 0.5:  # High 404 rate
            anomalies.append('High 404 error rate')
        
        if anomalies:
            behavior_stats['anomaly_detection'][ip] = anomalies
    
    return behavior_stats

def main():
    """Main Streamlit application"""
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: white; margin: 0;">🛡️</h1>
            <h2 style="color: white; margin: 0;">Security Intel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Mode toggle
        ai_mode = st.checkbox("🤖 AI Enhanced Mode", value=st.session_state.ai_mode)
        st.session_state.ai_mode = ai_mode
        
        if ai_mode:
            st.markdown('<div class="ai-badge">AI Enhanced</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "Navigate",
            ["📊 Dashboard", "📁 Upload & Analysis", "📋 Log Browser", "🌐 IP Intelligence", "🤖 AI Insights", "📈 Reports", "⚙️ Settings"]
        )
    
    # Main content area
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "📁 Upload & Analysis":
        show_upload_analysis()
    elif page == "📋 Log Browser":
        show_log_browser()
    elif page == "🌐 IP Intelligence":
        show_ip_intelligence()
    elif page == "🤖 AI Insights":
        show_ai_insights()
    elif page == "📈 Reports":
        show_reports()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Display the main dashboard"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Advanced Security Intelligence Platform</h1>
        <p>AI-Powered Threat Detection & Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analysis_data:
        # Show analysis results
        display_analysis_dashboard()
    else:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h2>Welcome to Security Intelligence Platform</h2>
                <p style="font-size: 1.2rem; color: #64748b; margin: 2rem 0;">
                    Upload a log file to begin comprehensive security analysis and threat detection
                </p>
                <div style="margin: 2rem 0;">
                    <span style="background: #3b82f6; color: white; padding: 1rem 2rem; border-radius: 8px; font-size: 1.1rem;">
                        🚀 Get Started
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick stats if available
            if st.session_state.analysis_data:
                summary = st.session_state.analysis_data['summary']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📄 Total Logs", summary['total_logs'])
                with col2:
                    st.metric("🌐 Unique IPs", summary['unique_ips'])
                with col3:
                    st.metric("⚠️ High-Risk IPs", summary['high_risk_ips'])
                with col4:
                    st.metric("📈 Total Requests", st.session_state.analysis_data['data']['overall']['total_requests'])

def show_upload_analysis():
    """File upload and analysis section"""
    
    st.title("📁 File Upload & Analysis")
    
    # File upload section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a log file",
        type=['log', 'txt'],
        help="Upload your server access log file for analysis"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis options
    col1, col2 = st.columns(2)
    
    with col1:
        real_time_monitoring = st.checkbox("🔄 Enable Real-time Monitoring", value=False)
    
    with col2:
        deep_analysis = st.checkbox("🔍 Enable Deep Analysis", value=True, disabled=not st.session_state.ai_mode)
    
    # Analyze button
    if uploaded_file is not None:
        if st.button("🔍 Start Analysis", type="primary", use_container_width=True):
            perform_analysis(uploaded_file, real_time_monitoring, deep_analysis)
    
    # Display current analysis results
    if st.session_state.analysis_data:
        st.success("✅ Analysis Complete!")
        display_analysis_results()

def show_log_browser():
    """Interactive log browser with detailed analysis"""
    
    st.title("📋 Log Browser & Detailed Analysis")
    
    if not st.session_state.raw_logs:
        st.info("Please upload and analyze a log file first to access the log browser.")
        return
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "🔍 Log Entries", "🚨 Attack Patterns", "👤 User Behavior", "📈 Time Analysis"
    ])
    
    with tab1:
        show_log_overview()
    
    with tab2:
        show_log_entries()
    
    with tab3:
        show_attack_patterns()
    
    with tab4:
        show_user_behavior()
    
    with tab5:
        show_time_analysis()

def show_log_overview():
    """Show comprehensive log overview"""
    
    metadata = st.session_state.log_metadata
    detailed_stats = st.session_state.detailed_stats
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total Log Entries", metadata.get('total_lines', 0))
    
    with col2:
        st.metric("🌐 Unique IPs", metadata.get('unique_ips', 0))
    
    with col3:
        st.metric("🔧 Unique User Agents", metadata.get('unique_user_agents', 0))
    
    with col4:
        time_span = metadata.get('time_span', {})
        if time_span:
            duration = time_span.get('duration')
            if duration:
                st.metric("⏱️ Time Span", f"{duration.days}d {duration.seconds//3600}h")
    
    # HTTP Methods Distribution
    st.subheader("📊 HTTP Methods Distribution")
    methods = metadata.get('http_methods', {})
    if methods:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_methods = px.pie(
                values=list(methods.values()),
                names=list(methods.keys()),
                title="HTTP Methods"
            )
            st.plotly_chart(fig_methods, use_container_width=True)
        
        with col2:
            # Status codes
            status_codes = metadata.get('status_codes', {})
            if status_codes:
                fig_status = px.bar(
                    x=list(status_codes.keys()),
                    y=list(status_codes.values()),
                    title="Status Codes Distribution"
                )
                st.plotly_chart(fig_status, use_container_width=True)
    
    # Top Paths
    st.subheader("🔗 Most Requested Paths")
    top_paths = metadata.get('top_paths', [])
    if top_paths:
        df_paths = pd.DataFrame(top_paths, columns=['Path', 'Count'])
        st.dataframe(df_paths, use_container_width=True)
    
    # File Extensions
    st.subheader("📁 File Extensions")
    extensions = metadata.get('file_extensions', {})
    if extensions:
        fig_ext = px.bar(
            x=list(extensions.keys()),
            y=list(extensions.values()),
            title="File Extensions Requested"
        )
        st.plotly_chart(fig_ext, use_container_width=True)

def show_log_entries():
    """Show detailed log entries with filtering"""
    
    logs = st.session_state.raw_logs
    
    # Filters
    st.subheader("🔍 Log Entry Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # IP filter
        unique_ips = list(set(log['ip'] for log in logs if log['ip'] != '-'))
        selected_ip = st.selectbox("Filter by IP", ["All"] + unique_ips)
    
    with col2:
        # Status code filter
        unique_status = list(set(log.get('status', '') for log in logs))
        selected_status = st.selectbox("Filter by Status Code", ["All"] + unique_status)
    
    with col3:
        # Method filter
        unique_methods = list(set(log.get('method', '') for log in logs))
        selected_method = st.selectbox("Filter by Method", ["All"] + unique_methods)
    
    # Search
    search_term = st.text_input("🔍 Search in logs", placeholder="Enter search term...")
    
    # Apply filters
    filtered_logs = logs
    
    if selected_ip != "All":
        filtered_logs = [log for log in filtered_logs if log['ip'] == selected_ip]
    
    if selected_status != "All":
        filtered_logs = [log for log in filtered_logs if log.get('status', '') == selected_status]
    
    if selected_method != "All":
        filtered_logs = [log for log in filtered_logs if log.get('method', '') == selected_method]
    
    if search_term:
        filtered_logs = [log for log in filtered_logs if search_term.lower() in str(log).lower()]
    
    # Display results
    st.subheader(f"📋 Log Entries ({len(filtered_logs)} of {len(logs)})")
    
    # Pagination
    page_size = st.selectbox("Entries per page", [50, 100, 200, 500], index=1)
    total_pages = (len(filtered_logs) + page_size - 1) // page_size
    
    if total_pages > 1:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_logs = filtered_logs[start_idx:end_idx]
    else:
        page_logs = filtered_logs
    
    # Display logs
    for i, log in enumerate(page_logs):
        with st.expander(f"Line {start_idx + i + 1}: {log.get('ip', 'N/A')} - {log.get('method', 'N/A')} {log.get('path', 'N/A')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**IP:** {log.get('ip', 'N/A')}")
                st.write(f"**Timestamp:** {log.get('timestamp', 'N/A')}")
                st.write(f"**Method:** {log.get('method', 'N/A')}")
                st.write(f"**Path:** {log.get('path', 'N/A')}")
            
            with col2:
                st.write(f"**Status:** {log.get('status', 'N/A')}")
                st.write(f"**Bytes:** {log.get('bytes_sent', 'N/A')}")
                st.write(f"**Referer:** {log.get('referer', 'N/A')}")
                st.write(f"**User Agent:** {log.get('user_agent', 'N/A')[:100]}...")

def show_attack_patterns():
    """Show detected attack patterns"""
    
    logs = st.session_state.raw_logs
    attack_patterns = detect_attack_patterns(logs)
    
    st.subheader("🚨 Detected Attack Patterns")
    
    # Summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("SQL Injection", len(attack_patterns['sql_injection']))
    
    with col2:
        st.metric("XSS Attempts", len(attack_patterns['xss_attempts']))
    
    with col3:
        st.metric("Directory Traversal", len(attack_patterns['directory_traversal']))
    
    with col4:
        st.metric("Bot Traffic", len(attack_patterns['bot_traffic']))
    
    # Detailed patterns
    pattern_types = [
        ('sql_injection', 'SQL Injection Attempts', '🔴'),
        ('xss_attempts', 'XSS Attempts', '🟡'),
        ('directory_traversal', 'Directory Traversal', '🟠'),
        ('bot_traffic', 'Bot Traffic', '🔵'),
        ('suspicious_paths', 'Suspicious Paths', '🟣')
    ]
    
    for pattern_key, pattern_name, emoji in pattern_types:
        if attack_patterns[pattern_key]:
            with st.expander(f"{emoji} {pattern_name} ({len(attack_patterns[pattern_key])})"):
                df = pd.DataFrame(attack_patterns[pattern_key])
                st.dataframe(df, use_container_width=True)

def show_user_behavior():
    """Show user behavior analysis"""
    
    logs = st.session_state.raw_logs
    behavior_stats = analyze_user_behavior(logs)
    
    st.subheader("👤 User Behavior Analysis")
    
    # Session analysis
    session_data = behavior_stats['session_analysis']
    anomaly_data = behavior_stats['anomaly_detection']
    
    # Top active IPs
    st.subheader("🔥 Most Active IPs")
    if session_data:
        # Sort by total requests
        sorted_ips = sorted(session_data.items(), key=lambda x: x[1]['total_requests'], reverse=True)
        
        for ip, stats in sorted_ips[:10]:
            with st.expander(f"🌐 {ip} - {stats['total_requests']} requests"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Total Requests:** {stats['total_requests']}")
                    st.write(f"**Session Duration:** {stats['session_duration']:.2f}s" if stats['session_duration'] else "**Session Duration:** N/A")
                    st.write(f"**Request Rate:** {stats['request_rate']:.2f} req/hour")
                    st.write(f"**Unique Paths:** {stats['unique_paths']}")
                
                with col2:
                    st.write("**HTTP Methods:**")
                    for method, count in stats['methods'].items():
                        st.write(f"  • {method}: {count}")
                    
                    st.write("**Status Codes:**")
                    for status, count in stats['status_codes'].items():
                        st.write(f"  • {status}: {count}")
    
    # Anomaly detection
    if anomaly_data:
        st.subheader("⚠️ Anomaly Detection")
        for ip, anomalies in anomaly_data.items():
            st.warning(f"🌐 {ip}: {', '.join(anomalies)}")

def show_time_analysis():
    """Show time-based analysis"""
    
    detailed_stats = st.session_state.detailed_stats
    
    st.subheader("📈 Time-Based Analysis")
    
    # Hourly distribution
    hourly_data = detailed_stats.get('hourly_distribution', {})
    if hourly_data:
        st.subheader("🕐 Hourly Request Distribution")
        
        # Convert to DataFrame for plotting
        hours = []
        counts = []
        for hour_key, count in sorted(hourly_data.items()):
            hours.append(hour_key)
            counts.append(count)
        
        if hours and counts:
            df_hourly = pd.DataFrame({'Hour': hours, 'Requests': counts})
            fig_hourly = px.line(df_hourly, x='Hour', y='Requests', title='Requests Over Time')
            st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Daily distribution
    daily_data = detailed_stats.get('daily_distribution', {})
    if daily_data:
        st.subheader("📅 Daily Request Distribution")
        
        days = []
        counts = []
        for day_key, count in sorted(daily_data.items()):
            days.append(day_key)
            counts.append(count)
        
        if days and counts:
            df_daily = pd.DataFrame({'Day': days, 'Requests': counts})
            fig_daily = px.bar(df_daily, x='Day', y='Requests', title='Daily Request Volume')
            st.plotly_chart(fig_daily, use_container_width=True)

def perform_analysis(uploaded_file, real_time_monitoring, deep_analysis):
    """Perform security analysis on uploaded file"""
    
    # Create progress containers
    progress_container = st.container()
    status_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Save uploaded file temporarily
        with open("temp_log.log", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Step 1: Parse log file
        status_text.text("📄 Parsing log file...")
        progress_bar.progress(20)
        
        logs = parse_log_file("temp_log.log")
        unique_ips = set(l["ip"] for l in logs if l["ip"] != "-")
        
        # Step 2: CTI lookups
        status_text.text("🌐 Performing CTI lookups...")
        progress_bar.progress(40)
        
        high_risk_ips = []
        ip_cti_mapping = {}
        for ip in unique_ips:
            cti = get_cti_data(ip)
            ip_cti_mapping[ip] = cti
            if (cti['abuse_score'] and cti['abuse_score'] > 50) or cti['web_reputation'] in ['Untrusted', 'Questionable']:
                high_risk_ips.append(ip)
        
        # Step 3: Statistical analysis
        status_text.text("📊 Analyzing statistics...")
        progress_bar.progress(60)
        
        stats, overall = analyze_stats(logs, high_risk_ips)
        ua_stats = analyze_user_agents(logs, high_risk_ips)
        
        # Step 4: AI analysis
        status_text.text("🤖 Generating AI analysis...")
        progress_bar.progress(80)
        
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
        
        # Store results
        st.session_state.analysis_data = {
            'data': final_data,
            'summary': {
                'total_logs': len(logs),
                'unique_ips': len(unique_ips),
                'high_risk_ips': len(high_risk_ips),
                'high_risk_list': high_risk_ips
            }
        }
        
        # Store raw logs and detailed analysis
        st.session_state.raw_logs = logs
        st.session_state.log_metadata = analyze_log_metadata(logs)
        st.session_state.detailed_stats = generate_detailed_statistics(logs)
        
        # Complete
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        st.session_state.analysis_complete = True
        
        # Clean up temp file
        os.remove("temp_log.log")
        
        # Auto-refresh to show results
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ Analysis failed")

def display_analysis_dashboard():
    """Display the analysis dashboard with metrics and charts"""
    
    if not st.session_state.analysis_data:
        return
    
    summary = st.session_state.analysis_data['summary']
    data = st.session_state.analysis_data['data']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📄 Total Log Entries",
            value=summary['total_logs'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="🌐 Unique IPs",
            value=summary['unique_ips'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="⚠️ High-Risk IPs",
            value=summary['high_risk_ips'],
            delta=None
        )
    
    with col4:
        st.metric(
            label="📈 Total Requests",
            value=data['overall']['total_requests'],
            delta=None
        )
    
    # Risk level distribution
    st.subheader("🎯 Risk Level Distribution")
    
    risk_data = []
    for ip in summary['high_risk_list']:
        ip_data = data['ips'][ip]
        risk_level = "HIGH" if ip_data['cti']['abuse_score'] >= 75 else "MEDIUM"
        risk_data.append({
            'IP': ip,
            'Risk Level': risk_level,
            'Abuse Score': ip_data['cti']['abuse_score'],
            'Country': ip_data['cti']['country'],
            'Total Requests': ip_data['stats']['total_requests']
        })
    
    if risk_data:
        df_risk = pd.DataFrame(risk_data)
        
        # Risk level pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            risk_counts = df_risk['Risk Level'].value_counts()
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Level Distribution",
                color_discrete_map={'HIGH': '#ef4444', 'MEDIUM': '#f59e0b'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Abuse score distribution
            fig_hist = px.histogram(
                df_risk,
                x='Abuse Score',
                title="Abuse Score Distribution",
                color='Risk Level',
                color_discrete_map={'HIGH': '#ef4444', 'MEDIUM': '#f59e0b'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Detailed risk table
        st.subheader("🚨 High-Risk IP Details")
        st.dataframe(df_risk, use_container_width=True)

def display_analysis_results():
    """Display detailed analysis results"""
    
    if not st.session_state.analysis_data:
        return
    
    summary = st.session_state.analysis_data['summary']
    data = st.session_state.analysis_data['data']
    
    st.subheader("📊 Analysis Results")
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📄 {summary['total_logs']}</h3>
            <p>Total Log Entries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌐 {summary['unique_ips']}</h3>
            <p>Unique IPs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚠️ {summary['high_risk_ips']}</h3>
            <p>High-Risk IPs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 {data['overall']['total_requests']}</h3>
            <p>Total Requests</p>
        </div>
        """, unsafe_allow_html=True)

def show_ip_intelligence():
    """IP Intelligence and geolocation section"""
    
    st.title("🌐 IP Intelligence & Geolocation")
    
    if not st.session_state.analysis_data:
        st.info("Please upload and analyze a log file first.")
        return
    
    data = st.session_state.analysis_data['data']
    summary = st.session_state.analysis_data['summary']
    
    # IP details
    st.subheader("🔍 IP Analysis Details")
    
    for ip in summary['high_risk_list']:
        ip_data = data['ips'][ip]
        risk_level = "HIGH" if ip_data['cti']['abuse_score'] >= 75 else "MEDIUM"
        risk_class = "risk-high" if risk_level == "HIGH" else "risk-medium"
        
        with st.expander(f"🌐 {ip} - {risk_level} Risk"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**CTI Data:**")
                st.write(f"• Abuse Score: {ip_data['cti']['abuse_score']}")
                st.write(f"• Total Reports: {ip_data['cti']['total_reports']}")
                st.write(f"• Country: {ip_data['cti']['country']}")
                st.write(f"• Web Reputation: {ip_data['cti']['web_reputation']}")
                st.write(f"• Owner: {ip_data['cti']['owner']}")
            
            with col2:
                st.markdown("**Statistics:**")
                st.write(f"• Total Requests: {ip_data['stats']['total_requests']}")
                st.write(f"• Client Errors: {ip_data['stats']['client_errors']}")
                st.write(f"• Suspicious Agents: {', '.join(ip_data['user_agents']['suspicious_agents']) if ip_data['user_agents']['suspicious_agents'] else 'None'}")
                st.write(f"• High Priority: {'Yes' if ip_data['user_agents']['high_priority'] else 'No'}")
            
            st.markdown("**AI Analysis:**")
            st.write(ip_data['ai_note'])

def show_ai_insights():
    """AI-powered insights section"""
    
    st.title("🤖 AI-Powered Security Insights")
    
    if not st.session_state.ai_mode:
        st.warning("AI Enhanced Mode is not enabled. Enable it in the sidebar to access AI insights.")
        return
    
    if not st.session_state.analysis_data:
        st.info("Please upload and analyze a log file first.")
        return
    
    data = st.session_state.analysis_data['data']
    
    # Advanced AI Analysis
    st.subheader("🧠 Advanced AI Analysis")
    
    st.markdown(f"""
    <div class="metric-card">
        <h4>AI Security Assessment</h4>
        <p>{data['advanced_ai']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Recommendations
    st.subheader("💡 AI Recommendations")
    
    recommendations = [
        "🔍 Monitor IPs with abuse scores above 75 for immediate blocking",
        "🛡️ Implement rate limiting for suspicious IP addresses",
        "📊 Set up automated alerts for high-risk traffic patterns",
        "🌐 Consider geo-blocking for countries with high threat levels",
        "🤖 Enable continuous AI monitoring for real-time threat detection"
    ]
    
    for rec in recommendations:
        st.markdown(f"• {rec}")

def show_reports():
    """Reports and analytics section"""
    
    st.title("📈 Reports & Analytics")
    
    if not st.session_state.analysis_data:
        st.info("Please upload and analyze a log file first.")
        return
    
    # Export options
    st.subheader("📄 Export Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export to CSV", use_container_width=True):
            export_to_csv()
    
    with col2:
        if st.button("📝 Export to Markdown", use_container_width=True):
            export_to_markdown()
    
    with col3:
        if st.button("📈 Export to JSON", use_container_width=True):
            export_to_json()

def show_settings():
    """Settings and configuration section"""
    
    st.title("⚙️ Settings & Configuration")
    
    st.subheader("🔧 Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Risk Score Threshold", min_value=0, max_value=100, value=50)
        st.number_input("Request Rate Limit", min_value=1, max_value=1000, value=100)
    
    with col2:
        st.selectbox("Default Analysis Mode", ["Standard", "Deep", "AI Enhanced"])
        st.checkbox("Enable Real-time Monitoring", value=False)
    
    st.subheader("🌐 API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("AbuseIPDB API Key", type="password")
        st.text_input("VirusTotal API Key", type="password")
    
    with col2:
        st.text_input("Mistral AI API Key", type="password")
        st.selectbox("AI Model", ["mistral-tiny", "mistral-small", "mistral-medium"])

def export_to_csv():
    """Export analysis results to CSV"""
    if st.session_state.analysis_data:
        try:
            # Export high-risk IPs data
            data = st.session_state.analysis_data['data']
            summary = st.session_state.analysis_data['summary']
            
            # Create CSV data
            csv_data = []
            for ip in summary['high_risk_list']:
                ip_data = data['ips'][ip]
                csv_data.append({
                    'IP': ip,
                    'Abuse_Score': ip_data['cti']['abuse_score'],
                    'Total_Reports': ip_data['cti']['total_reports'],
                    'Country': ip_data['cti']['country'],
                    'Web_Reputation': ip_data['cti']['web_reputation'],
                    'Owner': ip_data['cti']['owner'],
                    'Total_Requests': ip_data['stats']['total_requests'],
                    'Client_Errors': ip_data['stats']['client_errors'],
                    'AI_Note': ip_data['ai_note']
                })
            
            df = pd.DataFrame(csv_data)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="📊 Download CSV Report",
                data=csv,
                file_name=f"security_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            st.success("✅ CSV export ready for download!")
            
        except Exception as e:
            st.error(f"❌ CSV export failed: {str(e)}")

def export_to_markdown():
    """Export analysis results to Markdown"""
    if st.session_state.analysis_data:
        try:
            data = st.session_state.analysis_data['data']
            summary = st.session_state.analysis_data['summary']
            metadata = st.session_state.log_metadata
            
            # Generate markdown report
            markdown_content = f"""# Security Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Total Log Entries:** {summary['total_logs']:,}
- **Unique IPs:** {summary['unique_ips']:,}
- **High-Risk IPs:** {summary['high_risk_ips']:,}
- **Total Requests:** {data['overall']['total_requests']:,}

## High-Risk IP Analysis

"""
            
            for ip in summary['high_risk_list']:
                ip_data = data['ips'][ip]
                markdown_content += f"""### {ip}
- **Abuse Score:** {ip_data['cti']['abuse_score']}
- **Total Reports:** {ip_data['cti']['total_reports']}
- **Country:** {ip_data['cti']['country']}
- **Web Reputation:** {ip_data['cti']['web_reputation']}
- **Total Requests:** {ip_data['stats']['total_requests']}
- **AI Analysis:** {ip_data['ai_note']}

"""
            
            markdown_content += f"""## Log Metadata
- **Time Span:** {metadata.get('time_span', {}).get('start', 'N/A')} to {metadata.get('time_span', {}).get('end', 'N/A')}
- **HTTP Methods:** {', '.join(metadata.get('http_methods', {}).keys())}
- **Status Codes:** {', '.join(metadata.get('status_codes', {}).keys())}

## AI Advanced Analysis
{data['advanced_ai']}
"""
            
            st.download_button(
                label="📝 Download Markdown Report",
                data=markdown_content,
                file_name=f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
            st.success("✅ Markdown export ready for download!")
            
        except Exception as e:
            st.error(f"❌ Markdown export failed: {str(e)}")

def export_to_json():
    """Export analysis results to JSON"""
    if st.session_state.analysis_data:
        try:
            # Prepare comprehensive JSON data
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'analysis_data': st.session_state.analysis_data,
                'log_metadata': st.session_state.log_metadata,
                'detailed_stats': st.session_state.detailed_stats,
                'attack_patterns': detect_attack_patterns(st.session_state.raw_logs),
                'user_behavior': analyze_user_behavior(st.session_state.raw_logs)
            }
            
            json_data = json.dumps(export_data, indent=2, default=str)
            
            st.download_button(
                label="📈 Download JSON Report",
                data=json_data,
                file_name=f"security_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            st.success("✅ JSON export ready for download!")
            
        except Exception as e:
            st.error(f"❌ JSON export failed: {str(e)}")

if __name__ == "__main__":
    main()
