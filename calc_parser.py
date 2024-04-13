from calc_tokenizer import *


# classes for AST nodes
class UnaryOp:
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num:
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var:
    def __init__(self, token):
        self.token = token
        self.coef = token.value[0]
        self.value = token.value[1]




class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        # set current token to the first token taken from the input
        try:
            self.current_token = self.tokenizer.get_next_token()
        except:
            print('Exception: invalid character')


    def error(self):
        raise SyntaxError('invalid syntax')

    def eat(self, token_type):
        '''Compare the current token type with the passed token
        type and if they match then "eat" the current token
        and assign the next token to the self.current_token,
        otherwise raise a SyntaxError.'''
        if self.current_token.type == token_type:
            try:
                self.current_token = self.tokenizer.get_next_token()
            except:
                print('Exception: invalid character')
        else:
            self.error()

    def factor(self):
        '''Return a UnaryOp/Num/Var node
        or call expr() in case of parentheses,
        otherwise raise a SyntaxError.
        '''
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == NUM:
            self.eat(NUM)
            return Num(token)
        elif token.type == VAR:
            self.eat(VAR)
            return Var(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        self.error()

    def term(self):
        '''Return a MUL/DIV BinOp node or a factor node
        if no MUL/DIV token found.'''
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        '''Return a PLUS/MINUS BinOp node or a term node
        if no PLUS/MINUS token found.'''
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        '''Build and return an AST.'''
        return self.expr()
