import argparse
import sys
import itertools

'''
# Generate permutations of characters
characters=['r', 'x', 'b']
permutations = []
for r in range(1, len(characters) + 1):
        permutations.extend(itertools.permutations(characters, r))
ops = [''.join(permutation) for permutation in permutations]
'''

byte_mode=True

# functions operations
def tobytes(output):
    global byte_mode
    try:
        byte_mode=False
        return [bytes.fromhex(hex_str) for hex_str in output]
    except:
        byte_mode=True
        return [line.strip().encode() for line in output]

def tohex(output):
    return [bs.hex() for bs in output]

#expects bytes
def bytes_reverse(output):
    return [bs[::-1] for bs in output]

#expects bytes
def bytes_xor(output):
    result = []

    for i in range(0, len(output) - 1, 2):
        if i + 1 < len(output):
            if len(output[i]) != len(output[i + 1]):
                print(f"fuckmyhex.py: error: xor: bytes of different length:\n{i}: {output[i]} is {len(output[i])} bytes\n{i+1}: {output[i+1]} is {len(output[i+1])} byts") 
                exit(-1)
            xored_byte = bytes(a ^ b for a, b in zip(output[i], output[i + 1]))
            result.append(xored_byte)

    # If there's an odd number of bytes, append the last one as is 
    if len(output) % 2 == 1:
        result.append(output[-1])
    return result


# parsing args
parser = argparse.ArgumentParser(description='Hex tool for various ops')
parser.add_argument('-f', '--file', type=argparse.FileType('rb'), default=sys.stdin, help="specify a file path to read from input. stdin is default if not provided")
parser.add_argument('ops', nargs='*', default=[], help='Do operations with bytes or hex provided. Operations: (h): hex mode, (b) bytes mode, (r): revert bytes line by line, (x) xor byte lines two by two')
args = parser.parse_args()
file = args.file
valid_ops = ['r', 'h', 'b', 'x']
ops = list(itertools.chain.from_iterable(args.ops))
for op in ops:
    if op not in valid_ops:
        print(f"fuckmyhex.py: error: argument ops: invalid choice: '{op}' (choose from {valid_ops})")
        exit(-1)


# reading data from file
output = tobytes(file.readlines())

# handling ops
for op in ops:
    #convert bytes to hex
    if op == 'h':
        byte_mode = False

    #convert hex to bytes
    if op == 'b':
        byte_mode = True
        
    # revert
    if op == 'r':
        output = bytes_reverse(output)
   
   # xor
    if op == 'x':
        output = bytes_xor(output)

# always print modified file
if not byte_mode:
    output = tohex(output)
for line in output:
    print(line)
