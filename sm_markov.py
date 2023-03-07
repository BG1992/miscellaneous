from itertools import product
from fractions import Fraction
import numpy as np

inds = []
ords = {}
ind = 0

N = 3
target_sm = 9

for r in range(N+1):
    for prod in product([i for i in range(1, 7)], repeat=r):
        ords[prod] = ind
        inds.append(prod)
        ind += 1

A = np.zeros(shape=(len(ords), len(ords)), dtype=np.float64)
#A2 = [[Fraction(0,1)]*len(ords) for _ in range(len(ords))]

for prod in ords:
    for i in range(1, 7):
        new_prod = (prod + (i,))[-N:]
        A[ords[prod], ords[new_prod]] = 1/6

inds_sm = []
for prod in ords:
    if sum(prod) == target_sm: inds_sm.append(ords[prod])

A = np.delete(A, inds_sm, axis = 0)
A = np.delete(A, inds_sm, axis = 1)

print(A.shape)
B = np.linalg.inv(np.eye(len(ords)-len(inds_sm), dtype=np.float64) - A)
C = np.dot(B, np.ones(shape=len(ords)-len(inds_sm)))

print(C)

inds2 = []
ords2 = {}
ind2 = 0

ords2[(0, None, 0)] = 0
inds2.append((0, None, 0))
ind2 += 1

for r in range(1, N+1):
    for first_num in range(1, 7):
        for sm in range(6*N+1):
            ords2[(r, first_num, sm)] = ind2
            inds2.append((r, first_num, sm))
            ind2 += 1

print(len(ords2))

A2 = np.zeros(shape=(len(ords2), len(ords2)), dtype=np.float64)

for prod in ords:
    if len(prod) > 0:
        first_num = prod[0]
    else:
        first_num = None
    p = (len(prod), first_num, sum(prod))
    for i in range(1, 7):
        new_prod = (prod + (i,))[-N:]
        new_p = (len(new_prod), new_prod[0], sum(new_prod))
        A2[ords2[p], ords2[new_p]] += 1

for i in range(A2.shape[0]):
    sm = A2[i,:].sum()
    if sm > 0:
        A2[i,:] /= sm

inds_sm2 = []
for prod in ords2:
    if prod[2] == target_sm and prod[0] == N: inds_sm2.append(ords2[prod])

A2 = np.delete(A2, inds_sm2, axis = 0)
A2 = np.delete(A2, inds_sm2, axis = 1)

print(A2.shape)
B2 = np.linalg.inv(np.eye(len(ords2)-len(inds_sm2), dtype=np.float64) - A2)
C2 = np.dot(B2, np.ones(shape=len(ords2)-len(inds_sm2)))

print(C2)