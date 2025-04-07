import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from MBTIntelligence.main import MBTIProcessorGUI

if __name__ == "__main__":
    root = tk.Tk()
    gui = MBTIProcessorGUI(root)
    root.mainloop()