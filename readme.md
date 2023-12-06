```
      _________       _______________          ________________________________ _______        
      __  ____/____  ___  ___/_|__  /______    ___  __/_  __ \_  __ \__  /__  /___  __ \___  __
      _  /    __  / / /____ \___/_ <_  ___/    __  /  _  / / /  / / /_  /__  __ \  / / /_  |/_/
      / /___  _  /_/ /____/ /____/ // /__      _  /   / /_/ // /_/ /_  / _  /_/ / /_/ /__>  <  
      \____/  _\__, / /____/ /____/ \___/      /_/    \____/ \____/ /_/  /_.___/\____/ /_/|_|  
              /____/                                                                           
```

# CyS3c t00lb0x <!-- omit in toc -->
> CySec Toolbox is a collection of cybersecuirty tools for CTF automation


- [About](#about)
- [Installation](#installation)
  - [Dependencies](#dependencies)
- [The tools and directory structure](#the-tools-and-directory-structure)
  - [genbin](#genbin)
    - [shellcodes](#shellcodes)



# About
These tools were developed during the POLIMI ODC 23-24 course for comfort, ease of use, and, most importantly, because it was fun. While initially designed for use in CTFs, there's nothing preventing you from incorporating them into your daily operations as well.

<p align="center">
  <img src="https://i.ibb.co/5FqSq8Y/image.png" alt="Your Image Alt Text" width="200">
  <br>
  <em>superuser and his toolbox</em>
</p>

# Installation
The majority of these tools are command-line scripts, requiring only BASH or Python for execution. Each script includes a help message accessible via the `-h` command line option, and a brief description of each tool is provided below.

> **Note**: It is essential to thoroughly comprehend the functionality of any script you intend to utilize. <br>
> Tools vary, and their behavior may be unpredictable. <br>
> Always refer to the commented source code for comprehensive understanding. <br>


## Dependencies 
Certain tools are built upon others to facilitate interaction and encourage automation. It's crucial to grasp the functionality of a script before execution. A comprehensive list of dependencies is available in `/configurations/installed.txt`. Familiarizing yourself with this list will help ensure the seamless operation of the tools.

# The tools and directory structure

## genbin
```
# writes to stdout the hex bytecodes of an assmebled assembly file given from stdin with 64 bit architecture
# if no file is provided, stdin is read
```
This script is tailored for shellcode CTFs, where crafting a specific shellcode and assembling it accurately is often required for a functional payload. While many individuals resort to web assemblers such as [defuse.ca](https://defuse.ca/online-x86-assembler.htm), I personally found them cumbersome due to the copy-pasting hurdle. `genbin` directly addresses this challenge by allowing you to write your assembly code in a file. It takes care of the assembly process and provides you with the hex bytecodes on stdout. This approach proves advantageous, as you can seamlessly call it from your script.py without relying on an internet connection. Moreover, it enhances code readability by eliminating the need for long hex strings, which may be unclear until de-assembled.

### shellcodes
This directory contains some useful shellcodes I wrote, each one with niche properties that make each of them special. `genbin` usually phishes from this directory the shellcodes so in most cases you will not have to write **any line of assembly**!


**genbin**: you will just need to give him some assembly instructions and he will generate you an optimized version of machine code!

**genscript**: this is a friend that just spawns a script template for binary ctfs

**fuckmyhex**: a cool guy. You don't wanna mess with him cause he speak 2 languages: binary and hex! And can do some very interesting manipulations with them...

**illtrace**: You can't escape. It will find your ptrace and NOP it. It's the big brother and he's watching you.

**gadget_finder**: automation tool to filter all the cool gadgets. It uses ROPgadget tool

**LOTTA1GADGETS**: automation tool that uses the one\_gadget tool and runs a script providing each one\_gadget found in input

**libc_analyzer**: dynamic analysis tool for extracting informations out of a libc shared object file and prints related informaitons.

**shellcodes**: the sweet honey. They always here when you need one (and they come in different flavors too).

**configurations**: Here I share all my config files. More efficiency, across multiple machines.
