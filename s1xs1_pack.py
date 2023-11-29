import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from helper_functions import *
import argparse
import time

# Test commit 3
# Test commit 5
# get options from command line
parser = argparse.ArgumentParser(
                    prog='S1xS1_Packing',
                    description='Packs n points ~evenly in S1xS1')                  
parser.add_argument('--number_of_particles', type=int, default=1)
parser.add_argument('--force_order', type=float, default=6)
parser.add_argument('--tile_range', type=int, default=2)
parser.add_argument('--sensitivity', type=float, default=0.0001)
parser.add_argument('--decay', type=float, default=1.005)
parser.add_argument('--iterations', type=int, default=0)
parser.add_argument('--search_block_iterations', type=int, default=100)
parser.add_argument('--animate', action='store_true')
parser.add_argument('--bounding_circles', action='store_true')
parser.add_argument('--lattice', action='store_true')
args = parser.parse_args()

number_of_particles = args.number_of_particles
force_order = args.force_order
tile_range = args.tile_range
sensitivity = args.sensitivity
decay = args.decay
iterations = args.iterations
search_block_iterations = args.search_block_iterations
animate = args.animate
bounding_circles = args.bounding_circles
lattice = args.lattice

# initialize plot and particles
fig, axs = plt.subplots()
axs.set_title(str(number_of_particles)+' points packed ~evenly in S1xS1')
particle_dict = {}

if lattice:
    lattice_defining_vectors = find_best_lattice_defining_vectors(number_of_particles)
    u,v = lattice_basis(lattice_defining_vectors, number_of_particles)
    particle_number = 0
    for i in range(lattice_defining_vectors[1],lattice_defining_vectors[0]+1):
        for j in range(lattice_defining_vectors[2]+lattice_defining_vectors[3]+1):
            if (0 <= i*u[0]+j*v[0]) and (i*u[0]+j*v[0] < 0.999999) and (0 <= i*u[1]+j*v[1]) and (i*u[1]+j*v[1] < 0.999999):
                x = i*u[0]+j*v[0]
                y = i*u[1]+j*v[1]
                particle_dict[particle_number] = Particle(particle_number, x, y)
                particle_number = particle_number+1
else:        
    for particle_number in range(number_of_particles):
        particle_dict[particle_number] = Particle(particle_number, random.random(), random.random())
    
for tile_x in range(-tile_range,tile_range+1):
        for tile_y in range(-tile_range,tile_range+1):
                rect = patches.Rectangle((tile_x, tile_y), 1, 1, linewidth=1, edgecolor='b', facecolor='none')
                axs.add_patch(rect)
rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='r', facecolor='none')
axs.add_patch(rect)

particles = [[],[]]
for particle in particle_dict:
            for tile_x in range(-tile_range,tile_range+1):
                for tile_y in range(-tile_range,tile_range+1):
                    particles[0].append(tile_x+particle_dict[particle].x)
                    particles[1].append(tile_y+particle_dict[particle].y)
ln = axs.scatter(particles[0], particles[1], color='black')
plt.draw()
plt.pause(0.001)

# gradient descent to low-energy solution
min_energy = total_energy(particle_dict, tile_range, force_order)
for iteration in range(iterations):
    if (iteration+1) % search_block_iterations == 0:
        # return to best solution in last search block
        print("search_block_complete")
        for particle in particle_dict:
            particle_dict[particle].x = particle_dict[particle].min_energy_x
            particle_dict[particle].y = particle_dict[particle].min_energy_y
    energy = total_energy(particle_dict, tile_range, force_order)
    
    if energy < min_energy:
        # update best solution if new one is found
        for particle in particle_dict:
            particle_dict[particle].min_energy_x =  particle_dict[particle].x
            particle_dict[particle].min_energy_y = particle_dict[particle].y
    # clear old scatter plot
    ln.remove()
    plt.pause(0.001)
    # gradient descent
    update_all_particle_derivatives(particle_dict, tile_range, force_order)
    update_particle_positions(particle_dict, sensitivity)
    sensitivity = sensitivity/decay
    # make new scatter plot
    particles = [[],[]]
    for particle in particle_dict:
            for tile_x in range(-tile_range,tile_range+1):
                for tile_y in range(-tile_range,tile_range+1):
                    particles[0].append(tile_x+particle_dict[particle].x)
                    particles[1].append(tile_y+particle_dict[particle].y)
                    #print(particle, particle_dict[particle].x, particle_dict[particle].y)
    ln = axs.scatter(particles[0], particles[1], color='black')
    
    
    if animate==True:
        plt.draw()
        plt.pause(0.001)

# draw bounding circles
set_radii(particle_dict)
if bounding_circles:                
    for particle in particle_dict:
        for tile_x in range(-tile_range,tile_range+1):
                for tile_y in range(-tile_range,tile_range+1):
                    circ = patches.Circle((tile_x+particle_dict[particle].x, tile_y+particle_dict[particle].y), particle_dict[particle].radius, linewidth=1, edgecolor='black', facecolor='none')
                    axs.add_patch(circ)

circle_area = total_circle_area(particle_dict)
radius_variance = normalized_radius_variance(particle_dict)
print('Total circle area (in 1x1 S1xS1) = ' + str(circle_area) + '. Normalized radius variance (average radius 1) = ' + str(radius_variance))
plt.draw()
plt.show()
