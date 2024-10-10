from matplotlib import pyplot as plt
import numpy as np


def load_time_data(f):
    data = np.load(f)
    w = np.array(0)
    l = np.array(0)
    t = np.array(0)
    for i in range(0, len(data), 3):
        w = np.append(w, int(data[i]))
        l = np.append(l, int(data[i+1]))
        t = np.append(t, data[i+2])
    return w, l, t

data_1 = load_time_data("time_data_m1.npy")
data_2 = load_time_data("time_data_m2.npy")

plt.plot(data_1[0], data_1[2], 'bo')
plt.plot(data_2[0], data_2[2], 'ro')
plt.show()