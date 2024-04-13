from calc_parser import *


class Evaluator:
    def __init__(self, parser):
        self.parser = parser




    def trav(self, tree):
        if not tree:
            return None
        if type(tree) == UnaryOp:
            print(tree.token)
            self.trav(tree.expr)
        elif type(tree) != BinOp:
            print(tree.token)
        else:
            self.trav(tree.left)
            print(tree.token)
            self.trav(tree.right)
            



    def mul(self, tree):
        if type(tree) == UnaryOp and tree.token.type == PLUS:
            simp = self.mul(tree.expr)
            if simp.token.type == NUM:
                return Num(Token(NUM, +simp.value))
            elif simp.token.type == VAR:
                return Var(Token(VAR, (+simp.coef, simp.value)))
            elif simp.token.type in (PLUS, MINUS):
                return simp
            return UnaryOp(tree.token, simp)

        
        elif type(tree) == UnaryOp and tree.token.type == MINUS:
            simp = self.mul(tree.expr)
            if simp.token.type == NUM:
                return Num(Token(NUM, -simp.value))
            elif simp.token.type == VAR:
                return Var(Token(VAR, (-simp.coef, simp.value)))
            elif simp.token.type in (PLUS, MINUS):
                return BinOp(self.mul(UnaryOp(Token(MINUS, '-'), simp.left)),
                             simp.token,
                             self.mul(UnaryOp(Token(MINUS, '-'), simp.right)))
            return UnaryOp(tree.token, simp)



        
        elif tree.token.type in (NUM, VAR):
            return tree

        
        elif tree.token.type in (PLUS, MINUS):
            return BinOp(self.mul(tree.left),
                             tree.token,
                             self.mul(tree.right))


        
        
        elif tree.token.type == MUL:
            
            if type(tree.left) == UnaryOp or type(tree.right) == UnaryOp:
                return self.mul(BinOp(self.mul(tree.left),
                             tree.token,
                             self.mul(tree.right)))
            
            elif tree.left.token.type in (PLUS, MINUS):
                return BinOp(self.mul(BinOp(tree.left.left, Token(MUL, '*'), tree.right)),
                             tree.left.token,
                             self.mul(BinOp(tree.left.right, Token(MUL, '*'), tree.right)))

            elif tree.right.token.type in (PLUS, MINUS):
                return BinOp(self.mul(BinOp(tree.right.left, Token(MUL, '*'), tree.left)),
                             tree.right.token,
                             self.mul(BinOp(tree.right.right, Token(MUL, '*'), tree.left)))

            elif tree.left.token.type in (MUL, DIV) or tree.right.token.type in (MUL, DIV):
                return self.mul(BinOp(self.mul(tree.left), Token(MUL, '*'), self.mul(tree.right)))

            elif tree.left.token.type == VAR and tree.right.token.type == NUM:
                return Var(Token(VAR, (tree.left.coef*tree.right.value, tree.left.value)))

            elif tree.left.token.type == NUM and tree.right.token.type == VAR:
                return Var(Token(VAR, (tree.right.coef*tree.left.value, tree.right.value)))

            elif tree.left.token.type == NUM and tree.right.token.type == NUM:
                return Num(Token(NUM, tree.left.value*tree.right.value))




        elif tree.token.type == DIV:
            if type(tree.left) == UnaryOp or type(tree.right) == UnaryOp:
                return self.mul(BinOp(self.mul(tree.left),
                             tree.token,
                             self.mul(tree.right)))
            
            elif tree.left.token.type in (PLUS, MINUS):
                return BinOp(self.mul(BinOp(tree.left.left, Token(DIV, '/'), tree.right)),
                             tree.left.token,
                             self.mul(BinOp(tree.left.right, Token(DIV, '/'), tree.right)))

##            elif tree.right.token.type in (PLUS, MINUS):
##                return BinOp(self.mul(BinOp(tree.right.left, Token(MUL, '*'), tree.left)),
##                             tree.right.token,
##                             self.mul(BinOp(tree.right.right, Token(MUL, '*'), tree.left)))

            elif tree.left.token.type in (MUL, DIV) or tree.right.token.type in (MUL, DIV):
                return self.mul(BinOp(self.mul(tree.left), Token(DIV, '/'), self.mul(tree.right)))

            elif tree.left.token.type == VAR and tree.right.token.type == NUM:
                return Var(Token(VAR, (tree.left.coef/tree.right.value, tree.left.value)))

            elif tree.left.token.type == VAR and tree.right.token.type == VAR:
                return Num(Token(NUM, tree.left.coef/tree.right.coef))

            elif tree.left.token.type == NUM and tree.right.token.type == NUM:
                return Num(Token(NUM, tree.left.value/tree.right.value))
            




    def plus(self, tree):
        if tree.token.type == NUM:
            return [tree]

        if tree.token.type == VAR:
            return [tree]
        
        if tree.token.type == PLUS:
            return self.plus(tree.left) + self.plus(tree.right)

        elif tree.token.type == MINUS:
            return self.plus(tree.left) + self.minus(tree.right)


    def minus(self, tree):
        if tree.token.type == NUM:
            return [Num(Token(NUM, -tree.value))]

        if tree.token.type == VAR:
            return [Var(Token(VAR, (-tree.coef, tree.value)))]

        if tree.token.type == PLUS:
            return self.minus(tree.left) + self.minus(tree.right)

        elif tree.token.type == MINUS:
            return self.minus(tree.left) + self.plus(tree.right)     


    def stringify(self, tree):
        const = 0
        var_coef = {}
        
        nodes_to_sum = self.plus(tree)
        #print(nodes_to_sum)

        for node in nodes_to_sum:
            if node.token.type == NUM:
                const += node.value
            elif node.token.type == VAR:
                if node.value not in var_coef:
                    var_coef.update({node.value: node.coef})
                else:
                    var_coef.update({node.value: var_coef[node.value]+node.coef})
        
        out = ''
        for var in var_coef:
            if out == '':
                if var_coef[var] == 0:
                    pass
                elif var_coef[var] == 1:
                    out += var
                elif var_coef[var] == -1:
                    out += '-' + var
                else:
                    out += str(var_coef[var]) + var
            else:
                if var_coef[var] == 0:
                    pass
                elif var_coef[var] == 1:
                    out += ' + ' + var
                elif var_coef[var] == -1:
                    out += ' - ' + var
                elif var_coef[var] < 0:
                    out += ' - ' + str(abs(var_coef[var])) + var
                else:
                    out += ' + ' + str(var_coef[var]) + var

        if out == '': 
            out += str(const)
        else:
            if const < 0:
                out += ' - ' + str(abs(const))
            elif const == 0:
                pass
            else:
                out += ' + ' + str(const)
                
        return out
    



    def evaluate(self):
        tree = self.parser.parse()
        simplified_tree = self.mul(tree)
        return self.stringify(simplified_tree)


