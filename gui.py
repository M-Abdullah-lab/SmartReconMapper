import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import os
import csv
import json
import heapq
from datetime import datetime
import queue

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from scanner import ReconEngine
from prioritizer import prioritize_targets

class SmartReconGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Smart Recon & Attack Surface Mapper")
        self.root.geometry("1280x900")
        self.root.configure(bg="#0f172a")
        
        self.current_analyzed = None
        self.current_extra_info = None
        self.target_url = ""
        
        self.message_queue = queue.Queue()
        self.process_queue()
        
        self.style_setup()
        self.create_widgets()

    def style_setup(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Accent.TButton", background="#22c55e", foreground="white")

    def create_widgets(self):
        # Header, controls, buttons, etc. (same clean UI)
        header = tk.Frame(self.root, bg="#1e2937", height=100)
        header.pack(fill="x")
        tk.Label(header, text="🔍 Smart Recon Mapper", font=("Arial", 26, "bold"), 
                fg="#60a5fa", bg="#1e2937").pack(pady=18)

        control_frame = tk.Frame(self.root, bg="#0f172a")
        control_frame.pack(pady=12, fill="x", padx=30)

        tk.Label(control_frame, text="Target URL:", font=("Arial", 11, "bold"), fg="#e2e8f0", bg="#0f172a").pack(anchor="w")
        self.url_entry = tk.Entry(control_frame, width=90, font=("Consolas", 11), bg="#1e2937", fg="#93c5fd")
        self.url_entry.pack(pady=8, ipady=8)
        self.url_entry.insert(0, "https://example.com")

        opt_frame = tk.Frame(control_frame, bg="#0f172a")
        opt_frame.pack(fill="x", pady=8)
        
        tk.Label(opt_frame, text="Max Pages:", bg="#0f172a", fg="#e2e8f0").pack(side="left")
        self.max_pages_var = tk.IntVar(value=80)
        tk.Spinbox(opt_frame, from_=30, to=250, textvariable=self.max_pages_var, width=8).pack(side="left", padx=10)

        self.progress = ttk.Progressbar(opt_frame, mode='determinate', length=520)
        self.progress.pack(side="left", padx=20, fill="x", expand=True)

        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text="🚀 Start Advanced Scan", style="Accent.TButton", 
                  command=self.start_scan_thread).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="📤 Export CSV", command=self.export_csv).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="💾 Save Full JSON Report", command=self.save_full_report).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="🧹 Clear", command=self.clear_logs).pack(side="left", padx=10)

        self.status_var = tk.StringVar(value="Ready to Scan")
        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 11, "bold"), fg="#34d399", bg="#0f172a").pack(pady=8)

        tk.Label(self.root, text="📊 Scan Results", font=("Arial", 13, "bold"), fg="#e2e8f0", bg="#0f172a").pack(anchor="w", padx=30)
        self.log_area = scrolledtext.ScrolledText(self.root, height=36, font=("Consolas", 11),
                                                 bg="#1e2937", fg="#c4d0ff", wrap=tk.WORD)
        self.log_area.pack(padx=30, pady=10, fill="both", expand=True)

    def process_queue(self):
        try:
            while True:
                msg = self.message_queue.get_nowait()
                if msg[0] == "log":
                    self.log_area.insert(tk.END, msg[1] + "\n")
                    self.log_area.see(tk.END)
                elif msg[0] == "progress":
                    self.progress['value'] = msg[1]
                elif msg[0] == "status":
                    self.status_var.set(msg[1])
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def safe_log(self, message):
        self.message_queue.put(("log", message))

    def safe_progress(self, value):
        self.message_queue.put(("progress", value))

    def safe_status(self, status):
        self.message_queue.put(("status", status))

    def start_scan_thread(self):
        threading.Thread(target=self.run_scan, daemon=True).start()

    def run_scan(self):
        self.safe_log(f"[+] Starting scan on → {self.url_entry.get().strip()}")
        self.safe_progress(0)
        self.safe_status("🔄 Crawling...")

        self.target_url = self.url_entry.get().strip()
        if not self.target_url.startswith("http"):
            self.target_url = "https://" + self.target_url

        max_pages = self.max_pages_var.get()

        def progress_callback(val):
            self.safe_progress(val)

        try:
            engine = ReconEngine()
            result = engine.run(self.target_url, max_pages, progress_callback=progress_callback)

            self.current_analyzed = result["endpoints"]
            self.current_extra_info = result["extra_info"]

            self.safe_progress(45)
            self.safe_log(f"✅ Discovered {result['total_endpoints']} endpoints!")

            self.safe_progress(65)

            # Display High Risk
            self.safe_log("\n🔥 HIGH RISK ENDPOINTS:")
            high_risk = [item for item in result["endpoints"] if item['risk_score'] >= 8]
            for item in high_risk[:20]:
                self.safe_log(f"   • {item['url']} → Risk: {item['risk_score']}")

            # Display Priority Targets
            self.safe_log("\n🏆 SMART PRIORITY TARGETS:")
            for i in range(min(12, len(result["prioritized"]))):
                _, risk, bonus, target = heapq.heappop(result["prioritized"])
                self.safe_log(f"   {i+1:2d}. {target} → Risk: {risk} (Priority: {risk+bonus})")

            self.safe_progress(100)
            self.safe_log(f"\n🎉 Scan Completed at {datetime.now().strftime('%H:%M:%S')}")
            self.safe_status("✅ Completed")

        except Exception as e:
            self.safe_log(f"❌ Error: {str(e)}")
            self.safe_status("❌ Failed")
            self.safe_progress(0)

    # Export functions remain the same (export_csv and save_full_report)
    def export_csv(self):
        if not self.current_analyzed:
            messagebox.showwarning("Warning", "Run a scan first!")
            return
        # ... (same as before)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"priority_targets_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        )
        if not file_path: return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Rank", "URL", "Risk Score", "Priority Score", "Category"])
                temp = prioritize_targets(self.current_analyzed)
                rank = 1
                while temp and rank <= 30:
                    _, risk, bonus, url = heapq.heappop(temp)
                    cat = "Critical" if risk >= 15 else "High" if risk >= 10 else "Medium"
                    writer.writerow([rank, url, risk, risk + bonus, cat])
                    rank += 1
            self.safe_log(f"✅ CSV Saved: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_full_report(self):
        if not self.current_analyzed:
            messagebox.showwarning("Warning", "No scan data!")
            return
        # ... (same full report logic as before)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"full_recon_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        )
        if not file_path: return
        try:
            report = {
                "target": self.target_url,
                "scan_time": datetime.now().isoformat(),
                "total_endpoints_discovered": len(self.current_analyzed),
                "high_risk_count": len([x for x in self.current_analyzed if x['risk_score'] >= 8]),
                "extra_info": self.current_extra_info,
                "priority_targets": [],
                "all_endpoints": []
            }

            temp = prioritize_targets(self.current_analyzed)
            for i in range(min(25, len(temp))):
                _, risk, bonus, url = heapq.heappop(temp)
                report["priority_targets"].append({
                    "rank": i + 1, "url": url, "risk_score": risk, "priority_score": risk + bonus
                })

            for item in self.current_analyzed:
                report["all_endpoints"].append({
                    "url": item['url'],
                    "risk_score": item['risk_score']
                })

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)

            self.safe_log(f"💾 Full Report Saved: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_logs(self):
        self.log_area.delete(1.0, tk.END)
        self.progress['value'] = 0

    def run(self):
        self.root.mainloop()