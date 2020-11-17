#1852471
from BKITVisitor import BKITVisitor
from BKITParser import BKITParser
from AST import *

class ASTGeneration(BKITVisitor):
    def visitProgram(self,ctx:BKITParser.ProgramContext):
        return Program(ctx.decl_list().accept(self))

    def visitDecl_list(self,ctx:BKITParser.Decl_listContext):
        param1 = []
        param2 = []
        if ctx.var_declist():
            param1 = ctx.var_declist().accept(self)
        if ctx.func_declist():
            param2 = ctx.func_declist().accept(self)
        return param1 + param2

    def visitVar_declist(self,ctx:BKITParser.Var_declistContext):
        return ctx.variable_decl().accept(self) + ctx.var_list().accept(self) if ctx.var_list() else ctx.variable_decl().accept(self)

    def visitVar_list(self,ctx:BKITParser.Var_listContext):
        return ctx.variable_decl().accept(self) + ctx.var_list().accept(self) if ctx.var_list() else ctx.variable_decl().accept(self)

    def visitVariable_decl(self,ctx: BKITParser.Variable_declContext):
        return ctx.variable_list().accept(self)

    def visitVariable_list(self,ctx:BKITParser.Variable_listContext):
        return [ctx.var_decl().accept(self)] + ctx.varlist().accept(self) if ctx.varlist() else [ctx.var_decl().accept(self)]

    def visitVarlist(self,ctx:BKITParser.VarlistContext):
        return [ctx.var_decl().accept(self)] + ctx.varlist().accept(self) if ctx.varlist() else [ctx.var_decl().accept(self)]

    def visitVar_decl(self, ctx: BKITParser.Var_declContext):
        param2 = []
        param3 = None
        if ctx.index_list():
            param2 = ctx.index_list().accept(self)
        if ctx.all_literal():
            param3 = ctx.all_literal().accept(self)

        return VarDecl(Id(ctx.ID().getText()), param2, param3)

    def visitIndex_list(self,ctx: BKITParser.Index_listContext):
        return [int(ctx.INT().getText(), 0)] + ctx.index_list().accept(self) if ctx.index_list() else [int(ctx.INT().getText(), 0)]

    def visitFunc_declist(self,ctx:BKITParser.Func_declistContext):
        return [ctx.func_decl().accept(self)] + ctx.func_prime().accept(self) if ctx.func_prime() else [ctx.func_decl().accept(self)]

    def visitFunc_prime(self,ctx:BKITParser.Func_primeContext):
        return [ctx.func_decl().accept(self)] + ctx.func_prime().accept(self) if ctx.func_prime() else [ctx.func_decl().accept(self)]

    def visitFunc_decl(self, ctx:BKITParser.Func_declContext):
        param1 = Id(ctx.ID().getText())
        param2= []
        param3= ctx.body().accept(self)
        if ctx.parameter():
            param2 = ctx.parameter().accept(self)
        
        return FuncDecl(param1 , param2, param3)


    def visitBody(self, ctx: BKITParser.BodyContext):
        return ctx.stmtlst().accept(self)
    
    def visitParameter(self, ctx: BKITParser.ParameterContext):
        return [ctx.param().accept(self)] + ctx.parameter_list().accept(self) if ctx.parameter_list() else [ctx.param().accept(self)]
    
    def visitParameter_list(self, ctx: BKITParser.Parameter_listContext):
        return [ctx.param().accept(self)] + ctx.parameter_list().accept(self) if ctx.parameter_list() else [ctx.param().accept(self)]
    
    def visitParam(self, ctx: BKITParser.ParamContext):
        param2 = []
        if ctx.index_list():
            param2 = ctx.index_list().accept(self)
        return VarDecl(Id(ctx.ID().getText()), param2, None)

    def visitStmtlst(self, ctx: BKITParser.StmtlstContext):
        param1 = []
        param2 = []
        if ctx.var_declist():
            param1 = ctx.var_declist().accept(self)
        if ctx.stmtlist():
            param2 = ctx.stmtlist().accept(self)

        return (param1, param2)

    def visitStmtlist(self, ctx: BKITParser.StmtlistContext):
        return [ctx.stmt().accept(self)]+ ctx.stmttail().accept(self) if ctx.stmttail() else [ctx.stmt().accept(self)]
    
    def visitStmttail(self, ctx: BKITParser.StmttailContext):
        return [ctx.stmt().accept(self)] + ctx.stmttail().accept(self) if ctx.stmttail() else [ctx.stmt().accept(self)]
    
    def visitStmt(self, ctx: BKITParser.StmtContext):
        if ctx.assign_stmt():
            return ctx.assign_stmt().accept(self)
        elif ctx.if_stmt():
            return ctx.if_stmt().accept(self)
        elif ctx.for_stmt():
            return ctx.for_stmt().accept(self)
        elif ctx.while_stmt():
            return ctx.while_stmt().accept(self)
        elif ctx.dowhile_stmt():
            return ctx.dowhile_stmt().accept(self)
        elif ctx.call_stmt():
            return ctx.call_stmt().accept(self)
        elif ctx.return_stmt():
            return ctx.return_stmt().accept(self)
        elif ctx.continue_stmt():
            return ctx.continue_stmt().accept(self)
        elif ctx.break_stmt():
            return ctx.break_stmt().accept(self)

    def visitAssign_stmt(self, ctx: BKITParser.Assign_stmtContext):
        param1 = None
        param2 = None
        if ctx.ID():
            param1 = Id(ctx.ID().getText())
        elif ctx.expr7():
            param1 = ArrayCell(ctx.expr7().accept(self), ctx.index_op().accept(self))


        param2 = ctx.expr().accept(self)

        return Assign(param1, param2)

    def visitIndex_op(self, ctx: BKITParser.Index_opContext):
        return [ctx.expr0().accept(self)] + ctx.index_op().accept(self) if ctx.index_op() else [ctx.expr0().accept(self)]

    def visitIf_stmt(self, ctx: BKITParser.If_stmtContext):
        param1 = [tuple([ctx.expr().accept(self)] +  list(ctx.stmtlst().accept(self)))]
        if ctx.elif_stmt_list():    
            param1 = param1 + ctx.elif_stmt_list().accept(self)
        param2 = ([], [])
        if ctx.else_stmt():
            param2 = ctx.else_stmt().accept(self)
        return If(param1, param2)
    
    
    def visitElif_stmt_list(self, ctx: BKITParser.Elif_stmt_listContext):
        return [ctx.elif_stmt().accept(self)] + ctx.elif_stmt_list().accept(self) if ctx.elif_stmt_list() else [ctx.elif_stmt().accept(self)]
    
    def visitElif_stmt(self, ctx: BKITParser.Elif_stmtContext):
        return tuple([ctx.expr().accept(self)] +  list(ctx.stmtlst().accept(self)))

    def visitElse_stmt(self, ctx: BKITParser.Else_stmtContext):
        return ctx.stmtlst().accept(self)

    def visitFor_stmt(self, ctx: BKITParser.For_stmtContext):
        
        param0 = Id(ctx.ID().getText())
        param1 = ctx.expr(0).accept(self)
        param2 = ctx.expr(1).accept(self)
        param3 = ctx.expr(2).accept(self)
        param4 = ctx.stmtlst().accept(self) if ctx.stmtlst() else ([], [])
        return  For(param0, param1, param2, param3, param4)
    

    def visitWhile_stmt(self, ctx: BKITParser.While_stmtContext):
        param0 = ctx.expr().accept(self)
        param1 = ctx.stmtlst().accept(self)
        return While(param0, param1)

    def visitDowhile_stmt(self, ctx: BKITParser.Dowhile_stmtContext):
        param0 = ctx.stmtlst().accept(self)
        param1 = ctx.expr().accept(self)
        return Dowhile(param0, param1)

    def visitBreak_stmt(self, ctx: BKITParser.Break_stmtContext):
        return Break()

    def visitContinue_stmt(self, ctx: BKITParser.Continue_stmtContext):
        return Continue()
    
    def visitCall_stmt(self, ctx: BKITParser.Call_stmtContext):
        param1 = []
        if ctx.call_list():
            param1 = ctx.call_list().accept(self)
        return CallStmt(Id(ctx.ID().getText()), param1)
    
    def visitReturn_stmt(self, ctx: BKITParser.Return_stmtContext):
        val = None
        if ctx.expr():
            val = ctx.expr().accept(self)
        return Return(val)

    def visitExpr(self, ctx: BKITParser.ExprContext):
        if ctx.expr0():
            return ctx.expr0().accept(self)
        elif ctx.STRING():
            return StringLiteral(ctx.STRING().getText())
        elif ctx.array():
            return ctx.array().accept(self)

    def visitExpr0(self, ctx: BKITParser.Expr0Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.RELATIONAL().getText(), ctx.expr1(0).accept(self), ctx.expr1(1).accept(self))
        else:
            return ctx.expr1(0).accept(self)
           

    def visitExpr1(self, ctx: BKITParser.Expr1Context):
        if ctx.getChildCount() == 1:
            return ctx.expr2().accept(self)
        else:
            return BinaryOp(ctx.BINLOGICAL().getText(), ctx.expr1().accept(self), ctx.expr2().accept(self))

    def visitExpr2(self, ctx: BKITParser.Expr2Context):
        if ctx.getChildCount() == 1:
            return ctx.expr3().accept(self)
        else:
            if ctx.ADDING():
                return BinaryOp(ctx.ADDING().getText(), ctx.expr2().accept(self), ctx.expr3().accept(self))
            else:
                return BinaryOp(ctx.SIGN().getText(), ctx.expr2().accept(self), ctx.expr3().accept(self))

    def visitExpr3(self, ctx: BKITParser.Expr3Context):
        if ctx.getChildCount() == 1:
            return ctx.expr4().accept(self)
        else:
            return BinaryOp(ctx.MULTIPLYING().getText(), ctx.expr3().accept(self), ctx.expr4().accept(self))

    def visitExpr4(self, ctx: BKITParser.Expr4Context):
        if ctx.getChildCount() == 1:
            return ctx.expr5().accept(self)
        else:
            return UnaryOp(ctx.UNLOGICAL().getText(), ctx.expr4().accept(self))


    def visitExpr5(self, ctx: BKITParser.Expr5Context):
        if ctx.getChildCount() == 1:
            return ctx.expr6().accept(self)
        else:
           return UnaryOp(ctx.SIGN().getText(), ctx.expr5().accept(self))


    def visitExpr6(self, ctx: BKITParser.Expr6Context):
        if ctx.getChildCount() == 1:
            return ctx.expr7().accept(self)
        else:
            return ArrayCell(ctx.expr7().accept(self), ctx.index_op().accept(self))
    
    def visitExpr7(self, ctx: BKITParser.Expr7Context):
        if ctx.getChildCount() == 1:
            return ctx.expr8().accept(self)
        else:
            param1 = Id(ctx.ID().getText())
            param2 = []
            if ctx.call_list():
                param2 = ctx.call_list().accept(self)

            return CallExpr(param1, param2)


    def visitExpr8(self, ctx: BKITParser.Expr8Context):
        if ctx.getChildCount() == 3: 
            return ctx.expr0().accept(self)
        else:
            if ctx.literal():
                return ctx.literal().accept(self)
            elif ctx.ID():
                return Id(ctx.ID().getText())
            return None

    def visitCall_list(self, ctx: BKITParser.Call_listContext):
        exprlist = [ctx.callee().accept(self)]
        if ctx.calltail():
            exprlist = exprlist + ctx.calltail().accept(self)

        return exprlist

    def visitCalltail(self, ctx: BKITParser.CalltailContext):
        exprlist = [ctx.callee().accept(self)]
        if ctx.calltail():
            return exprlist + ctx.calltail().accept(self)
        return exprlist

    def visitCallee(self, ctx: BKITParser.CalleeContext):
        if ctx.expr():
            return ctx.expr().accept(self)
        return None

    def visitArray(self, ctx: BKITParser.ArrayContext):
        ret = []
        if ctx.array_elelist():
            ret = ctx.array_elelist().accept(self)


        return ArrayLiteral(ret)

    def visitArray_elelist(self, ctx: BKITParser.Array_elelistContext):
        ret = [ctx.all_literal().accept(self)]

        if ctx.array_elelst():
            ret = ret + ctx.array_elelst().accept(self)
        return ret


    def visitArray_elelst(self, ctx: BKITParser.Array_elelstContext):
        ret = [ctx.all_literal().accept(self)]

        if ctx.array_elelst():
            ret = ret + ctx.array_elelst().accept(self)
        return ret

    def visitAll_literal(self, ctx: BKITParser.All_literalContext):
        if ctx.array():
            return ctx.array().accept(self)
        elif ctx.literal():
            return ctx.literal().accept(self)
        elif ctx.STRING():
            return StringLiteral(ctx.STRING().getText())
        return None



    def visitLiteral(self, ctx: BKITParser.LiteralContext):
        if ctx.INT():
            return IntLiteral(int(ctx.INT().getText(), 0))
        elif ctx.FLOAT():
            return FloatLiteral(float(ctx.FLOAT().getText()))
        elif ctx.BOOLEAN():
            return BooleanLiteral(bool(ctx.BOOLEAN().getText() == 'True'))
        return None
        



        

