import sys

operators = {
"=": "OP_PRIDRUZI",
    "+": "OP_PLUS",
    "-": "OP_MINUS",
    "*": "OP_PUTA",
    "/": "OP_DIJELI",
    "(": "L_ZAGRADA",
    ")": "D_ZAGRADA",
}

control = {
    "za": "KR_ZA",
    "od": "KR_OD",
    "do": "KR_DO",
    "az": "KR_AZ",
}

for line in enumerate(sys.stdin, start=1):
    curr_line, newline = line[1], ""

    if curr_line.find("//") != -1: curr_line = curr_line[0:curr_line.find("//")]  # remove comments
    if len(curr_line.strip()) == 0: continue # skip empty lines, strip to also remove \n

    prev_char = curr_line[0]
    for curr_char in curr_line:
        if curr_char in operators.keys() or ((prev_char in operators.keys() and curr_char not in operators.keys()) or (prev_char not in operators.keys() and curr_char in operators.keys())):
            newline += " "
        newline += curr_char
        prev_char = curr_char

    newline = newline[0:newline.find("//")]

    beg = 0
    if line[1].split()[0][0].isnumeric():
        while line[1][beg].isnumeric():
            beg += 1

    line = tuple([line[0], newline[0:beg] + " " + newline[beg:]])

    for word in line[1].split():
        if word == "//":
            break
        if word in operators.keys():
            print(f"{operators[word]} {line[0]} {word}")
        elif word[0].isnumeric():
            print(f"BROJ {line[0]} {word}")
        elif word in control.keys():
            print(f"{control[word]} {line[0]} {word}")
        else:
            print(f"IDN {line[0]} {word}")
