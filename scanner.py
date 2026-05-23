# scanner.py
from crawler import crawl
from analyzer import analyze_endpoints
from prioritizer import prioritize_targets


class ReconEngine:
    """
    Core Reconnaissance Engine - Clean separation of logic from GUI
    """
    def run(self, url: str, max_pages: int = 80, progress_callback=None):
        """
        Run full reconnaissance scan and return structured results.
        """
        print(f"[+] ReconEngine started on: {url}")

        # Step 1: Crawling
        graph, endpoints, extra_info = crawl(
            url, 
            max_pages=max_pages, 
            progress_callback=progress_callback
        )

        # Step 2: Analysis
        analyzed = analyze_endpoints(endpoints)

        # Step 3: Prioritization
        prioritized = prioritize_targets(analyzed)

        print(f"[+] ReconEngine completed. {len(endpoints)} endpoints discovered.")

        return {
            "endpoints": analyzed,
            "prioritized": prioritized,
            "extra_info": extra_info,
            "total_endpoints": len(endpoints),
            "graph": graph
        }