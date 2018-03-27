import numpy as np
di = {'#':['#','#']}
di = np.save('product_details.npy',di)

# Load
read_dictionary = np.load('product_details.npy').item()
print(read_dictionary)
print(type(read_dictionary))
