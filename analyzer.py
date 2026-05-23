from urllib.parse import urlparse

RISK_KEYWORDS = {
    # High Critical
    "wp-admin": 16, "admin": 15, "administrator": 15, "upload": 14, "login": 12,
    "dashboard": 13, "config": 14, "backup": 15,
    "api": 11, "v1": 10, "v2": 10, "v3": 10,

    # Medium-High
    "debug": 12, "test": 9, "staging": 13, "dev": 12, "development": 11,
    "php": 8, "asp": 8, "aspx": 8, "jsp": 8, "env": 14,
    "sql": 10, "database": 11, "user": 7, "password": 13,
    "secret": 12, "token": 11, "key": 10,

    # Other risky patterns
    "shell": 13, "cmd": 12, "exec": 12, "console": 10,
    "log": 7, "logs": 8, "old": 9, "temp": 8,
    "beta": 10, "demo": 9, "internal": 11, "private": 12,
    "oauth": 10, "auth": 9, "signin": 11, "register": 8,
}

def calculate_risk_score(url):
    #Calculate improved risk score
    score = 0
    url_lower = url.lower()
    path = urlparse(url).path.lower()

    # Keyword matching
    for keyword, weight in RISK_KEYWORDS.items():
        if keyword in path:  # path is more precise; use only path
            score += weight
        elif keyword in urlparse(url).query.lower():  # separately check query string
            score += weight // 2  # lower weight for query params

    # Additional smart scoring
    if '?' in url and ('id=' in url_lower or 'user=' in url_lower or 'pass' in url_lower):
        score += 8
    if any(ext in url_lower for ext in ['.php', '.asp', '.aspx', '.jsp', '.env', '.bak', '.old']):
        score += 7
    if '/api/' in path or '/rest/' in path or '/graphql' in path:
        score += 6
    if 'wp-' in path or 'wordpress' in url_lower:
        score += 8

    MAX_RAW_SCORE = 120
    normalized_score = min((score / MAX_RAW_SCORE) * 100, 100)
    return round(normalized_score, 2)

def analyze_endpoints(endpoints):
    """Analyze and sort endpoints by risk"""
    analyzed = []
    for url in endpoints:
        score = calculate_risk_score(url)
        analyzed.append({
            'url': url,
            'risk_score': score,
            'path': urlparse(url).path
        })

    # Sort by risk score (highest first)
    analyzed.sort(key=lambda x: x['risk_score'], reverse=True)
    return analyzed