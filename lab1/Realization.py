import re
import sys


class Realization:
    def __init__(self):
        self.Operators = ["for", 'do']
        self.Separators = [";", "(", ")"]
        self.Comparis = ["<=", "=>", "!=", "=="]
        self.Controls = [" ", "\t", "\n"]

        self.compar = ''
        self.word = ''
        self.code = []
        self.type = []
        self.index = 0

    def printTable(self):
        for name, type in zip(self.code, self.type):
            print("%-50s" % name, type, "\n")

    def analysisInputLanguage(self):
        for str in sys.stdin:
            for symbol in str:

                self.index += 1

                if symbol in self.Separators:
                    self.analysisWord()
                    self.code.append(symbol)
                    self.type.append("Separators")
                    self.word = ''

                elif not re.match("[a-z A-Z 0-9 ,]*$", self.word) and re.match("[<>!=a-zA-Z0-9 ,]*$", self.word):
                    if str[self.index - 1] == '=' or str[self.index - 1] == '>':
                        self.compar += self.word[-1]
                        self.compar += symbol
                        self.word = self.word[:-1]
                        self.analysisWord()
                        self.code.append(self.compar)
                        self.type.append("Comparis")

                    else:
                        self.compar += self.word[-1]
                        self.word = self.word[:-1]
                        self.analysisWord()
                        self.code.append(self.compar)
                        self.type.append("Assigment")

                    self.compar = ''
                    self.word = ''

                elif not re.match("[0-9 a-z A-Z]*$", self.word) and re.match("[0-9 a-z A-Z #]*$", self.word):
                    self.code.append(str[self.index-2:])
                    self.type.append("Comments")
                    self.word = ''
                    break

                elif symbol in self.Controls:
                    self.analysisWord()

                if symbol not in self.Controls:
                    if symbol in self.Separators:
                        symbol = ''
                    self.word += symbol

            self.index = 0
            self.printTable()
            self.code.clear()
            self.type.clear()

    def analysisWord(self):
        if self.word == "exit":
            sys.exit()

        elif self.word in self.Operators:
            self.code.append(self.word)
            self.type.append("Operators")
            self.word = ''

        elif self.word.isdigit() and re.match("[.]*$", self.word):
            self.code.append(self.word)
            self.type.append("Const")
            self.word = ''

        elif not re.match("[a-z A-Z 0-9 ,]*$", self.word) and re.match("[== a-z A-Z 0-9 ,]*$", self.word):
            self.code.append(self.word)
            self.type.append("Assigment1")
            self.word = ''

        elif re.match("=", self.word):
            self.code.append(self.word)
            self.type.append("Assigment2")
            self.word = ''

        elif self.word in self.Comparis:
            self.code.append(self.word)
            self.type.append("Comparis")
            self.word = ''

        elif re.match("[ ( ) ;]*$", self.word):
            self.word = ''

        elif re.match("[A-Za-z_]*$", self.word):
            self.code.append(self.word)
            self.type.append("Identifier")
            self.word = ''

        else:
            self.code.append(self.word)
            self.type.append("Error")
            self.word = ''

