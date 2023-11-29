# S1xS1_Packing
 Pack n points ~evenly in S1xS1.

 # Description
 This tool finds an evenly-spaced packing of $n$ points in the torus $S^{1} \times S^{1}$. This is done by treating points as mutually-repulsive particles and using gradient descent to find a low-energy configuration. With coordinates $`(\theta,\omega) \in \mathbb{R}/\mathbb{Z} \times \mathbb{R}/\mathbb{Z}`$, distance $D$ between points $`(\theta_{1},\omega_{1}),(\theta_{2},\omega_{2})`$ is measured using the euclidean distance $\sqrt{(\theta_{1}-\theta_{2})^{2} + (\omega_{1}-\omega_{2})^{2}}$. The repulsive force between particles is $\frac{1}{D^{p}}$, with $p$ a `FORCE_ORDER` paramater set when running the program. The energy function is then proportional to $\frac{1}{D^{p-1}}$. Considering the distance between points is tricky because the same coordinate can be expressed multiple ways, e.g., $`(0.5,0.5)\equiv(-0.5,1.5)`$. If u tile the plane with copies of $S^{1} \times S^{1}$, this trick is seen in the fact that you can draw multiple straight lines between two given points, depending on which tiles you choose to represent those points. This program considers interactions across mutiple tiles, e.g., a point at $`(1,1)`$ will be repelled by both representations of the point $`(0.5,0.5)\equiv(-0.5,1.5)`$ according to the distance formula above. Because the force of interactions diminishes rapidly with distance, u only need to consider interactions between tiles within `TILE_RANGE` of each other, another paramater set when running the program.

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
`NUMBER_OF_PARTICLES` (default 1) is an integer value for the number of points u wish to pack.  
`TILE_RANGE` (default 2)is an integer value that tells the program the range of $S^{1} \times S^{1}$ tiles to consider interactions between. If set to 1, only particles from the same or adjacent tiles will influence eachother.  
`FORCE_ORDER` (default 6) is a float which determines the strength of particle interactions. For particles distance $D$ apart, the repulsive force is $\frac{1}{D^{p+1}}$. Seting this between 3 and 7 seems to work well.  
`SENSITIVITY` (default 0.0001) is a float which determines the speed of the gradient descent. The best value for this paramater seems to vary with the number of points as well as the `DECAY` paramter below. If `DECAY` is large enough then `SENSITIVITY` will drop very fast and so can be set initially high with a value maybe between 1 and 5. If `DECAY` is very small then it is best to start with a small `SENSITIVITY`, potentially on the order of ~0.00001.  
`DECAY` (default 1.005) is a float which determines the factor by which the `SENSITIVITY` value is reduced after each iteration of the gradient descent. This should be $1+\epsilon$.  
`ITERATIONS` (default 0) is an integer value for the number of iterations of gradient descent to be run.  
After iterating `SEARCH_BLOCK_ITERATIONS` (default 100), the program will set the configuration to the best-known solution found up to that point and then continue the gradient descent. Setting this value between 10 and 100 seems to work well.  
`ANIMATE` is an optional flag that determines whether to animate each step of the gradient descent. Include to animate.  
`BOUNDING_CIRCLES` is an optional flag that determines whether to draw maximum bounding circles at the end of the program. Include to draw.

# Output
The program will print a statement every time `SEARCH_BLOCK_ITERATIONS` run and will also print two values at the end of the run to evaluate the evenness of the packing. The first is the total area of the bounding circles in one tile of $S^{1} \times S^{1}$, assuming said tile is of dimension 1x1. Bounding circles are expanded uniformaly from each point until they hit other bounding circles. The second is the normalized variance of the radii of the bounding circles, assuming the average radius is 1.  
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

# Theory
One easy way to arrange points on $S^{1} \times S^{1}$ is with a lattice. If a lattice is compatible it will be possible to draw a square from four points in the lattice as in the picture below:

<img width="413" alt="Screen Shot 2023-11-27 at 1 25 04 PM" src="https://github.com/ms-dolecki/S1xS1_Packing/assets/151703986/69e20145-fac7-4dd1-a435-7337b830ea9e">

