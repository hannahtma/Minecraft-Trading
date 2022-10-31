from hash_table import LinearProbeTable

table = LinearProbeTable(21)
f = open("names.txt", "r")
lst = (f.read().split("\n"))
for name in lst:
    table.__setitem__(name, name+"-value")
f.close()
print(table.statistics())

table = LinearProbeTable(21)
f = open("asia_countries.txt", "r")
lst = (f.read().split("\n"))
for name in lst:
    table.__setitem__(name, name+"-value")
f.close()
print(table.statistics())
