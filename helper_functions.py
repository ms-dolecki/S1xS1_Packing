import math
import numpy as np
import sys
import random

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

class Coefficients:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

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
                        if distance**(p-1) > 0:
                            energy += 0.5/distance**(p-1)
                        else:
                            energy = sys.float_info.max
    return energy
                        
# finds the gradient of the energy function between two particles
def energy_derivative(particle_main, particle_influence, particle_dict, tile_x, tile_y, p):
    distance = find_distance(particle_main, particle_influence, particle_dict, tile_x, tile_y)
    if distance**(p+1) > 0:
        x_component = -(tile_x + particle_dict[particle_main].x - particle_dict[particle_influence].x)/distance**(p+1)
        y_component = -(tile_y + particle_dict[particle_main].y - particle_dict[particle_influence].y)/distance**(p+1)
    else:
        x_component = random.random()
        y_component = random.random()
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

# updates net energy gradient for all particles
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

# for given main particle finds influencing particle which limits main particle's bounding radius      
def find_nearest_neighbor(particle_main, particle_dict, set_radius):
    radius = 1
    if not particle_dict[particle_main].radius_set:
        particle_dict[particle_main].radius_set = set_radius
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
        find_nearest_neighbor(particle_main, particle_dict, False)
    while pair_nearest_neighbors(particle_dict):
        for particle_main in particle_dict:
            find_nearest_neighbor(particle_main, particle_dict, False)
    # sort particles by radius
    radius_sorted_particles = sorted(particle_dict.items(), key=lambda item: item[1].radius)
    for particle_main in radius_sorted_particles:
        find_nearest_neighbor(particle_main[1].particle_id, particle_dict, True)

# finds total area of bounding circles in S1xS1`            
def total_circle_area(particle_dict):
    area = 0
    for particle in particle_dict:
        area += particle_dict[particle].radius**2
    area = area*math.pi
    return area

# finds average radius of bounding circles in S1xS1
def average_circle_radius(particle_dict):
    radius = 0
    for particle in particle_dict:
        radius += particle_dict[particle].radius
    radius = radius/len(particle_dict)
    return radius

# nomralizing average radius to 1, finds the variance of bounding circle radii in S1xS1
def normalized_radius_variance(particle_dict):
    variance = 0
    average_radius = average_circle_radius(particle_dict)
    for particle in particle_dict:
        variance += (particle_dict[particle].radius/average_radius - 1)**2
    return variance

# returns the factors of given number
def find_factors(num):
    factors = []
    for i in range(num):
        if num % (i+1) == 0:
            factors.append(i+1)
    return factors

# checks if quadratic form ax^2+bxy+cy^2 or cx^2+bxy+ax^2 is reduced
def is_reduced(coefficients):
    if (abs(coefficients.b) <= coefficients.a) and (abs(coefficients.b) <= coefficients.c):
        return True
    else:
        return False

# performs one iterations of the reduction algorithm on ax^2+bxy+cy^2
def reduce_algorithm(coefficients):
    min_a_c = min(coefficients.a,coefficients.c)
    if coefficients.a <= coefficients.c:
        a_prime = min_a_c
    else:
        c_prime = min_a_c
    b_prime = coefficients.b
    m = 0
    if coefficients.b > min_a_c:
        plus_minus = -1
    else:
        plus_minus = 1
    while abs(b_prime) > min_a_c:
        b_prime = b_prime + plus_minus*2*min_a_c
        m = m + plus_minus
    if coefficients.a  <= coefficients.c:
        c_prime = coefficients.a*m**2 + coefficients.b*m + coefficients.c
    else:
        a_prime = coefficients.c*m**2 + coefficients.b*m + coefficients.a
    return Coefficients(a_prime,b_prime,c_prime)

# performs reduction algorithm on ax^2+bxy+cy^2
def reduce(coefficients):
    while not is_reduced(coefficients):
        coefficients = reduce_algorithm(coefficients)
    return coefficients

# find the minimum distance between points for two lattice-defining vectors 
def coeff(a1,a2,b1,b2):
    a = a1**2+a2**2
    b = 2*(a1*b1+a2*b2)
    c = b1**2+b2**2
    reduced_coefficients = reduce(Coefficients(a,b,c))
    return min(reduced_coefficients.a,reduced_coefficients.c)

# finds the bounding-circle-area-maximizing lattice-defining vectors for a given number of points
def find_best_lattice_defining_vectors(num):
    best_coeff = 0
    best_lattice_defining_vectors = [0,0,0,0]
    for i in range(int(math.ceil((num+1)/2.0))):
        if i == 0:
            factors = find_factors(num)
            for factor in factors:
                current_coeff = coeff(factor,0,0,num/factor)
                if current_coeff > best_coeff:
                    best_coeff = current_coeff
                    best_lattice_defining_vectors = [factor,0,0,num/factor]
        else:
            j = num-i
            factors_j = find_factors(j)
            factors_i = find_factors(i)
            for factor_j in factors_j:
                for factor_i in factors_i:
                    current_coeff = coeff(factor_j,-factor_i,i/factor_i,j/factor_j)
                    if current_coeff > best_coeff:
                        best_coeff = current_coeff
                        best_lattice_defining_vectors = [factor_j,-factor_i,i/factor_i,j/factor_j]
    return best_lattice_defining_vectors

# find a basis for the optimal lattice for a given number of points
def lattice_basis(lattice_defining_vectors, num):
    u1 = lattice_defining_vectors[3]/float(num)
    u2 = -lattice_defining_vectors[2]/float(num)
    v1 = -lattice_defining_vectors[1]/float(num)
    v2 = lattice_defining_vectors[0]/float(num)
    return [u1,u2], [v1,v2]
