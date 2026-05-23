# 🔍 Smart Recon & Attack Surface Mapper

A powerful, intelligent web reconnaissance tool designed for security researchers, penetration testers, and security professionals to identify and analyze exposed endpoints, vulnerable paths, and potential attack vectors on target websites.

![Python Version](https://img.shields.io/badge/Python-3.1%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [GUI Mode](#gui-mode)
  - [CLI Mode](#cli-mode)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## 📖 Overview

Smart Recon is an advanced reconnaissance engine that crawls web applications to discover endpoints, analyze security risks, and prioritize targets for further investigation. It combines intelligent web crawling, risk scoring algorithms, and smart prioritization to help security professionals identify the most critical attack surface areas.

**Key Capability**: Discover hundreds of endpoints and instantly rank them by security risk using our weighted prioritization system.

---

## ✨ Features

### 🕷️ **Intelligent Web Crawler**
- Crawls HTML, XML, and dynamic web content
- Discovers endpoints from multiple sources (links, forms, scripts, iframes)
- Handles redirects, cookies, and custom headers
- Configurable crawl depth and page limits (up to 80 pages)
- Smart error handling for non-200 status codes

### 🎯 **Advanced Risk Scoring**
- **50+ Security Keywords** with weighted scoring
- Detects sensitive paths (admin, login, dashboard, API endpoints)
- Identifies risky file extensions (.env, .bak, .old, .php, .asp)
- Query parameter analysis
- WordPress-specific detection
- Normalized risk scores (0-100 scale)

### 🏆 **Smart Prioritization Engine**
- **Weighted Greedy Algorithm** combining:
  - Risk Score (primary factor)
  - Path Importance Bonuses
  - Depth Penalty (shallow paths prioritized)
- Identifies top targets for manual testing
- Supports custom bonus rules for specific endpoints

### 📊 **Comprehensive Reporting**
- **CSV Export**: Quick tabular view of priority targets
- **JSON Export**: Complete detailed reports with metadata
- Real-time scanning progress display
- Categorized risk levels (Critical, High, Medium)
- Discovered forms, JavaScript files, and error pages

### 🖥️ **User-Friendly GUI**
- Dark theme interface (modern and clean)
- Real-time progress tracking
- Adjustable scan parameters (max pages, crawl delay)
- One-click exports
- Color-coded risk indicators
- Scrollable log output with timestamp

---

## 🚀 Installation

### Prerequisites
- Python 3.1 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/smart-recon.git
cd smart-recon
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
```
requests>=2.28.0
beautifulsoup4>=4.11.0
```

### Step 3: Run the Application
```bash
python main.py
```

---

## 📖 Usage

### GUI Mode (Recommended)

1. **Launch the application:**
   ```bash
   python main.py
   ```

2. **Enter target URL:**
   - Paste or type your target domain (e.g., `example.com` or `https://example.com`)
   - The tool automatically adds `https://` if missing

3. **Configure scan parameters:**
   - **Max Pages**: Number of pages to crawl (default: 80)
   - **Crawl Delay**: Seconds between requests (default: 0.6s)

4. **Start scan:**
   - Click the **"Start Recon"** button
   - Monitor progress in real-time

5. **Export results:**
   - **CSV Export**: High-risk endpoints in tabular format
   - **Full Report**: Complete JSON report with all endpoints and metadata
   - **Clear Logs**: Reset the interface for a new scan

### CLI Mode (Direct Engine Usage)

```python
from scanner import ReconEngine

engine = ReconEngine()
result = engine.run("https://example.com", max_pages=50)

# Access results
endpoints = result["endpoints"]           # All discovered endpoints
prioritized = result["prioritized"]       # Priority queue of targets
extra_info = result["extra_info"]         # Forms, JS files, error pages
total = result["total_endpoints"]         # Total count
```

---

## ⚙️ Configuration

### Adjust Risk Keywords

Edit `analyzer.py` to modify keyword weights:

```python
RISK_KEYWORDS = {
    "admin": 15,           # Higher weight = higher priority
    "api": 11,
    "config": 14,
    # Add or modify keywords...
}
```

### Crawl Behavior

Modify in `crawler.py`:

```python
def crawl(start_url, max_pages=80, delay=0.6, progress_callback=None):
    # max_pages: Maximum endpoints to discover
    # delay: Seconds between requests (be respectful to servers)
```

### Prioritization Logic

Customize bonus scoring in `prioritizer.py`:

```python
if any(x in path for x in ['admin', 'login', 'dashboard']):
    bonus += 10  # Adjust bonus values
```

---

## 🔧 How It Works

### Phase 1: Crawling 🕷️
- Starts from the target URL
- Uses BFS (Breadth-First Search) to discover pages
- Extracts links from:
  - `<a href>` tags
  - `<link>` tags (stylesheets)
  - `<script src>` tags
  - `<form action>` tags
  - `<iframe src>` tags
  - XML sitemaps (`<loc>` tags)
- Normalizes and validates all URLs
- Only follows internal links (same domain)

### Phase 2: Analysis 🎯
- **Keyword Matching**: Checks path and query parameters against 50+ security-sensitive keywords
- **Risk Calculation**: Assigns weighted scores based on:
  - Keyword presence in URL path (higher weight)
  - Keyword presence in query params (lower weight)
  - File extensions (`.env`, `.bak`, `.php`)
  - API endpoint patterns (`/api/`, `/rest/`, `/graphql`)
  - WordPress-specific patterns
- **Normalization**: Converts raw scores to 0-100 scale

### Phase 3: Prioritization 🏆
- **Greedy Algorithm**: Uses max-heap priority queue
- **Scoring Formula**: `Priority = Risk Score + Path Bonus - (Depth × 1.5)`
- **Bonus Categories**:
  - Admin/Login paths: +10 bonus
  - Upload/Config/Secrets: +9 bonus
  - API endpoints: +7 bonus
  - Auth/OAuth: +8 bonus
  - Debug/Dev endpoints: +6 bonus
- **Depth Penalty**: Shallower URLs ranked higher (typically more exposed)

### Phase 4: Reporting 📊
- Aggregates results with metadata
- Identifies high-risk endpoints (risk_score ≥ 8)
- Extracts discovered forms and JavaScript files
- Logs error pages for further investigation

---

## 🏗️ Architecture

```
smart-recon/
├── main.py              # Application entry point
├── gui.py               # Tkinter GUI interface & threading
├── scanner.py           # Core ReconEngine orchestrator
├── crawler.py           # Web crawler with BFS algorithm
├── analyzer.py          # Risk scoring engine
├── prioritizer.py       # Smart target prioritization
├── utils.py             # URL normalization & validation
└── requirements.txt     # Python dependencies
```

### Component Interactions

```
main.py → gui.py → scanner.py
                    ├── crawler.py
                    ├── analyzer.py
                    └── prioritizer.py
                    
utils.py (shared utilities)
```

---

## 📊 Example Output

### High-Risk Endpoints
```
🔥 HIGH RISK ENDPOINTS:
   • https://example.com/wp-admin → Risk: 24.17
   • https://example.com/admin/dashboard → Risk: 22.50
   • https://example.com/api/v1/users → Risk: 18.33
   • https://example.com/.env → Risk: 20.00
```

### Priority Targets
```
🏆 SMART PRIORITY TARGETS:
   1. https://example.com/admin → Risk: 28.33 (Priority: 38.33)
   2. https://example.com/api/v1 → Risk: 18.33 (Priority: 25.33)
   3. https://example.com/backup → Risk: 21.67 (Priority: 30.67)
```

### CSV Export Format
```
Rank,URL,Risk Score,Priority Score,Category
1,https://example.com/admin,28.33,38.33,Critical
2,https://example.com/api/v1,18.33,25.33,High
3,https://example.com/backup,21.67,30.67,Critical
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas for Contribution
- Additional keyword detection patterns
- Performance optimizations for large-scale crawls
- Support for JavaScript-rendered content
- Enhanced reporting formats (HTML, PDF)
- Additional security check modules
- Integration with vulnerability databases

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**Legal Notice**: This tool is intended for authorized security testing and reconnaissance purposes ONLY.

- ✅ Use only on systems you own or have explicit written permission to test
- ✅ Comply with all applicable laws and regulations in your jurisdiction
- ✅ Respect robots.txt and rate limiting
- ❌ Do not use for unauthorized access attempts
- ❌ Do not use for malicious purposes
- ❌ The authors are not responsible for misuse

**Responsible Disclosure**: If you discover vulnerabilities during testing, follow responsible disclosure practices and notify the system owner privately before public disclosure.

---

## 🙋 Support & Questions

- 📧 **Email**: mabdullah.sec@protonmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/M-Abdullah-lab/smart-recon/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/M-Abdullah-lab/smart-recon/discussions)

---

## 🔐 Security Considerations

- **Rate Limiting**: Default crawl delay is 0.6s to be respectful to target servers
- **User-Agent Spoofing**: Uses `SmartRecon/2.2` identifier (be transparent about your reconnaissance)
- **HTTPS Support**: Automatically handles both HTTP and HTTPS
- **Error Handling**: Gracefully handles connection errors and parsing issues
- **Data Privacy**: Reports are stored locally; no data is sent externally

---

## 📈 Roadmap

- [ ] Support for JavaScript-rendered content (Selenium/Playwright)
- [ ] API endpoint (REST API for integration)
- [ ] Vulnerability database integration (CVSS scoring)
- [ ] Parallel crawling threads for faster discovery
- [ ] Advanced filtering and search in results
- [ ] HTML report generation
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Scheduling and automated scans

---

## 👥 Authors

- **Muhammad Abdullah** - Cyber security Engineer and Bug Bounty Hunter

---

## 🙏 Acknowledgments

- Built with [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Powered by [Requests](https://requests.readthedocs.io/) for HTTP handling
- GUI powered by [Tkinter](https://docs.python.org/3/library/tkinter.html)

---

<div align="center">

**Made with ❤️ for the security community**

[⬆ back to top](#-smart-recon--attack-surface-mapper)

</div>
