import sys


class SintaksniAnalizator:
    def __init__(self, data: list):
        self.curr_line, self.it = None, None
        self.data = data
        self.indent = 0
        self.output = ""
        self.program()

    def program(self):
        self.output += "<program>\n"
        self.indent += 1
        self.it = iter(self.data)
        self.curr_line = next(self.it, None)
        self.lista_naredbi()
        print(self.output.strip())

    def lista_naredbi(self):
        self.output += self.calc_indent() + "<lista_naredbi>"
        self.indent += 1
        if self.curr_line is None or self.curr_line.strip() == "":
            self.output += '\n' + self.calc_indent() + "$\n"
            self.indent -= 1
        elif self.curr_line.strip().split()[0] == "KR_AZ":
            self.output += '\n' + self.calc_indent() + "$\n"
            self.indent -= 1
        else:
            self.naredba()
            self.lista_naredbi()
            self.indent -= 1

    def naredba(self) -> None:
        self.output += "\n" + self.calc_indent() + "<naredba>\n"
        self.indent += 1
        if self.curr_line:
            if self.curr_line.strip().split()[0] == "KR_ZA":
                self.za()
            elif self.curr_line.strip().split()[0] == "IDN":
                self.idn()
            else:
                print(f"err {self.curr_line}", end="")
                exit(0)
        self.indent -= 1

    def idn(self) -> None:
        self.output += self.calc_indent() + "<naredba_pridruzivanja>\n"
        self.indent += 1
        self.append_and_move()
        if self.curr_line.strip().split()[0] != "OP_PRIDRUZI":
            print("err" + self.curr_line)
            exit(0)
        self.append_and_move()
        self.exit_if_eof()
        self.e()
        self.indent -= 1

    def e(self) -> None:
        self.output += self.calc_indent() + "<E>\n"
        self.indent += 1
        self.t()
        self.e_lista()
        self.indent -= 1

    def t(self) -> None:
        self.output += self.calc_indent() + "<T>\n"
        self.indent += 1
        self.p()
        self.t_lista()
        self.indent -= 1

    def p(self) -> None:
        self.output += self.calc_indent() + "<P>\n"
        self.indent += 1
        if self.curr_line:
            first_word = self.curr_line.strip().split()[0]
            if first_word in ["OP_PLUS", "OP_MINUS"]:
                self.output += self.calc_indent() + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
                self.p()
            elif first_word == "L_ZAGRADA":
                self.output += self.calc_indent() + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
                self.e()
                self.output += self.calc_indent() + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
            elif first_word in ["IDN", "BROJ"]:
                self.output += self.calc_indent() + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
        self.indent -= 1

    def t_lista(self) -> None:
        self.output += self.calc_indent() + "<T_lista>\n"
        self.indent += 1
        if self.curr_line and self.curr_line.strip().split()[0] in ["OP_PUTA", "OP_DIJELI"]:
            self.output += self.calc_indent() + self.curr_line.strip() + "\n"
            self.curr_line = next(self.it)
            self.t()
        else:
            self.output += self.calc_indent() + "$\n"
        self.indent -= 1

    def e_lista(self) -> None:
        self.output += self.calc_indent() + "<E_lista>\n"
        self.indent += 1
        if self.curr_line and self.curr_line.strip().split()[0] in ["OP_PLUS", "OP_MINUS"]:
            self.output += self.calc_indent() + self.curr_line.strip() + "\n"
            self.curr_line = next(self.it, None)
            self.e()
        else:
            self.output += self.calc_indent() + "$\n"
        self.indent -= 1

    def za(self):
        self.output += self.calc_indent() + "<za_petlja>\n"
        self.indent += 1
        # for kw in ["IDN" "KR_OD", "KR_DO"]

        self.append_and_move()
        self.exit_if_eof()
        self.exit_if_not_type("IDN")

        self.append_and_move()
        self.exit_if_eof()
        self.exit_if_not_type("KR_OD")

        self.append_and_move()
        self.exit_if_eof()
        self.exit_if_type("KR_DO")

        self.e()
        # do
        self.append_and_move()
        self.e()
        self.lista_naredbi()  # how to now process az
        self.append_and_move()
        self.indent -= 1

    def append_and_move(self):
        self.output += self.calc_indent() + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)

    def calc_indent(self) -> str:
        return self.indent * " "

    def exit_if_eof(self):
        if not self.curr_line:
            print("err kraj")
            exit(0)

    def exit_if_type(self, typ: str):
        if self.curr_line.strip().split()[0] == typ:
            print(f"err {self.curr_line}", end="")
            exit(0)

    def exit_if_not_type(self, typ: str):
        if self.curr_line.strip().split()[0] != typ:
            print(f"err {self.curr_line}", end="")
            exit(0)


if __name__ == "__main__":
    SintaksniAnalizator(sys.stdin.readlines())
