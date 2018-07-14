import time
import math
from math import cos, sin, pi, pow, atan, atan2
from types import SimpleNamespace


class Earth:

    def __init__(self, name, i=None, omega=None, rho=None, alpha=None, eta=None, e=None, mu=None):
        """

        :param i: Inclination
        :param omega: Longitude of the Ascending Node
        :param rho: Longitude of the Perihelion
        :param alpha: Mean Distance
        :param eta: Daily Motion
        :param e: Eccentricity
        :param mu: Mean Longitude

        https://www.hackster.io/30506/calculation-of-right-ascension-and-declination-402218
        """
        self.name = name
        self.inclination = i
        self.ascending_node = omega
        self.perihelion = rho
        self.mean_distance = alpha
        self.daily_motion = eta
        self.eccentricity = e
        self.mean_longitude = mu
        self.elements = SimpleNamespace()
        self.coordinates = SimpleNamespace()

    def mean_anomaly(self, day_num):
        self.elements.mean_anomaly = self.daily_motion * day_num + self.mean_longitude - self.perihelion
        self.elements.mean_anomaly = self.elements.mean_anomaly % 360.0

    def true_anomaly(self):
        ecc2, ecc3, ecc4, ecc5 = pow(self.eccentricity, 2), pow(self.eccentricity, 3), \
                                 pow(self.eccentricity, 4), pow(self.eccentricity, 5)
        sin1, sin2, sin3, sin4, sin5 = sin(self.elements.mean_anomaly), sin(2 * self.elements.mean_anomaly), \
                                       sin(3 * self.elements.mean_anomaly), sin(4 * self.elements.mean_anomaly), \
                                       sin(5 * self.elements.mean_anomaly)
        el1 = (2 * self.eccentricity - 0.25 * ecc3 + 5/96*ecc5) * sin1
        el2 = (1.25*ecc2 - 11/24 * ecc4) * sin2
        el3 = (13/12*ecc3 - 43/64 * ecc5) * sin3
        el4 = 103/96 * ecc4 +1097/960 * ecc5 * sin5
        self.elements.true = self.elements.mean_anomaly + el1 + el2 + el3 + el4

    def radius_vector(self, semi_major_axis):
        a = semi_major_axis * (1 - self.eccentricity**2)
        b = 1 + self.eccentricity * math.cos(self.elements.true)
        self.elements.radius = a / b

    def heliocentric_coordinates(self):
        self.coordinates.x = self.elements.radius * cos(self.elements.true + self.perihelion)
        self.coordinates.y = self.elements.radius * sin(self.elements.true + self.perihelion)
        self.coordinates.z = 0.0


class Planet:

    def __init__(self, name, i=None, omega=None, rho=None, alpha=None, eta=None, e=None, mu=None, obliquity=None):
        """

        :param i: Inclination
        :param omega: Longitude of the Ascending Node
        :param rho: Longitude of the Perihelion
        :param alpha: Mean Distance
        :param eta: Daily Motion
        :param e: Eccentricity
        :param mu: Mean Longitude

        https://www.hackster.io/30506/calculation-of-right-ascension-and-declination-402218
        """
        self.name = name
        self.inclination = i
        self.ascending_node = omega
        self.perihelion = rho
        self.mean_distance = alpha
        self.daily_motion = eta
        self.eccentricity = e
        self.mean_longitude = mu
        self.obliquity = obliquity
        self.elements = SimpleNamespace()
        self.elements.mean_anomaly = None
        self.elements.true_anomaly = None
        self.coordinates = SimpleNamespace()
        self.elements.radius = None
        self.right_ascenscion = None
        self.declination = None
        self.distance = None
        self._date_updated = None

    def mean_anomaly(self, day_num):
        self.elements.mean_anomaly = self.daily_motion * day_num + self.mean_longitude - self.perihelion
        self.elements.mean_anomaly = self.elements.mean_anomaly % 360.0

    def true_anomaly(self):
        ecc2, ecc3, ecc4, ecc5 = pow(self.eccentricity, 2), pow(self.eccentricity, 3), \
                                 pow(self.eccentricity, 4), pow(self.eccentricity, 5)
        sin1, sin2, sin3, sin4, sin5 = sin(self.elements.mean_anomaly), sin(2 * self.elements.mean_anomaly), \
                                       sin(3 * self.elements.mean_anomaly), sin(4 * self.elements.mean_anomaly), \
                                       sin(5 * self.elements.mean_anomaly)
        el1 = (2 * self.eccentricity - 0.25 * ecc3 + 5/96*ecc5) * sin1
        el2 = (1.25*ecc2 - 11/24 * ecc4) * sin2
        el3 = (13/12*ecc3 - 43/64 * ecc5) * sin3
        el4 = 103/96 * ecc4 +1097/960 * ecc5 * sin5
        self.elements.true = self.elements.mean_anomaly + el1 + el2 + el3 + el4

    def radius_vector(self, semi_major_axis):
        a = semi_major_axis * (1 - self.eccentricity**2)
        b = 1 + self.eccentricity * math.cos(self.elements.true)
        self.elements.radius = a / b

    def set_heliocentric_coordinates(self):
        c_omega, s_omega, c_arith, s_arith = cos(self.ascending_node), sin(self.ascending_node), \
                                             cos(self.elements.true + self.perihelion - self.ascending_node),\
                                             sin(self.elements.true + self.perihelion - self.ascending_node)
        x = self.elements.radius * (c_omega * c_arith) - s_omega * s_arith * cos(self.inclination)
        y = self.elements.radius * (s_omega * c_arith + c_omega * s_arith * cos(self.inclination))
        z = self.elements.radius * (s_arith * sin(self.inclination))
        self.coordinates.x = x
        self.coordinates.y = y
        self.coordinates.z = z

    def set_geocentric_coordiantes(self):
        self.coordinates.xg = self.coordinates.x - Earth.coordinates.x
        self.coordinates.yg = self.coordinates.y - Earth.coordinates.y
        self.coordinates.zg = self.coordinates.z - Earth.coordinates.z

    def geocentric_equitorial(self):
        self.coordinates.xq = self.coordinates.xg
        self.coordinates.yq = self.coordinates.yg * cos(self.obliquity) - self.coordinates.zg * sin(self.obliquity)
        self.coordinates.zq = self.coordinates.yg * sin(self.obliquity) + self.coordinates.zg * cos(self.obliquity)

    def set_RA_Dec(self):
        alpha = atan2(self.coordinates.yq, self.coordinates.xq)
        if self.coordinates.xq < 0:
            alpha += pi
        elif self.coordinates.xq > 0 and self.coordinates.yq < 0:
            alpha += 2 * pi
        self.right_ascenscion = math.degrees(alpha) / 15  #convert to hours
        declination = atan2(self.coordinates.zq, math.sqrt(self.coordinates.xq **2 + self.coordinates.yq **2))
        self.declination = math.degrees(declination)
        self.distance = math.sqrt(self.coordinates.xq ** 2 + self.coordinates.yq ** 2 + self.coordinates.zq ** 2)


Mercury = Planet("Mercury")
Venus = Planet("Venus")
Earth = Earth("Earth")
Mars = Planet("Mars")
Jupiter = Planet("Jupiter")
Saturn = Planet("Saturn")
Uranus = Planet("Uranus")
Neptune = Planet("Neptune")

planets = {"Mercury": Mercury, "Venus": Venus, "Mars": Mars, "Saturn": Saturn, "Jupiter": Jupiter,
           "Neptune": Neptune, "Uranus": Uranus}

