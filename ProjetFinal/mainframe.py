import numpy as np
import tkinter as tk
from tkinter import ttk
from airfoildataframe import AirfoilDataFrame
from handler import Handler
from aerodynamics import Aerodynamics
from atmosphere import Atmosphere


class App(tk.Tk):
    """
    GUI and starting class.
    """
    def __init__(self):
        super().__init__()

        self.airfoil_dataframe = AirfoilDataFrame(self)
        self.airfoil_dataframe.pack(expand=True)

        self.handler = Handler()
        self.handler.airfoil_obj = self.airfoil_dataframe

        self.geometry('1500x770+2+1')
        self.title('MGA802 Final project')

        self.lbl_info = ttk.Label(self, text="Re=6M, Mach=0")
        self.lbl_info.place(relx=0.8, rely=0.78, anchor='ne')

        self.lbl_weight = ttk.Label(self, text="Weight (lb)")
        self.lbl_surface = ttk.Label(self, text="Surface (ft^2)")
        self.lbl_wingspan = ttk.Label(self, text="Wingspan (ft)")
        self.lbl_thrust = ttk.Label(self, text="Jet Thrust (lb)")
        self.lbl_altitude = ttk.Label(self, text="Altitude (ft)")

        self.lbl_weight.place(relx=0.01, rely=0.83, anchor='sw')
        self.lbl_surface.place(relx=0.01, rely=0.86, anchor='sw')
        self.lbl_wingspan.place(relx=0.01, rely=0.89, anchor='sw')
        self.lbl_thrust.place(relx=0.01, rely=0.92, anchor='sw')
        self.lbl_altitude.place(relx=0.01, rely=0.95, anchor='sw')

        self.txt_weight = tk.Entry(self)
        self.txt_surface = tk.Entry(self)
        self.txt_wingspan = tk.Entry(self)
        self.txt_thrust = tk.Entry(self)
        self.txt_altitude = tk.Entry(self)

        self.txt_weight.place(relx=0.1, rely=0.83, anchor='sw')
        self.txt_surface.place(relx=0.1, rely=0.86, anchor='sw')
        self.txt_wingspan.place(relx=0.1, rely=0.89, anchor='sw')
        self.txt_thrust.place(relx=0.1, rely=0.92, anchor='sw')
        self.txt_altitude.place(relx=0.1, rely=0.95, anchor='sw')

        self.btn_stall_speed = tk.Button(self, text="Stall speed", command=self.compute_stall_speed)
        self.btn_takeoff_speed = tk.Button(self, text="Takeoff speed", command=self.compute_takeoff_speed)
        self.btn_optimal_speed = tk.Button(self, text="Optimal speed max distance", command=self.compute_optimal_speed)

        self.btn_stall_speed.place(relx=0.25, rely=0.835, anchor='sw')
        self.btn_takeoff_speed.place(relx=0.25, rely=0.875, anchor='sw')
        self.btn_optimal_speed.place(relx=0.25, rely=0.915, anchor='sw')

        self.btn_takeoff_distance = tk.Button(self, text="Takeoff distance", command=self.compute_takeoff_distance)
        self.btn_landing_distance = tk.Button(self, text="Landing distance", command=self.compute_landing_distance)

        self.btn_takeoff_distance.place(relx=0.4, rely=0.835, anchor='sw')
        self.btn_landing_distance.place(relx=0.4, rely=0.875, anchor='sw')

    def treat_text_range_to_points(self, text, allow_range):
        """
        Treat the text as float points array or single point

        :param text: single float value **or** the range, ex: 1000-1200
        :param allow_range: allow range bool value (in case of false, even the text is given in range format will consider only the first value)

        :return: single float **or** the float range array.
        """
        arr = text.split("-")
        if (len(arr) > 1) and allow_range:
            start_limit = float(arr[0])
            end_limit = float(arr[len(arr) - 1])
            num = int(abs(end_limit - start_limit) * 10)
            # let's limit to [1000-3000] points max
            np.clip(num, 1000, 3000)
            arr_range = np.linspace(start_limit, end_limit, num)
        elif len(arr) > 1:
            # we will take only the first value and will ignore the rest
            arr_range = float(arr[0])
        else:
            arr_range = float(text)
        return arr_range

    def populate_from_frame_to_objects(self):
        """
        Populate the user data from the frame to the objects.

        - airfoil_dataframe,
        - handler's aero_obj,
        - handler's atm_obj.
        """
        selected_row = self.airfoil_dataframe.table.getSelectedRow()
        # wing aerodynamics
        cl_max = self.airfoil_dataframe.dataset_airfoils.at[selected_row, 'Cl max']
        l_d_max = self.airfoil_dataframe.dataset_airfoils.at[selected_row, 'Cl/Cd max']

        # we can take only one range between the provided datas. If the user enters more than 1 range,
        # we will take only the first one, the rest will be ignored and we will take only the first value
        allow_range = True

        weight = self.treat_text_range_to_points(self.txt_weight.get(), allow_range=allow_range)
        allow_range = allow_range and isinstance(weight, float)

        surface = self.treat_text_range_to_points(self.txt_surface.get(), allow_range=allow_range)
        allow_range = allow_range and isinstance(surface, float)

        wingspan = self.treat_text_range_to_points(self.txt_wingspan.get(), allow_range=allow_range)
        allow_range = allow_range and isinstance(wingspan, float)

        thrust = self.treat_text_range_to_points(self.txt_thrust.get(), allow_range=allow_range)
        allow_range = allow_range and isinstance(thrust, float)

        self.handler.aero_obj = Aerodynamics(weight,
                                             surface,
                                             wingspan,
                                             thrust,
                                             cl_max=float(cl_max),
                                             l_d_max=float(l_d_max))

        # Air
        # convert altitude from foot to meter
        altitude = self.treat_text_range_to_points(self.txt_altitude.get(), allow_range=allow_range) * 0.3048
        self.handler.atm_obj = Atmosphere(altitude)

    def compute_stall_speed(self):
        """
        Compute the stall speed.
        Read the user entered values in the form.
        Call Handler's function to Compute the stall speed.
        """
        self.populate_from_frame_to_objects()
        self.handler.compute_stall_speed()

    def compute_takeoff_speed(self):
        """
        Compute the takeoff speed.
        Read the user entered values in the form.
        Call Handler's function to Compute the takeoff speed.
        """
        self.populate_from_frame_to_objects()
        self.handler.compute_takeoff_speed()

    def compute_optimal_speed(self):
        """
        Compute the optimal speed.
        Read the user entered values in the form.
        Call Handler's function to Compute the optimal speed.
        """
        self.populate_from_frame_to_objects()
        self.handler.compute_optimal_speed()

    def compute_takeoff_distance(self):
        """
        Compute the takeoff distance.
        Read the user entered values in the form.
        Call Handler's function to Compute the takeoff distance.
        """
        self.populate_from_frame_to_objects()
        self.handler.compute_takeoff_distance()

    def compute_landing_distance(self):
        """
        Compute the landing distance.
        Read the user entered values in the form.
        Call Handler's function to Compute the landing distance.
        """
        self.populate_from_frame_to_objects()
        self.handler.compute_landing_distance()


if __name__ == "__main__":
    app = App()
    app.mainloop()
