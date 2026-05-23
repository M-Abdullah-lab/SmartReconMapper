# prioritizer.py
import heapq

def prioritize_targets(analyzed_endpoints):
    """
    Weighted Greedy Prioritization System
    
    Combines Risk Score + Path Importance Bonus - Depth Penalty
    Uses a max-heap (priority queue) to rank high-value targets first.
    """
    priority_queue = []
    
    for item in analyzed_endpoints:
        url = item['url']
        risk = item.get('risk_score', 0)
        
        # Use pre-parsed path for efficiency
        path = item.get('path', '').lower()
        
        # Bonus points for security-sensitive / high-value paths
        bonus = 0
        if any(x in path for x in ['admin', 'administrator', 'wp-admin', 'login', 'dashboard']):
            bonus += 10
        if any(x in path for x in ['upload', 'backup', 'config', '.env', 'secret']):
            bonus += 9
        if any(x in path for x in ['api', '/v1/', '/v2/', '/rest/', 'graphql']):
            bonus += 7
        if any(x in path for x in ['debug', 'test', 'staging', 'dev', 'beta', 'internal']):
            bonus += 6
        if any(x in path for x in ['password', 'token', 'key', 'auth', 'oauth']):
            bonus += 8
        
        # Depth penalty: shallower paths are usually more important
        depth = path.count('/')
        final_priority = risk + bonus - (depth * 1.5)
        
        # Push into max-heap (-priority for heapq behavior)
        heapq.heappush(priority_queue, (-final_priority, risk, bonus, url))
    
    return priority_queue