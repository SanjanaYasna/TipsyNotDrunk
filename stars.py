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
from astropy.io.votable import parse
from astropy.coordinates import (SkyCoord, Distance, Galactic, 
                                 EarthLocation, AltAz)
import re

@dataclass
class star:
    position = [] #convert to np arrays for pytipsy
    velocity = []
    #metals: float
    #float tform ;
    #float eps;
    #float phi ;



#eg: star1 = star(---arguments where applicable, in order thye appear in sruct?)
#input: ra, dec, from icrs coordinates. maybe distance too (default 100)
#guide: https://docs.astropy.org/en/stable/coordinates/
def J2000_to_pos(c: star) -> list:
    c = c.represent_as("cartesian")  
    arr = [c.x.value, c.y.value, c.z.value]

    return arr

#temp load in one star
def intialize_star(right_acension, declination, distance, pm_ra_cosdec, pm_dec, radial_velocity) -> star:
    c = SkyCoord(ra= right_acension*u.degree, 
                 dec=declination*u.degree, 
                 distance = distance*u.pc, 
                 pm_ra_cosdec = pm_ra_cosdec*u.mas/u.yr,
                 pm_dec = pm_dec*u.mas/u.yr, 
                 radial_velocity = radial_velocity*u.km/u.s,
                 frame='icrs')
    return c

# read votable
def temp_load(file_name: str = "simbad.xml") -> tuple[float]:
    votable = parse(file_name)
    
    #first table in votable file
    table = votable.get_first_table()
    data = table.array

    # get right ascentsion (RA), declination (Dec) radial velocity (RV)
    ra = data['RA_d'] # unit degrees
    ra = float(ra[:1])
    dec = data['DEC_d'] #unit degrees
    dec = float(dec[:1])
    rv = data['RV_VALUE'] #unit km.s-1
    rv = float(rv[1:2])

    #get proper motions, pm_ra_cosdec is same as pm_ra, but pm_ra_cosdec is what's used for astropy docs
    pm_ra_cosdec = data['PMRA'] # float, unit mas.yr-1
    pm_ra_cosdec = float(pm_ra_cosdec[:1])
    pm_dec = data['PMDEC'] # float, unit mas.yr-1
    pm_dec = float(pm_dec[:1])
   
    #distance yet to be properly implemented...defaulted to 100
    parallax = data['PLX_VALUE'] # unit mas, milli-arcseconds: 1 mas = 1/1000 arcsecond
    parallax = float(parallax[:1])

    # parallax * 0.001 -> arcsec. 1/(parallax*0.001) -> parsec
    # getting 10000 (wrong) instead of 7500
    distance = 1 / (parallax*0.001) # unit parsec
    print(distance)
    distance = 100 

    print(f"Parallax: {parallax}. Distance: {distance} psec")

    #below are empty, 
    #a,b,c = data['Distance_unit'],  data['Distance_method'],data['Distance_distance']


    return ra, dec, distance, pm_ra_cosdec, pm_dec, rv

if __name__ == "__main__":
    star_data = temp_load("simbad.xml")
    star1 = intialize_star(*star_data)
   
    star.position = J2000_to_pos(star1)
    print(star.position)

    #temp, find better way to make list from velocity 
    star_vel = str(star1.velocity)
    star_vel = re.sub(r"km / s|\(|\)", '', star_vel).strip().split(",")
    velocities = [ -9999, -9999,-9999]
    i = 0
    for vel in star_vel: 
        velocities[i] = float(vel)
        i += 1
    star.velocity = velocities   

    print("Velocities: ", star.velocity)
    print("Positions: ", star.position)