# Tetrahedron Volume Calculator

This Python script calculates the smallest possible volume of a tetrahedron formed by points from a given file, where each point has three spatial coordinates and a numerical attribute. The tetrahedrons are formed from points whose numerical attributes sum to exactly 100.

## Functions

### `volume_of_tetrahedron(p1, p2, p3, p4)`

Calculates the volume of a tetrahedron given four points in 3D space. Each point is a tuple of four values (x, y, z, n), where x, y, and z represent spatial coordinates, and n is ignored in this calculation. The volume is computed using the scalar triple product of vectors formed by these points.

**Parameters:**
- `p1, p2, p3, p4`: Tuples representing the points in 3D space.

**Returns:**
- The absolute value of the scalar triple product divided by 6, representing the volume of the tetrahedron.

### `read_points(filename)`

Reads points from a specified file. Each line in the file should contain a point represented by four float values separated by commas, formatted as (x, y, z, n).

**Parameters:**
- `filename`: Path to the file containing the points.

**Returns:**
- A list of tuples, where each tuple represents a point and contains four float values: x, y, z, and n.

### `process_chunk(chunk)`

Processes a chunk of points to find the tetrahedron with the smallest volume. This function is intended to be used with multiprocessing to handle large datasets efficiently.

**Parameters:**
- `chunk`: A subset of the total points.

**Returns:**
- A tuple containing the smallest volume found in the chunk and the indices of the points forming this tetrahedron.

### `find_smallest_tetrahedron(filename)`

Coordinates the reading of points from a file and the distributed processing of these points to find the smallest possible tetrahedron volume.

**Parameters:**
- `filename`: Path to the file containing the points.

**Returns:**
- A list of indices of the points forming the tetrahedron with the smallest volume.


