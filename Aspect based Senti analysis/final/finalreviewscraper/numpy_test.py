import numpy as np

# Load
read_dictionary = np.load('product_details.npy').item()
print(read_dictionary)
print(type(read_dictionary))