In orange and green are four line segments along the lattice connecting three of the points in the square. Label the lengths of these segments, in terms of the number of points traversed along them, $a_1,a_2,b_1,b_2$.  $a_1$ is the length of the rightmost green segment, traversed while moving between the bottom-left and bottom-right points of the square, and $b_1$ is the length of the rightmost orange segment, traversed while moving between the same two points of the square. $a_2$ is the length of the leftmost green segment and $b_2$ the length of the leftmost orange segment. Note that the actual distance separating points along the orange and green axes may differ if the lattice is not regular, e.g., the units differ between $a_1,a_2$ and $b_1,b_2$. Define the length $a_2$ to be negative becuase the corresponding segment extends in the negative-green direction from the bottom-left point of the square.

You can imagine rotating these segments about the center of the square to complete a parallelogram. Perform a linear transformation on the lattice so that it becomes a square lattice with unit-length spacing. If the bottom-most and left-most sides of the drawn-square on the original lattice are basis vectors, this transformation is represented with the matrix ${a_1 \enspace a_2 \choose b_1 \enspace b_2}$. The area of the tranformed-square is then $a_1b_2-a_2b_1$. Because the drawn-square tiled the original lattice in identical copies, so does this transformed-square on the new lattice. This means, since the density of points on the new lattice is $1/unit^2$, that the number of points contained in the transformed-square, and thus the original drawn-square, must be the equal to its area, or $n = a_1b_2-a_2b_1$.  

The preimage of a unit square of lattice points in the new lattice is a parallelogram in the original lattice. From the inverse of the transfomation matrix, the basis vectors of this parallelogram are ${b_2/n \choose -b_1/n},{-a_2/n \choose a_1/n}$. If we flip these basis vectors across the second coordinate axis (changing the sign of the first coordinate), rotate the first vector 180 degrees (changing the sign of both its coordinates), and then flip the first and second coordinate axes, the resulting parallelogram, with basis vectors ${b_1/n \choose b_2/n},{a_1/n \choose a_2/n}$, has the exact same shape as the first (although rotated and translated). Call this new parallelogram $\mathcal{P}$. Define $\vec{A}\coloneqq{a_1 \choose a_2},\vec{B}\coloneqq{b_1 \choose b_2}\$. Note $n = |\vec{A}\times\vec{B}| \implies \mathcal{P}$ has area $|\vec{A}\times\vec{B}|^{-1}$. If we tile $\mathcal{P}$ along the original lattice, the bounding circles centered at the vertices in this tiling have diameter equal to the shortest distance between points in the lattice. That is $\min \\{ \lVert x_1\frac{\vec{A}}{n}+x_2\frac{\vec{B}}{n}\rVert \\}$ with $(x_1,x_2)\neq(0,0)\in\mathbb{Z}\times\mathbb{Z}$. The total area of the bounding circles of the $n$ points in the 1x1 $S_{1} \times S_{1}$ tile is $\frac{\pi}{4}\cdot\frac{\min \\{ x_1^2\lVert\vec{A}\rVert^2+2x_1x_2\langle\vec{A},\vec{B}\rangle+x_2^2\lVert\vec{B}\rVert^2 \\}}{n}$. The expression in the numerator of the second fraction is a positive-definite binary quadratic form and so can be put into a [reduced form](http://mathonline.wikidot.com/reduced-binary-quadratic-forms>) $ax_1^2 + bx_1x_2 + cx_2^2$, which takes on a minimum non-zero value equal to the leading coefficient $a$. For a given, $\vec{A},\vec{B}$, denote this obtained leading coefficient $\mathnormal{Coeff(\vec{A},\vec{B})}$. For a given number of points, $n=\vec{A}\times\vec{B}$, the best choice of lattice-defining vectors $\vec{A},\vec{B}$ then is the one which maximizes $\mathnormal{Coeff(\vec{A},\vec{B})}$.

# Advanced Usage
If you want to configure the points to start in one of the optimal lattices, found using the method described above, add the `--lattice` flag to the command. You can view properties of the lattice itself without performing gradient descent by setting `--iterations` to 0 (default). Example:
```
python s1xs1_pack.py --number_of_particles 15 --lattice
Total circle area (in 1x1 S1xS1) = 0.890117918517. Normalized radius variance (average radius 1) = 1.57772181044e-30
```
Note that the lattice solution is not always the best one, evaluated on total bounding circle area given an equal-radius constraint, as is clearly seen in the case of 3 points.
