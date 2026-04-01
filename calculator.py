class Calculator:
    def __init__(self):
        self.operation = {"(": 0, ")": 1, "+": 2, "-": 2, "*": 3, "/": 3}
        self.unary_minus = False
        self.expression = ""
        self.tokens = []
        self.rpn = []
        self.result = None

    def start_calculator(self, expression):
        self.expression = expression
        self.unary_minus = False

        if type(expression) is not str:
            raise ValueError("Введено не строчное выражение")
        elif len(expression) == 0:
            raise ValueError("Пустое выражение")
        else:
            self.token()
        return self.rpn

    def check_priority(self, symbol):
        if symbol == "(":
            self.tokens.append(symbol)
            self.unary_minus = True
            return

        if symbol == ")":
            while self.tokens and self.tokens[-1] != "(":
                self.rpn.append(self.tokens.pop())
            if self.tokens and self.tokens[-1] == "(":
                self.tokens.pop()
            self.unary_minus = False
            return

        if symbol == "-" and self.unary_minus:
            self.tokens.append("~")
            return

        while self.tokens and self.tokens[-1] != "(" and self.tokens[-1] != "~" and self.operation[symbol] <= self.operation[self.tokens[-1]]:
            self.rpn.append(self.tokens.pop())

        self.tokens.append(symbol)
        self.unary_minus = True

    def token(self):
        symbol = ""
        i = 0
        self.unary_minus = True

        while i < len(self.expression):
            char = self.expression[i]

            if char not in self.operation.keys():
                symbol += char
                i += 1
                self.unary_minus = False
            else:
                if symbol != "":
                    self.rpn.append(symbol)
                    symbol = ""

                if char == "-" and self.unary_minus:
                    if i + 1 < len(self.expression) and self.expression[i + 1] == "(":
                        self.tokens.append("~")
                        i += 1
                        continue
                    elif i + 1 < len(self.expression) and self.expression[i + 1] not in self.operation.keys():
                        symbol = "-"
                        i += 1
                        continue
                    else:
                        self.tokens.append("~")
                        i += 1
                        continue

                self.check_priority(char)
                i += 1

        if symbol != "":
            self.rpn.append(symbol)

        while self.tokens:
            self.rpn.append(self.tokens.pop())

    def calculate(self, expression=None, variables=None):
        if expression is not None:
            self.tokens = []
            self.rpn = []
            self.start_calculator(expression)

        if not self.rpn:
            raise ValueError("Нет выражения для вычисления")

        stack = []

        for token in self.rpn:
            if token in self.operation or token == "~":
                if token == "~":
                    if len(stack) < 1:
                        raise ValueError("Недостаточно операндов для унарного минуса")
                    a = stack.pop()
                    result = -a
                    stack.append(result)
                else:
                    if len(stack) < 2:
                        raise ValueError(f"Недостаточно операндов для операции {token}")
                    b = stack.pop()
                    a = stack.pop()

                    if token == "+":
                        result = a + b
                    elif token == "-":
                        result = a - b
                    elif token == "*":
                        result = a * b
                    elif token == "/":
                        if b == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        result = a / b
                    else:
                        raise ValueError(f"Неизвестный оператор {token}")

                    stack.append(result)
            else:
                if variables and token in variables:
                    value = variables[token]
                else:
                    try:
                        value = float(token)
                    except ValueError:
                        if token.isalpha():
                            raise ValueError(f"Неизвестная переменная '{token}'. "
                                             f"Укажите значение в параметре variables")
                        else:
                            raise ValueError(f"Неверный операнд '{token}'")

                stack.append(value)

        if len(stack) != 1:
            raise ValueError(f"Ошибка вычисления: в стеке осталось {len(stack)} элементов")

        self.result = stack[0]
        return self.result


if __name__ == "__main__":
    string = "18+18-2*(-13+6-3/5)-64"
    rpn = Calculator()
    print(rpn.calculate(string))
