from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
def DTW(datalist):
    data = np.zeros((datalist[0].shape[0], datalist[0].shape[1] * len(datalist)))
    data[:, :datalist[0].shape[1]] = datalist[0]
    for i in range(1, len(datalist)):
        data[0, i * datalist[0].shape[1] : (i + 1) * datalist[0].shape[1]] = datalist[0][0, :]
        for j in range(1, datalist[0].shape[0]):
            distance, path = fastdtw(datalist[0][j, :], datalist[i][j, :], dist=euclidean)
            ynew = datalist[i][j, :][dict(path).values()]
            data[j, i * datalist[0].shape[1] : (i + 1) * datalist[0].shape[1]] = ynew
    return data

