NUM, VAR, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'NUM', 'VAR', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        '''String representation of a token.

        Examples:
            Token(NUM, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        '''
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Tokenizer:
    def __init__(self, text):
        # input string possibly containing an expression
        self.text = text
        # current position within the given string
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('invalid character')

    def advance(self):
        '''Move current position and set the current character.'''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def num(self):
        '''Inspect a substring beginning with a digit
        and return either NUM or VAR token.
        '''
        number = ''
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()

        if self.current_char is not None and self.current_char.isalpha():
            # pass number to var() as an int coefficient
            return Token(VAR, self.var(int(number)))

        # check if the number is a float
        elif self.current_char is not None and self.current_char == '.':
            number += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                number += self.current_char
                self.advance()
                
            if self.current_char is not None and self.current_char.isalpha():
                # pass number to var() as a float coefficient
                return Token(VAR, self.var(float(number)))
            
            return Token(NUM, float(number))
        
        return Token(NUM, int(number))

    def var(self, coef=1):
        '''Return a tuple with a numeric coefficient
        and a substring consisting of lettres representing a variable name.
        '''
        name = ''
        while self.current_char is not None and self.current_char.isalpha():
            name += self.current_char
            self.advance()
        return (coef, name)

    def get_next_token(self):
        '''Recognize a valid character in the input string
        and return the respective token.
        '''
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.num()

            if self.current_char.isalpha():
                return Token(VAR, self.var())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            # if no valid character found, raise an error
            self.error()

        return Token(EOF, None)
