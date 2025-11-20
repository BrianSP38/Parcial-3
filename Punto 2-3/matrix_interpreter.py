import sys
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4 import ParseTreeVisitor

from MatrixLexer import MatrixLexer
from MatrixParser import MatrixParser
from MatrixVisitor import MatrixVisitor

class MatrixEnv:
    def __init__(self):
        self.tables = {}

    def declare(self, name, values):
        if values is None:
            values = []
        if len(values) == 0:
            rows = 0
            cols = 0
        else:
            rows = len(values)
            cols = len(values[0])
        for r in values:
            if len(r) != cols:
                raise Exception(f"Matrix '{name}' not rectangular: rows lengths differ")
        self.tables[name] = {'rows': rows, 'cols': cols, 'values': values}

    def get(self, name):
        if name not in self.tables:
            raise Exception(f"Identifier '{name}' not declared")
        return self.tables[name]

def multiply(A, B):
    if A['cols'] != B['rows']:
        raise Exception(f"Incompatible dimensions for multiplication: {A['rows']}x{A['cols']} * {B['rows']}x{B['cols']}")
    R = [[0.0 for _ in range(B['cols'])] for __ in range(A['rows'])]
    for i in range(A['rows']):
        for j in range(B['cols']):
            s = 0.0
            for k in range(A['cols']):
                s += A['values'][i][k] * B['values'][k][j]
            R[i][j] = s
    return {'rows': A['rows'], 'cols': B['cols'], 'values': R}

class EvalVisitor(MatrixVisitor):
    def __init__(self):
        self.env = MatrixEnv()

    def visitProgram(self, ctx: MatrixParser.ProgramContext):
        return self.visitChildren(ctx)

    def visitStmt_list(self, ctx: MatrixParser.Stmt_listContext):
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
        for s in ctx.stmt():
            self.visit(s)
        return None

    def visitMatrix_decl(self, ctx: MatrixParser.Matrix_declContext):
        name = ctx.ID().getText()
        ml = ctx.matrix_literal()
        rows = []
        rl = ml.row_list()
        if rl is not None:
            for rctx in rl.row():
                nl = rctx.num_list()
                if nl is None:
                    nums = []
                else:
                    nums = [ float(tok.getText()) for tok in nl.NUMBER() ]
                rows.append(nums)
        self.env.declare(name, rows)
        return None

    def visitAssign_stmt(self, ctx: MatrixParser.Assign_stmtContext):
        left = ctx.ID().getText()
        expr = ctx.expression()
        if expr.getChildCount() == 3 and expr.getChild(1).getText() == '*':
            A_name = expr.ID(0).getText()
            B_name = expr.ID(1).getText()
            A = self.env.get(A_name)
            B = self.env.get(B_name)
            C = multiply(A, B)
            self.env.declare(left, C['values'])
        else:
            src = expr.ID(0).getText()
            S = self.env.get(src)
            vals = [ list(r) for r in S['values'] ]
            self.env.declare(left, vals)
        return None

    def visitPrint_stmt(self, ctx: MatrixParser.Print_stmtContext):
        name = ctx.ID().getText()
        M = self.env.get(name)
        print(f"Matrix {name} = {M['rows']} x {M['cols']}")
        for r in M['values']:
            print(r)
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python matrix_interpreter.py archivo.mtx")
        sys.exit(1)
    input_path = sys.argv[1]
    data = FileStream(input_path, encoding='utf-8')
    lexer = MatrixLexer(data)
    stream = CommonTokenStream(lexer)
    parser = MatrixParser(stream)
    tree = parser.program()
    visitor = EvalVisitor()
    visitor.visit(tree)
