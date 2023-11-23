# S1xS1_Packing
 Pack n points ~evenly in S1xS1

 # Description
 This tool finds an evenly-spaced packing of $n$ points in the torus $S^{1} \times S^{1}$. This is done by treating points as mutually-repulsive particles and using gradient descent to find a low-energy configuration. With coordinates $`(\theta,\omega) \in \mathbb{R}/\mathbb{Z} \times \mathbb{R}/\mathbb{Z}`$, distance $D$ between points $`(\theta_{1},\omega_{1}),(\theta_{2},\omega_{2})`$ is measured using the euclidean distance $\sqrt{(\theta_{1}-\theta_{2})^{2} + (\omega_{1}-\omega_{2})^{2}}$. The repulsive force between particles is $\frac{1}{D^{p+1}}$, with $p$ a `FORCE_ORDER` paramater set when running the program. The energy function is then proportional to $\frac{1}{D^{p}}$. Considering the distance between points is tricky becuase the same coordinate can be expressed multiple ways, e.g., $`(0.5,0.5)\equiv(-0.5,1.5)`$. If u tile the plane with copies of $S^{1} \times S^{1}$, this trick is seen in the fact that you can draw multiple straight lines between two given points, depending on which tiles you choose to represent those points. This program considers interactions across mutiple tiles, e.g., a point at $`(1,1)`$ will be repelled by both representations of the point $`(0.5,0.5)\equiv(-0.5,1.5)`$ according to the distance formula above. Because the force of interactions diminishes rapidly with distance, u only need to consider interactions between tiles within `TILE_RANGE` of each other, another paramater set when running the program.

 # Instructions
 Run the program with the following command:  
 ```
 python s1xs1_pack.py --number_of_particles NUMBER_OF_PARTICLES --tile_range TILE_RANGE --force_order FORCE_ORDER --sensitivity SENSITIVITY --decay DECAY --iterations ITERATIONS --search_block_iterations SEARCH_BLOCK_ITERATIONS --animate ANIMATE --bounding_circles BOUNDING_CIRCLES
```  
 With sample values:  
 ```
 python s1xs1_pack.py --number_of_particles 8 --tile_range 2  --force_order 5 --sensitivity 4 --decay 1.01 --iterations 5000 --search_block_iterations 1000 --animate True --bounding_circles True
```

 # Parameters
`NUMBER_OF_PARTICLES` is an integer value for the number of points u wish to pack.  
`TILE_RANGE` is an integer value that tells the program the range of $S^{1} \times S^{1}$ tiles to consider interactions between. If set to 1, only particles from the same or adjacent tiles will influence eachother.  
`FORCE_ORDER` is a float which determines the strength of particle interactions. For particles distance $D$ apart, the repulsive force is $\frac{1}{D^{p+1}}$. This should be set between 3 and 5  
`SENSITIVITY` is a float which determines the speed of the gradient descent. This should be set between 1 and 5.  
`DECAY` is a float which determines how much the `SENSITIVITY` value is reduced after each iteration of the gradient descent. This should be set between 1.005 and 1.1.  
`ITERATIONS` is an integer value for the number of iterations of gradient descent to be run.  
After iterating `SEARCH_BLOCK_ITERATIONS`, the program will set the configuration to the best-known solution found up to that point and then continue the gradient descent. Set this value to a fifth or tenth of the total number of iterations.  
`ANIMATE` is a boolean that determines whether to animate each step of the gradient descent. Set to True to animate.  
`BOUNDING_CIRCLES` is a boolean that tells the program to draw maximum bounding circles at the end of the program if set to True.

# Output
The program will print a statement every time `SEARCH_BLOCK_ITERATIONS` run and will also print two values at the end of the run to evaluate the eveness of the packing. The first is the total area of the bounding circles in one tile of $S^{1} \times S^{1}$, assuming said tile is of dimension 1x1. Bounding circles are expanded uniformally from each point until they hit other bounding circles. The second is the normalized variance of the radii of the bounding circles, assuming the average radius is 1.  
Sample output:  
```
python s1xs1_pack.py --number_of_particles 8  --tile_range 2 --sensitivity 4 --decay 1.01 --iterations 5000 --search_block_iterations 1000 --animate True --bounding_circles True --force_order 5
search_block_complete
search_block_complete
search_block_complete
search_block_complete
search_block_complete
Total circle area (in 1x1 S1xS1) = 0.785012559394. Normalized radius variance (average radius 1) = 3.45636776242e-07
```
<img width="486" alt="Screen Shot 2023-11-22 at 12 55 29 AM" src="https://github.com/ms-dolecki/S1xS1_Packing/assets/151703986/c878c396-afb3-451e-823c-faa35983989b">

