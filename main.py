import sys

testData = {14: 2, 1969: 966, 100756: 50346}
fuelCalc = lambda x: int(int(x) / 3) - 2


def getData():
    with open(sys.argv[1]) as f:
        weights = f.readlines()
    return weights


def moduleFuel(weights):
    fuel = 0
    for w in weights:
        f = fuelCalc(w)
        g = fuelFuel(f) + f
        fuel += g
    return fuel


def fuelFuel(fuel):
    f = fuelCalc(fuel)
    g = 0
    if f > 0:
        g = fuelFuel(f)
        # print(f"Called with {fuel} got {f} + {g}")
        return f + g
    else:
        # print(f"Ending with {f}")
        return 0


if __name__ == "__main__":
    for value, answer in testData.items():
        result = moduleFuel([value])
        if result == answer:
            print("Passed")
        else:
            print(f"Failed; value {value} returned {result} but expected {answer}")
            sys.exit()
    print(moduleFuel(getData()))

