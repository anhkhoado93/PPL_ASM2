import sys, os

TARGET = '../target/main/bkit/parser'
sys.path.append(TARGET)
locpath = ['./main/bkit/parser/','./main/bkit/astgen/','./main/bkit/utils/','./test/']
for p in locpath:
    if not p in sys.path:
        sys.path.append(p)

from TestUtils import TestAST
from AST import *

f = open("./test/ASTGenSuite.py", "w")
content = "import unittest\nfrom TestUtils import TestAST\nfrom AST import *\n\nclass ASTGenSuite(unittest.TestCase):\n\n"
with open("ASTtest.txt", "r") as tc:
    line = ""
    while True:
        try:
            counter = int(tc.readline())
        except:
            break
        print(counter)
        inp = ""
        expect = ""
        while True:
            line = tc.readline().strip('\n')
            if line == ".":
                break
            inp = inp + '\n\t\t\t' + line
        inp = inp[1:]
        testcase = "\tdef test_ast_{}(self):\n\t\tinput = \"\"\"\n{}\n\t\t\"\"\"".format(counter, inp)
        TestAST.checkASTGen(inp, expect, 300 + counter)
        dest = open("./test/solutions/" + str(300 + counter) + ".txt","r")
        expect = dest.read()
        testcase = testcase + "\n\t\texpect = " + expect + "\n\t\tself.assertTrue(TestAST.checkASTGen(input,expect,{}))\n\n".format(300 + counter)
        content = content + testcase

f.write(content)
f.close()
