import logging
import numpy as np
from scipy.spatial import KDTree
from itertools import combinations
import sys
import multiprocessing
from tqdm import tqdm

def volume_of_tetrahedron(p1, p2, p3, p4):
    AB = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    AC = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    AD = (p4[0] - p1[0], p4[1] - p1[1], p4[2] - p1[2])
    cross_product_x = AB[1] * AC[2] - AB[2] * AC[1]
    cross_product_y = AB[2] * AC[0] - AB[0] * AC[2]
    cross_product_z = AB[0] * AC[1] - AB[1] * AC[0]
    scalar_triple_product = (AD[0] * cross_product_x + AD[1] * cross_product_y + AD[2] * cross_product_z)
    return abs(scalar_triple_product) / 6.0

def read_points(filename):
    with open(filename, 'r') as file:
        points = []
        for line_number, line in enumerate(file, 1):
            try:
                x, y, z, n = map(float, line.strip()[1:-1].split(','))
                points.append((x, y, z, n))
            except ValueError as e:
                print(f"Error reading line {line_number}: {line.strip()}. Error: {e}")
    return points

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_chunk(chunk):
    logging.info("Starting chunk with size: {}".format(len(chunk)))
    spatial_coords = [p[:3] for p in chunk]
    tree = KDTree(spatial_coords)
    smallest_volume = sys.float_info.max
    best_indices = []

    dynamic_k = min(60, len(chunk) - 1)
    for idx in range(len(chunk)):
        _, indices = tree.query(spatial_coords[idx], k=dynamic_k)
        if len(indices) >= 4:
            for combo in combinations(indices, 4):
                p1, p2, p3, p4 = chunk[combo[0]], chunk[combo[1]], chunk[combo[2]], chunk[combo[3]]
                if (p1[3] + p2[3] + p3[3] + p4[3]) == 100:
                    vol = volume_of_tetrahedron(p1, p2, p3, p4)
                    if vol < smallest_volume:
                        smallest_volume = vol
                        best_indices = [chunk.index(p) for p in [p1, p2, p3, p4]]
    logging.info("Completed chunk with best volume: {}".format(smallest_volume))
    return smallest_volume, best_indices


def find_smallest_tetrahedron(filename):
    points = read_points(filename)
    if len(points) < 4:
        print("Error: Need at least four points to form a tetrahedron.")
        return []

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    dynamic_chunk_size = max(10, len(points) // (10 * num_processes)) 

    chunk_size = dynamic_chunk_size 

    chunks = [points[i:i + chunk_size] for i in range(0, len(points), chunk_size)]
    
    results = list(tqdm(pool.imap(process_chunk, chunks), total=len(chunks)))

    smallest_volume = sys.float_info.max
    best_group_indices = []
    for volume, indices in results:
        if volume < smallest_volume:
            smallest_volume = volume
            best_group_indices = indices

    pool.close()
    pool.join()
    return best_group_indices

if __name__ == '__main__':
    small_result = find_smallest_tetrahedron('points_small.txt')
    print("Smallest tetrahedron indices for small file:", small_result)

    large_result = find_smallest_tetrahedron('points_large.txt')
    print("Smallest tetrahedron indices for large file:", large_result)
