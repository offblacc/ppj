import sys

def main():
    blstack = [[]] # short for block stack, as in every new block of code adds a list to the stack
    output = ""
    curr_line = 0
    prev_line = -1
    for line in sys.stdin:
        line = line.strip().split()
        prev_line = curr_line
        if line[0] == "OP_ZA":
            blstack.append([])
        elif line[0] == "OP_AZ":
            blstack.pop()
        elif line[0] == "IDN":
            curr_line = line[1]
            if curr_line == prev_line:
                if lol_contains(blstack, line[2]):
                    output += line[1] + " " + get_row_from_2d_list(blstack, line[2]) + " "  + line[2] + '\n'
            else:
                blstack[-1].append((line[1], line[2]))

    print(blstack)
    print(output.strip())

def lol_contains(l: list, e: any):
    for subl in l:
        for elem in subl:
            if elem[1] != e: continue
            return True
    return False

def get_row_from_2d_list(l: list, e: any):
    for subl in reversed(l):
        for elem in reversed(subl):
            if elem[1] == e:
                return elem[0]


if __name__ == "__main__":
    main()

