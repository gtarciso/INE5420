x = [0, 0, 1, 0]
y = [0, 1, 1, 1]
i = 0
print(x[0])
z = []
while i < len(x):
    z.append( x[i] and y[i])
    print(z[i])
    i += 1


print(z)
