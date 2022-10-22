import sys

"""
<program> ::= <lista_naredbi>
<lista_naredbi> ::= <naredba> <lista_naredbi>
<lista_naredbi> ::= $
<naredba> ::= <naredba_pridruzivanja>
<naredba> ::= <za_petlja>
<naredba_pridruzivanja> ::= IDN OP_PRIDRUZI <E>
<za_petlja> ::= KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ
<E> ::= <T> <E_lista>
<E_lista> ::= OP_PLUS <E>
<E_lista> ::= OP_MINUS <E>
<E_lista> ::= $
<T> ::= <P> <T_lista>
<T_lista> ::= OP_PUTA <T>
<T_lista> ::= OP_DIJELI <T>
<T_lista> ::= $
<P> ::= OP_PLUS <P>
<P> ::= OP_MINUS <P>
<P> ::= L_ZAGRADA <E> D_ZAGRADA
<P> ::= IDN
<P> ::= BROJ
"""

class SintaksniAnalizator:
    data: list
    indent: int
    output: str
    curr_line: str

    def __init__(self, data: list):
        self.data = data
        self.indent = 0
        self.output = ""
        self.index = 0
        self.program()
        print(self.output)
        

    def program(self):
        self.output += "<program>\n"
        self.indent += 1
        self.lista_naredbi()

    def lista_naredbi(self):
        self.it = iter(self.data)
        while True:
            self.indent = 1
            self.output += self.indent * " " + "<lista_naredbi>\n"
            self.indent += 1
            self.curr_line = next(self.it, None)
            if (self.curr_line is None or self.curr_line.strip() == ""):
                self.indent += 1
                self.output += self.indent * " " + "$\n"
                self.indent -= 2
                break
            self.naredba()

    def naredba(self) -> None:
        self.output += self.indent * " " + "<naredba>\n"
        self.indent += 1
        if self.curr_line.strip().split()[0] == "KR_ZA": self.za()
        elif self.curr_line.strip().split()[0] == "IDN": self.idn()


    def idn(self) -> None:
        self.output += self.indent * " " + "<naredba_pridruzivanja>\n"
        self.indent += 1
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.curr_line = next(self.it, None)
        if (self.curr_line is None):
            print("err kraj")
            exit(0)
        if (self.curr_line.strip().split()[0] != "OP_PRIDRUZI"):
            print("err" + self.curr_line)
            exit(0)
        self.output += self.indent * " " + self.curr_line.strip() + "\n"
        self.e()
        

    def za(self):
        pass

    def e(self) -> None:
        self.output += self.indent * " " + "<E>\n"
        self.indent += 1
        self.curr_line = next(self.it, None)
        if (self.curr_line is None):
            print("err kraj")
            exit(0)
        self.t()
        self.e_lista()

    def t(self) -> None:
        self.output += self.indent * " " + "<T>\n"
        self.indent += 1
        self.p()
        self.t_lista()

    def p(self) -> None:
        self.output += self.indent * " " + "<P>\n"
        self.indent += 1
        if self.curr_line.strip().split()[0] in ["OP_PLUS", "OP_MINUS"]:
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.p()
        elif self.curr_line.strip().split()[0] == "L_ZAGRADA":
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.e()
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
        elif self.curr_line.strip().split()[0] in ["IDN", "BROJ"]:
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.indent -= 1

    def t_lista(self) -> None:
        self.output += self.indent * " " + "<T_lista>\n"
        self.indent += 1
        if self.curr_line.strip().split()[0] in ["OP_PUTA", "OP_DIJELI"]:
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.t()
        else:
            self.output += self.indent * " " + "$\n"
            self.indent -=2

    def e_lista(self) -> None:
        self.output += self.indent * " " + "<E_lista>\n"
        self.indent += 1
        if self.curr_line.strip().split()[0] in ["OP_PLUS", "OP_MINUS"]:
            self.output += self.indent * " " + self.curr_line.strip() + "\n"
            self.e()
        else:
            self.output += self.indent * " " + "$\n"
            self.indent -=2





"""
<P> ::= OP_PLUS <P>
<P> ::= OP_MINUS <P>
<P> ::= L_ZAGRADA <E> D_ZAGRADA
<P> ::= IDN
<P> ::= BROJ
"""


if __name__ == "__main__":
    data = sys.stdin.readlines()
    SintaksniAnalizator(data)