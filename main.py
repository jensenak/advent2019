import sys

testData = [
    {
        "values": [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
        "answer": [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
    },
    {"values": [1, 0, 0, 0, 99], "answer": [2, 0, 0, 0, 99]},
    {"values": [2, 3, 0, 3, 99], "answer": [2, 3, 0, 6, 99]},
    {"values": [2, 4, 4, 5, 99, 0], "answer": [2, 4, 4, 5, 99, 9801]},
    {"values": [1, 1, 1, 4, 99, 5, 6, 0, 99], "answer": [30, 1, 1, 4, 2, 5, 6, 0, 99]},
]
realData = [
    1,
    12,
    2,
    3,
    1,
    1,
    2,
    3,
    1,
    3,
    4,
    3,
    1,
    5,
    0,
    3,
    2,
    10,
    1,
    19,
    1,
    6,
    19,
    23,
    1,
    23,
    13,
    27,
    2,
    6,
    27,
    31,
    1,
    5,
    31,
    35,
    2,
    10,
    35,
    39,
    1,
    6,
    39,
    43,
    1,
    13,
    43,
    47,
    2,
    47,
    6,
    51,
    1,
    51,
    5,
    55,
    1,
    55,
    6,
    59,
    2,
    59,
    10,
    63,
    1,
    63,
    6,
    67,
    2,
    67,
    10,
    71,
    1,
    71,
    9,
    75,
    2,
    75,
    10,
    79,
    1,
    79,
    5,
    83,
    2,
    10,
    83,
    87,
    1,
    87,
    6,
    91,
    2,
    9,
    91,
    95,
    1,
    95,
    5,
    99,
    1,
    5,
    99,
    103,
    1,
    103,
    10,
    107,
    1,
    9,
    107,
    111,
    1,
    6,
    111,
    115,
    1,
    115,
    5,
    119,
    1,
    10,
    119,
    123,
    2,
    6,
    123,
    127,
    2,
    127,
    6,
    131,
    1,
    131,
    2,
    135,
    1,
    10,
    135,
    0,
    99,
    2,
    0,
    14,
    0,
]


def opCode(data, a):
    if data[a] == 99:
        # print("Done")
        return False
    else:
        b = data[a + 1]
        c = data[a + 2]
        d = data[a + 3]
    # print(f"Addrs {b}, {c}, {d}, values {data[b]}, {data[c]}, {data[d]}")
    if data[a] == 1:
        data[d] = data[b] + data[c]
    elif data[a] == 2:
        data[d] = data[b] * data[c]
    else:
        print("Error! Invalid OpCode")
    # print(f"New value: {data[d]}")
    return True


for test in testData:
    sp = 0
    while opCode(test["values"], sp):
        sp += 4
    if test["values"] != test["answer"]:
        print("Failed!")
        print(test)
        sys.exit()
    print("Passed")

for i in range(99):
    for j in range(99):
        data = realData.copy()
        data[1] = i
        data[2] = j
        ip = 0
        while opCode(data, ip):
            ip += 4
        if data[0] == 19690720:
            print(f"{i}{j}")

