"""
    Very Simple Defining Language
            ~* VSDL *~

    Version: 0.0.1        
    
    Intended for storing data in a simplified manner and converting it to different data types and data structures with ease.
    Trayambak Rai / xTrayambak 2021

    Examples:
    Create a file 'yourfile.vsdl' or 'yourfile', then add this into the file
    ```
    @! this is a comment, the parser ignores this.
    foo = bar
    myNumber = 1234
    ```
    then,
    ```
    from vsdl import Parser

    myParser = Parser()
    values = myParser.parse("yourfile.vsdl")
    print(values)
    ``` 

    The output will be in a dictionary, much like JSON.

    ```
    {"foo": "bar", "myNumber": 1234}
    ```

    To convert a .vsdl file into a JSON file (proper conversion),
    use Parser.toJSON
    
    See docs for more info.
"""

from json import dump
import sqlite3

EXTENSION = ".vsdl"

VS_NULL = "NULL"
VS_OPERANDS = [
    "+",
    "-",
    "*",
    "/",
    "^",
    "%"
]

__title__ = "Very Simplistic Defining Language"
__author__ = 'Trayambak "xTrayambak" Rai'
__license__ = "MIT"
__copyright__ = "Copyright 2021 xTrayambak"
__version__ = "0.0.1"

def isOperand(letter):
    if letter in VS_OPERANDS:
        return True
    return False

def isInt(letter):
    try:
        int(letter)
        return True
    except:
        return False

class Parser:
    def __init__(self):
        pass

    def generateTokens(self, line):
        tokens = []
        for _tok in line.split(" "):
            tokens.append(_tok)

        return tokens

    def classifyTokens(self, tokens):
        classified = {
            "name": "",
            "declare_symbol": "",
            "value": ""
        }

        if tokens[0] == "@!":
            return

        for token in tokens:
            idx = tokens.index(token)
            if idx == 0:
                classified["name"] = token
            elif idx == 1:
                classified["declare_symbol"] = token
            elif idx == 2:
                classified["value"] = token

        return classified

    def _finalizeValue(self, value):
        numbers = []
        signs = []
        for letter in value:
            ifIsInt = isInt(letter)
            ifIsOperand = isOperand(letter)
            if ifIsInt:
                numbers.append(int(letter))
            if ifIsOperand:
                signs.append(str(ifIsOperand))

        if len(numbers) > 0 and len(signs) > 0:
            pass

    def finalizeValue(self, value):
        if isInt(value):
            return int(value)
        elif value == "":
            return VS_NULL
        else:
            return str(value)

    def parse(self, file):
        if not EXTENSION in file: 
            file += EXTENSION

        f = open(file, "r")
        data = f.read()

        _d = {}
        
        for line in data.split("\n"):
            tokens = self.generateTokens(line)
            classified = self.classifyTokens(tokens)
            _d.update({
                classified["name"]: self.finalizeValue(classified["value"])
            })

        return _d

    def toJSON(self, file):
        parsedData = self.parse(file)
        _f = file.split(".vsdl")[0]
        _f += ".json"
        
        try:
            dump(parsedData, open(_f, "w"))
            return 0
        except:
            return -1

    def toSqlite3(self, file):
        raise DeprecationWarning("Work in progress; extremely unstable.")
        parsedData = self.parse(file)
        _f = file.split(".vsdl")[0]
        _f += ".db"
        
        db = sqlite3.connect(_f)
        cursor = db.cursor()
        
        for name in parsedData:
            value = parsedData[name]
            if isInt(value):
                cursor.execute("CREATE TABLE values(name TEXT, value INTEGER)")
                cursor.execute("INSERT INTO values VALUES ({}, {})".format(name, int(value)))
            else:
                cursor.execute("CREATE TABLE values(name TEXT, value TEXT)")
                cursor.execute("INSERT INTO values VALUES ({}, {})".format(name, value))