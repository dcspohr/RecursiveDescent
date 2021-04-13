# RecursiveDescent
Python recursive descent parser

# Tokens
Integers are non-empty sequences of digits optionally preceded with either a ‘+’ or ‘-’ sign.
Decimal numbers are Integers followed by a ‘.’, followed by a non-empty sequence of digits.
Strings are any non-space sequences of characters enclosed in “”, e.g. “hello” “abc123”.
Keywords are the following strings: :=, +, -, *, /, OR, AND, ~, (, ), <, >, = , #, ;, PRINT, IF, ELSE, ENDIF, WHILE, ENDW, PROC, RETURN,  BEGIN, END.  (Notice: keywords are uppercase)
Identifiers are sequences of digits or letters. The first character must be a letter, and an identifier cannot be a Keyword. 
Tokens are always separated by white-spaces.

# Grammar
Programs conform to the following EBNF grammar where:
"FunctionSequence"  is the start symbol.
Terminal symbols are in bold. 
Collections of terminal symbols are in blue
Brackets,  ‘[‘ and ‘]’ , denote an optional section of a rule.  
Braces,  ‘{‘ and ‘}’,  denote repetition of a rule section (possibly 0 times). 

Relation :=   < | > | = | #  
AddOperator :=   + | - | OR 
MulOperator :=   * | / | AND

Expression := SimpleExpression [ Relation SimpleExpression ]
SimpleExpression := Term { AddOperator Term }
Term := Factor { MulOperator Factor }
Factor :=  integer | decimal | string | identifier | ( Expression ) | ~ Factor

Assignment := identifier := Expression 
PrintStatement := PRINT ( Expression )
RetStatement := RETURN identifier 
IfStatement := IF ( Expression ) StatementSequence [ ELSE StatementSequence ]
          ENDIF
WhileStatement = WHILE ( Expression ) StatementSequence ENDW

Statement := Assignment | PrintStatement | IfStatement | WhileStatement
StatementSequence = Statement { ; Statement }

ParamSequence :=  identifier  { , identifier }
FunctionDeclaration := PROC identifier ( [ ParamSequence ] ) BEGIN StatementSequence [ RetStatement ] END.

FunctionSequence := FunctionDeclaration { FunctionDeclaration }
