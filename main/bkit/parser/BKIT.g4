// 1852471
grammar BKIT;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:       
        raise UncloseString(result.text[1:])
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text[1:])
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    elif (tk == self.STRING):
        result.text = result.text[1:-1]
        return result
    else:
        return result;
}

options{
	language=Python3;
}

program  : decl_list EOF;

fragment Digit: [0-9];

ID: [a-z]([a-zA-Z0-9_])* ;

decl_list: var_declist? func_declist?;

var_declist: variable_decl var_list?;
var_list: variable_decl var_list?;

func_declist: func_decl func_prime?;
func_prime: func_decl func_prime?;

//variable declaration
variable_decl: VAR COLON variable_list SEMI;
variable_list: var_decl varlist?;
varlist: COMMA var_decl varlist?;
var_decl: ID index_list? (ASSIGN all_literal)?;
index_list: (LS INT RS) index_list?;


//fucntion declaration
func_decl: FUNCTION COLON ID parameter? body;
parameter: PARAMETER COLON param parameter_list?; 
parameter_list: COMMA param parameter_list?;
param: ID index_list?;
body: BODY COLON stmtlst ENDBODY DOT;



stmtlst: var_declist? stmtlist?;

stmtlist: stmt stmttail?;
stmttail: stmt stmttail?;
//statement 
stmt: assign_stmt | if_stmt | for_stmt | while_stmt | dowhile_stmt | call_stmt 
        | return_stmt | continue_stmt | break_stmt;


assign_stmt: (ID | expr7 index_op) ASSIGN expr SEMI;
if_stmt: IF expr THEN stmtlst elif_stmt_list? else_stmt? ENDIF DOT;
elif_stmt_list: elif_stmt elif_stmt_list?;
elif_stmt: ELSEIF expr THEN stmtlst;
else_stmt: ELSE stmtlst;
for_stmt: FOR LP ID ASSIGN expr COMMA expr COMMA expr RP DO stmtlst ENDFOR DOT;
while_stmt: WHILE expr DO stmtlst ENDWHILE DOT;
dowhile_stmt: DO stmtlst WHILE expr ENDDO DOT;
break_stmt: BREAK SEMI;
continue_stmt: CONTINUE SEMI;
call_stmt: ID LP call_list? RP SEMI;
return_stmt: RETURN expr? SEMI;


//expressions
index_op: LS expr0 RS index_op?;
expr: expr0 | STRING | array;
expr0: expr1 | expr1 RELATIONAL expr1;
expr1: expr2 | expr1 BINLOGICAL expr2;
expr2: expr3 | expr2 (ADDING|SIGN) expr3;
expr3: expr4 | expr3 MULTIPLYING expr4;
expr4: expr5 | UNLOGICAL expr4;
expr5: expr6 | SIGN expr5;
expr6: expr7 | expr7 index_op;
expr7: expr8 | ID LP call_list? RP;
expr8: literal | ID | LP expr0 RP;

call_list: callee calltail?;
calltail: COMMA callee calltail?;
callee: expr;
array: LB array_elelist? RB;
array_elelist: all_literal array_elelst?;
array_elelst: COMMA all_literal array_elelst?;
all_literal: array | literal | STRING;
literal: INT | FLOAT | BOOLEAN;

SEMI: ';' ;
COLON: ':' ;
VAR: 'Var' ;
BODY: 'Body';
BREAK: 'Break';
CONTINUE: 'Continue';
DO: 'Do';
ELSE: 'Else';
ELSEIF: 'ElseIf';
ENDBODY: 'EndBody';
ENDIF: 'EndIf';
ENDFOR: 'EndFor';
ENDWHILE: 'EndWhile';
FOR: 'For';
FUNCTION: 'Function';
IF: 'If';
PARAMETER: 'Parameter';
RETURN: 'Return';
ENDDO: 'EndDo';
THEN: 'Then';
WHILE: 'While';
SIGN: '-' | '-.';
UNLOGICAL: '!';
MULTIPLYING: '*' | '*.' | '\\' | '\\.' | '%';
ADDING: '+' | '+.';
BINLOGICAL: '&&' | '||';
RELATIONAL: '==' | '!=' | '<' | '<=' | '>' | '>=' | '=/=' | '<.' | '<=.' | '>.' | '>=.';

COMMA: ',';
LP: '(';
RP: ')';
LS: '[';
RS: ']';
LB: '{';
RB: '}';
DOT: '.';

ASSIGN: '=';

fragment Decimal: [1-9]Digit* | '0';
fragment Hexcadecimal : '0'[xX]('0' | [A-F1-9]([A-F] | Digit)*);
fragment Octadecimal: '0'[oO]('0' | [1-7][0-7]*);
INT: Decimal | Hexcadecimal | Octadecimal;

fragment Exponent: [eE][+-]?Digit+ ;
fragment FloatingPoint: DOT Digit*;
FLOAT: Decimal ( FloatingPoint | FloatingPoint Exponent | Exponent );

BOOLEAN : 'True' | 'False';

ESCP_SQN: '\\' ('b' | 'f' | 'r' | 'n' | 't' | '\'' | '\\');

STRING: '"' (~['"\n\r\\] | ESCP_SQN | '\'"')*? '"'; 

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

COMMENT: '**' (.)*? '**' -> skip;
ILLEGAL_ESCAPE:  '"' (~["])*? ('\\' ~('b' | 'f' | 'r' | 'n' | 't' | '\'' | '\\')  |  '\'' ~["]); 
UNCLOSE_STRING: '"' (~['"\n\r\\] | ESCP_SQN | '\'"')*;
UNTERMINATED_COMMENT: '**' (. | [\n\t\r] | ESCP_SQN)*?  ;
ERROR_CHAR: .;




