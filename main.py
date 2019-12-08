with open("data.txt") as f:
    data = f.readline()

pic = [0 for _ in range(15000)]
for z in range(100):
    for x in range(150):
        d = data[x * z]
        if d != 2:
            pic[x] = d
for y in range(6):
    for x in range(25):
        print(pic[y * 25 + x], end="")
# print(len(data))

# mn = 150
# sm = 0
# for i in range(100):
#     r = i * 150
#     z = data[r : r + 150].count("0")
#     o = data[r : r + 150].count("1")
#     t = data[r : r + 150].count("2")
#     print(f"{i}: {z+o+t} {z} {o} {t}")
#     if z < mn:
#         mn = z
#         sm = o * t
#         print(f"{mn} {z} {sm}")

# print(sm)

