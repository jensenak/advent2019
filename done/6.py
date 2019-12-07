class space:
    def __init__(self, name, parent=None):
        self.satellites = []
        self.name = name
        self.parent = parent

    def addSatellite(self, sat):
        self.satellites.append(sat)

    def countOrbits(self, parents):
        own = parents
        for sat in self.satellites:
            own += sat.countOrbits(parents + 1)
        return own

    def hasSatellite(self, sat):
        # print(f"search from {self.name}")
        if sat in self.satellites:
            print(f"{self.name} has it")
            return [self.name]
        else:
            for subsat in self.satellites:
                resp = subsat.hasSatellite(sat)
                if resp:
                    print(f"found it around {self.name}")
                    resp.append(self.name)
                    return resp
        return None

    def parentSearch(self, sat):
        uppath = []
        downpath = []
        cur = self.parent
        while True:
            downpath = cur.hasSatellite(sat)
            if downpath:
                uppath.extend(downpath)
                return uppath
            uppath.append(cur.name)
            if cur.parent:
                cur = cur.parent
            else:
                return []


with open("data.txt") as f:
    data = f.readlines()

system = {}
for line in data:
    mass, sat = line.strip().split(")")

    if mass not in system.keys():
        system[mass] = space(mass)
    if sat not in system.keys():
        system[sat] = space(sat, system[mass])
    else:
        system[sat].parent = system[mass]
    system[mass].addSatellite(system[sat])

cur = system[mass]
while cur.parent:
    cur = cur.parent

print(cur.countOrbits(0))

cur = system["YOU"]
path = cur.parentSearch(system["SAN"])
print(path)
print(len(path))
