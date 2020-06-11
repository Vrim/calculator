from __future__ import annotations

from typing import Union, List
import doctest


class Calculator:

    @staticmethod
    def calculate(equation: Equation) -> Union[int, float]:
        """Takes an Equation and returns the answer
        """
        return equation.evaluate()

    def check_input(self, s: str) -> Union[int, float]:
        eq = Equation(s)
        return self.calculate(eq)


class Equation:
    content: str

    def __init__(self, content: str) -> None:
        self.content = content.replace(" ", "")

    def __str__(self) -> str:
        return self.content

    def evaluate(self) -> Union[Equation, int, float]:
        if self.content.isdigit():
            return int(self.content)
        elif self.content.replace(".", "", 1).isdigit():
            return float(self.content)
        elif '(' in self:
            if ')' not in self:
                raise UnevenBracketError
            return self.eval_brackets().evaluate()
        elif ')' in self:
            raise UnevenBracketError
        elif '[' in self:
            if ']' not in self:
                raise UnevenBracketError
            return self.eval_brackets('[', ']').evaluate()
        elif ']' in self:
            raise UnevenBracketError
        elif '^' in self:
            equations = self.split("^")
            value = equations[0].evaluate()
            for eq in equations[1:]:
                value **= eq.evaluate()
        elif '+' in self:
            equations = self.split('+')
            value = equations[0].evaluate()
            for eq in equations[1:]:
                value += eq.evaluate()
        # Check if minus sign or negative number
        elif '-' in self and \
            (self.content.index('-') > 0) and \
            (self.content[(self.content.index('-') - 1)] not in "*/+-^%(["): 
            equations = self.split('-')
            value = equations[0].evaluate()
            for eq in equations[1:]:
                value -= eq.evaluate()        
        elif '*' in self:
            equations = self.split('*')
            value = equations[0].evaluate()
            for eq in equations[1:]:
                value *= eq.evaluate()
        elif '/' in self:
            equations = self.split('/')
            value = equations[0].evaluate()
            for eq in equations[1:]:
                value /= eq.evaluate()
        elif '%' in self:
            equations = self.split('%')
            value = equations[0].evaluate()
            for eq in equations[1:]:
                value %= eq.evaluate()
        # This is a negative symbol, not minus sign.
        elif '-' in self and \
            (self.content.index('-') == 0) or \
            (self.content[(self.content.index('-') - 1)] in "*/+-^%(["):
            value = (-1) * Equation(self.content[1:]).evaluate()
        else:
            raise NoOperatorError
        return value

    def eval_brackets(self, l_br: str = '(', r_br: str = ')') -> Union[Equation, int, float]:
        c = self.content
        openbr = 1
        closebr = 0
        index_of_end = -1
        start = c.find(l_br)
        for i in range(start + 1, len(c)):
            if c[i] == r_br:
                closebr += 1
            elif c[i] == l_br:
                openbr += 1
            if openbr == closebr:
                index_of_end = i
                break
        left_side = c[:start]
        right_side = c[index_of_end + 1:]

        # Check if there is an operator beside the bracket, else, multiply
        if len(left_side) > 0:
            end_l = left_side[-1]
            if end_l not in "*/+-^%([":
                left_side += '*'
        if len(right_side) > 0:
            start_r = right_side[0]
            if start_r not in "*/+-^%])":
                right_side = '*' + right_side

        new_c = left_side + \
            str(Equation(c[start + 1: index_of_end]).evaluate()) + \
            right_side
        return Equation(new_c)

    def __contains__(self, item: str) -> bool:
        return item in self.content

    def split(self, delim: str) -> List[Equation]:
        c = self.content.split(delim)
        equations = []
        for i in c:
            equations.append(Equation(i))
        return equations


class NoOperatorError(Exception):
    """Exception that is raised when the equation doesn't have an operator"""


class UnevenBracketError(Exception):
    """Exception that is raised when the equation has a missing bracket"""


if __name__ == "__main__":
    doctest.testmod()

    # import python_ta
    # python_ta.check_all()

    calculator = Calculator()
    while True:
        input_ = input("Enter Equation:")

        try:
            answer = calculator.check_input(input_)
            print(answer)
        except (NoOperatorError, UnevenBracketError) as e:
            print(f"Invalid Equation! Invalid Format!")
