; sys code that does a write
lea rsi, [rel $-0x65] ; buffer from where to read
mov rdi, 0x01 ; write to stdout
mov rdx, 0x30 ; how many bytes to write
mov rax, 0x01 ; write syscall number
syscall
