d1 = {"hello": "name"}
d2 = d1

print(id(d1))
print(id(d2))

d3 = dict(d1)
print d3
print id(d3)