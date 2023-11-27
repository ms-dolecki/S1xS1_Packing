# S1xS1_Packing
 Pack n points ~evenly in S1xS1

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
`NUMBER_OF_PARTICLES` is an integer value for the number of points u wish to pack.  
`TILE_RANGE` is an integer value that tells the program the range of $S^{1} \times S^{1}$ tiles to consider interactions between. If set to 1, only particles from the same or adjacent tiles will influence eachother.  
`FORCE_ORDER` is a float which determines the strength of particle interactions. For particles distance $D$ apart, the repulsive force is $\frac{1}{D^{p+1}}$. This should be set between 3 and 5  
`SENSITIVITY` is a float which determines the speed of the gradient descent. This should be set between 2 and 5.  
`DECAY` is a float which determines how much the `SENSITIVITY` value is reduced after each iteration of the gradient descent. Values between 1.005 and 1.1 work well  
`ITERATIONS` is an integer value for the number of iterations of gradient descent to be run.  
After iterating `SEARCH_BLOCK_ITERATIONS`, the program will set the configuration to the best-known solution found up to that point and then continue the gradient descent. Set this value to a fifth or tenth of the total number of iterations.  
`ANIMATE` is a boolean that determines whether to animate each step of the gradient descent. Set to True to animate.  
`BOUNDING_CIRCLES` is a boolean that tells the program to draw maximum bounding circles at the end of the program if set to True.

# Output
The program will print a statement every time `SEARCH_BLOCK_ITERATIONS` run and will also print two values at the end of the run to evaluate the evenness of the packing. The first is the total area of the bounding circles in one tile of $S^{1} \times S^{1}$, assuming said tile is of dimension 1x1. Bounding circles are expanded uniformally from each point until they hit other bounding circles. The second is the normalized variance of the radii of the bounding circles, assuming the average radius is 1.  
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

In orange and red are the lattice axes connecting three of the points in the square. The triangles formed from these axes and the sides of the square can be arranged into a quadralateral with two right angles:

<img width="276" alt="Screen Shot 2023-11-27 at 1 54 05 PM" src="https://github.com/ms-dolecki/S1xS1_Packing/assets/151703986/4e3c3ee9-76df-438a-bb68-4e7c0105b76a">

If the lattice is not regular then the spacing of points along the orange sides will not match that along the green sides. Let $\vec{A} \coloneqq (a_1,a_2) \in \mathbb{Z} \times \mathbb{Z}$ denote the pair of green lengths (let indices denote left-right order, so $a_1$ refers to the left-most green side and $a_2$ the right-most), where unit distance is the distance between points along the green axis, and $\vec{B} \coloneqq (b_1,b_2) \in \mathbb{Z} \times \mathbb{Z}$ denote the pair of orange lengths, where unit distance is the distance between points along the green axis. Let the distance between points along the green axis be the unit length on the quadralateral. Then the distance between points on the orange sides is $\frac{\lVert\vec{B}\rVert}{\lVert\vec{A}\rVert}$ and the left-right diaganal has length $\lVert\vec{A}\rVert$. To get the length of the up-down diaganal, $L$, the side length of the square, we can use the law of sines. Specifically, if $\alpha,\beta$ denote the interior angeles of the left and right vertices, $L=\lVert\vec{A}\rVert \cdot \sin{\alpha}=\lVert\vec{A}\rVert \cdot \sin{\beta}$. If u were to scale down the quadralateral by a factor of $\lVert\vec{A}\rVert$, the length of a given side would become equal to the sine of the opposite interior angle on the corresponding green-or-orange right triangle. From this and the law of sines we can get $L=\lVert\vec{A}\rVert \cdot \frac{\lVert\vec{B}\rVert}{\lVert\vec{A}\rVert} \cdot \frac{a_1b_2 + a_2b_1}{{\lVert\vec{A}\rVert}^2}$
