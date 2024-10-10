# Implementation of Method 2 of this thesis on finding identities of Abelian Sandpiles for square grids
# https://fse.studenttheses.ub.rug.nl/21391/1/bMath_2020_DomanN.pdf

from matplotlib import pyplot as plt
import numpy as np
import time
import os.path

#Create topple matrix (4*(identity) - adjacency matrix)
def generate_topple_matrix(w, l):
    n = w*l
    topple_matrix = np.identity(n) * 4
    for i in range(n):
        for j in range(n):
            if (abs(i-j)==1 and i//l == j//l or abs(i-j)==w)and i != j:
                topple_matrix[i%n, j%n] = -1   
    return topple_matrix 

#implementation of T_i (toppling of an individual vertex)
def topple_particle(config, i, tm):
    x = np.zeros(len(config))
    x[i] = 1
    toppled_config = config - np.dot(tm, x)
    return toppled_config 

#implementation of T (toppling of all unstable vertices until sandpile is stable)
def topple_till_stable(config, breakout, tm):
    count = -1
    breakout_counter = 0
    while count != 0 and breakout_counter <= breakout:
        count = 0
        breakout_counter += 1
        for i in range(len(config)):
            if config[i] >= 4: 
                config = topple_particle(config, i, tm)
                count += 1
    if breakout_counter > breakout:
        print("Max topples till stable exceeded, aborting calculation.")
        return np.array(-1)
    return config

#implementation of ⊕, the toppling operation
def toppling_operation(u,v, breakout, tm):
    if len(u) != len(v):
        print("Non-conformal vectors in ⊕!")
        return np.array(-1)
    return topple_till_stable(u + v, breakout, tm)

def save_time_data(w, l, time_taken, method):
    existing = np.load(f"time_data_m{method}.npy") if os.path.isfile(f"time_data_m{method}.npy") else []
    np.save(f"time_data_m{method}.npy", np.append(existing, np.array((w, l, time_taken))))

def grid_identity_method_2(breakout, tm, w, l):
    start = time.time()
    n = w*l
    I = np.dot(tm, np.ones(n))
    while True:
        prev_I = I
        I = toppling_operation(I,I, breakout, tm)   
        if (I == np.array(-1)).all():
            return I
        if (I==prev_I).all():
            end = time.time()
            print(f"Identity returned (method 2) in {end - start} seconds." )
            save_time_data(w, l, end - start, 2)
            return I
        
def grid_identity_method_1(breakout, tm, w, l):
    start = time.time()
    n = w*l
    x = 2 * 3 * np.ones(n)
    I = topple_till_stable(x - topple_till_stable(x, breakout, tm), breakout, tm)
    end = time.time()
    print(f"Identity returned (method 1) in {end - start} seconds." )
    save_time_data(w, l, end - start, 1)
    return I

w = 30
l = 30
tm = generate_topple_matrix(w, l)
result = grid_identity_method_2(10e5, tm, w, l)
if (result != np.array(-1)).all():
    plt.axis("off")
    plt.tight_layout()
    result = result.reshape((w,l))
    plt.imshow(result)
    plt.clim(0, 3)
    plt.savefig(f'images/{w}x{l}.png', bbox_inches='tight')
    plt.show()
else:
    print("Error in calculation, image could not be shown.")
    

