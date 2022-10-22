import os

dirs = sorted(os.listdir("tests"))
failed = []

maxname = max([len(x) for x in dirs])

for test in dirs:
    print(f"Running test {test}", end="")
    res = os.popen(
        f"python3 SintaksniAnalizator.py < tests/{test}/test.in").read()
    if res == open(f"tests/{test}/test.out", "r").read():
        print(f"{(maxname - len(test)) * ' '}\tOK")
    else:
        print(f"{(maxname - len(test)) * ' '}\tFAIL")
        # print(f"Expected: {open(f'tests/{test}/test.out', 'r').read()}")
        # print(f"Got: {res}")
        failed.append(test)
print(f"Summary: {len(dirs) - len(failed)}/{len(dirs)} tests passed")
