import numpy as np
from atmosphere import Atmosphere
import plot


class Handler:
    """
    Class handler is the manager of the current program.
    It is handling the calculations and the displaying of the results.
    """
    def __init__(self):
        self.aero_obj = None
        self.atm_obj = None
        self.atm_0_obj = Atmosphere(0)
        self.airfoil_obj = None
        np.set_printoptions(threshold=100)

    def convert_speed_imperial_to_knots(self, speed):
        """
        Convert speed from ft/s to kts
        :param speed: speed in ft/s
        :return: speed in kts.
        """
        return speed / 1.687811

    def find_object_in_interval(self):
        """
        Find if any of the entered value is in interval.
        :return: First met interval, if exists, otherwise None
        :return: First met interval label, if exists, otherwise empty string.
        """
        if isinstance(self.aero_obj.weight, np.ndarray):
            return self.aero_obj.weight, "Weight (lb)"
        elif isinstance(self.aero_obj.surface, np.ndarray):
            return self.aero_obj.surface, "Surface (sq.ft)"
        elif isinstance(self.aero_obj.wingspan, np.ndarray):
            return self.aero_obj.wingspan, "Wingspan (ft)"
        elif isinstance(self.aero_obj.thrust, np.ndarray):
            return self.aero_obj.thrust, "Thrust (lb)"
        elif isinstance(self.atm_obj.altitude, np.ndarray):
            return (self.atm_obj.altitude / 0.3048), "Altitude (ft)"  # convert to foot for display
        else:
            return None, ""

    # in kts
    def stall_speed(self):
        """
        Calculate the stall speed
        :return: stall speed in kts.
        """
        v_stall = np.sqrt((self.aero_obj.weight / self.aero_obj.surface) *
                          2 / (self.atm_obj.compute_density_imperial() * self.aero_obj.cl_max))
        v_stall = self.convert_speed_imperial_to_knots(v_stall)
        # v_stall = np.round(v_stall, 3)
        return v_stall

    def compute_stall_speed(self):
        """
        Compute stall speed, plot diagram, print the speed
        :return: stall speed.
        """
        v_stall = self.stall_speed()

        obj, obj_name = self.find_object_in_interval()
        plot.plot_diagrams(v_stall, 'Stall speed (kts)', obj, obj_name)

        print(f"stall speed is: {v_stall} (kts)")
        return v_stall

    def compute_takeoff_speed(self):
        """
        Compute takeoff speed, plot diagram, print the speed
        :return: takeoff speed.
        """
        v_takeoff = 1.2 * self.stall_speed()
        obj, obj_name = self.find_object_in_interval()
        plot.plot_diagrams(v_takeoff, 'Takeoff speed (kts)', obj, obj_name)

        print(f"takeoff speed is: {v_takeoff} (kts)")
        return v_takeoff

    def compute_optimal_speed(self):
        """
        Compute optimal speed, plot diagram, print the speed
        :return: optimal speed.
        """
        v_optimal = np.sqrt((2 * self.aero_obj.weight) / (self.atm_obj.compute_density_imperial() * self.aero_obj.surface)) * \
                    (3 * self.aero_obj.coeff_K() / self.aero_obj.coeff_drag0()) ** 0.25
        v_optimal = self.convert_speed_imperial_to_knots(v_optimal)
        # v_optimal = np.round(v_optimal, 3)
        obj, obj_name = self.find_object_in_interval()
        plot.plot_diagrams(v_optimal, 'Optimal speed for max distance (kts)', obj, obj_name)

        print(f"optimal speed is: {np.round(v_optimal, 3)} (kts)")
        return v_optimal

    def compute_takeoff_distance(self):
        """
        Compute takeoff distance, plot diagram, print the distance
        :return: takeoff distance.
        """
        density_ratio = self.atm_obj.compute_density_imperial() / self.atm_0_obj.compute_density_imperial()
        TOP = (self.aero_obj.weight / self.aero_obj.surface) * \
              (1 / self.aero_obj.cl_max) * \
              (self.aero_obj.weight / self.aero_obj.thrust) * (1 / density_ratio)

        takeoff_distance = 20.9 * TOP + 87 * np.sqrt(TOP * (self.aero_obj.thrust / self.aero_obj.weight))
        obj, obj_name = self.find_object_in_interval()
        plot.plot_diagrams(takeoff_distance, 'Takeoff distance (ft)', obj, obj_name)

        print(f"takeoff distance is: {takeoff_distance} (ft)")
        return takeoff_distance

    def compute_landing_distance(self):
        """
        Compute landing distance, plot diagram, print the distance
        :return: landing distance.
        """
        density_ratio = self.atm_obj.compute_density_imperial() / self.atm_0_obj.compute_density_imperial()
        LP = (self.aero_obj.weight / self.aero_obj.surface) * (1 / (density_ratio * self.aero_obj.cl_max))

        landing_distance = 118 * LP + 400
        obj, obj_name = self.find_object_in_interval()
        plot.plot_diagrams(landing_distance, 'Landing distance (ft)', obj, obj_name)

        print(f"landing distance is: {landing_distance} (ft)")
        return landing_distance
