import sys
import logging
import itertools

logging.basicConfig(format="[%(levelname)s] %(message)s")
log = logging.getLogger("main")
log.setLevel("INFO")


class compute:
    def __init__(self, data, inputs):
        self.data = data
        self.ip = 0
        self.inputs = inputs
        self.output = []
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
        self.data[dest] = self.inputs.pop()  # int(input())
        return False

    def showOutput(self, src):
        log.debug(f"{src} -> output")
        # print(self.data[src])
        self.output.append(self.data[src])
        return False

    def stop(self):
        log.info("Compute stopped")
        self.running = False
        return True


with open("data.txt") as f:
    for l in f.readlines():
        program = [int(x) for x in l.split(",")]

programs = [
    {
        "data": [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
        "inputs": [4, 3, 2, 1, 0],
        "expected": 43210,
    },
    {
        "data": [
            3,
            23,
            3,
            24,
            1002,
            24,
            10,
            24,
            1002,
            23,
            -1,
            23,
            101,
            5,
            23,
            23,
            1,
            24,
            23,
            23,
            4,
            23,
            99,
            0,
            0,
        ],
        "inputs": [0, 1, 2, 3, 4],
        "expected": 54321,
    },
    {
        "data": [
            3,
            31,
            3,
            32,
            1002,
            32,
            10,
            32,
            1001,
            31,
            -2,
            31,
            1007,
            31,
            0,
            33,
            1002,
            33,
            7,
            33,
            1,
            33,
            31,
            31,
            1,
            32,
            31,
            31,
            4,
            31,
            99,
            0,
            0,
            0,
        ],
        "inputs": [1, 0, 4, 3, 2],
        "expected": 65210,
    },
]

for prog in programs:
    out = 0
    for i in range(5):
        c = compute(prog["data"], [out, prog["inputs"][i]])
        c.run()
        out = c.output[0]
    if out == prog["expected"]:
        print("Success!")
    else:
        print(f"Expected {prog['expected']} but got {out}")
        sys.exit(1)

perms = list(itertools.permutations([0, 1, 2, 3, 4]))

mx = 0
mxperm = []
for perm in perms:
    out = 0
    for i in range(5):
        c = compute(program, [out, perm[i]])
        c.run()
        out = c.output[0]
        if out > mx:
            mxperm = perm
            mx = out

print(mx)
print(mxperm)
