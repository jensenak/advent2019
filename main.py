with open("data.txt") as f:
    data = f.readline()

print(len(data))

mn = 150
sm = 0
for i in range(100):
    r = i * 150
    z = data[r : r + 150].count("0")
    o = data[r : r + 150].count("1")
    t = data[r : r + 150].count("2")
    print(f"{i}: {z+o+t} {z} {o} {t}")
    if z < mn:
        mn = z
        sm = o * t
        print(f"{mn} {z} {sm}")

print(sm)

