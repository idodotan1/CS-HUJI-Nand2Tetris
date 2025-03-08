// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
(START)
@8192
D = A
@i
M = D
@KBD
D = M
@BLACK
D;JGT
@WHITE
D;JEQ
(BLACK)
@i
D = M
@START
D;JEQ
@8192
D = A - D
@SCREEN
A = A + D
M = -1
@i
M = M-1
@BLACK
0;JMP
(WHITE)
@i
D = M
@START
D;JEQ
@8192
D = A - D
@SCREEN
A = A + D
M = 0
@i
M = M-1
@WHITE
0;JMP
