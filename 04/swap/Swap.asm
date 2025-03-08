// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
@R15
D = M 
@i 
M = D
@R14
D = M
@curad
M = D
@minad
M = D
@maxad 
M = D
A = M
D = M
@min 
M = D
@max
M = D
@cur
M = D
(LOOP)
@i 
D = M 
@LOOPEND
D;JEQ
@curad
M = M + 1
A = M 
D = M
@cur
M = D
@min
D = D - M
@CHANGEMIN
D;JLT
@cur
D = M 
@max
D = D - M
@CHANGEMAX
D;JGE
(CONTINUELOOP)
@i
M = M - 1
@LOOP
0;JMP
(CHANGEMIN)
@cur
D = M
@min 
M = D
@curad
D = M 
@minad
M = D
@CONTINUELOOP
0;JMP
(CHANGEMAX)
@cur
D = M
@max
M = D
@curad
D = M 
@maxad
M = D
@CONTINUELOOP
0;JMP
(LOOPEND)
@minad
A = M
D = M        
@temp
M = D 
@maxad
A = M
D = M       
@minad
A = M
M = D          
@temp
D = M
@maxad
A = M
M = D        
(END)
@END
0;JMP







