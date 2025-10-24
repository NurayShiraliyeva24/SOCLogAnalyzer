from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import tempfile
from main import (
    parse_log_file, get_cti_data, analyze_stats, 
    analyze_user_agents, ai_note, advanced_ai_analysis
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_logs():
    try:
        if 'logfile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['logfile']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.log') as temp_file:
            content = file.read().decode('utf-8')
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse logs
            logs = parse_log_file(temp_file_path)
            unique_ips = set(l["ip"] for l in logs if l["ip"] != "-")
            
            # High-Risk IP Detection
            high_risk_ips = []
            ip_cti_mapping = {}
            for ip in unique_ips:
                cti = get_cti_data(ip)
                ip_cti_mapping[ip] = cti
                if (cti['abuse_score'] and cti['abuse_score'] > 50) or cti['web_reputation'] in ['Untrusted', 'Questionable']:
                    high_risk_ips.append(ip)
            
            # Analysis
            stats, overall = analyze_stats(logs, high_risk_ips)
            ua_stats = analyze_user_agents(logs, high_risk_ips)
            
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
            
            return jsonify({
                'success': True,
                'data': final_data,
                'summary': {
                    'total_logs': len(logs),
                    'unique_ips': len(unique_ips),
                    'high_risk_ips': len(high_risk_ips),
                    'high_risk_list': high_risk_ips
                }
            })
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_report', methods=['POST'])
def download_report():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create temporary report file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md') as temp_file:
            md_content = "# Security Analysis Report\n\n"
            
            for ip, ip_data in data.get('ips', {}).items():
                md_content += f"## IP: {ip}\n"
                cti = ip_data.get('cti', {})
                stats = ip_data.get('stats', {})
                ua = ip_data.get('user_agents', {})
                
                md_content += f"- **CTI Data:**\n"
                md_content += f"  - Abuse Score: {cti.get('abuse_score', 'N/A')}\n"
                md_content += f"  - Total Reports: {cti.get('total_reports', 'N/A')}\n"
                md_content += f"  - Country: {cti.get('country', 'N/A')}\n"
                md_content += f"  - Web Reputation: {cti.get('web_reputation', 'N/A')}\n"
                md_content += f"  - Owner: {cti.get('owner', 'N/A')}\n"
                md_content += f"  - Malicious Vendors: {cti.get('malicious_vendors', 'N/A')}\n"
                
                md_content += f"- **Statistics:**\n"
                md_content += f"  - Total Requests: {stats.get('total_requests', 'N/A')}\n"
                md_content += f"  - Client Errors: {stats.get('client_errors', 'N/A')}\n"
                
                md_content += f"- **AI Analysis:** {ip_data.get('ai_note', 'N/A')}\n"
                
                md_content += f"- **User Agents:**\n"
                md_content += f"  - Suspicious Agents: {ua.get('suspicious_agents', [])}\n"
                md_content += f"  - High Priority: {ua.get('high_priority', False)}\n\n"
            
            overall = data.get('overall', {})
            md_content += f"### Overall Statistics\n"
            md_content += f"- Total Requests: {overall.get('total_requests', 'N/A')}\n"
            md_content += f"- Unique IPs: {overall.get('unique_ips', 'N/A')}\n"
            md_content += f"- 404/200 Ratio: {overall.get('ratio_404_200', 'N/A')}\n\n"
            
            md_content += f"### Advanced AI Analysis\n"
            md_content += f"{data.get('advanced_ai', 'N/A')}\n"
            
            temp_file.write(md_content)
            temp_file_path = temp_file.name
        
        return send_file(temp_file_path, as_attachment=True, download_name='security_report.md')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
