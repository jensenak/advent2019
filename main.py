import sys
import logging

logging.basicConfig(format="[%(levelname)s] %(message)s")
log = logging.getLogger("main")
log.setLevel("INFO")

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


class compute:
    def __init__(self, data):
        self.data = data
        self.ip = 0
        self.opCodes = {
            1: {"len": 4, "func": self.add},
            2: {"len": 4, "func": self.mult},
            3: {"len": 2, "func": self.getInput},
            4: {"len": 2, "func": self.showOutput},
            5: {"len": 3, "func": self.jumpTrue},
            6: {"len": 3, "func": self.jumpFalse},
            7: {"len": 4, "func": self.comp},
            8: {"len": 4, "func": self.eq},
            99: {"len": 1, "func": self.stop},
        }
        log.debug(f"Initiated with data length {len(data)}")

    def run(self):
        self.running = True
        log.info("Compute started")
        while self.running:
            self.nextOp()

    def nextOp(self):
        raw = str(self.data[self.ip])
        code = int(raw[-2:])  # Get the opcode
        log.debug(f"Got code {code} with IP {self.ip}")
        pointers = []
        for param in range(1, self.opCodes[code]["len"]):  # skip opcode
            if param > len(raw) - 2:  # Leading zeros are dropped
                mode = 0
            else:  # If it's a 1, immediate mode
                mode = int(raw[-(2 + param)])
            if mode == 0:
                pointers.append(self.data[self.ip + param])  # Get value from address
            else:
                log.debug(f"Immediate {self.ip}, {param}")
                pointers.append(self.ip + param)  # Use immediate value
        log.debug(f"Final values: {pointers}")
        jumped = self.opCodes[code]["func"](*pointers)
        if not jumped:
            self.ip += self.opCodes[code]["len"]

    def jumpTrue(self, a, b):
        if self.data[a] > 0:
            self.ip = self.data[b]
            return True
        return False

    def jumpFalse(self, a, b):
        if self.data[a] == 0:
            self.ip = self.data[b]
            return True
        return False

    def comp(self, a, b, dest):
        if self.data[a] < self.data[b]:
            self.data[dest] = 1
        else:
            self.data[dest] = 0
        return False

    def eq(self, a, b, dest):
        if self.data[a] == self.data[b]:
            self.data[dest] = 1
        else:
            self.data[dest] = 0
        return False

    def add(self, a, b, dest):
        log.debug(f"{a} + {b} -> {dest}")
        self.data[dest] = self.data[a] + self.data[b]
        return False

    def mult(self, a, b, dest):
        log.debug(f"{a} * {b} -> {dest}")
        self.data[dest] = self.data[a] * self.data[b]
        return False

    def getInput(self, dest):
        log.debug(f"input -> {dest}")
        self.data[dest] = int(input())
        return False

    def showOutput(self, src):
        log.debug(f"{src} -> output")
        print(self.data[src])
        return False

    def stop(self):
        log.info("Compute stopped")
        self.running = False
        return True


with open("data.txt") as f:
    for l in f.readlines():
        program = [int(x) for x in l.split(",")]
# [3, 0, 101, 4, 0, 0, 2, 13, 0, 0, 4, 0, 99, 5]
programs = [
    program,
    [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8],
    [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8],
    [3, 3, 1108, -1, 8, 3, 4, 3, 99],
    [3, 3, 1107, -1, 8, 3, 4, 3, 99],
    [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
    [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
    [
        3,
        21,
        1008,
        21,
        8,
        20,
        1005,
        20,
        22,
        107,
        8,
        21,
        20,
        1006,
        20,
        31,
        1106,
        0,
        36,
        98,
        0,
        0,
        1002,
        21,
        125,
        20,
        4,
        20,
        1105,
        1,
        46,
        104,
        999,
        1105,
        1,
        46,
        1101,
        1000,
        1,
        20,
        4,
        20,
        1105,
        1,
        46,
        98,
        99,
    ],
]
c = compute(programs[0])
c.run()

