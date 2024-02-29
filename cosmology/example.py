import pytipsy
import numpy as np

def example_file(filename = "onestar.tipsy"):
    try: 
        header_ex = {'time': 1.0, 'n': 3, 'ndim': 3, 'ngas': 1, 'ndark': 1, 'nstar': 1}

        gas_particle_ex = {
            'mass': np.array([1]), 
            'x': np.array([1]), 'y': np.array([1]), 'z': np.array([1]), 
            'vx': np.array([1]), 'vy': np.array([1]), 'vz': np.array([-1]), 
            'dens': np.array([1]), 
            'tempg': np.array([1]), 
            'h': np.array([1]), 
            'zmetal': np.array([1]), 
            'phi': np.array([1])
        }

        dark_particle_ex = {
            'mass': np.array([1]), 
            'x': np.array([1]), 'y': np.array([1]), 'z': np.array([1]), 
            'vx': np.array([1]), 'vy': np.array([1]), 'vz': np.array([-1]), 
            'eps': np.array([1]), 
            'phi': np.array([1]), 
            'h': np.array([1]), 
            'zmetal': np.array([1])
        }

        star_particle_ex = {
            'mass': np.array([1.0]),
            'x': np.array([1]), 'y': np.array([1]), 'z': np.array([1]), 
            'vx': np.array([1]), 'vy': np.array([1]), 'vz': np.array([-1]),
            'metals': np.array([1.0]),
            'tform': np.array([1.0]),
            'eps': np.array([1.0]),
            'phi': np.array([1.0])
        }

        pytipsy.wtipsy(filename, header_ex, gas_particle_ex, dark_particle_ex, star_particle_ex)
        print("Data written to:", filename)
    except Exception:
        print("Couldn't write to file.")

if __name__ == "__main__":
    example_file() #writes to onestar.tipsy
    header, catg, catd, cats = pytipsy.rtipsy("onestar.tipsy")
    print("Dim:", header["ndim"],". N =", header["n"] )
