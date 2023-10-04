; not a shellcode
; read syscall implementation for multistage shellcode
; reads from stdin 0x100 bytes and put them in a buffer
lea    rsi,[rax+0x13] ; address of buffer
xor    rax,rax
xor    rdi,rdi
mov    rdx,0x100
syscall
