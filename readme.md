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

- [1. About](#1-about)
- [2. Installation](#2-installation)
  - [2.1. Dependencies](#21-dependencies)
- [3. The tools and directory structure](#3-the-tools-and-directory-structure)
  - [3.1. `genbin`](#31-genbin)
    - [3.1.1. `shellcodes/`](#311-shellcodes)
  - [3.2. `genscript/genscript`](#32-genscriptgenscript)
  - [3.3. `illtrace`](#33-illtrace)
    - [3.3.1. NOPping `ptrace`](#331-nopping-ptrace)
  - [3.4. `gadget_finder`](#34-gadget_finder)
  - [3.5. `1gadgetsarmy`](#35-1gadgetsarmy)
  - [3.6. `libc_analyzer/libc_analyzer`](#36-libc_analyzerlibc_analyzer)
    - [3.6.1. `libc_analyzer/check_tcache.c`](#361-libc_analyzercheck_tcachec)
  - [3.7. `notes/`](#37-notes)
  - [3.8. `configurations/`](#38-configurations)
- [4. Roadmap](#4-roadmap)
- [5. Contributing](#5-contributing)
  - [5.1. How to contribute to THIS repo?](#51-how-to-contribute-to-this-repo)
  - [5.2. I have an idea for a new tool, can we collaborate?](#52-i-have-an-idea-for-a-new-tool-can-we-collaborate)
- [6. Acknowledgments](#6-acknowledgments)
- [7. Meta](#7-meta)



# 1. About
These tools were developed during the POLIMI ODC 23-24 course for comfort, ease of use, and, most importantly, because it was fun. While initially designed for use in CTFs, there's nothing preventing you from incorporating them into your daily operations as well.

<p align="center">
  <img src="https://i.ibb.co/5FqSq8Y/image.png" alt="Your Image Alt Text" width="200">
  <br>
  <em>csarg and his toolbox</em>
</p>

# 2. Installation
The majority of these tools are command-line scripts, requiring only BASH or Python for execution. Each script includes a help message accessible via the `-h` command line option, and a brief description of each tool is provided below.

> ❗️ **Note**: It is essential to thoroughly comprehend the functionality of any script you intend to utilize. <br>
> Tools vary, and their behavior may be unpredictable. <br>
> Always refer to the commented source code for comprehensive understanding. <br>


## 2.1. Dependencies 
Certain tools are built upon others to facilitate interaction and encourage automation. It's crucial to grasp the functionality of a script before execution. A comprehensive list of dependencies is available in `/configurations/installed.txt`. Familiarizing yourself with this list will help ensure the seamless operation of the tools.

# 3. The tools and directory structure

## 3.1. `genbin`
> *"It eats assembly and produces optimized machine code! Basically a digital microorganism"*
```
# writes to stdout the hex bytecodes of an assmebled assembly file given from stdin with 64 bit architecture
# if no file is provided, stdin is read
```
This script is tailored for shellcode CTFs, where crafting a specific shellcode and assembling it accurately is often required for a functional payload. While many individuals resort to web assemblers such as [defuse.ca](https://defuse.ca/online-x86-assembler.htm), I personally found them cumbersome due to the copy-pasting hurdle. `genbin` directly addresses this challenge by allowing you to write your assembly code in a file. It takes care of the assembly process and provides you with the hex bytecodes on stdout. This approach proves advantageous, as you can seamlessly call it from your script.py without relying on an internet connection. Moreover, it enhances code readability by eliminating the need for long hex strings, which may be unclear until de-assembled.

### 3.1.1. `shellcodes/`
> *"The sweet honey. They always here when you need one (and they come in different flavors too)."*

This directory comprises a compilation of useful shellcodes, each possessing unique properties that set them apart. By utilizing the `genbin` tool, you can easily extract code snippets from this directory, eliminating the need to **write any assembly code** in most cases.

## 3.2. `genscript/genscript`
> *"A script replicator! What is this "Blade Runner"??"*
```
# creates in current working directory a template python file for pwning named "script.py"
# the generated script file is already set with the parameters passed in input
```
> ⚠️ This tool depends and it is built on top of `pwntools`. You can view and install `pwntools` [here](https://github.com/Gallopsled/pwntools/tree/dev).

One of the most important tools for automating CTFs as it automatically generates you a `script.py` template directly in your working directory. You can pass as command line parameters the IP, PORT and local EXECUTABLE file in order to find them again already set inside the template. There are 2 types of templates: `/genscript/pwn_script.py` for binary exploitation and `/genscript/web_script.py` for web app exploitation.

## 3.3. `illtrace`
> *"A cold, emotionless hitman machine. What is this "Terminator??"*
```
# search in an executable file a call for ptrace and NOPs it
# it can also NOP a particular bytes signature provided by input
```
This tool automates binary patching, specifically addressing scenarios in CTFs where executables employ measures such as ptrace calls or alarm functions to evade dynamic analysis. By default, the script searches and NOPs ptrace calls. NOPping involves substituting bytecode with consecutive NOP codes, effectively replacing the previous function with a "skip" instruction. Additionally, you can specify a particular bytecode, obtained through reverse engineering, to search for and NOP using command line options.

### 3.3.1. NOPping `ptrace`
To identify the `ptrace` call, `illtrace` relies on two bytecode patterns: 
 1. A sequence of consecutive instructions that load common parameters into registers for the `ptrace` call.
 2. A bytecode sequence checking for `if result == 0`, a common flow indicating the use of `ptrace` for checking if it is being traced. 

If the dynamic search yields no results, you can explicitly provide the bytecode signature discovered through reverse engineering.

##  3.4. `gadget_finder`
> *"It's like a truffle dog but for gadgets"*
```
# script for gadgets finding optimization
# it runs ROPgadget and puts the output to `gadgets` file
# it then parses gadgets with different `awk` filters and prints the outputs to `stdout`
# current filters are:
# 	- all lines that have only `pop` operations
# 	- all lines that contain a `mov rsp, ***` operation
```
> ⚠️ This tool depends and it is built on top of `ROPgadget`. You can view and install `ROPgadget` [here](https://github.com/JonathanSalwan/ROPgadget).

`gadget_finder` serves as an automation tool for `ROPgadget`, streamlining the process by running the `ROPgadget` tool and applying specific filters to its output. These filters are the ones common to search for in a temptative of [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming) attack scenario.

## 3.5. `1gadgetsarmy`
> *"You know what's better than one magic gadget? LOTS of magic gadgets!"*
```
# This shell script takes an input file and searches for all the magic gadgets within it. 
# It then proceeds to call the provided Python script with each discovered magic gadget offset as an argument.
```
> ⚠️ This tool depends and it is built on top of `one_gadget`. You can view and install `one_gadget` [here](https://github.com/david942j/one_gadget).

Automation tool wrapped around one_gadget for magic gadget exploitation. It executes your exploitation script (e.g.: `script.py`) giving it in as command line argument "MAGIC_GADGET" the magic gadget's offset found first by running `one_gadget`, basically "bruteforcing" your exploit with magic gadgets.

It continues this process until discovering new offsets. This ensures ongoing interaction with your exploit script, allowing you to interrupt the execution at your discretion.

## 3.6. `libc_analyzer/libc_analyzer`
> *"Let's shake the black box and listen waht's inside."*
```
# shell script that "analyzes" a libc shared object provided and outputs some common informations found on it
# It tries to understand if the libc version provided in input is using tcache
# and if yes, how it behaves (allocating, deallocating, key implementation, fastbin attack...)

# this script works with patchelf and check_tcache.c template c file
# it pathces the c file with patchelf with the libc and ld provided in input
# and then it compiles and runs the file and outputs to stdout what it discovered
```
> ⚠️ This tool depends and it is built on top of `patchelf`. You can view and install `patchelf` [here](https://github.com/NixOS/patchelf).

Dynamic analysis tool for HEAP exploitation. It makes use of carefully crafted C programs to gather informations on the executable file in a black box manner. <br>
Sometimes you are given a libc version wich is unknown or that has been opportunately modified. Exploiting `ptmalloc` heavily depends on the implementation of `libc` you're dealing with and getting to know a-priori the behavior of it might be helpful for speedingup operations and do less confusion.

### 3.6.1. `libc_analyzer/check_tcache.c`
This particular C file tries to understand if the `libc` used by it has `T-Cache` implementation and how it behaves.

## 3.6. `patcher/patcher.py`
> *"Surgeon on its work.. patching codes"*
```
# Script that patches a binary file provided.
# It does provide NOP and ZERO out-of-the-box patches but it's possible
# to also inject via file your custum one.
```

Substitutres code in certain precise points. It provides already premade patches:
 - NOP: Substitutes every byte from OFFSET with the `NOP` opcode (`0x90`). It requires the bytes LENGTH of how much you want to patch.
 - ZERO: Substitutes every byte from OFFSET with the `NULL` byte (`0x00`). It requires the bytes LENGTH of how much you want to patch.
 - It's possible to provide in input also a custum binary file that will be used to overwrite from OFFSET.
The tool also does boundaries chekcing on the OFFSET and LENGTH provided in input.

### 3.6.1. `patcher/patcher`
Simple shell script used for calling the python script. It passes all its command line arguments to the script.

## 3.7. `notes/`
Just a collection of slides and useful material to review during exploitation.

## 3.8. `configurations/`
> *"Home is where you can double-quote automated."*

This is a directory used for replicating and syncing the setup I'M comfortable with.

Here you can find all my settings file and instructions to refresh my mind on how to setup services.

I won't dwell my self on this part cause its very subjective to me but if you're interested or you don't understand something absoloutely contact me and I'll try to help you as I can 👍🏻!

# 4. Roadmap
- [ ] Create a Docker image containing the toolbox and all the dependent software already setup
- [ ] Enhance `configurations/` directory content
- [ ] Add more web app exploitation tools
- [ ] Add examples directory
- [ ] Improve `fuckmyhex.py` on its branch
- [ ] Remove `ptrace` signature search for illtrace or improve it
- [ ] Improving `notes/` material and adding more files

See the [open issues](https://github.com/thisisnotcsarg/CySec-toolbox/issues) for a full list of proposed features (and known issues).

# 5. Contributing
Contributions are more than welcome! Here's a [short video tutorial](https://www.youtube.com/watch?v=8lGpZkjnkt4) on how to open a pull request.

## 5.1. How to contribute to THIS repo?
Finding bugs, testing, enhancing code or just helping with documentation is appreciated. <br>
Don't hesitate to contact me even just for questions or suggestions.

## 5.2. I have an idea for a new tool, can we collaborate?
Yes! If you want we can create together a universal CTF toolbox repo with the useful tools of everyone.

# 6. Acknowledgments
 - [pwntools](https://github.com/Gallopsled/pwntools/tree/dev)
 - [ROPgadget](https://github.com/JonathanSalwan/ROPgadget)
 - [one_gadget](https://github.com/david942j/one_gadget)
 - [patchelf](https://github.com/NixOS/patchelf)

*Contributors will get added to the list*

# 7. Meta
csarg

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/thisisnotcsarg/CySec-toolbox">CySec-toolbox</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/thisisnotcsarg">csarg</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>

https://github.com/thisisnotcsarg
