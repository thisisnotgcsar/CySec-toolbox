#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// template file for libc_analyzer


// where I will allocate for fastbin attack
// static will load data in .bss elf section
static long long data[8];

// prints n qwords (64 bit, 8 bytes) along with their addresses
// 2 qwords per line
void print_qword(void* data, int n64){
	int i;
	for(i = 0; i < n64-2; i += 2)
		printf("%p: 0x%016llx\t0x%016llx\n", (long long*)data + i, *(((long long*)data) + i), *(((long long*)data) + i+1));
	if(n64 % 2 != 0)
		printf("%p: 0x%016llx\n", (long long*)data + i, *(((long long*)data) + i));
}

int main(){
	//initializing every byte of destination memory to \xff so we can know what bytes changed
	memset(data, 0xffffffff, sizeof(data));
	
	// creating a big chunk and initializing every byte of it \xff so we know what bytes changed
	// this is inside heap
	int i = 0;
	char* big = (char*)malloc(0x600);
	char* small = (char*)malloc(0x50); //no coalascing
	for(i; i<0x600; i++)
		big[i] = 0xff;
	free(big);
	
	// display what happens when I allocate a possible tcache chunk
	void* tcache = malloc(0x30);
	printf("ALLOC @ %p\n", tcache - 0x10);
	print_qword(tcache - 0x10, 9);
	
	// display what happens when I free the chunk
	// here fw pointer should be set to 0 and if there is tcache backward pointer could be set to the key
	free(tcache);
	printf("FREE @ %p\n", tcache - 0x10);
	print_qword(tcache - 0x10, 9);
	
	// setting the fw pointer of freed chunk to point inside data
	// if libc used doesnt have tcache this could already trigger an error of use after free
	// cause we didnt created the classical loop for the fastbin attack
	// memory corruption error!
	*((long long*)tcache) = (long long)data + 0x10;
	//allocating again first chunk
	tcache = malloc(0x30); //first
	
	// performing fastbin
	// we are allocating in an area (data inside .bss) where all bytes are set to \xff
	// allocating withhout the proper chunk size set should also trigger an error
	// if current libc is not using tcache
	void* tcache2 = malloc(0x30); //second (tcache2 should point to data)
	printf("&data: %p, FASTBIN ATTACK ALLOC @ %p\n", data, tcache2);
	print_qword(tcache2 - 0x10, 9);
	return 0;
}

// at the end if this program has ended gently without errors it means that the libc version uses tcache
// otherwise the error will be displayed and the program aborted
