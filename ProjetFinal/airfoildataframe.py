import tkinter as tk
from pandastable import Table
import pandas as pd

AIRFOILS_FILE = "airfoils.csv"


class AirfoilDataFrame(tk.Frame):
    """
    AirfoilDataFrame class read data from the csv file and creates pandastable.
    """
    def __init__(self, parent=None):
        self.parent = parent
        tk.Frame.__init__(self)
        self.main = self.master
        # self.main.geometry('1350x200+1+1')
        f = tk.Frame(self.main)
        f.pack(fill=tk.BOTH, expand=1)

        # read csv file and set in dataframe
        self.dataset_airfoils = pd.read_csv(AIRFOILS_FILE, sep=',', header=0)
        # set in pandas table
        self.table = pt = Table(f, dataframe=self.dataset_airfoils, showtoolbar=True, showstatusbar=True)
        # make it visible
        pt.show()
        return
