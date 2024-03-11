import yt 
#below doesn't work since ti's not a recognized format
# def NewField(field, data):
#     q = data[('STAR', 'age')]
#     print("BBB",data)
#     return q
# data = yt.load("/Users/sanjanayasna/Downloads/sizmbhloz-clref04SNth-rs9_a0.9011/sizmbhloz-clref04SNth-rs9_a0.9011.g000")


#trying out ENZO format (/Users/sanjanayasna/Downloads/IsolatedGalaxy_Gravity/galaxy0030)

#MUSIC ENZO INITIAL CONDITIONS FROM HDF5 FILE GENERATION: https://bitbucket.org/ohahn/music/src/master/src/plugins/output_enzo.cc 
'''
https://enzo.readthedocs.io/en/latest/parameters/index.html check hierarchy file output format to see particle type numbers, and see what indices corespond to what, basically how t oread output files and store them into meaningful vectors
'''