import argparse
import os

# Function to convert a string in a number
# Works with decimal base and hex base numbers
def check_number(data):
	try:
		return int(data)
	except ValueError:
		try:
			return int(data, 16)
		except:
			raise argparse.ArgumentTypeError(f"Invalid argument: {data}. Must be a valid base 10 or 16 number.")

# check if the provided argument's value for PATCH is legit
def check_patch(data):
	if data.upper() in ("NOP", "ZERO"):
		return data.upper()
	elif os.path.isfile(data):
		return data
	else:
		raise argparse.ArgumentTypeError(f"Invalid argument: {data}. Must be 'NOP', 'ZERO', or a valid file path.")

#check if OFFSET + PATCH IS 

# INPUT:
# file: the input file to be patched, read as binary
# the patch, read as binary
# the offset in the file from where to start patching
def patch(file, patch, offset):
	return file[:offset] + patch + file[offset+len(patch):]

def main():
	parser = argparse.ArgumentParser(description='SURGEON PATCHER: Find and replace bytes surgically', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('FILE', type=argparse.FileType('rb'), help="Path of the file to be patched.")
	parser.add_argument('OFFSET', type=check_number, help="Offset of the file from which to start patching.")
	parser.add_argument('PATCH', type=check_patch, help="The patch. Possible values are:\nNOP: Substitute every byte with the NOP opcode (0x90)\nZERO: Substitute every byte with the null byte (0x00)\npath: A cusutm patch file that will be read as binary and used as patch.")
	args = parser.parse_args()



	print(args.OFFSET)
if __name__ == "__main__":
	main()
