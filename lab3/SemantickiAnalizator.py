import sys


def main():
    blstack, output, curr_line, prev_line, za_declaration, circ_def_chk = [[]], "", 0, -1, False, None
    for line in [x.strip().split() for x in sys.stdin]:
        prev_line = curr_line
        if line[0] == "KR_ZA":
            blstack.append([])
            za_declaration = True
        elif line[0] == "KR_AZ":
            blstack.pop()
        elif line[0] == "IDN":
            curr_line = line[1]
            if circ_def_chk is not None and circ_def_chk[1] != curr_line: circ_def_chk = None
            if za_declaration:
                blstack[-1].append((curr_line, line[2]))
                circ_def_chk, za_declaration = (line[2], curr_line), False
            elif curr_line != prev_line and not lol_contains(blstack, line[2]):
                blstack[-1].append((curr_line, line[2]))
                circ_def_chk = (line[2], curr_line)
            elif curr_line == prev_line and lol_contains(blstack, line[2]):
                if circ_def_chk is not None and circ_def_chk[0] == line[2]:
                    output += f"err {curr_line} {line[2]}"
                    break
                else:
                    output += f"{curr_line} {get_row_from_2d_list(blstack, line[2])} {line[2]}\n"
            elif not lol_contains(blstack, line[2]):
                output += f"err {curr_line} {line[2]}"
                break
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
