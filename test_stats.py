from hash_table import LinearProbeTable

table = LinearProbeTable(48, tablesize_override = 13)
f = open("asia_countries.txt", "r")
lst = (f.read().split("\n"))

for name in lst:
    table.__setitem__(name, name+"-value")

f.close()

conflict, probe_total, probe_max, rehash = table.statistics()
self.assertGreaterEqual(conflict, 4)
self.assertGreaterEqual(probe_total, 3)
self.assertGreaterEqual(probe_max, 2)
self.assertGreaterEqual(rehash, 1)
