from pprint import pprint


carte = """
  J3J3J3J3J3J3  J2J2J2J2
  J3J3J3J3J3J3  J2J2J2J2
  J3J3J3J3J3J3  J2J2J2J2
  """

pprint(carte)
print("----------------")
lines = carte.split("\n")
pprint(lines)

print("---------------")
size_brick=2
temp = list()
for line in lines:
    temp.append([line[i:i+size_brick] for i in range(0, len(line), size_brick)])

print("---------------")
lines=temp[:]
pprint(lines)





