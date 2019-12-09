import sys
import logging
import itertools
import threading
import queue

logging.basicConfig(stream=sys.stdout, format="[%(levelname)s] %(message)s")
log = logging.getLogger("main")
log.setLevel("INFO")


class ioQueue:
    def __init__(self, name="io"):
        self.name = name

    def put(self, v):
        print(f"{self.name}: {v}")

    def get(self):
        return int(input(f"{self.name}? "))


class dynamicMemory(list):
    def __getitem__(self, idx):
        if idx >= len(self):
            log.debug(f"{idx} out of range, returning 0")
            return 0
        return list.__getitem__(self, idx)

    def __setitem__(self, idx, v):
        if idx >= len(self):
            log.debug(f"{idx} is greater than {len(self)}, growing list")
            self.extend([0] * (idx + 1 - len(self)))
        list.__setitem__(self, idx, v)


class compute:
    def __init__(self, name, data, qs):
        self.data = dynamicMemory(data.copy())
        self.ip = 0
        self.bp = 0
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
            9: {"len": 2, "func": self.moveBP},
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
        log.debug(f"{self.name}: [{self.ip}] > {self.data[self.ip]}")
        pointers = []
        for param in range(1, self.opCodes[code]["len"]):  # skip opcode
            if param > len(raw) - 2:  # Leading zeros are dropped
                mode = 0
            else:  # If it's a 1, immediate mode
                mode = int(raw[-(2 + param)])
            if mode == 1:
                log.debug(f"{self.name}: Immediate {param} ({self.ip + param})")
                pointers.append(self.ip + param)  # Use immediate value
            elif mode == 2:
                log.debug(
                    f"{self.name}: Relative {self.bp} {self.ip + param}({self.data[self.ip + param]})"
                )
                pointers.append(
                    self.bp + self.data[self.ip + param]
                )  # Use relative value
            else:
                pointers.append(self.data[self.ip + param])  # Get value from address
        log.debug(f"{self.name}: Performing {code} with {pointers}")
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

    def moveBP(self, value):
        self.bp += self.data[value]
        log.info(f"{self.name}: bp + {value}({self.data[value]}) = {self.bp}")

    def stop(self):
        log.info(f"{self.name} stopped")
        # log.debug(f"{self.data}")
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

ioQ = ioQueue()
end = ioQueue("exit")
compute(0, program, {"in": ioQ, "out": ioQ, "exit": end}).run()

# programs = [
#     {
#         "data": [
#             109,
#             1,
#             204,
#             -1,
#             1001,
#             100,
#             1,
#             100,
#             1008,
#             100,
#             16,
#             101,
#             1006,
#             101,
#             0,
#             99,
#         ]
#     },
#     {"data": [1102, 34915192, 34915192, 7, 4, 7, 99, 0]},
#     {"data": [104, 1125899906842624, 99]},
#     {"data": [3, 20, 1008, 20, 1, 21, 4, 21, 99]},
# ]

# prog = 3
# compute(0, programs[prog]["data"], {"in": ioQ, "out": ioQ, "exit": end}).run()

