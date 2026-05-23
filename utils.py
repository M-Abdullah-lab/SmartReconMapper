from urllib.parse import urljoin, urlparse, urlunparse

def normalize_url(base_url, url):
    if not url or url.startswith(('javascript:', 'mailto:', '#', 'tel:', 'data:')):
        return None
    full_url = urljoin(base_url, url.strip())
    parsed = urlparse(full_url)
    cleaned = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', parsed.query, ''))
    return cleaned

def is_internal_link(base_url, url):
    base_domain = urlparse(base_url).netloc.lower()
    link_domain = urlparse(url).netloc.lower()
    if not link_domain:
        return True
    return link_domain == base_domain or link_domain.endswith('.' + base_domain)