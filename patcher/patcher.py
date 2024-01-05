import argparse
import os

# Script that patches a binary file provided.
# It does provide NOP and ZERO out-of-the-box patches but it's possible
# to also inject via file your custum one.
# superuser

# Function to convert a string in a number
# Works with decimal base and hex base numbers
def check_number(data):
	try:
		return int(data)
	except:
		try:
			return int(data, 16)
		except:
			print(f"Invalid argument: {data}. Must be a valid base 10 or 16 number.")
			exit(-1)

# check if the provided argument's value for PATCH is legit
class Check_Patch(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		result = []
		if values[0].upper() in ("NOP", "ZERO"):
			if not len(values) == 2:
				print("With NOP and ZERO you must provide also a LEN value.")
				exit(-1)
			result.append(values[0].upper())
			result.append(check_number(values[1]))
		elif os.path.isfile(values[0]):
			result.append("FILE")
			result.append(values[0])
		else:
			print(f"Invalid argument: {values}. Must be 'NOP', 'ZERO', or a valid file path.")
			exit(-1)
		setattr(namespace, self.dest, result)

def check_lengths(in_length, offset, out_length):
	if offset + out_length > in_length:
		print("Invalid OFFSET + LEN: patch length exceeds input file.")
		exit(-1)

# INPUT:
# file: the input file to be patched, read as binary
# the patch, read as binary
# the offset in the file from where to start patching
def patch(in_file, offset, patch_data):
	return in_file[:offset] + patch_data + in_file[offset+len(patch_data):]

def main():
	parser = argparse.ArgumentParser(	description='PATCHER: Find and replace bytes',
										formatter_class=argparse.RawTextHelpFormatter,
										usage="patcher [-h, --help] [-o, --output] FILE OFFSET PATCH {LEN}")
	parser.add_argument('FILE', type=argparse.FileType('rb'), help="Path of the file to be patched.")
	parser.add_argument('OFFSET', type=check_number, help="Offset of the file from which to start patching.")
	parser.add_argument('PATCH', nargs="+", action=Check_Patch, help="The patch. Possible values are:\nNOP: Substitute every byte with the NOP opcode (0x90) for LEN bytes\nZERO: Substitute every byte with the null byte (0x00) for LEN bytes\npath: A cusutm patch file that will be read as binary and used as patch.")
	parser.add_argument("-o", "--output", type=str, help="patched output file path. DEFUALT is FILE_patched.")
	args = parser.parse_args()


	# reading in_file to be patched as binary file
	in_file = args.FILE.read()
	
	#building or reading patch
	if args.PATCH[0] == "NOP":
		patch_data = bytes([0x90] * args.PATCH[1])
	elif args.PATCH[0] == "ZERO":
		patch_data = bytes([0x00] * args.PATCH[1])
	else:
		with open(args.PATCH[1], "rb") as f:
			patch_data = f.read()
	check_lengths(len(in_file), args.OFFSET, len(patch_data))
	
	#creating output file
	if args.output is not None:
		out_file_path = args.output
	else:
		out_file_path = args.FILE.name+"_patched"
	out_file = open(out_file_path, "wb")

	#writing patched file
	out_file.write(patch(in_file, args.OFFSET, patch_data))

if __name__ == "__main__":
	main()
