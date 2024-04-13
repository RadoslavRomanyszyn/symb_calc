from calc_tokenizer import *
from calc_parser import *
from calc_evaluator import *


def main():
    while True:
        try:
            expression = input('>>> ')
        except EOFError:
            break
        if not expression:
            continue


        tokenizer = Tokenizer(expression)
        parser = Parser(tokenizer)
        evaluator = Evaluator(parser)
        try:
            print(evaluator.evaluate())
        except ZeroDivisionError:
            print('ZeroDivisionError: division by zero')
            continue
        except SyntaxError:
            print('SyntaxError: invalid syntax')
            continue
        except:
            continue
        
        
main()
