from generated.PAMVisitor import PAMVisitor
from generated.PAMParser import PAMParser
from termcolor import colored


class ExtendedVisitor(PAMVisitor):
    # associative dictionary for storing variable values
    variable_values = {}

    # a value that will be assigned to variable in case of error
    CONST_ERROR_VALUE = -999999

    # constructor
    def __init__(self):
        # read and convert the input data into the array of numbers
        data = open('data.txt', 'r').read()
        data_array = data.split(',')

        # add a class property data_array to be able to use it in methods
        self.data_array = [int(elem) for elem in data_array]

        # declare and initialize a counter for an array of input data
        self.counter = 0

    # Visit a parse tree produced by PAMParser #progr.
    def visitProgr(self, ctx: PAMParser.ProgrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser #series.
    def visitSeries(self, ctx: PAMParser.SeriesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser #stmt.
    def visitStmt(self, ctx: PAMParser.StmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser #input_stmt.
    def visitInput_stmt(self, ctx: PAMParser.Input_stmtContext):
        varlist = self.visitVarlist(ctx.getChild(1))

        # assign numbers from file to variables
        for varname in varlist:
            self.variable_values[varname] = self.data_array[self.counter]

            # increment a counter
            # (next time some variable will be read, the next element of input array will be taken)
            self.counter += 1

        # print(str(self.variable_values))

    # Visit a parse tree produced by PAMParser #output_stmt.
    def visitOutput_stmt(self, ctx: PAMParser.Output_stmtContext):
        varlist = self.visitVarlist(ctx.getChild(1))

        # output the values of variables (in one line, if it is a varlist)
        for varname in varlist:
            if varname in self.variable_values:
                print(self.variable_values[varname], end=" ")
            else:
                print(colored('Error: cannot access variable ' + varname + ' value', 'magenta'))

        print()

    # Visit a parse tree produced by PAMParser #assign_stmt.
    def visitAssign_stmt(self, ctx: PAMParser.Assign_stmtContext):
        varname = str(ctx.getChild(0))
        expr = self.visitExpr(ctx.getChild(2))

        self.variable_values[varname] = expr

        print(colored(str(self.variable_values), 'blue'))

    # Visit a parse tree produced by PAMParser#cond_stmt.
    def visitCond_stmt(self, ctx: PAMParser.Cond_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser#loop.
    def visitLoop(self, ctx: PAMParser.LoopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser#compar.
    def visitCompar(self, ctx: PAMParser.ComparContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser #varlist.
    def visitVarlist(self, ctx: PAMParser.VarlistContext):
        get_child_count = ctx.getChildCount()
        children = []

        if get_child_count == 1:
            children.append(str(ctx.getChild(0)))

        else:
            for i in range(get_child_count):
                if i % 2 == 0:
                    children.append(str(ctx.getChild(i)))

        return children

    # Visit a parse tree produced by PAMParser #expr.
    def visitExpr(self, ctx: PAMParser.ExprContext):
        # in grammar --> expr : term (WEAKOP term)*;

        # if there is only one child (one term), we should visit term
        if ctx.getChildCount() == 1:
            return self.visitTerm(ctx.getChild(0))

        # otherwise, we should process each term and implement addition on subtraction
        else:
            operation = str(ctx.getChild(1))
            term1 = self.visitTerm(ctx.getChild(0))
            term2 = self.visitTerm(ctx.getChild(2))

            # addition
            if operation == '+':
                return term1 + term2

            # subtraction
            else:
                return term1 - term2

    # Visit a parse tree produced by PAMParser #term.
    def visitTerm(self, ctx: PAMParser.TermContext):
        # in grammar --> elem (STRONGOP elem)*;

        # if there is only one child (one elem), we should visit elem
        if ctx.getChildCount() == 1:
            return self.visitElem(ctx.getChild(0))

        # otherwise, we should process each elem and implement multiplication on division
        else:
            operation = str(ctx.getChild(1))
            elem1 = self.visitElem(ctx.getChild(0))
            elem2 = self.visitElem(ctx.getChild(2))

            # multiplication
            if operation == '*':
                return elem1 * elem2

            # division
            else:
                # round the float result to the nearest integer number
                return round(elem1 / elem2)

    # Visit a parse tree produced by PAMParser #elem.
    def visitElem(self, ctx: PAMParser.ElemContext):
        # in grammar --> elem : NUMBER | BOOLEAN | VARNAME | '(' expr ')';

        # if there is only one child, we can just return its value
        if ctx.getChildCount() == 1:
            elem_value = str(ctx.getChild(0))

            # if the assigned value is a bool, it can be assigned as a string
            if elem_value == "true" or elem_value == "false":
                return elem_value

            # or, if the value is numeric, we can cast it to integer, and assign the integer
            elif elem_value.isnumeric():
                return int(elem_value)

            # if it is not a number, not a boolean and not an expression in parentheses, then it is a varname
            # varname should be handled differently
            else:
                # check, whether the assigned variable has a value
                if elem_value in self.variable_values:
                    # if yes, that it is returned
                    return self.variable_values[elem_value]
                else:
                    # if not, output an error and assign some special value to variable
                    print(colored('Error: cannot access variable ' + elem_value + ' value', 'magenta'))
                    return self.CONST_ERROR_VALUE

        # if there is more than 1 child it means it is an expr in parentheses,
        # so we have to process the expression
        else:
            return self.visitExpr(ctx.getChild(1))

    # Visit a parse tree produced by PAMParser#log_expr.
    def visitLog_expr(self, ctx: PAMParser.Log_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser#log_weak_term.
    def visitLog_weak_term(self, ctx: PAMParser.Log_weak_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser#log_term.
    def visitLog_term(self, ctx: PAMParser.Log_termContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PAMParser#log_elem.
    def visitLog_elem(self, ctx: PAMParser.Log_elemContext):
        return self.visitChildren(ctx)
