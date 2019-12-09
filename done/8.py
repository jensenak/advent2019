with open("data.txt") as f:
    data = f.readline()

pic = ["2" for _ in range(150)]
for z in range(100):
    for x in range(150):
        d = data[x + (z * 150)]
        if pic[x] == "2":
            pic[x] = d
for i in range(len(pic)):
    if i % 25 == 0:
        print()
    if pic[i] == "0":
        print(" ", end="")
    else:
        print(pic[i], end="")
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

