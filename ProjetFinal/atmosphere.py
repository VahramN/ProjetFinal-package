# Class copied from the MGA802 course notes
import numpy as np

class Atmosphere:
    def __init__(self, altitude=0.):
        self.altitude = altitude  # meters

    def compute_pressure(self):
        """
        Compute the pressure

        :return: pressure.
        """
        p0 = 101325  # Pa - Pression standard au niveau de la mer
        pressure = p0 * (1 - 0.0000225577 * self.altitude) ** 5.25588  # Pa - https://fr.wikipedia.org/wiki/Formule_du_nivellement_barom%C3%A9trique
        return pressure

    def compute_density(self):
        """
        Compute the density

        :return: density.
        """
        g = 9.81  # m/s^2
        M = 0.0289644  # kg/mol - Masse molaire de l'air
        R = 8.31447  # J/(mol*K) - Constante des gaz parfaits
        T0 = 288.15  # K - Température standard au niveau de la mer

        density = self.compute_pressure() * M / (R * self.compute_temperature())  # kg/m^3 - Densité de l'air en fonction de la pression et de la température, equation gaz parfait
        return density

    def compute_density_imperial(self):
        """
        convert the density from kg/m^3 to slug/cu.ft

        :return: density.
        """
        return self.compute_density() / 515.378818492

    def compute_temperature(self):
        """
        compute the temperature

        :return: temperature.
        """
        T0 = 288.15  # K
        L = 0.0065  # K/m
        return T0 - L * self.altitude

    def compute_gravity(self):
        """
        Compute the gravity

        :return: gravity.
        """
        G = 9.81  # accélération gravitationnelle en m/s^2
        rayon_terre = 6.371e6  # rayon de la Terre en mètres
        return G * (rayon_terre / (rayon_terre + self.altitude))**2

    def speed_of_sound(self):
        """
        Compute the speed of the sound

        :return: sound speed.
        """
        # Supposons que la vitesse du son dans l'air dépende de la température selon la formule suivante :
        # a = sqrt(gamma * R * T), où gamma est le coefficient de dilatation adiabatique de l'air,
        # R est la constante spécifique de l'air, T est la température en Kelvin
        gamma = 1.4  # coefficient de dilatation adiabatique de l'air
        R = 287  # J/kg/K
        T = self.temperature()
        return np.sqrt(gamma * R * T)

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, value):
        self._altitude = value
