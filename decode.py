import struct

def read_tipsy_data(file_path):
    particle_data = []

    with open(file_path, 'rb') as file:
        # Read the header
        header = struct.unpack('>di4i', file.read(28))
        num_particles = header[1]
        nsph = header[3]
        ndark = header[4] 
        nstar = header[5]
        
        # Read gas particle data if present
        for i in range(nsph):
            gas_particle_data = struct.unpack('>7f', file.read(28))
            particle_data.append(('gas',) + gas_particle_data)

        # Read dark matter particle data
        for i in range(ndark):
            dark_particle_data = struct.unpack('>4f4f', file.read(32))
            particle_data.append(('dark',) + dark_particle_data) 

        # Read star particle data
        for i in range(nstar):
            star_particle_data = struct.unpack('>3f4f', file.read(28))
            particle_data.append(('star',) + star_particle_data)

    return particle_data

def write_to_SVR_file(output_file_path, particle_data):
    with open(output_file_path, 'w') as output_file:
        for i, data in enumerate(particle_data, start=1):
            particle_type = data[0]
            output_file.write(f'{particle_type.capitalize()} Particle {i}: '
                            f'Mass={data[1]}, x={data[2]}, y={data[3]}, z={data[4]}, '
                            f'vx={data[5] if len(data) > 5 else "N/A"}, '
                            f'vy={data[6] if len(data) > 6 else "N/A"}, '
                            f'vz={data[7] if len(data) > 7 else "N/A"}, '
                            f'eps={data[8] if len(data) > 8 else "N/A"}\n')

    print(f'Particle data saved to {output_file_path}')
    
def write_to_all_output():
    #all means output, which comes from the benchmark files.
    for i in range(0, 10): 
        file_path = f"your_path_to/dwf1.2048.bench.00000{i}"
        if (i == 10):
            file_path = "your_path_to/dwf1.2048.bench.000010"
    
        particle_data = read_tipsy_data(file_path)
        output_file_path = f"your_path_to/decoding_tipsy_all_{i}.txt"
        write_to_SVR_file(output_file_path, particle_data)

def write_to_c_input():
    # "_c " means input, which comes from the dwf1.2048.00384 file
    file_path = 'your_path_to/dwf1.2048.00384'
    particle_data = read_tipsy_data(file_path)  
    input_file_path = 'your_path_to/decoding_tipsy_input_c.txt'
    write_to_SVR_file(input_file_path, particle_data)

