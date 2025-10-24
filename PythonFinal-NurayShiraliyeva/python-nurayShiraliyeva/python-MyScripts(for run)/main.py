import os
import json
import argparse
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# -----------------------------
# --- Mistral AI API Client Setup ---
# -----------------------------
MISTRAL_API_KEY = "uKtNxfeeArkKqT9q8Zsm57NVue2upwvP"  # Mistral API key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  # Mistral endpoint

def mistral_generate_text(prompt, max_tokens=120):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-tiny",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        r = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        result = r.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except RequestException as e:
        print(f"[!] Mistral API error: {e}")
        return "AI analysis not available."

# -----------------------------
# --- Step 1: Log Parsing ---
# -----------------------------
def parse_log_file(filepath):
    logs = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    json_part = line[line.find("{"):]
                    data = json.loads(json_part)
                    logs.append({
                        "ip": data.get("remote_addr", "-"),
                        "timestamp": data.get("timestamp", "-"),
                        "method": data.get("method", "-"),
                        "path": data.get("uri", "-"),
                        "status": int(data.get("status", -1)),
                        "user_agent": data.get("user_agent", "-")
                    })
                except (ValueError, json.JSONDecodeError):
                    print(f"[!] Line {i} skipped: Malformed log line")
    except FileNotFoundError:
        print(f"[!] Log file not found: {filepath}")
        exit(1)
    print(f"[✓] Parsed {len(logs)} valid log entries")
    return logs

# -----------------------------
# --- Step 2: CTI Integration ---
# -----------------------------
ABUSEIPDB_API_KEY = "5a21b708c97103f3c51a8303ddb4052168464328e82c404b4a88e47557e6f38baa41f7555efa1c91"
VT_API_KEY = "a77b73084778d17f25ff760e405f27ef3e90aaedca0eca032a2cdf2f599622e9"

