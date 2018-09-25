# RubikLite
A lightweight Python implementation of a Rubik's cube. 

Initial implementation expanded on Problem set 6 from an MIT Algorithms course which can be found here:
https://courses.csail.mit.edu/6.006/fall11/psets.shtml

The implementation of the cube there was for a 2x2 so I included edges to create a 3x3. 
This represented the cube as a 48-tuple. Each corner took 3 places, each edge taking 2. 

After consideration I realized it would be trivial to shrink this down to a 20-tuple by only including 1 piece of information for each corner and 1 piece for each edge. The other information for each piece and each edge can be found from the first one. The orientation of the piece would still be preserved.

For example instead of represting the first 3 of the solved cube in 48-tuple format as (0, 1, 2, ...) it can be represented simply as (0, ... ) because 1 and 2 are known by rotating the data in 0. 
This works because each turn is represented as a permutation of the original cube which preserved the ordering of the pairs. 

Through this process I was able to greatly decrease the amount of data needed to represent the cube.

