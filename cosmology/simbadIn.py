#reads in votable to dataframe
import sys
from astropy.io.votable import parse
import pandas as pd
from old_delete_soon.stars import *
import os
def votable_to_pandas(votable_file):
    votable = parse(votable_file)
    table = votable.get_first_table().to_table(use_names_over_ids=True)
    return table.to_pandas()

if __name__ == "__main__":
    df = votable_to_pandas(f"simbad").head(5).reset_index()
    print("data frame input has length of ",len(df))
    #initialize array of size x with dtype of star_np defined in stars.py
    np_arr = np.zeros((len(df),), dtype = star_np )
    vectorized_init = np.vectorize(intialize_star)
    np_arr["star_obj"] = vectorized_init(df["RA_d"].values, #right ascension
                            df["DEC_d"].values, #declination
                            df["Distance:distance"].values, #distance (unfortunately, mostly nan, so it's based off of 1/parallax in the case that parallax is not nan)
                            df["Distance:unit"].values, #unit of distance quantitiy
                            df["PMRA"].values,
                            df["PMDEC"].values,
                            df["RV_VALUE"].values,
                            df["PLX_VALUE"].values,
                             )
    
    #vectorize metallicity yoperatoin, and take those values from the df and fill them into the np_arr of star structs
    vectorized_metallicity = np.vectorize(get_metallicity)
    np_arr["metallicity"] = vectorized_metallicity(df["Fe_H:Fe_H"].values) #.values immediately converts to np array

    #calculate positions in cartesian
    #TO DO: better way? vectorization rose ValueError: setting an array element with a sequence.
    np_arr["position"] = np.array(list(map(J2000_to_pos, np.array(np_arr["star_obj"], dtype = SkyCoord) )))
    np_arr["velocity"] = np.array(list(map(cartesian_velocities, np.array(np_arr["star_obj"], dtype = SkyCoord) )))


    
    print("values", np_arr[0])
    sys.exit()
    
    # star1 = star()
    # star1.position = J2000_to_pos(250, 36)
    # star1.velocity = cartesian_velocities(-3.117, -2.574, -247, star1)
    # print("velocities received: ", star1.velocity)
