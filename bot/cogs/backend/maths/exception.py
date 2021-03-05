class CalculatorException(Exception):
    pass

class BadCharacter(CalculatorException):
    def __init__(self, message, char, pos):
        self.message = message
        self.char = char
        self.pos = pos

    def __str__(self):
        return f"{self.message}: {self.char} (Pos: {self.pos})"


class BadExpression(CalculatorException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class BadFunction(CalculatorException):
    def __init__(self, message, func):
        self.message = message
        self.func = func

    def __str__(self):
        return f"{self.message}: {self.func}"


class BadBrackets(CalculatorException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)