def abuseipdb_lookup(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Accept": "application/json", "Key": ABUSEIPDB_API_KEY}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()["data"]
        return {
            "abuse_score": data.get("abuseConfidenceScore", 0),
            "total_reports": data.get("totalReports", 0),
            "country": data.get("countryCode", "Unknown")
        }
    except RequestException as e:
        print(f"[!] AbuseIPDB error for {ip}: {e}")
        return {"abuse_score": 0, "total_reports": 0, "country": "Unknown"}

def virustotal_lookup(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        analysis_stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        return analysis_stats.get("malicious", 0)
    except RequestException as e:
        print(f"[!] VirusTotal error for {ip}: {e}")
        return 0

def talos_lookup(ip):
    """Talos lookup with 403 handling"""
    url = f"https://talosintelligence.com/reputation_center/lookup?search={ip}"
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        web_reputation = soup.select_one(".reputation_status").text.strip() if soup.select_one(".reputation_status") else "Unknown"
        owner = soup.select_one(".owner_info").text.strip() if soup.select_one(".owner_info") else "Unknown"
        return {"web_reputation": web_reputation, "owner": owner}
    except RequestException:
        return {"web_reputation": "Unavailable", "owner": "Unavailable"}

def get_cti_data(ip):
    abuse = abuseipdb_lookup(ip)
    vt = virustotal_lookup(ip)
    talos = talos_lookup(ip)
    return {
        "abuse_score": abuse["abuse_score"],
        "total_reports": abuse["total_reports"],
        "country": abuse["country"],
        "web_reputation": talos["web_reputation"],
        "owner": talos["owner"],
        "malicious_vendors": vt
    }

# -----------------------------
# --- Step 3: Statistical Analysis ---
# -----------------------------
def analyze_stats(logs, high_risk_ips):
    stats = {}
    overall_requests = len(logs)
    overall_404 = sum(1 for l in logs if l["status"] == 404)
    unique_ips = len(set(l["ip"] for l in logs if l["ip"] != "-"))

    for ip in high_risk_ips:
        ip_logs = [l for l in logs if l["ip"] == ip]
        total_requests = len(ip_logs)
        client_errors = sum(1 for l in ip_logs if 400 <= l["status"] < 500)
        stats[ip] = {"total_requests": total_requests, "client_errors": client_errors}

    overall = {
        "total_requests": overall_requests,
        "unique_ips": unique_ips,
        "ratio_404_200": overall_404 / overall_requests if overall_requests else 0
    }
    return stats, overall

# -----------------------------
# --- Step 4: AI Note (Mistral) ---
# -----------------------------
def ai_note(ip, cti, stats):
    prompt = f"""
    Provide a concise security analysis for IP {ip}:
    - Abuse Score: {cti['abuse_score']}
    - Web Reputation: {cti['web_reputation']}
    - Total Requests: {stats['total_requests']}
    - Client Errors: {stats['client_errors']}
    - Malicious Vendors: {cti['malicious_vendors']}
    
    Give a brief 2-3 sentence assessment of the risk level and key concerns.
    """
    return mistral_generate_text(prompt, max_tokens=120)

# -----------------------------
# --- Step 6: User-Agent Correlation ---
# -----------------------------
SUSPICIOUS_AGENTS = ["sqlmap", "nmap", "hydra", "nikto", "curl", "python-requests"]

def analyze_user_agents(logs, high_risk_ips):
    ua_stats = {}
    for ip in high_risk_ips:
        ip_logs = [l for l in logs if l["ip"] == ip]
        detected = [ua for l in ip_logs for ua in SUSPICIOUS_AGENTS if ua in l["user_agent"].lower()]
        ua_stats[ip] = {"suspicious_agents": list(set(detected)), "high_priority": bool(detected)}
    return ua_stats

# -----------------------------
# --- Step 7: Advanced AI Analysis (Mistral) ---
# -----------------------------
def advanced_ai_analysis(overall_stats, high_risk_ips):
    prompt = f"""
    Analyze server traffic patterns for security threats:
    - Total Requests: {overall_stats['total_requests']}
    - Unique IPs: {overall_stats['unique_ips']}
    - 404/200 Ratio: {overall_stats['ratio_404_200']}
    - High-Risk IPs: {high_risk_ips}
    
    Provide a brief 3-4 sentence summary of key security concerns and patterns.
    """
    return mistral_generate_text(prompt, max_tokens=150)

# -----------------------------
# --- Step 8: Reporting ---
# -----------------------------
def save_report(final_data, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    md_path = os.path.join(output_dir, "final_report.md")
    html_path = os.path.join(output_dir, "final_report.html")

    md_content = "# Security Analysis Report\n\n"
    for ip, data in final_data["ips"].items():
        md_content += f"## IP: {ip}\n"
        md_content += f"- CTI: Abuse Score={data['cti']['abuse_score']}, Total Reports={data['cti']['total_reports']}, Country={data['cti']['country']}, Web Reputation={data['cti']['web_reputation']}, Owner={data['cti']['owner']}, Malicious Vendors={data['cti']['malicious_vendors']}\n"
        md_content += f"- Stats: Total Requests={data['stats']['total_requests']}, Client Errors={data['stats']['client_errors']}\n"
        md_content += f"- AI Note: {data['ai_note']}\n"
        md_content += f"- User-Agent: Suspicious Agents={data['user_agents']['suspicious_agents']}, High Priority={data['user_agents']['high_priority']}\n\n"

    md_content += f"### Overall Stats\n"
    md_content += f"- Total Requests: {final_data['overall']['total_requests']}\n"
    md_content += f"- Unique IPs: {final_data['overall']['unique_ips']}\n"
    md_content += f"- 404/200 Ratio: {final_data['overall']['ratio_404_200']}\n\n"
    md_content += f"### Advanced AI Analysis\n- {final_data['advanced_ai']}\n"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    html_content = md_content.replace("\n", "<br>").replace("# ", "<h1>").replace("## ", "<h2>").replace("### ", "<h3>")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] Reports saved: {md_path}, {html_path}")

# -----------------------------
# --- Main CLI ---
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="SOC Log Analysis Tool")
    parser.add_argument("--logfile", required=True, help="Path to access.log")
    parser.add_argument("--output-dir", default="reports", help="Directory to save reports")
    args = parser.parse_args()

    logs = parse_log_file(args.logfile)
    unique_ips = set(l["ip"] for l in logs if l["ip"] != "-")

    # --- High-Risk IP Detection ---
    high_risk_ips = []
    ip_cti_mapping = {}
    for ip in unique_ips:
        cti = get_cti_data(ip)
        ip_cti_mapping[ip] = cti
        if (cti['abuse_score'] and cti['abuse_score'] > 50) or cti['web_reputation'] in ['Untrusted', 'Questionable']:
            high_risk_ips.append(ip)

    final_data = {"ips": {}, "overall": {}, "advanced_ai": ""}
    stats, overall = analyze_stats(logs, high_risk_ips)
    ua_stats = analyze_user_agents(logs, high_risk_ips)

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
    save_report(final_data, args.output_dir)

if __name__ == "__main__":
    main()                                           