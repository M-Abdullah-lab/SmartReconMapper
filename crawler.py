import requests
from collections import deque
import time
import sys
import os
import warnings
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

# Suppress the XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Path fix
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils import normalize_url, is_internal_link

def crawl(start_url, max_pages=80, delay=0.6, progress_callback=None):
    """
    Advanced Crawler - Handles HTML + XML + Error Pages
    """
    visited = set()
    graph = {}
    queue = deque([(start_url, 0)])
    discovered = []
    forms_found = []
    js_files = []
    error_pages = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; SmartRecon/2.2)'
    }

    print(f"[+] Starting Intelligent Crawl on {start_url}")

    while queue and len(visited) < max_pages:
        current_url, depth = queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)
        discovered.append(current_url)
        graph.setdefault(current_url, [])

        try:
            print(f"[+] Crawling: {current_url} (Depth: {depth})")
            response = requests.get(current_url, headers=headers, timeout=12, allow_redirects=True)

            status = response.status_code
            if status != 200:
                print(f"   → Status: {status} (still parsing)")
                error_pages.append((current_url, status))

            # Smart parser selection
            content_type = response.headers.get('Content-Type', '').lower()

            if 'xml' in content_type or current_url.endswith('.xml'):
                soup = BeautifulSoup(response.text, features="xml")
            else:
                soup = BeautifulSoup(response.text, 'html.parser')

            links = []
            for tag in soup.find_all(['a', 'link', 'script', 'form', 'iframe', 'loc']):  # 'loc' for sitemaps
                for attr in ['href', 'src', 'action', 'data-src']:
                    href = tag.get(attr)
                    if href:
                        full_url = normalize_url(current_url, href)
                        if full_url and is_internal_link(start_url, full_url):
                            links.append(full_url)

                            if tag.name == 'script' and '.js' in str(href).lower():
                                js_files.append(full_url)
                            if tag.name == 'form':
                                forms_found.append({
                                    'page': current_url,
                                    'action': full_url,
                                    'status': status
                                })

            links = list(set(links))

            for link in links:
                if link not in visited and link not in graph[current_url]:
                    graph[current_url].append(link)
                    queue.append((link, depth + 1))

            if progress_callback:
                progress = min(35, int((len(visited) / max_pages) * 35))
                progress_callback(progress)

            time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print(f"[-] Connection Error on {current_url}: {e}")
        except Exception as e:
            print(f"[-] Parsing Error on {current_url}: {e}")

    print(f"[+] Crawl completed! Total pages: {len(discovered)} | Error Pages: {len(error_pages)}")

    extra_info = {
        'forms': forms_found[:25],
        'js_files': list(set(js_files))[:30],
        'error_pages': error_pages[:15]
    }

    if progress_callback:
        progress_callback(40)

    return graph, discovered, extra_info
