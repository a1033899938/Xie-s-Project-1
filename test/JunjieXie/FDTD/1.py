import numpy as np
Ix = np.array([[1, 2], [3, 4], [5, 6]])
print(Ix)
Ix = np.abs(Ix) ** 2
print(Ix)
Ix = Ix[:, ::-1]
print(Ix)
Ix = Ix.T
print(Ix)
print(np.shape(Ix))