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

@dataclass
class star:
    position = [] #maybe convert to np arrays or better structure
    velocity = []


#eg: star1 = star(---arguments where applicable, in order thye appear in sruct?)
#input: ra, dec, from icrs coordinates. maybe distance too (default 100)
#guide: https://docs.astropy.org/en/stable/coordinates/
def J2000_to_pos(right_acension, declination, distance = 100):
    #distance yet to be properly implemented...defaulted to 100
    c = SkyCoord(ra= right_acension*u.degree, dec=declination*u.degree, distance = distance*u.pc, frame='icrs')
    c = c.represent_as("cartesian")  
    arr = [c.x.value, c.y.value, c.z.value]
    return arr
star1 = star()
star1.position = J2000_to_pos(50, 13)
print("star1 postion set? ", star1.position)