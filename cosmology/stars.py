#dataset: https://simbad.cds.unistra.fr/simbad/sim-id?Ident=Cl*+NGC+6205+++++AJ+++++++2&NbIdent=query_hlinks&Coord=16+41+05.0724333192%2B36+28+20.864287632&parents=1&siblings=526&submit=siblings&hlinksdisplay=h_all
#siblings of following star: https://simbad.cds.unistra.fr/simbad/sim-id?mescat.fe_h=on&mescat.plx=on&mescat.pm=on&Ident=%402885722&Name=Cl*+NGC+6205+++++AJ+++++++2&submit=display+all+measurements#lab_meas

'''
que necesitamos:
struct star_particle {
    float mass;
    float pos[3];
    float vel[3];
    float metals ;
    float tform ;
    float eps;
    float phi ;
} ;
'''

from dataclasses import dataclass
import pandas as pd 
import numpy as np 
from astropy import units as u
from astropy.coordinates import (SkyCoord, Distance, Galactic, 
                                 EarthLocation, AltAz)
import re 
import math

star_np = np.dtype([
    ('position', np.float64, (3,)), #position is np subarray of 3 float64
    ('velocity', np.float64, (3,)), #velocity is np subarray of 3 float64,
    ("metallicity", np.float64),
    ("star_obj", SkyCoord)
])
@dataclass
class star:
    position = [] #maybe convert to np arrays or better structure
    velocity = []
    tform = 0 #generally set to 0 in many IC generators, but maybe there is a way to determine such?
    #eps and phi have decent formulas from pyics, so that's probably covered. credit them ig
    #____star specific
    ra = 0
    dec = 0
    pm_ra = 0
    pm_dec = 0
    distance = 0

#return metallicity value, or 0 if nan
def get_metallicity(index):
    if math.isnan(index) : return 0
    return index

#temp load in one star, and this should fild the skycoord_obj parameter of star_np that handles the rest mostly from these key params
def intialize_star(right_acension, declination, distance, distance_unit, pm_ra_cosdec, pm_dec, radial_velocity, parallax) -> star:
    #get some distance value if it's nan. If parallax, get distance from calcaulte_distance. If both distance and parallax nan, default to 10
    if (math.isnan(distance)):
        if  not math.isnan(parallax):
            distance = calculate_distance(parallax)
        else :  distance = 10
    #default distance unit parsecs
    distance_unit = u.pc
    if distance_unit:
        if distance_unit == "pc":
            distance_unit = u.pc 
        elif distance_unit == "kpc":
            distance_unit = u.kpc
        else:
            distance_unit = u.kpc
            distance = distance * 1000 #convert distance to kpc, since no mpc unit
    c = SkyCoord(ra= right_acension*u.degree, 
                 dec=declination*u.degree, 
                 distance = distance*distance_unit, 
                 pm_ra_cosdec = pm_ra_cosdec*u.mas/u.yr,
                 pm_dec = pm_dec*u.mas/u.yr, 
                 radial_velocity = radial_velocity*u.km/u.s,
                 frame='icrs')
    return c

#calculate distance as 1 / parallax
def calculate_distance(parallax):
    return 1 / parallax

#input: ra, dec, from icrs coordinates. 
#guide: https://docs.astropy.org/en/stable/coordinates/
def J2000_to_pos(star,right_acension = star.ra, declination = star.dec, distance = star.distance):  
    star = star.represent_as("cartesian")
    arr = np.array([star.x.value, star.y.value, star.z.value])
    return arr

#https://astropy-cjhang.readthedocs.io/en/latest/coordinates/velocities.html as a guide
#maybe check the pm_ra_cosdec value again, it's a bit complicated
def cartesian_velocities(star, proper_motion_ra = star.pm_ra, proper_motion_dec = star.pm_dec, radial_velocity = star.ra):
    # star.pm_dec = proper_motion_dec
    # star.pm_ra = proper_motion_ra
    arr = np.array([star.velocity.d_x.value, star.velocity.d_y.value, star.velocity.d_z.value])
    return arr

# if __name__ == "__main__":
#     star1 = star()
#     star1.position = J2000_to_pos(250, 36)
#     star1.velocity = cartesian_velocities(-3.117, -2.574, -247, star1)
#     print("velocities received: ", star1.velocity)