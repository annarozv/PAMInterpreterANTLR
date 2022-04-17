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
        data_array = data.split(',') if data != '' else []

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
        # grammar --> input_stmt : 'read' varlist;
        varlist = self.visitVarlist(ctx.getChild(1))

        # assign numbers from file to variables
        for varname in varlist:
            self.variable_values[varname] = self.data_array[self.counter]

            # increment a counter
            # (next time some variable will be read, the next element of input array will be taken)
            self.counter += 1

        # print(colored(str(self.variable_values), 'blue'))

    # Visit a parse tree produced by PAMParser #output_stmt.
    def visitOutput_stmt(self, ctx: PAMParser.Output_stmtContext):
        # grammar --> output_stmt : 'write' varlist;
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
        # grammar --> assign_stmt : VARNAME ':=' expr;
        varname = str(ctx.getChild(0))
        expr = self.visitExpr(ctx.getChild(2))

        self.variable_values[varname] = expr

        # print(colored(str(self.variable_values), 'blue'))

    # Visit a parse tree produced by PAMParser #cond_stmt.
    def visitCond_stmt(self, ctx: PAMParser.Cond_stmtContext):
        # grammar --> cond_stmt : 'if' log_expr 'then' series ('else' series)? 'fi';

        # get the condition value
        condition = self.visitLog_expr(ctx.getChild(1))
        child_count = ctx.getChildCount()

        # if there is no 'else'
        if child_count == 5:
            if condition == 'true':
                # execute everything in if block
                return self.visitSeries(ctx.getChild(3))

        # if there is 'else' branch
        if child_count == 7:
            if condition == 'true':
                # execute everything in if block
                return self.visitSeries(ctx.getChild(3))
            elif condition == 'false':
                # execute everything in 'else' block
                return self.visitSeries(ctx.getChild(5))

    # Visit a parse tree produced by PAMParser #loop.
    def visitLoop(self, ctx: PAMParser.LoopContext):
        # grammar --> loop : 'while' log_expr 'do' series 'end';

        # get the condition value
        condition = self.visitLog_expr(ctx.getChild(1))

        # while condition is true, execute the command series
        while condition == 'true':
            self.visitSeries(ctx.getChild(3))
            # then evaluate the condition again
            condition = self.visitLog_expr(ctx.getChild(1))

    # Visit a parse tree produced by PAMParser #compar.
    def visitCompar(self, ctx: PAMParser.ComparContext):
        # grammar --> compar : expr RELATION expr;

        relation = str(ctx.getChild(1))
        expr1 = self.visitExpr(ctx.getChild(0))
        expr2 = self.visitExpr(ctx.getChild(2))

        # for each relation, figure out the result
        if relation == '=':
            return "true" if expr1 == expr2 else "false"
        elif relation == '<>':
            return "true" if expr1 != expr2 else "false"
        elif relation == '<':
            return "true" if expr1 < expr2 else "false"
        elif relation == '>':
            return "true" if expr1 > expr2 else "false"
        elif relation == '=<':
            return "true" if expr1 <= expr2 else "false"
        elif relation == '>=':
            return "true" if expr1 >= expr2 else "false"
        else:
            return "false"

    # Visit a parse tree produced by PAMParser #varlist.
    def visitVarlist(self, ctx: PAMParser.VarlistContext):
        # grammar --> varlist : VARNAME (',' VARNAME)*;
        child_count = ctx.getChildCount()
        children = []

        if child_count == 1:
            children.append(str(ctx.getChild(0)))

        else:
            for i in range(child_count):
                if i % 2 == 0:
                    children.append(str(ctx.getChild(i)))

        return children

    # Visit a parse tree produced by PAMParser #expr.
    def visitExpr(self, ctx: PAMParser.ExprContext):
        # grammar --> expr : term (WEAKOP term)*;

        child_count = ctx.getChildCount()

        # if there is only one child (one term), we should visit term
        if child_count == 1:
            return self.visitTerm(ctx.getChild(0))

        # otherwise, we should process each term and implement addition on subtraction
        else:
            term1 = self.visitTerm(ctx.getChild(0))
            sum = term1
            operation = str(ctx.getChild(1))
            i = 1

            while not i == child_count:
                if i % 2 == 1:
                    operation = str(ctx.getChild(i))
                else:
                    term2 = self.visitTerm(ctx.getChild(i))

                    # addition
                    if operation == '+':
                        sum += term2

                    # subtraction
                    else:
                        sum -= term2

                i += 1

            return sum

    # Visit a parse tree produced by PAMParser #term.
    def visitTerm(self, ctx: PAMParser.TermContext):
        # grammar --> elem (STRONGOP elem)*;

        child_count = ctx.getChildCount()

        # if there is only one child (one elem), we should visit elem
        if child_count == 1:
            return self.visitElem(ctx.getChild(0))

        # otherwise, we should process each elem and implement multiplication or division
        else:
            elem1 = self.visitElem(ctx.getChild(0))
            product = elem1
            operation = str(ctx.getChild(1))
            i = 1

            while not i == child_count:
                if i % 2 == 1:
                    operation = str(ctx.getChild(i))
                else:
                    elem2 = self.visitElem(ctx.getChild(i))

                    # multiplication
                    if operation == '*':
                        product *= elem2
                    # division
                    else:
                        product /= elem2

                i += 1

            return round(product)

    # Visit a parse tree produced by PAMParser #elem.
    def visitElem(self, ctx: PAMParser.ElemContext):
        # grammar --> elem : NUMBER | BOOLEAN | VARNAME | '(' expr ')';

        # if there is only one child, we can just return its value
        if ctx.getChildCount() == 1:
            elem_value = str(ctx.getChild(0))

            # if the assigned value is a bool, it can be assigned as a string
            if elem_value == "true" or elem_value == "false":
                return elem_value

            # or, if the value is numeric, we can cast it to integer, and assign the integer
            elif elem_value.isnumeric():
                return int(elem_value)

            # else, if it is not a number, not a boolean and not an expression in parentheses, then it is a varname
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

    # Visit a parse tree produced by PAMParser #log_expr.
    def visitLog_expr(self, ctx: PAMParser.Log_exprContext):
        # grammar --> log_expr: log_weak_term (DISJUNCTION log_weak_term)* ;

        child_count = ctx.getChildCount()

        # if there is only one child, we should visit the weak logical term
        if child_count == 1:
            return self.visitLog_weak_term(ctx.getChild(0))
        # else, we have to calculate the value of all the logical weak terms
        else:
            log_term1 = self.visitLog_weak_term(ctx.getChild(0))
            i = 1

            if log_term1 == "true":
                return "true"

            while not i == child_count:
                if i % 2 == 0:
                    log_term2 = self.visitLog_weak_term(ctx.getChild(i))

                    # if at least one of the logical terms is true, we have to return true (disjunction)
                    if log_term2 == "true":
                        return "true"

                i += 1

            # if none of the weak terms were true, return false
            return "false"

    # Visit a parse tree produced by PAMParser #log_weak_term.
    def visitLog_weak_term(self, ctx: PAMParser.Log_weak_termContext):
        # grammar --> log_weak_term: log_term (CONJUNCTION log_term)* ;

        child_count = ctx.getChildCount()

        # if there is only one child, we should visit the logical term
        if child_count == 1:
            return self.visitLog_term(ctx.getChild(0))
        # else, we have to calculate the value of all the logical terms
        else:
            log_term1 = self.visitLog_term(ctx.getChild(0))
            i = 1

            if log_term1 != "true":
                return "false"

            while not i == child_count:
                if i % 2 == 0:
                    log_term2 = self.visitLog_term(ctx.getChild(i))

                    # if at least one of the logical terms is false, we have to return false (conjunction)
                    if log_term2 != "true":
                        return "false"

                i += 1

            # if none of the terms were false, return true
            return "true"

    # Visit a parse tree produced by PAMParser #log_term.
    def visitLog_term(self, ctx: PAMParser.Log_termContext):
        # grammar --> (NEGATION)* log_elem;
        child_count = ctx.getChildCount()

        # if there is only one child, we should visit the logical elem
        if child_count == 1:
            return self.visitLog_elem(ctx.getChild(0))
        # else, the term can contain some negations, that should be processed
        else:
            # if number of children is even, it means there is an odd number of negations,
            # it can be shortened to one negation
            if child_count % 2 == 0:
                elem_value = self.visitLog_elem(ctx.getChild(child_count - 1))

                if elem_value == "true":
                    return "false"
                elif elem_value == "false":
                    return "true"
                else:
                    return "false"

            # else, the negations are mutually exclusive, so we have to just process the value of the last element
            else:
                return self.visitLog_elem(ctx.getChild(child_count - 1))

    # Visit a parse tree produced by PAMParser #log_elem.
    def visitLog_elem(self, ctx: PAMParser.Log_elemContext):
        # grammar --> compar | VARNAME | BOOLEAN | '(' log_expr ')';
        child_count = ctx.getChildCount()

        # if there is only one child, it is either a variable name or a boolean, or a comparison
        if child_count == 1:
            # if it is a comparison, we process it as a comparison
            if ctx.compar():
                return self.visitCompar(ctx.getChild(0))

            elem_value = str(ctx.getChild(0))

            # if the assigned value is a bool, it can be returned as a string
            if elem_value == "true" or elem_value == "false":
                return elem_value
            # else, it is a varname
            else:
                # check, whether the variable has a value
                if elem_value in self.variable_values:
                    # if yes, that it is returned
                    return self.variable_values[elem_value]
                else:
                    # if not, output an error and return false
                    print(colored('Error: cannot access variable ' + elem_value + ' value', 'magenta'))
                    return "false"

        # if there is more than 1 child, it is a logical expression in parentheses
        else:
            return self.visitLog_expr(ctx.getChild(1))
