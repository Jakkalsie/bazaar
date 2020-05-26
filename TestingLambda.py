arr = [[0, 1], [2, 3]]


def new_array(a):
    new_array = []
    for item in a:
        new_array.append(item[1])
    return new_array


def new_array_lambda(a): return a[:][1]


print(new_array(arr))
print(new_array_lambda(arr))

print([item[1] for item in arr])
