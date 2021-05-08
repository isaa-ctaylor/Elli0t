try:
    from .exception import BadBrackets, CalculatorException, BadCharacter, BadExpression, BadFunction
except ImportError:
    from exception import BadBrackets, CalculatorException, BadCharacter, BadExpression, BadFunction
import math
import re
import traceback


class func:
    def __init__(self, name: str, variables: dict, value: str):
        self.name = name
        self.variables: dict = variables
        self.value = value

    def __str__(self):
        variables = ", ".join(self.variables)
        return f"{self.name}({variables}) = {self.value}"


def parse_variables(fx, variables: dict, funcs: dict):
    split = fx.split(";")

    assignment = split[:-1]
    new_fx = split[-1]

    for i in assignment:
        tempvars = []
        if "=" in i:
            if i.startswith("def"):
                function, value = i[4:].split("=", 1)

                try:
                    name = function.replace(" ", "").split("(")[0]
                    tempvars = function.replace(" ", "").split(
                        "(")[-1].split(")")[0].split(",")
                    value = value.replace(" ", "")
                except:
                    raise BadFunction(
                        "The function is not defined properly", name or "Unknown")

                if str(name) in funcs:
                    raise BadExpression(f"Cannot redefine variable: {name}")

                elif str(name) in variables:
                    raise BadExpression(
                        f"Variable \"{name}\" has matching name to variable")

                funcs[str(name)] = func(str(name), tempvars, value)


            elif not i.startswith("def"):
                variable, value = i.split("=", 1)
                variable = variable.replace(" ", "")
                vaule = value.replace(" ", "")
                if variable in variables:
                    raise BadExpression(f"Cannot redefine variable: {variable}")

                elif variable in funcs:
                    raise BadExpression(f"Variable \"{variable}\" has matching name to function")

                else:            
                    variables[str(variable)] = str(eval(value, variables, funcs))

    return new_fx, variables, funcs

    


def parse(fx):

    variables = {}
    functions = {}

    if ";" in fx:
        while ";" in fx:
            fx, variables, functions = parse_variables(fx, variables, functions)

    return eval(fx, variables, functions)


def eval(fx: str, variables: dict, funcs: dict):
    fx = fx.strip().lower().replace(" ", "")
    fx = fx.lower().replace("**", "^")

    value = 0.0
    number = ""
    function = ""
    hasNumber = False
    hasFunction = False

    i = 0

    while (i < len(fx)):
        character = fx[i]

        if character == '*':
            new_fx = nextFunction(fx[i + 1:len(fx)])
            if hasNumber == True:
                numb = number
                value = float(numb) * float(eval(new_fx, variables, funcs))
                hasNumber = False
                number = ""
            elif hasFunction == True:
                value = float(eval(function, variables, funcs)) * \
                    float(eval(new_fx, variables, funcs))
                hasFunction = False
                function = ""
            else:
                value = float(value) * float(eval(new_fx, variables, funcs))
            i = i + len(new_fx)
        elif character == '+':

            new_fx = nextMinusFunction(fx[i + 1:len(fx)])
            if hasNumber == True:
                numb = number
                value = float(numb) + float(eval(new_fx, variables, funcs))
                hasNumber = False
                number = ""
            elif hasFunction == True:
                value = float(eval(function, variables, funcs)) + \
                    float(eval(new_fx, variables, funcs))
                hasFunction = False
                function = ""
            else:
                value = float(value) + float(eval(new_fx, variables, funcs))
            i += len(new_fx)
        elif character == '-':

            new_fx = nextMinusFunction(fx[i + 1:len(fx)])
            if hasNumber == True:
                numb = number
                value = float(numb) - float(eval(new_fx, variables, funcs))
                hasNumber = False
                number = ""
            elif hasFunction == True:
                value = float(eval(function, variables, funcs)) - \
                    float(eval(new_fx, variables, funcs))
                hasFunction = False
                function = ""
            else:
                value = float(value) - float(eval(new_fx, variables, funcs))
            i += len(new_fx)
        elif character == '/':
            new_fx = nextFunction(fx[i + 1:len(fx)])
            if hasNumber == True:
                numb = number
                value = float(numb) / float(eval(new_fx, variables, funcs))
                hasNumber = False
                number = ""
            elif hasFunction == True:
                value = float(eval(function, variables, funcs)) / \
                    float(eval(new_fx, variables, funcs))
                hasFunction = False
                function = ""
            else:
                value = float(value) / float(eval(new_fx, variables, funcs))
            i = i + len(new_fx)
        elif character == '^':
            new_fx = nextFunction(fx[i + 1:len(fx)])
            if hasNumber == True:
                numb = number
                value = math.pow(float(numb), float(eval(new_fx, variables, funcs)))
                hasNumber = False
                number = ""
            elif hasFunction == True:
                value = math.pow(float(eval(function, variables, funcs)),
                                 float(eval(new_fx, variables, funcs)))
                hasFunction = False
                function = ""
            else:
                value = math.pow(float(value), float(eval(new_fx, variables, funcs)))
            i = i + len(new_fx)
        elif character == '0' or character == '1' or character == '2' or character == '3' or character == '4' or character == '5' or character == '6' or character == '7' or character == '8' or character == '9':

            if hasFunction == True:
                function += character

            else:
                hasNumber = True
                number = number + character
                if i == len(fx) - 1:
                    value = number
                    number = ""
                    hasNumber = False

        elif character == '.':
            if i == len(fx) - 1:
                raise BadExpression("The expression ends in \".\"")

            if hasNumber == True and len(number) > 0:
                number += character

        elif character == '(':

            if i == len(fx) - 1:
                raise BadExpression("The expression ends in \"(\"")

            new_fx = fx[i + 1:nextBracket(fx)]
            if hasFunction == True:
                if function == "sin":
                    value = math.sin(float(eval(new_fx, variables, funcs)))

                elif function == "cos":
                    value = math.cos(float(eval(new_fx, variables, funcs)))

                elif function == "tan":
                    value = math.tan(float(eval(new_fx, variables, funcs)))

                elif function == "sinh":
                    value = math.sinh(float(eval(new_fx, variables, funcs)))

                elif function == "cosh":
                    value = math.cosh(float(eval(new_fx, variables, funcs)))

                elif function == "tanh":
                    value = math.tanh(float(eval(new_fx, variables, funcs)))

                elif function == "asin":
                    value = math.asin(float(eval(new_fx, variables, funcs)))

                elif function == "acos":
                    value = math.acos(float(eval(new_fx, variables, funcs)))

                elif function == "atan":
                    value = math.atan(float(eval(new_fx, variables, funcs)))

                elif function == "log":
                    value = math.log(float(eval(new_fx, variables, funcs)))

                elif function == "log10":
                    value = math.log10(float(eval(new_fx, variables, funcs)))

                elif function == "sqrt":
                    value = math.sqrt(float(eval(new_fx, variables, funcs)))


                elif function in ["factorial", "fact"]:
                    value = math.factorial(float(eval(new_fx, variables, funcs)))


                else:
                    if len(funcs) > 0:
                        try:
                            func = funcs[str(function)]

                            temp = func.value

                            for p, j in enumerate(func.variables):
                                temp = temp.replace(str(j), str(new_fx.replace(
                                    " ", "").split(",")[p]))

                            value = float(eval(temp, variables, funcs))
                        except Exception as e:
                            raise BadFunction(
                                "The function is not well defined", str(function))

                    else:
                        raise BadFunction(
                            "The function is not defined", str(function))

                hasFunction = False
                function = ""

            else:
                value = eval(new_fx, variables, funcs)

            i = i + len(new_fx) + 1

        elif character == ')':
            raise BadBrackets(" '(' is not finished ")

        elif character == ' ':
            j = 0
        else:
            if isValidCharacter(character):
                function = function + character
                hasFunction = True

                if i == len(fx) - 1:

                    if function == "e":
                        value = math.e

                    elif function == "pi":
                        value = math.pi

                    elif function == "tau":
                        value = math.tau

                    elif len(variables) > 0:
                        try:
                            value = getValue(function, variables)
                        except:
                            raise BadCharacter(
                                "Invalid character", str(function), i + 1)

                    else:
                        raise BadCharacter(
                            "Invalid character", str(function), i + 1)

            else:
                raise BadCharacter("Invalid character", str(character), i + 1)

        i += 1
    return value


