from __future__ import print_function
import os
import re
import struct
import numpy as np
#filename: name of output tipsy file
#header: ngas, ndark, nstar (how much of each, basically)
#
def wtipsy(filename, header, catg = 0, catd = 0, cats = 0, STANDARD=True):
    try:
        f = open(filename, 'wb')
    except:
        print("WTIPSY ERROR: Can't open file")
        return 0
    f.write(struct.pack(">diiiii", header['time'], header['n'], header['ndim'], header['ngas'], header['ndark'], header['nstar']))
    if STANDARD:
        f.write(struct.pack("xxxx"))
    for i in range(header['nstar']):
        print(cats[i]['mass'])
        f.write(struct.pack(">fffffffffff" ,     
                            cats[i]['mass'],
                            cats[i]['position'][0],
                            cats[i]['position'][1],
                            cats[i]['position'][2],
                            cats[i]['velocity'][0],
                            cats[i]['velocity'][1],
                            cats[i]['velocity'][2],
                            cats[i]['metallicity'],
                            cats[i]['time_formation'],
                            cats[i]['softening'],
                            cats[i]['potential']) )

    f.close()
header = {
    "time" : 0,
    "ndark" : 0,
    "nstar" : 5,
    "ngas" : 0,
    "n" : 5,
    "ndim" : 3
}
