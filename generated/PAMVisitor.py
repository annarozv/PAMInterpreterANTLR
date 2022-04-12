# Generated from PAM.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PAMParser import PAMParser
else:
    from PAMParser import PAMParser

# This class defines a complete generic visitor for a parse tree produced by PAMParser.

class PAMVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PAMParser#progr.
    def visitProgr(self, ctx:PAMParser.ProgrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#series.
    def visitSeries(self, ctx:PAMParser.SeriesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#stmt.
    def visitStmt(self, ctx:PAMParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#input_stmt.
    def visitInput_stmt(self, ctx:PAMParser.Input_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#output_stmt.
    def visitOutput_stmt(self, ctx:PAMParser.Output_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#assign_stmt.
    def visitAssign_stmt(self, ctx:PAMParser.Assign_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#cond_stmt.
    def visitCond_stmt(self, ctx:PAMParser.Cond_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#loop.
    def visitLoop(self, ctx:PAMParser.LoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#compar.
    def visitCompar(self, ctx:PAMParser.ComparContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#varlist.
    def visitVarlist(self, ctx:PAMParser.VarlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#expr.
    def visitExpr(self, ctx:PAMParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#term.
    def visitTerm(self, ctx:PAMParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#elem.
    def visitElem(self, ctx:PAMParser.ElemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#log_expr.
    def visitLog_expr(self, ctx:PAMParser.Log_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#log_weak_term.
    def visitLog_weak_term(self, ctx:PAMParser.Log_weak_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#log_term.
    def visitLog_term(self, ctx:PAMParser.Log_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PAMParser#log_elem.
    def visitLog_elem(self, ctx:PAMParser.Log_elemContext):
        return self.visitChildren(ctx)



del PAMParser