def getValue(function, xi):

    value = 0
    if len(function) == 1:

        if isinstance(xi, dict):

            if function.lower() in xi:
                value = xi[function.lower()]
            elif function.upper() in xi:
                value = xi[function.upper()]
            else:
                raise BadFunction(
                    "Function is not well defined", str(function))

        elif isinstance(xi, int):
            value = xi
        elif isinstance(xi, float):
            value = xi
        elif isinstance(xi, str):
            value = eval(xi, xi)
        else:
            raise BadFunction("Function is not well defined", str(function))

    return value


def nextFunction(fx):

    fx = fx.strip()

    result = ""

    i = 0

    while (i < len(fx)):
        character = fx[i]

        if character == '+' or character == '-' or character == '*' or character == '/':
            i = len(fx)

        elif character == '^' or character == '.' or character == ' ':
            result += character

        elif character == '(':

            new_fx = fx[i:nextBracket(fx)+1]
            result += new_fx
            i = (i + len(fx))-1

        elif character == ')':
            raise BadBrackets(" '(' is not finished ")

        else:
            if isValidNumericAndCharacter(character):
                result = result + character
            else:
                raise BadCharacter("Invalid character", str(character), i + 1)
        i += 1

    return result


def nextMinusFunction(fx):

    fx = fx.strip()

    result = ""

    i = 0

    while (i < len(fx)):

        character = fx[i]

        if character == '+' or character == '-':
            i = len(fx)

        elif character == '^' or character == '.' or character == ' ' or character == '*' or character == '/':
            result += character

        elif character == '(':

            new_fx = fx[i:nextBracket(fx)+1]
            result += new_fx
            i = (i + len(fx))-1

        elif character == ')':
            raise BadBrackets(" '(' is not finished ")

        else:
            if isValidNumericAndCharacter(character):
                result = result + character
            else:
                raise BadCharacter("Invalid character", str(character), i + 1)

        i += 1
    return result


def isValidCharacter(character):

    regexCharacter = re.compile('[a-z]')
    result = False

    if regexCharacter.match(character):
        result = True
    else:
        result = False

    return result


def isValidNumericAndCharacter(character):

    regexNumericAndCharacter = re.compile('\w')
    result = False

    if regexNumericAndCharacter.match(character):
        result = True
    else:
        result = False

    return result


def nextBracket(fx):

    result = 0
    count = 0

    for i in range(0, len(fx)):
        character = fx[i]

        if character == '(':
            result = i
            count = count+1

        elif character == ')':
            result = i
            count = count-1
            if count == 0:
                return i
        else:
            result = i

    if count != 0:
        raise BadBrackets("Bracket is not closed")

    return result
