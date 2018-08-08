import datetime
import math
from math import cos, sin, pi, pow, atan, atan2, radians, degrees
from types import SimpleNamespace
import pandas as pd


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
        self.inclination = radians(i)
        self.ascending_node = radians(omega)
        self.perihelion = rho
        self.mean_distance = alpha
        self.daily_motion = eta
        self.eccentricity = e
        self.mean_longitude = mu
        self.elements = SimpleNamespace()
        self.coordinates = SimpleNamespace()
        self.main()

    @staticmethod
    def julian_day_number():
        julian_date = datetime.datetime.now()
        julian_day = julian_date - datetime.datetime(2013, 8, 16)
        return julian_day.days + 1

    def mean_anomaly(self, day_num):
        self.elements.mean_anomaly = self.daily_motion * day_num + self.mean_longitude - self.perihelion
        self.elements.mean_anomaly = self.elements.mean_anomaly % 360.0

    def true_anomaly(self):
        ecc2, ecc3, ecc4, ecc5 = pow(self.eccentricity, 2), pow(self.eccentricity, 3), \
                                 pow(self.eccentricity, 4), pow(self.eccentricity, 5)
        mean_rads = math.radians(self.elements.mean_anomaly)
        sin1, sin2, sin3, sin4, sin5 = sin(mean_rads), sin(2 * mean_rads), \
                                       sin(3 * mean_rads), sin(4 * mean_rads), \
                                       sin(5 * mean_rads)
        el1 = (2 * self.eccentricity - 0.25 * ecc3 + 5/96*ecc5) * sin1
        el2 = (1.25*ecc2 - 11/24 * ecc4) * sin2
        el3 = (13/12*ecc3 - 43/64 * ecc5) * sin3
        el4 = 103/96 * ecc4 +1097/960 * ecc5 * sin5
        self.elements.true = degrees(mean_rads+ el1 + el2 + el3 + el4)

    def radius_vector(self, semi_major_axis):
        a = semi_major_axis * (1 - self.eccentricity**2)
        b = 1 + self.eccentricity * math.cos(radians(self.elements.true))
        self.elements.radius = a / b

    def heliocentric_coordinates(self):
        self.coordinates.x = self.elements.radius * cos(radians(self.elements.true) + radians(self.perihelion))
        self.coordinates.y = self.elements.radius * sin(radians(self.elements.true)+ radians(self.perihelion))
        self.coordinates.z = 0.0

    def main(self):
        self.mean_anomaly(self.julian_day_number())
        self.true_anomaly()
        self.radius_vector(1)
        self.heliocentric_coordinates()


