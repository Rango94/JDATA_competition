import numpy as np

a=np.array([[1,2],[3,4]])
b=np.array([1,2])

print(np.where((b==a).all(1))[0])