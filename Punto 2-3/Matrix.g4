// Matrix.g4
grammar Matrix;

// Parser rules
program     : stmt_list EOF ;
stmt_list   : (stmt SEMI)* ;
stmt        : matrix_decl
            | assign_stmt
            | print_stmt
            ;
matrix_decl : MATRIX ID EQ matrix_literal ;
matrix_literal
            : LBR row_list? RBR ;
row_list    : row (COMMA row)* ;
row         : LBR num_list? RBR ;
num_list    : NUMBER (COMMA NUMBER)* ;
assign_stmt : ID EQ expression ;
expression  : ID STAR ID
            | ID
            ;
print_stmt  : PRINT LP ID RP ;

// Lexer rules (keywords first to take precedence)
MATRIX  : 'matrix' ;
PRINT   : 'print' ;
EQ      : '=' ;
STAR    : '*' ;
COMMA   : ',' ;
SEMI    : ';' ;
LBR     : '[' ;
RBR     : ']' ;
LP      : '(' ;
RP      : ')' ;

// Numbers and identifiers
NUMBER  : [0-9]+ ('.' [0-9]+)? ;
ID      : [a-zA-Z_] [a-zA-Z0-9_]* ;

// Whitespace and comments
WS      : [ \t\r\n]+ -> skip ;
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