class Planet:

    def __init__(self, planet, i=None, omega=None, rho=None, alpha=None, eta=None, e=None, mu=None, M_0 = None,
                 obliquity=None, date = None):
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
        self.name = planet
        self.inclination = radians(i)
        self.ascending_node = radians(omega)
        self.perihelion = rho
        self.semi_major = alpha
        self.daily_motion = eta
        self.eccentricity = e
        self.mean_longitude = mu
        self.M_0 = M_0
        self.obliquity = radians(obliquity)
        self.elements = SimpleNamespace()
        self.elements.mean_anomaly = None
        self.elements.true_anomaly = None
        self.coordinates = SimpleNamespace()
        self.elements.radius = None
        self.right_ascenscion = None
        self.declination = None
        self.distance = None
        self._date_updated = None
        if date is None:
            self.date = datetime.datetime.now()
        else:
            date = date
        self.main(date)

    @staticmethod
    def julian_day_number(date = datetime.datetime.now()):
        julian_date = date
        epoch = datetime.datetime(2000,1,1,12)
        days_since_2000 = julian_date - epoch
        days_since_2000 = days_since_2000.days + (days_since_2000.seconds/3600)/24
        elements_days = datetime.datetime(2013, 8, 16, 0) - epoch
        elements_days = elements_days.days + (elements_days.seconds/3600)/24
        julian_day = days_since_2000 - elements_days
        return julian_day

    def mean_anomaly(self, day_num):
        self.elements.mean_anomaly = self.daily_motion * day_num + self.M_0
        self.elements.mean_anomaly = self.elements.mean_anomaly % 360.0

    def true_anomaly(self):
        ecc2, ecc3, ecc4, ecc5 = pow(self.eccentricity, 2), pow(self.eccentricity, 3), \
                                 pow(self.eccentricity, 4), pow(self.eccentricity, 5)
        mean_rads = math.radians(self.elements.mean_anomaly)
        sin1, sin2, sin3, sin4, sin5 = sin(mean_rads), sin(2 * mean_rads), \
                                       sin(3 * mean_rads), sin(4 * mean_rads), \
                                       sin(5 * mean_rads)
        el1 = (2 * self.eccentricity - 0.25 * ecc3 + 5/96*ecc5) * sin1
        el2 = (1.25*ecc2 - 11/24 * ecc4) * sin2
        el3 = (13/12*ecc3 - 43/64 * ecc5) * sin3
        el4 = 103/96 * ecc4 +1097/960 * ecc5 * sin5
        self.elements.true = math.degrees(mean_rads + el1 + el2 + el3 + el4)

    def radius_vector(self, semi_major_axis):
        a = semi_major_axis * (1 - self.eccentricity**2)
        b = 1 + self.eccentricity * math.cos(math.radians(self.elements.true))
        self.elements.radius = a / b

    def set_heliocentric_coordinates(self):
        c_omega, s_omega, c_arith, s_arith = cos(self.ascending_node), sin(self.ascending_node), \
                                             cos(radians(self.elements.true) + radians(self.perihelion) - self.ascending_node),\
                                             sin(radians(self.elements.true) + radians(self.perihelion) - self.ascending_node)
        x = self.elements.radius * (c_omega * c_arith - s_omega * s_arith * cos(self.inclination))
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
        alpha = atan(self.coordinates.yq/self.coordinates.xq)
        if self.coordinates.xq < 0:
            alpha += pi
        elif self.coordinates.yq < 0 and self.coordinates.xq > 0:
            alpha += 2 * pi
        self.right_ascenscion = math.degrees(alpha) / 15  #convert to hours
        declination = atan2(self.coordinates.zq, math.sqrt(self.coordinates.xq **2 + self.coordinates.yq **2))
        self.declination = math.degrees(declination)
        self.distance = math.sqrt(self.coordinates.xq ** 2 + self.coordinates.yq ** 2 + self.coordinates.zq ** 2)

    def main(self, date = None):
        if date:
            d = self.julian_day_number(date=date)
        else:
            d = self.julian_day_number()
        self.mean_anomaly(d)
        self.true_anomaly()
        self.radius_vector(self.semi_major)
        self.set_heliocentric_coordinates()
        self.set_geocentric_coordiantes()
        self.geocentric_equitorial()
        self.set_RA_Dec()

    def __repr__(self):
        return "{0} - RA: {1} \t Dec: {2} \t Dist: {3} au".format(self.name,self.right_ascenscion, self.declination,
                                                                  self.distance)

    def __str__(self):
        return "{0} - JD: {4}:\n Mean: {1} \t True: {2} \t Dist to Sun: {3} au".format(self.name,
                                                                                        self.elements.mean_anomaly,
                                                                                        self.elements.true,
                                                                                        self.elements.radius,
                                                                                        self.julian_day_number(self.date))

def get_dict_inputs(elements, planet):
    """

    :param elements: DataFrame containing the elemets
    :param planet: string of planet that you want
    :type elements: pd.DataFrame
    :return:
    """
    obliquity = 23.439292
    row = elements.loc[elements["planet"] == planet].squeeze()
    ret_dict = row.to_dict()  # type: dict
    ret_dict["obliquity"] = obliquity
    return ret_dict

Earth = Earth("Earth", 0.0, 0.0, 103.147, 1.0, 0.985611, 0.016679, 324.5489)
elements = pd.read_csv("./planet_elements.csv")
Mercury = Planet(**get_dict_inputs(elements, "Mercury"))
Venus = Planet(**get_dict_inputs(elements, "Venus"))
Mars = Planet(**get_dict_inputs(elements, "Mars"))
Jupiter = Planet(**get_dict_inputs(elements, "Jupiter"))
Saturn = Planet(**get_dict_inputs(elements, "Saturn"))
Uranus = Planet(**get_dict_inputs(elements, "Uranus"))
Neptune = Planet(**get_dict_inputs(elements, "Neptune"))

planets = {"Mercury": Mercury, "Venus": Venus, "Mars": Mars, "Saturn": Saturn, "Jupiter": Jupiter,
           "Neptune": Neptune, "Uranus": Uranus}

if __name__ == '__main__':

    print(repr(Mercury))
    print(repr(Venus))
    print(repr(Mars))
    print(repr(Jupiter))
    print(repr(Saturn))
    print(repr(Uranus))
    print(repr(Neptune))
