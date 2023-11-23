import math
import numpy as np

class Particle:
    def __init__(self, id_value, x_value, y_value):
        self.x = x_value
        self.y = y_value
        self.min_energy_x = self.x
        self.min_energy_y = self.y
        self.particle_id = id_value
    dx = 0
    dy = 0
    radius = 1
    radius_set = False
    nearest_neighbor = -1
    
# finds the distance between main particle and influencing particle in tile (tile_x, tile_y)
def find_distance(particle_main, particle_influence, particle_dict, tile_x, tile_y):
    distance = math.sqrt((tile_x + particle_dict[particle_main].x - particle_dict[particle_influence].x)**2 + 
                         (tile_y + particle_dict[particle_main].y - particle_dict[particle_influence].y)**2)
    return distance

# finds total energy of system
def total_energy(particle_dict, tile_range, p):
    energy = 0
    for particle_main in particle_dict:
        for particle_influence in particle_dict:
            if particle_influence != particle_main:
                for tile_x in range(-tile_range, tile_range+1):
                    for tile_y in range(-tile_range, tile_range+1):
                        distance = find_distance(particle_main, particle_influence, particle_dict, tile_x, tile_y)
                        energy += 0.5/distance**(p)
    return energy
                        
# finds the gradient of the energy function between two particles
def energy_derivative(particle_main, particle_influence, particle_dict, tile_x, tile_y, p):
    distance = find_distance(particle_main, particle_influence, particle_dict, tile_x, tile_y)
    x_component = -(tile_x + particle_dict[particle_main].x - particle_dict[particle_influence].x)/distance**(p+1)
    y_component = -(tile_y + particle_dict[particle_main].y - particle_dict[particle_influence].y)/distance**(p+1)
    return np.array([x_component, y_component])

# for given main particle, sums the gradient of the energy function over all influencing particles
# and assigns to main particle
def update_particle_derivative(particle_main, particle_dict, tile_range, p):
    particle_main_energy_derivative = np.array([0.0,0.0])
    for particle_influence in particle_dict:
        if particle_influence !=  particle_main:
            for tile_x in range(-tile_range, tile_range+1):
                for tile_y in range(-tile_range, tile_range+1):
                    particle_main_energy_derivative += energy_derivative(particle_main, particle_influence, particle_dict, tile_x, tile_y, p)
    particle_dict[particle_main].dx = particle_main_energy_derivative[0]
    particle_dict[particle_main].dy = particle_main_energy_derivative[1]

# updates net energy gradient for all partricles
def update_all_particle_derivatives(particle_dict, tile_range, p):
    for particle_main in particle_dict:
        update_particle_derivative(particle_main, particle_dict, tile_range, p)

# updates all particle positions using gradient descent on the energy function        
def update_particle_positions(particle_dict, sensitivity):
    for particle in particle_dict:
        particle_dict[particle].x -= sensitivity*particle_dict[particle].dx
        particle_dict[particle].y -= sensitivity*particle_dict[particle].dy
        particle_dict[particle].x = particle_dict[particle].x % 1
        particle_dict[particle].y = particle_dict[particle].y % 1

# for given main particle finds influenceing particle which limits main particle's bounding radius      
def find_nearest_neighbor(particle_main, particle_dict):
    radius = 1
    if not particle_dict[particle_main].radius_set:
        for particle_influence in particle_dict:
            if particle_influence != particle_main:
                for tile_x in range(-1,2):
                    for tile_y in range(-1, 2):
                        distance = find_distance(particle_main, particle_influence, particle_dict, tile_x, tile_y)
                        if (not particle_dict[particle_influence].radius_set) and (distance/2 < radius):
                            radius = distance/2
                            particle_dict[particle_main].radius = radius
                            particle_dict[particle_main].nearest_neighbor = particle_influence
                        if particle_dict[particle_influence].radius_set and (distance - particle_dict[particle_influence].radius < radius):
                            radius = distance - particle_dict[particle_influence].radius
                            particle_dict[particle_main].radius = radius
                            particle_dict[particle_main].nearest_neighbor = particle_influence

# sets the radius of pairs of nearest neighbors                        
def pair_nearest_neighbors(particle_dict):
    found_pair = False
    for particle_main in particle_dict:
        for particle_influence in particle_dict:
            if particle_influence != particle_main:
                if (not particle_dict[particle_main].radius_set) and (not particle_dict[particle_influence].radius_set):
                    if particle_dict[particle_main].nearest_neighbor == particle_influence:
                        if particle_dict[particle_influence].nearest_neighbor == particle_main:
                            particle_dict[particle_main].radius_set = True
                            particle_dict[particle_influence].radius_set = True
                            found_pair = True
    return found_pair

# sets the radius of the bounding circle for all particles                                              
def set_radii(particle_dict):
    for particle_main in particle_dict:
        find_nearest_neighbor(particle_main, particle_dict)
    while pair_nearest_neighbors(particle_dict):
        for particle_main in particle_dict:
            find_nearest_neighbor(particle_main, particle_dict)
    # sort particles by radius
    sorted_particle_dict = dict(sorted(particle_dict.items(), key=lambda item: item.radius))
    for particle_main in sorted_particle_dict:
        find_nearest_neighbor(particle_main, sorted_particle_dict)

# finds total area of bounding circles in S1xS1`            
def total_circle_area(particle_dict):
    area = 0
    for particle in particle_dict:
        area += particle_dict[particle].radius**2
    area = area*math.pi
    return area

def average_circle_radius(particle_dict):
    radius = 0
    for particle in particle_dict:
        radius += particle_dict[particle].radius
    radius = radius/len(particle_dict)
    return radius

def normalized_radius_variance(particle_dict):
    variance = 0
    average_radius = average_circle_radius(particle_dict)
    for particle in particle_dict:
        variance += (particle_dict[particle].radius/average_radius - 1)**2
    return variance
    
