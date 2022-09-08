import sys

types = ["IDN", "BROJ", "OP_PRIDRUZI"]

for line in enumerate(sys.stdin, start=1):
    # "preparsing"
    line = tuple([line[0],line[1].strip()])
    newline = ""
    past_type, this_type = None, None
    for i in range(len(line[1])):
        if line[1][i].isalpha():
            this_type = "IDN"
        elif line[1][i].isdigit():
            this_type = "BROJ"
        elif line[1][i] == "=":
            this_type = "OP_PRIDRUZI"
        if this_type != past_type:
            newline += " " + line[1][i]
        else:
            newline += line[1][i]
    line = tuple([line[0],newline])

    if line[1].split()[0] == 'za':
        continue # TODO solve this case later

    if line[1].split()[0][0].isnumeric():
        beg = 0
        for char in line[1].split()[0]:
            if char.isnumeric():
                beg += 1
            else:
                print(f"BROJ {line[0]} {line[1].split()[0][0:beg]}")
                break
    else: beg = 0
    print("IDN", line[0], line[1].split()[0][beg:])

    if len(line[1].split()) > 1 and line[1].split()[1] == '=':
        print("OP_PRIDRUZI", line[0], line[1].split()[1])

    # TODO je li ispravna pretpostavka da ću, ako imam jednako, imat broj desno od njega?
    if len(line[1].split()) > 2 and line[1].split()[2].isnumeric():
        print("BROJ", line[0], line[1].split()[2])