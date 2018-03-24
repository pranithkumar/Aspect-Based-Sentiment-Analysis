import numpy as np

# Save
d1={'#':['#','#']}
np.save('../../aws/finalreviewscraper/product_details.npy', d1) 

# Load
read_dictionary = np.load('../../aws/finalreviewscraper/product_details.npy').item()
print(read_dictionary)
print(type(read_dictionary))