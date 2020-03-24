# Generative model - test

import sys
import numpy as np
import util as u

X_test_fpath = './data/X_test'
output_fpath = './output_{}.csv'

npzfile = np.load('save_gn.npz')
X_test = npzfile['arr_0']
w = npzfile['arr_1']
b = npzfile['arr_2']

with open(X_test_fpath) as f:
    next(f)
    X_test = np.array([line.strip('\n').split(',')[1:] for line in f], dtype = float)

# Predict testing labels
predictions = 1 - u._predict(X_test, w, b)
with open(output_fpath.format('generative'), 'w') as f:
    f.write('id,label\n')
    for i, label in  enumerate(predictions):
        f.write('{},{}\n'.format(i, label))

# Print out the most significant weights
ind = np.argsort(np.abs(w))[::-1]
with open(X_test_fpath) as f:
    content = f.readline().strip('\n').split(',')
features = np.array(content)
for i in ind[0:10]:
    print(features[i], w[i])
