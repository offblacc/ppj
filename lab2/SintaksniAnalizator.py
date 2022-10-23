import sys


class SintaksniAnalizator:
    data: list
    indent: int
    output: str
    curr_line: str

    def __init__(self, data: list):
        self.it = None
        self.data = data
        self.indent = 0
        self.output = ""
        self.index = 0
        self.program()

    def program(self):
        self.output += "<program>\n"
        self.indent += 1
        self.it = iter(self.data)
        self.curr_line = next(self.it, None)
        self.lista_naredbi()
        print(self.output.strip())

    def lista_naredbi(self):
        self.output += self.indent * " " + "<lista_naredbi>"
        self.indent += 1
        if self.curr_line is None or self.curr_line.strip() == "" or self.curr_line.strip().split()[0] == "KR_AZ":
            self.output += '\n' + self.indent * " " + "$\n"
            self.indent -= 1
            return
        self.naredba()
        self.lista_naredbi()

    def naredba(self) -> None:
        self.output += "\n" + self.indent * " " + "<naredba>\n"
        self.indent += 1
        if self.curr_line:
            if self.curr_line.strip().split()[0] == "KR_ZA":
                self.za()
            elif self.curr_line.strip().split()[0] == "IDN":
                self.idn()
        self.indent -= 1

    def idn(self) -> None:
        self.output += self.indent * " " + "<naredba_pridruzivanja>\n"
        self.indent += 1
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        if self.curr_line.strip().split()[0] != "OP_PRIDRUZI":
            print("err" + self.curr_line)
            exit(0)
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        if not self.curr_line:
            print("err kraj")
            exit(0)
        self.e()
        self.indent -= 1

    def e(self) -> None:
        self.output += self.indent * " " + "<E>\n"
        self.indent += 1
        self.t()
        self.e_lista()
        self.indent -= 1

    def t(self) -> None:
        self.output += self.indent * " " + "<T>\n"
        self.indent += 1
        self.p()
        self.t_lista()
        self.indent -= 1

    def p(self) -> None:
        self.output += self.indent * " " + "<P>\n"
        self.indent += 1
        if self.curr_line:
            first_word = self.curr_line.strip().split()[0]
            if first_word in ["OP_PLUS", "OP_MINUS"]:
                self.output += self.indent * " " + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
                self.p()
            elif first_word == "L_ZAGRADA":
                self.output += self.indent * " " + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
                self.e()
                self.output += self.indent * " " + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
            elif first_word in ["IDN", "BROJ"]:
                self.output += self.indent * " " + self.curr_line.strip() + "\n"
                self.curr_line = next(self.it, None)
        self.indent -= 1

    def t_lista(self) -> None:
        self.output += self.indent * " " + "<T_lista>\n"
        self.indent += 1
        if self.curr_line and self.curr_line.strip().split()[0] in ["OP_PUTA", "OP_DIJELI"]:
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.curr_line = next(self.it)
            self.t()
        else:
            self.output += self.indent * " " + "$\n"
        self.indent -= 1

    def e_lista(self) -> None:
        self.output += self.indent * " " + "<E_lista>\n"
        self.indent += 1
        if self.curr_line and self.curr_line.strip().split()[0] in ["OP_PLUS", "OP_MINUS"]:
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.curr_line = next(self.it, None)
            self.e()
        else:
            self.output += self.indent * " " + "$\n"
        self.indent -= 1

    # KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ
    def za(self):
        self.output += self.indent * " " + "<za_petlja>\n"
        self.indent += 1
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        # idn
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        # od
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        if not self.curr_line:
            print("err kraj")
            exit(0)
        if self.curr_line.strip().split()[0] not in ["OP_PLUS", "OP_MINUS"]:
            print(f"err {self.curr_line}", end="")
            exit(0)
        self.e()
        # do
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        self.e()
        self.lista_naredbi()  # how to now process az
        self.indent -= 1
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        self.indent -= 1

    def do(self):
        pass

    def az(self):
        pass



if __name__ == "__main__":
    SintaksniAnalizator(sys.stdin.readlines())
