import sys
import logging
import itertools
import threading
import queue

logging.basicConfig(stream=sys.stdout, format="[%(levelname)s] %(message)s")
log = logging.getLogger("main")
log.setLevel("WARN")


class compute:
    def __init__(self, name, data, qs):
        self.data = data.copy()
        self.ip = 0
        self.name = name
        self.qs = qs
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
        log.debug(f"{self.name}: Initiated with data length {len(data)}")

    def run(self):
        self.running = True
        log.info(f"{self.name} started")
        while self.running:
            self.nextOp()

    def nextOp(self):
        raw = str(self.data[self.ip])
        code = int(raw[-2:])  # Get the opcode
        log.debug(f"{self.name}: Got code {code} with IP {self.ip}")
        pointers = []
        for param in range(1, self.opCodes[code]["len"]):  # skip opcode
            if param > len(raw) - 2:  # Leading zeros are dropped
                mode = 0
            else:  # If it's a 1, immediate mode
                mode = int(raw[-(2 + param)])
            if mode == 0:
                pointers.append(self.data[self.ip + param])  # Get value from address
            else:
                log.debug(f"{self.name}: Immediate {self.ip}, {param}")
                pointers.append(self.ip + param)  # Use immediate value
        log.debug(f"{self.name}: Final values: {pointers}")
        jumped = self.opCodes[code]["func"](*pointers)
        if not jumped:
            self.ip += self.opCodes[code]["len"]

    def jumpTrue(self, a, b):
        log.debug(f"{self.name}: Jump if {a} ({self.data[a]} > 0)")
        if self.data[a] > 0:
            self.ip = self.data[b]
            return True
        return False

    def jumpFalse(self, a, b):
        log.debug(f"{self.name}: Jump if {a} ({self.data[a]} == 0)")
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
        log.debug(f"{self.name}: {a} ({self.data[a]}) + {b} ({self.data[b]}) -> {dest}")
        self.data[dest] = self.data[a] + self.data[b]
        return False

    def mult(self, a, b, dest):
        log.debug(f"{self.name}: {a} ({self.data[a]}) * {b} ({self.data[b]}) -> {dest}")
        self.data[dest] = self.data[a] * self.data[b]
        return False

    def getInput(self, dest):
        self.data[dest] = self.qs["in"].get()  # self.inputs.pop()  # int(input())
        log.info(f"{self.name}: IN -> {dest} = {self.data[dest]}")
        return False

    def showOutput(self, src):
        # print(self.data[src])
        # self.output.append(self.data[src])
        self.qs["out"].put(self.data[src])
        log.info(f"{self.name}: {src} = {self.data[src]} -> OUT")
        return False

    def stop(self):
        log.info(f"{self.name} stopped")
        self.running = False
        self.qs["exit"].put(self.name)
        return True


def main(program, phases):
    qs = [queue.Queue(maxsize=0) for i in range(5)]
    xq = queue.Queue(maxsize=0)
    cs = []
    # Create and start processors
    for i in range(5):
        cs.append(compute(i, program, {"in": qs[i - 1], "out": qs[i], "exit": xq}))
        qs[i - 1].put(phases[i])  # Phase config is the first queue item
        threading.Thread(target=cs[i].run).start()
    qs[4].put(0)  # Put this in to start the process

    done = 0
    while done < 5:
        msg = xq.get()
        done += 1
        log.warning(f"{msg} finished")

    return qs[4].get()


with open("data.txt") as f:
    for l in f.readlines():
        program = [int(x) for x in l.split(",")]

programs = [
    {
        "data": [
            3,
            26,
            1001,
            26,
            -4,
            26,
            3,
            27,
            1002,
            27,
            2,
            27,
            1,
            27,
            26,
            27,
            4,
            27,
            1001,
            28,
            -1,
            28,
            1005,
            28,
            6,
            99,
            0,
            0,
            5,
        ],
        "phases": [9, 8, 7, 6, 5],
        "expected": 139629729,
    },
    {
        "data": [
            3,
            52,
            1001,
            52,
            -5,
            52,
            3,
            53,
            1,
            52,
            56,
            54,
            1007,
            54,
            5,
            55,
            1005,
            55,
            26,
            1001,
            54,
            -5,
            54,
            1105,
            1,
            12,
            1,
            53,
            54,
            53,
            1008,
            54,
            0,
            55,
            1001,
            55,
            1,
            55,
            2,
            53,
            55,
            53,
            4,
            53,
            1001,
            56,
            -1,
            56,
            1005,
            56,
            6,
            99,
            0,
            0,
            0,
            0,
            10,
        ],
        "phases": [9, 7, 8, 5, 6],
        "expected": 18216,
    },
]

prog = 1
out = main(programs[prog]["data"], programs[prog]["phases"])
if out == programs[prog]["expected"]:
    print("Success!")
else:
    print(f"Got {out} but expected {programs[prog]['expected']}")

perms = list(itertools.permutations([5, 6, 7, 8, 9]))

mx = 0
mxperm = []
for perm in perms:
    out = main(program, perm)
    if out > mx:
        mxperm = perm
        mx = out

print(mx)
print(mxperm)
