import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from gui import SmartReconGUI

if __name__ == "__main__":
    print("🚀 Launching Smart Recon & Attack Surface Mapper...\n")
    app = SmartReconGUI()
    app.run()