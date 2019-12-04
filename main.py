testData = [
    {"combo": [1, 1, 1, 1, 1, 1], "valid": True},
    {"combo": [1, 2, 3, 4, 5, 6], "valid": False},
    {"combo": [1, 2, 3, 4, 5, 0], "valid": False},
]

low = [3, 5, 5, 5, 5, 5]  # 353096
hi = [7, 9, 9, 9, 9, 9]  # 843212

# RULES
# 6 digits
# No digit can be lower than one to its left
# Two digits are the same


def valid(combo):
    if len(combo) != 6:  # too short
        return False
    if len(set(combo)) == 6:  # no duplicates
        return False
    last = 0
    for d in combo:
        if d < last:
            return False
        last = d
    return True


def add(combo, d):
    if d < 0:
        return combo
    if combo[d] == 9:
        combo[d] = add(combo, d - 1)[d - 1]
    else:
        combo[d] += 1
    return combo


for test in testData:
    out = valid(test["combo"])
    if out == test["valid"]:
        print("Passed")
    else:
        print("Failed")

combos = 0
while low[0] < 8:
    if valid(low):
        # print(low)
        combos += 1
    low = add(low, 5)

print(combos)

