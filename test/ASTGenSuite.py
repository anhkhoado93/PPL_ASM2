#1852471
import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):

	def test_ast_0(self):
		input = """
			Var: x;
		"""
		expect = Program([VarDecl(Id("x"),[],None)])
		self.assertTrue(TestAST.checkASTGen(input,expect,300))

	def test_ast_1(self):
		input = """
			Var: a, b = 2, c;
		"""
		expect = Program([VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],IntLiteral(2)),VarDecl(Id("c"),[],None)])
		self.assertTrue(TestAST.checkASTGen(input,expect,301))

	def test_ast_2(self):
		input = """
			Var: arr[1] = "Hello";
		"""
		expect = Program([VarDecl(Id("arr"),[1],StringLiteral("Hello"))])
		self.assertTrue(TestAST.checkASTGen(input,expect,302))

	def test_ast_3(self):
		input = """
			Var: arr[1][2][3][4][5] = {{{{{}}}}};
		"""
		expect = Program([VarDecl(Id("arr"),[1,2,3,4,5],ArrayLiteral([ArrayLiteral([ArrayLiteral([ArrayLiteral([ArrayLiteral([])])])])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,303))

	def test_ast_4(self):
		input = """
			Var: x = "String", y[1] = {1,2}, z;
		"""
		expect = Program([VarDecl(Id("x"),[],StringLiteral("String")),VarDecl(Id("y"),[1],ArrayLiteral([IntLiteral(1),IntLiteral(2)])),VarDecl(Id("z"),[],None)])
		self.assertTrue(TestAST.checkASTGen(input,expect,304))

	def test_ast_5(self):
		input = """
			Function: func
			    Body:
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("func"),[],([],[]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,305))

	def test_ast_6(self):
		input = """
			Function: func
			    Parameter: a,b
			    Body:
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("func"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],([],[]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,306))

	def test_ast_7(self):
		input = """
			Function: func
			    Parameter: a,b[1]
			    Body:
			    print(a);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("func"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[1],None)],([],[CallStmt(Id("print"),[Id("a")])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,307))

	def test_ast_8(self):
		input = """
			Var: a = 10;
			Function: func
			    Parameter: a,b
			    Body:
			    a = 5;
			    EndBody.
		"""
		expect = Program([VarDecl(Id("a"),[],IntLiteral(10)),FuncDecl(Id("func"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None)],([],[Assign(Id("a"),IntLiteral(5))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,308))

	def test_ast_9(self):
		input = """
			Function: func
			    Body:
			    print("Hello,");
			    EndBody.
			Function: func
			    Body:
			    print(" World");
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("func"),[],([],[CallStmt(Id("print"),[StringLiteral("Hello,")])])),FuncDecl(Id("func"),[],([],[CallStmt(Id("print"),[StringLiteral(" World")])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,309))

	def test_ast_10(self):
		input = """
			Function: main
			    Parameter: a[3], b[4][5]
			    Body:
			        Var: i = "don\'\"t care\";
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([VarDecl(Id("i"),[],StringLiteral("don\'\"t care"))],[]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,310))

	def test_ast_11(self):
		input = """
			Function: main
			    Parameter: a[3], b[4][5]
			    Body:
			        If a[3] == 1 
			        Then
			            Var: c = 10;
			            b[4][5] = 5;
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[If([(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(1)),[VarDecl(Id("c"),[],IntLiteral(10))],[Assign(ArrayCell(Id("b"),[IntLiteral(4),IntLiteral(5)]),IntLiteral(5))])],([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,311))

	def test_ast_12(self):
		input = """
			Function: main
			    Parameter: a[3], b[4][5]
			    Body:
			        If a[3] == 1 Then
			            Var: c = 10;
			        ElseIf a[3] == 2 Then
			            Var: b = 50;
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[If([(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(1)),[VarDecl(Id("c"),[],IntLiteral(10))],[]),(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(2)),[VarDecl(Id("b"),[],IntLiteral(50))],[])],([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,312))

	def test_ast_13(self):
		input = """
			Function: main
			    Parameter: a[3], b[4][5]
			    Body:
			        If a[3] == 1 Then
			            Var: c = 10;
			            b[4][5] = 5;
			        ElseIf a[3] == 2 Then
			            Var: b = 50;
			        Else
			            Var: d = "Hello";
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[If([(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(1)),[VarDecl(Id("c"),[],IntLiteral(10))],[Assign(ArrayCell(Id("b"),[IntLiteral(4),IntLiteral(5)]),IntLiteral(5))]),(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(2)),[VarDecl(Id("b"),[],IntLiteral(50))],[])],([VarDecl(Id("d"),[],StringLiteral("Hello"))],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,313))

	def test_ast_14(self):
		input = """
			Function: main
			    Parameter: a[3], b[4][5]
			    Body:
			        If a[3] == 4 Then
			            b[a[3]][5] = {1,2,{4,5}};
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[If([(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(4)),[],[Assign(ArrayCell(Id("b"),[ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(5)]),ArrayLiteral([IntLiteral(1),IntLiteral(2),ArrayLiteral([IntLiteral(4),IntLiteral(5)])]))])],([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,314))

	def test_ast_15(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        If a[3] == 4 Then
			            b[a[3]][5] = {1,2,{4,5}};
			        ElseIf (a[3] != 4) && (b[4][5] <. 6) Then
			            Return;
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[If([(BinaryOp("==",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(4)),[],[Assign(ArrayCell(Id("b"),[ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(5)]),ArrayLiteral([IntLiteral(1),IntLiteral(2),ArrayLiteral([IntLiteral(4),IntLiteral(5)])]))]),(BinaryOp("&&",BinaryOp("!=",ArrayCell(Id("a"),[IntLiteral(3)]),IntLiteral(4)),BinaryOp("<.",ArrayCell(Id("b"),[IntLiteral(4),IntLiteral(5)]),IntLiteral(6))),[],[Return(None)])],([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,315))

	def test_ast_16(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        a = 4 == b && c + 5.e1;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),BinaryOp("==",IntLiteral(4),BinaryOp("&&",Id("b"),BinaryOp("+",Id("c"),FloatLiteral(50.0)))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,316))

	def test_ast_17(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        a = 4 == b || c - 5.25;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),BinaryOp("==",IntLiteral(4),BinaryOp("||",Id("b"),BinaryOp("-",Id("c"),FloatLiteral(5.25)))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,317))

	def test_ast_18(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        a = 4 == b * !!!!(True);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),BinaryOp("==",IntLiteral(4),BinaryOp("*",Id("b"),UnaryOp("!",UnaryOp("!",UnaryOp("!",UnaryOp("!",BooleanLiteral(True))))))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,318))

	def test_ast_19(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        a = f(5,a && 1,g(8));
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),CallExpr(Id("f"),[IntLiteral(5),BinaryOp("&&",Id("a"),IntLiteral(1)),CallExpr(Id("g"),[IntLiteral(8)])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,319))

	def test_ast_20(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        a = fg("String", 1 && 2, {1,{2,3}});
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),CallExpr(Id("fg"),[StringLiteral("String"),BinaryOp("&&",IntLiteral(1),IntLiteral(2)),ArrayLiteral([IntLiteral(1),ArrayLiteral([IntLiteral(2),IntLiteral(3)])])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,320))

	def test_ast_21(self):
		input = """
			Function: f
			    Parameter: a[3], b[4][5]
			    Body:
			        a = fg("String", 1 && 2, {1,{2,3}});
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("f"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),CallExpr(Id("fg"),[StringLiteral("String"),BinaryOp("&&",IntLiteral(1),IntLiteral(2)),ArrayLiteral([IntLiteral(1),ArrayLiteral([IntLiteral(2),IntLiteral(3)])])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,321))

	def test_ast_22(self):
		input = """
			Function: game
			    Parameter: a[3], b[4][5]
			    Body:
			        a = fg("String", 1 && 2, {1,{2,3}});
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("game"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[Assign(Id("a"),CallExpr(Id("fg"),[StringLiteral("String"),BinaryOp("&&",IntLiteral(1),IntLiteral(2)),ArrayLiteral([IntLiteral(1),ArrayLiteral([IntLiteral(2),IntLiteral(3)])])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,322))

	def test_ast_23(self):
		input = """
			Function: game
			    Parameter: a[3], b[4][5]
			    Body:
			        f(g(h(y(j,{1,{2,{3}}}))));
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("game"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[CallStmt(Id("f"),[CallExpr(Id("g"),[CallExpr(Id("h"),[CallExpr(Id("y"),[Id("j"),ArrayLiteral([IntLiteral(1),ArrayLiteral([IntLiteral(2),ArrayLiteral([IntLiteral(3)])])])])])])])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,323))

	def test_ast_24(self):
		input = """
			Function: game
			    Parameter: a[3], b[4][5]
			    Body:
			        While a == 1 Do 
			            print(os("Hello"));
			        EndWhile.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("game"),[VarDecl(Id("a"),[3],None),VarDecl(Id("b"),[4,5],None)],([],[While(BinaryOp("==",Id("a"),IntLiteral(1)),([],[CallStmt(Id("print"),[CallExpr(Id("os"),[StringLiteral("Hello")])])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,324))

	def test_ast_25(self):
		input = """
			Function: fnc
			    Body:
			        While "Hello" Do 
			            print(os("Hello"));
			        EndWhile.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("fnc"),[],([],[While(StringLiteral("Hello"),([],[CallStmt(Id("print"),[CallExpr(Id("os"),[StringLiteral("Hello")])])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,325))

	def test_ast_26(self):
		input = """
			Function: main
			    Body:
			        Return ans(5);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Return(CallExpr(Id("ans"),[IntLiteral(5)]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,326))

	def test_ast_27(self):
		input = """
			Function: fact
			    Parameter: n
			    Body:
			        Return n * fact(n-1);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("fact"),[VarDecl(Id("n"),[],None)],([],[Return(BinaryOp("*",Id("n"),CallExpr(Id("fact"),[BinaryOp("-",Id("n"),IntLiteral(1))])))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,327))

	def test_ast_28(self):
		input = """
			Function: main
			    Body:
			        foo[foo2[1]] = bar({1,2,3});
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Assign(ArrayCell(Id("foo"),[ArrayCell(Id("foo2"),[IntLiteral(1)])]),CallExpr(Id("bar"),[ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,328))

	def test_ast_29(self):
		input = """
			Function: main
			    Body:
			        a = -----.-.-.1e2;
			    EndBody.    
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-.",UnaryOp("-.",UnaryOp("-.",FloatLiteral(100.0)))))))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,329))

	def test_ast_30(self):
		input = """
			Function: main
			    Body:
			        a = -func("adding");
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),UnaryOp("-",CallExpr(Id("func"),[StringLiteral("adding")])))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,330))

	def test_ast_31(self):
		input = """
			Function: main
			Body:
			    Break;
			    Continue;
			    While True Do
			        Break;
			        Continue;
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Break(),Continue(),While(BooleanLiteral(True),([],[Break(),Continue()]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,331))

	def test_ast_32(self):
		input = """
			Function: main
			**Parameter: a,b **
			Body:
			    Var: a = 4;
			    While True Do
			        Break;
			        Continue;
			        Return;
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"),[],IntLiteral(4))],[While(BooleanLiteral(True),([],[Break(),Continue(),Return(None)]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,332))

	def test_ast_33(self):
		input = """
			Function: main
			Body:
			    Var : a;
			    Do 
			        a = a + 1;
			        Break;
			    While True EndDo.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"),[],None)],[Dowhile(([],[Assign(Id("a"),BinaryOp("+",Id("a"),IntLiteral(1))),Break()]),BooleanLiteral(True))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,333))

	def test_ast_34(self):
		input = """
			Function: main
			Body:
			    Var : a;
			    While True Do
			        While "String" Do
			        EndWhile.
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"),[],None)],[While(BooleanLiteral(True),([],[While(StringLiteral("String"),([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,334))

	def test_ast_35(self):
		input = """
			Function: main
			Body:
			    Var : a;
			    While !!!!!!!True Do
			        While "String" Do
			        EndWhile.
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("a"),[],None)],[While(UnaryOp("!",UnaryOp("!",UnaryOp("!",UnaryOp("!",UnaryOp("!",UnaryOp("!",UnaryOp("!",BooleanLiteral(True)))))))),([],[While(StringLiteral("String"),([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,335))

	def test_ast_36(self):
		input = """
			Function: main
			Body:
			    a = func(3) * foo("Daa");
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),BinaryOp("*",CallExpr(Id("func"),[IntLiteral(3)]),CallExpr(Id("foo"),[StringLiteral("Daa")])))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,336))

	def test_ast_37(self):
		input = """
			Function: main
			Body:
			    Return 13e-5 + True - False;
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Return(BinaryOp("-",BinaryOp("+",FloatLiteral(0.00013),BooleanLiteral(True)),BooleanLiteral(False)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,337))

	def test_ast_38(self):
		input = """
			Function: main
			Body:
			    foo(2,
			        3,
			        4
			        );
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[CallStmt(Id("foo"),[IntLiteral(2),IntLiteral(3),IntLiteral(4)])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,338))

	def test_ast_39(self):
		input = """
			Function: main
			Body:
			    mainly(eat,**alohamora**1);
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[CallStmt(Id("mainly"),[Id("eat"),IntLiteral(1)])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,339))

	def test_ast_40(self):
		input = """
			Function: main
			    Body:
			        Return ***8**;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Return(None)]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,340))

	def test_ast_41(self):
		input = """
			Var: n, a[10];
			Function: main
			Body:
			    Var: i = 4;
			    For(i = 0, i < 10, 1) Do
			        If (n+9 < 4) Then
			            ** do something **
			        Else
			            **please my lord**
			        EndIf.
			    EndFor.
			EndBody.
		"""
		expect = Program([VarDecl(Id("n"),[],None),VarDecl(Id("a"),[10],None),FuncDecl(Id("main"),[],([VarDecl(Id("i"),[],IntLiteral(4))],[For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(1),([],[If([(BinaryOp("<",BinaryOp("+",Id("n"),IntLiteral(9)),IntLiteral(4)),[],[])],([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,341))

	def test_ast_42(self):
		input = """
			Function: fact
			Parameter: x
			Body:
			    Return fact(x-1);
			EndBody.
			
			Function: main
			Body:
			    print(fact(5)); **Should get 120**
			EndBody.
		"""
		expect = Program([FuncDecl(Id("fact"),[VarDecl(Id("x"),[],None)],([],[Return(CallExpr(Id("fact"),[BinaryOp("-",Id("x"),IntLiteral(1))]))])),FuncDecl(Id("main"),[],([],[CallStmt(Id("print"),[CallExpr(Id("fact"),[IntLiteral(5)])])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,342))

	def test_ast_43(self):
		input = """
			Function: main
			Parameter: b
			Body:
			    Var : a;
			    While a - b == 4 Do
			        While "String" Do
			        EndWhile.
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("b"),[],None)],([VarDecl(Id("a"),[],None)],[While(BinaryOp("==",BinaryOp("-",Id("a"),Id("b")),IntLiteral(4)),([],[While(StringLiteral("String"),([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,343))

	def test_ast_44(self):
		input = """
			Function: main
			Parameter: x
			Body:
			    Var: y = {{5,5.,0x3}, {{False}}, {"True"}};
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("x"),[],None)],([VarDecl(Id("y"),[],ArrayLiteral([ArrayLiteral([IntLiteral(5),FloatLiteral(5.0),IntLiteral(3)]),ArrayLiteral([ArrayLiteral([BooleanLiteral(False)])]),ArrayLiteral([StringLiteral("True")])]))],[]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,344))

	def test_ast_45(self):
		input = """
			Function: main
			Parameter: x
			Body:
			    Return !True && False;
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("x"),[],None)],([],[Return(BinaryOp("&&",UnaryOp("!",BooleanLiteral(True)),BooleanLiteral(False)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,345))

	def test_ast_46(self):
		input = """
			Function: main
			Body:
			    foo[foo2[1]] = bar({1,2,3});
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Assign(ArrayCell(Id("foo"),[ArrayCell(Id("foo2"),[IntLiteral(1)])]),CallExpr(Id("bar"),[ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,346))

	def test_ast_47(self):
		input = """
			Function: main
			Body:
			    foo(bar() + dua() + 5.e10);
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[CallStmt(Id("foo"),[BinaryOp("+",BinaryOp("+",CallExpr(Id("bar"),[]),CallExpr(Id("dua"),[])),FloatLiteral(50000000000.0))])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,347))

	def test_ast_48(self):
		input = """
			Var: a = {"Hello"}, b, c,d = 8. ;
		"""
		expect = Program([VarDecl(Id("a"),[],ArrayLiteral([StringLiteral("Hello")])),VarDecl(Id("b"),[],None),VarDecl(Id("c"),[],None),VarDecl(Id("d"),[],FloatLiteral(8.0))])
		self.assertTrue(TestAST.checkASTGen(input,expect,348))

	def test_ast_49(self):
		input = """
			Var: a[0O7] = {};
		"""
		expect = Program([VarDecl(Id("a"),[7],ArrayLiteral([]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,349))

	def test_ast_50(self):
		input = """
			Var: a[1] = {};
			Function: main
			Body:
			    a = a + 2;
			EndBody.
		"""
		expect = Program([VarDecl(Id("a"),[1],ArrayLiteral([])),FuncDecl(Id("main"),[],([],[Assign(Id("a"),BinaryOp("+",Id("a"),IntLiteral(2)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,350))

	def test_ast_51(self):
		input = """
			Function: func
			Parameter: a
			Body:
			    ** factorial **
			    Return a * func(a);
			EndBody.
		"""
		expect = Program([FuncDecl(Id("func"),[VarDecl(Id("a"),[],None)],([],[Return(BinaryOp("*",Id("a"),CallExpr(Id("func"),[Id("a")])))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,351))

	def test_ast_52(self):
		input = """
			Function: main
			Body:
			    If !!!(a==3) Then
			        a = "String";
			    Else
			        a = 6;
			    EndIf.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[If([(UnaryOp("!",UnaryOp("!",UnaryOp("!",BinaryOp("==",Id("a"),IntLiteral(3))))),[],[Assign(Id("a"),StringLiteral("String"))])],([],[Assign(Id("a"),IntLiteral(6))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,352))

	def test_ast_53(self):
		input = """
			Function: main
			Body:
			    If main(2) Then
			        a = "String";
			    Else
			        a = 6;
			    EndIf.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[If([(CallExpr(Id("main"),[IntLiteral(2)]),[],[Assign(Id("a"),StringLiteral("String"))])],([],[Assign(Id("a"),IntLiteral(6))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,353))

	def test_ast_54(self):
		input = """
			Function: main
			Body:
			    If 1 +. 2.9 == 3.9e0 Then
			        print("Successful");
			    Else
			        a = 6;
			    EndIf.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[If([(BinaryOp("==",BinaryOp("+.",IntLiteral(1),FloatLiteral(2.9)),FloatLiteral(3.9)),[],[CallStmt(Id("print"),[StringLiteral("Successful")])])],([],[Assign(Id("a"),IntLiteral(6))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,354))

	def test_ast_55(self):
		input = """
			Var: n, a[10];
			Function: main
			Body:
			    Var: i = 4;
			    For(i = "heelo", "aloha", {{"unexpected"}}) Do
			        ** do something **
			    EndFor.
			EndBody.
		"""
		expect = Program([VarDecl(Id("n"),[],None),VarDecl(Id("a"),[10],None),FuncDecl(Id("main"),[],([VarDecl(Id("i"),[],IntLiteral(4))],[For(Id("i"),StringLiteral("heelo"),StringLiteral("aloha"),ArrayLiteral([ArrayLiteral([StringLiteral("unexpected")])]),([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,355))

	def test_ast_56(self):
		input = """
			Var: n, a[10];
			Function: main
			Body:
			    Var: i = 4;
			    For(i = {{1,2,3}}, ---.--i,a == 1) Do
			        ** do something **
			    EndFor.
			EndBody.
		"""
		expect = Program([VarDecl(Id("n"),[],None),VarDecl(Id("a"),[10],None),FuncDecl(Id("main"),[],([VarDecl(Id("i"),[],IntLiteral(4))],[For(Id("i"),ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])]),UnaryOp("-",UnaryOp("-",UnaryOp("-.",UnaryOp("-",UnaryOp("-",Id("i")))))),BinaryOp("==",Id("a"),IntLiteral(1)),([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,356))

	def test_ast_57(self):
		input = """
			Var: n, a[10];
			Function: main
			Body:
			    Var: i = 4;
			    For(i = {{1,"2",3}}, i > 12.e-4, --i) Do
			        ** do something **
			    EndFor.
			EndBody.
		"""
		expect = Program([VarDecl(Id("n"),[],None),VarDecl(Id("a"),[10],None),FuncDecl(Id("main"),[],([VarDecl(Id("i"),[],IntLiteral(4))],[For(Id("i"),ArrayLiteral([ArrayLiteral([IntLiteral(1),StringLiteral("2"),IntLiteral(3)])]),BinaryOp(">",Id("i"),FloatLiteral(0.0012)),UnaryOp("-",UnaryOp("-",Id("i"))),([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,357))

	def test_ast_58(self):
		input = """
			Var: n, a[10];
			Function: main
			Body:
			    Var: i = 4;
			    For(i = {{1,2,3}}, ---.--i,a == 1) Do
			        If i > 5 Then
			        While True Do
			        EndWhile.
			        EndIf.
			    EndFor.
			EndBody.
		"""
		expect = Program([VarDecl(Id("n"),[],None),VarDecl(Id("a"),[10],None),FuncDecl(Id("main"),[],([VarDecl(Id("i"),[],IntLiteral(4))],[For(Id("i"),ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])]),UnaryOp("-",UnaryOp("-",UnaryOp("-.",UnaryOp("-",UnaryOp("-",Id("i")))))),BinaryOp("==",Id("a"),IntLiteral(1)),([],[If([(BinaryOp(">",Id("i"),IntLiteral(5)),[],[While(BooleanLiteral(True),([],[]))])],([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,358))

	def test_ast_59(self):
		input = """
			Function: main
			Body:
			    Var: i = 4;
			    For(i = {{1,2,3}}, ---.--i,a == 1) Do
			        If i > 5 Then
			        Do **nothing** While i 
			        EndDo.
			        EndIf.
			    EndFor.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("i"),[],IntLiteral(4))],[For(Id("i"),ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)])]),UnaryOp("-",UnaryOp("-",UnaryOp("-.",UnaryOp("-",UnaryOp("-",Id("i")))))),BinaryOp("==",Id("a"),IntLiteral(1)),([],[If([(BinaryOp(">",Id("i"),IntLiteral(5)),[],[Dowhile(([],[]),Id("i"))])],([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,359))

	def test_ast_60(self):
		input = """
			Function: fnc
			    Body:
			        While {1,2,{3,4}} Do 
			            If clear == sky Then
			                print("Hello");
			            EndIf.
			        EndWhile.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("fnc"),[],([],[While(ArrayLiteral([IntLiteral(1),IntLiteral(2),ArrayLiteral([IntLiteral(3),IntLiteral(4)])]),([],[If([(BinaryOp("==",Id("clear"),Id("sky")),[],[CallStmt(Id("print"),[StringLiteral("Hello")])])],([],[]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,360))

	def test_ast_61(self):
		input = """
			
		"""
		expect = Program([])
		self.assertTrue(TestAST.checkASTGen(input,expect,361))

	def test_ast_62(self):
		input = """
			Function: fnc
			    Body:
			        While {1,2,{3,4}} Do 
			            While True Do
			                While "True" Do
			                EndWhile.
			            EndWhile.
			        EndWhile.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("fnc"),[],([],[While(ArrayLiteral([IntLiteral(1),IntLiteral(2),ArrayLiteral([IntLiteral(3),IntLiteral(4)])]),([],[While(BooleanLiteral(True),([],[While(StringLiteral("True"),([],[]))]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,362))

	def test_ast_63(self):
		input = """
			Function: fnc
			    Body:
			        While {1,2,{3,4}} Do 
			            While True Do
			                Do a = 4; While a == 4
			                EndDo.
			            EndWhile.
			        EndWhile.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("fnc"),[],([],[While(ArrayLiteral([IntLiteral(1),IntLiteral(2),ArrayLiteral([IntLiteral(3),IntLiteral(4)])]),([],[While(BooleanLiteral(True),([],[Dowhile(([],[Assign(Id("a"),IntLiteral(4))]),BinaryOp("==",Id("a"),IntLiteral(4)))]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,363))

	def test_ast_64(self):
		input = """
			Function: divide_conquer
			    Parameter: hello, begin, end
			    Body:
			        If begin == end Then
			            Return hello[begin];
			        Else
			            Return divide_conquer(hello, begin, end - 2) + divide_conquer(hello, end - 2 + 1, end);
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("divide_conquer"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[If([(BinaryOp("==",Id("begin"),Id("end")),[],[Return(ArrayCell(Id("hello"),[Id("begin")]))])],([],[Return(BinaryOp("+",CallExpr(Id("divide_conquer"),[Id("hello"),Id("begin"),BinaryOp("-",Id("end"),IntLiteral(2))]),CallExpr(Id("divide_conquer"),[Id("hello"),BinaryOp("+",BinaryOp("-",Id("end"),IntLiteral(2)),IntLiteral(1)),Id("end")])))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,364))

	def test_ast_65(self):
		input = """
			Function: divide_conquer
			    Parameter: hello, begin, end
			    Body:
			        hello(begin());
			        end();
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("divide_conquer"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[CallStmt(Id("hello"),[CallExpr(Id("begin"),[])]),CallStmt(Id("end"),[])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,365))

	def test_ast_66(self):
		input = """
			Function: divide_conquer
			    Parameter: hello, begin, end
			    Body:
			        Do
			            print({"string"});
			        While "String"
			        EndDo.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("divide_conquer"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[Dowhile(([],[CallStmt(Id("print"),[ArrayLiteral([StringLiteral("string")])])]),StringLiteral("String"))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,366))

	def test_ast_67(self):
		input = """
			Function: divide_conquer
			    Parameter: hello, begin, end
			    Body:
			        Break;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("divide_conquer"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[Break()]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,367))

	def test_ast_68(self):
		input = """
			Function: divide_conquer
			    Parameter: hello, begin, end
			    Body:
			        Continue;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("divide_conquer"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[Continue()]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,368))

	def test_ast_69(self):
		input = """
			Function: divide_conquer
			    Parameter: hello, begin, end
			    Body:
			        While True Do
			        Break;
			        EndWhile.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("divide_conquer"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[While(BooleanLiteral(True),([],[Break()]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,369))

	def test_ast_70(self):
		input = """
			Function: ret
			    Parameter: hello, begin, end
			    Body:
			        Return "chimsedinang";
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("ret"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[Return(StringLiteral("chimsedinang"))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,370))

	def test_ast_71(self):
		input = """
			Function: ret
			    Parameter: hello, begin, end
			    Body:
			        Return ret();
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("ret"),[VarDecl(Id("hello"),[],None),VarDecl(Id("begin"),[],None),VarDecl(Id("end"),[],None)],([],[Return(CallExpr(Id("ret"),[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,371))

	def test_ast_72(self):
		input = """
			Function: exp
			    Parameter: a
			    Body:
			        a = ---(!!!1);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("exp"),[VarDecl(Id("a"),[],None)],([],[Assign(Id("a"),UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("!",UnaryOp("!",UnaryOp("!",IntLiteral(1))))))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,372))

	def test_ast_73(self):
		input = """
			Function: exp
			    Parameter: a
			    Body:
			        a = 1+2-.3;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("exp"),[VarDecl(Id("a"),[],None)],([],[Assign(Id("a"),BinaryOp("-.",BinaryOp("+",IntLiteral(1),IntLiteral(2)),IntLiteral(3)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,373))

	def test_ast_74(self):
		input = """
			Function: exp
			    Parameter: a
			    Body:
			        a = f() * g() -. 0O0;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("exp"),[VarDecl(Id("a"),[],None)],([],[Assign(Id("a"),BinaryOp("-.",BinaryOp("*",CallExpr(Id("f"),[]),CallExpr(Id("g"),[])),IntLiteral(0)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,374))

	def test_ast_75(self):
		input = """
			Function: exp
			    Parameter: a
			    Body:
			        a = 0xFA;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("exp"),[VarDecl(Id("a"),[],None)],([],[Assign(Id("a"),IntLiteral(250))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,375))

	def test_ast_76(self):
		input = """
			Function: exp
			    Parameter: a
			    Body:
			        a = 0xFA + 0O17 + 12 + 5e1;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("exp"),[VarDecl(Id("a"),[],None)],([],[Assign(Id("a"),BinaryOp("+",BinaryOp("+",BinaryOp("+",IntLiteral(250),IntLiteral(15)),IntLiteral(12)),FloatLiteral(50.0)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,376))

	def test_ast_77(self):
		input = """
			Function: main
			    Body:
			        Var: x, y, z;
			        x = y----------z;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],None),VarDecl(Id("y"),[],None),VarDecl(Id("z"),[],None)],[Assign(Id("x"),BinaryOp("-",Id("y"),UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",UnaryOp("-",Id("z"))))))))))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,377))

	def test_ast_78(self):
		input = """
			Function: main
			    Parameter: n
			    Body:
			        If n > 1 Then
			            If n > 2 Then
			                If n > 3 Then
			                    If n > 4 Then
			                        If n > 5 Then
			                            If n > 6 Then
			                            EndIf.
			                        EndIf.
			                    EndIf.
			                EndIf.
			            EndIf.
			        EndIf.
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[VarDecl(Id("n"),[],None)],([],[If([(BinaryOp(">",Id("n"),IntLiteral(1)),[],[If([(BinaryOp(">",Id("n"),IntLiteral(2)),[],[If([(BinaryOp(">",Id("n"),IntLiteral(3)),[],[If([(BinaryOp(">",Id("n"),IntLiteral(4)),[],[If([(BinaryOp(">",Id("n"),IntLiteral(5)),[],[If([(BinaryOp(">",Id("n"),IntLiteral(6)),[],[])],([],[]))])],([],[]))])],([],[]))])],([],[]))])],([],[]))])],([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,378))

	def test_ast_79(self):
		input = """
			Function: main
			    Body:
			        Var: y;
			        y = y && y < y + y * !-y[foo(y)];
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("y"),[],None)],[Assign(Id("y"),BinaryOp("<",BinaryOp("&&",Id("y"),Id("y")),BinaryOp("+",Id("y"),BinaryOp("*",Id("y"),UnaryOp("!",UnaryOp("-",ArrayCell(Id("y"),[CallExpr(Id("foo"),[Id("y")])])))))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,379))

	def test_ast_80(self):
		input = """
			Function: main
			    Body:
			        Var: y;
			        y = y[foo(y)] + y[bar(y)] ;
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([VarDecl(Id("y"),[],None)],[Assign(Id("y"),BinaryOp("+",ArrayCell(Id("y"),[CallExpr(Id("foo"),[Id("y")])]),ArrayCell(Id("y"),[CallExpr(Id("bar"),[Id("y")])])))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,380))

	def test_ast_81(self):
		input = """
			Var: a[2][3][5] = {{1,2,3},{3,4,5},{4,5,6}};
		"""
		expect = Program([VarDecl(Id("a"),[2,3,5],ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]),ArrayLiteral([IntLiteral(3),IntLiteral(4),IntLiteral(5)]),ArrayLiteral([IntLiteral(4),IntLiteral(5),IntLiteral(6)])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,381))

	def test_ast_82(self):
		input = """
			Var: a[**comment**123] = {{}};
		"""
		expect = Program([VarDecl(Id("a"),[123],ArrayLiteral([ArrayLiteral([])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,382))

	def test_ast_83(self):
		input = """
			Function: testCallWithIndex
			    Parameter: a[5][5], i
			    Body:
			        print(a[i+2][i+3]);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("testCallWithIndex"),[VarDecl(Id("a"),[5,5],None),VarDecl(Id("i"),[],None)],([],[CallStmt(Id("print"),[ArrayCell(Id("a"),[BinaryOp("+",Id("i"),IntLiteral(2)),BinaryOp("+",Id("i"),IntLiteral(3))])])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,383))

	def test_ast_84(self):
		input = """
			Function: testCallWithString
			    Parameter: a[5][5], i
			    Body:
			        print(a[1==2][2==3]);
			    EndBody.
		"""
		expect = Program([FuncDecl(Id("testCallWithString"),[VarDecl(Id("a"),[5,5],None),VarDecl(Id("i"),[],None)],([],[CallStmt(Id("print"),[ArrayCell(Id("a"),[BinaryOp("==",IntLiteral(1),IntLiteral(2)),BinaryOp("==",IntLiteral(2),IntLiteral(3))])])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,384))

	def test_ast_85(self):
		input = """
			Function: func
			Body:
			    Var: i;
			    For(i={{0}},"anyting", **noonecare**i) Do
			        For(j={{0}},"anyting", **noonecare**j) Do
			            print(i);
			        EndFor.
			    EndFor.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("func"),[],([VarDecl(Id("i"),[],None)],[For(Id("i"),ArrayLiteral([ArrayLiteral([IntLiteral(0)])]),StringLiteral("anyting"),Id("i"),([],[For(Id("j"),ArrayLiteral([ArrayLiteral([IntLiteral(0)])]),StringLiteral("anyting"),Id("j"),([],[CallStmt(Id("print"),[Id("i")])]))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,385))

	def test_ast_86(self):
		input = """
			Function: testing
			Parameter: abc
			Body:
			    print("****");
			EndBody.
		"""
		expect = Program([FuncDecl(Id("testing"),[VarDecl(Id("abc"),[],None)],([],[CallStmt(Id("print"),[StringLiteral("****")])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,386))

	def test_ast_87(self):
		input = """
			Function: testing
			Parameter: abc
			Body:
			    print(**""**);
			EndBody.
		"""
		expect = Program([FuncDecl(Id("testing"),[VarDecl(Id("abc"),[],None)],([],[CallStmt(Id("print"),[])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,387))

	def test_ast_88(self):
		input = """
			Function: testing
			Parameter: a
			Body:
			    println("Im so out of idea");
			EndBody.
		"""
		expect = Program([FuncDecl(Id("testing"),[VarDecl(Id("a"),[],None)],([],[CallStmt(Id("println"),[StringLiteral("Im so out of idea")])]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,388))

	def test_ast_89(self):
		input = """
			Function: main
			Body:
			    Return (((i==j) == k[3]) == f(4)) == ((g == n) == mm);
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Return(BinaryOp("==",BinaryOp("==",BinaryOp("==",BinaryOp("==",Id("i"),Id("j")),ArrayCell(Id("k"),[IntLiteral(3)])),CallExpr(Id("f"),[IntLiteral(4)])),BinaryOp("==",BinaryOp("==",Id("g"),Id("n")),Id("mm"))))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,389))

	def test_ast_90(self):
		input = """
			Function: main
			Body:
			    Return 1<2;
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[Return(BinaryOp("<",IntLiteral(1),IntLiteral(2)))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,390))

	def test_ast_91(self):
		input = """
			Function: main
			Body:
			    If (e)[4] Then 
			    ElseIf (e)[a][b][c] Then
			    Else 
			    EndIf.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[If([(ArrayCell(Id("e"),[IntLiteral(4)]),[],[]),(ArrayCell(Id("e"),[Id("a"),Id("b"),Id("c")]),[],[])],([],[]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,391))

	def test_ast_92(self):
		input = """
			Function: main
			Body:
			    While a == 69 Do
			        Do 
			        **Nothing**
			        While c =/= 6. EndDo. 
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[While(BinaryOp("==",Id("a"),IntLiteral(69)),([],[Dowhile(([],[]),BinaryOp("=/=",Id("c"),FloatLiteral(6.0)))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,392))

	def test_ast_93(self):
		input = """
			Function: main
			Body:
			    While a == 69 Do
			        Do 
			        a = a - !b;
			        While c =/= 6. EndDo. 
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[While(BinaryOp("==",Id("a"),IntLiteral(69)),([],[Dowhile(([],[Assign(Id("a"),BinaryOp("-",Id("a"),UnaryOp("!",Id("b"))))]),BinaryOp("=/=",Id("c"),FloatLiteral(6.0)))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,393))

	def test_ast_94(self):
		input = """
			Function: main
			Body:
			    While a == 69 Do
			        Do 
			        a = a - -a;
			        While c =/= 6. EndDo. 
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[While(BinaryOp("==",Id("a"),IntLiteral(69)),([],[Dowhile(([],[Assign(Id("a"),BinaryOp("-",Id("a"),UnaryOp("-",Id("a"))))]),BinaryOp("=/=",Id("c"),FloatLiteral(6.0)))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,394))

	def test_ast_95(self):
		input = """
			Function: main
			Body:
			    While a == 69 Do
			        Do 
			        a = a + aa;
			        While c =/= 6. EndDo. 
			    EndWhile.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("main"),[],([],[While(BinaryOp("==",Id("a"),IntLiteral(69)),([],[Dowhile(([],[Assign(Id("a"),BinaryOp("+",Id("a"),Id("aa")))]),BinaryOp("=/=",Id("c"),FloatLiteral(6.0)))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,395))

	def test_ast_96(self):
		input = """
			Function: abc
			Body:
			    If a==b Then x = 1;
			        ElseIf a<b Then x = 2;
			        ElseIf a>b Then x = 3;
			        Else x = 4;
			    EndIf.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("abc"),[],([],[If([(BinaryOp("==",Id("a"),Id("b")),[],[Assign(Id("x"),IntLiteral(1))]),(BinaryOp("<",Id("a"),Id("b")),[],[Assign(Id("x"),IntLiteral(2))]),(BinaryOp(">",Id("a"),Id("b")),[],[Assign(Id("x"),IntLiteral(3))])],([],[Assign(Id("x"),IntLiteral(4))]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,396))

	def test_ast_97(self):
		input = """
			Var: a = 0x4, b = 0O3, c = 10.8, d = 14.e-10;
		"""
		expect = Program([VarDecl(Id("a"),[],IntLiteral(4)),VarDecl(Id("b"),[],IntLiteral(3)),VarDecl(Id("c"),[],FloatLiteral(10.8)),VarDecl(Id("d"),[],FloatLiteral(1.4e-09))])
		self.assertTrue(TestAST.checkASTGen(input,expect,397))

	def test_ast_98(self):
		input = """
			Var: a = "0x4, b = 0O3, c = 10.8, d = 14.e-10";
		"""
		expect = Program([VarDecl(Id("a"),[],StringLiteral("0x4, b = 0O3, c = 10.8, d = 14.e-10"))])
		self.assertTrue(TestAST.checkASTGen(input,expect,398))

	def test_ast_99(self):
		input = """
			Function: abc
			Body:
			    If a==b Then x = 1;
			    Else print("Finish!!!!");
			    EndIf.
			EndBody.
		"""
		expect = Program([FuncDecl(Id("abc"),[],([],[If([(BinaryOp("==",Id("a"),Id("b")),[],[Assign(Id("x"),IntLiteral(1))])],([],[CallStmt(Id("print"),[StringLiteral("Finish!!!!")])]))]))])
		self.assertTrue(TestAST.checkASTGen(input,expect,399))

