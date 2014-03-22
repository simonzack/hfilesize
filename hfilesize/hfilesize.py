
import math
import string
import re

class FileSize(int):
	'''
	Subclass of int to allow parsing & custom file size formatting.
	'''

	def __new__(cls, value, base=10):
		'''
		Parse file size, only accept ints as float has loss of precision, and using it is usually a user error.
		Otherwise allow any string int() allows.
		Upper-case is treated as binary, as this is commonly done in linux utilites (e.g. dd).
		'''
		if isinstance(value, str):
			matches = re.match(r'^(.*\d)\s*([a-zA-Z]*)$', value)
			if not matches:
				raise ValueError
			size_str, unit_str = matches.groups()
			size = int(size_str, base)
			if unit_str:
				exponent_str, unit_str = unit_str[0], unit_str[1:]
				exponent = 'kmgtpezy'.find(exponent_str.lower())
				if exponent == -1:
					raise ValueError
				if not unit_str or unit_str.lower()=='b':
					is_binary = exponent_str.isupper()
				elif unit_str.lower()=='ib':
					is_binary = True
				else:
					raise ValueError
				unit = 1024 if is_binary else 1000
				size *= unit**(exponent+1)
			return int(size)
		elif isinstance(value, int):
			return int(value)
		else:
			raise ValueError

	def __format__(self, fmt):
		'''
		format specifiers:
			em : formats the size as bits in IEC format i.e. 1024 bits (128 bytes) = 1Kib
			eM : formats the size as Bytes in IEC format i.e. 1024 bytes = 1KiB
			sm : formats the size as bits in SI format i.e. 1000 bits = 1kb
			sM : formats the size as bytes in SI format i.e. 1000 bytes = 1KB
			cm : format the size as bit in the common format i.e. 1024 bits (128 bytes) = 1Kb
			cM : format the size as bytes in the common format i.e. 1024 bytes = 1KB
		'''
		# is it an empty format or not a special format for the size class
		if fmt == "" or fmt[-2:].lower() not in ["em","sm","cm"]:
			if fmt[-1].lower() in ['b','c','d','o','x','n','e','f','g','%']:
				# Numeric format.
				return long(self).__format__(fmt)
			else:
				return str(self).__format__(fmt)

		# work out the scale, suffix and base
		factor, suffix = (8, "b") if fmt[-1] in string.lowercase else (1,"B")
		base = 1024 if fmt[-2] in ["e","c"] else 1000

		# Add the i for the IEC format
		suffix = "i"+ suffix if fmt[-2] == "e" else suffix

		mult = ["","K","M","G","T","P"]

		val = float(self) * factor
		i = 0 if val < 1 else int(math.log(val, base))+1
		v = val / math.pow(base,i)
		v,i = (v,i) if v > 0.5 else (v*base,i-1)

		# Identify if there is a width and extract it
		width = "" if fmt.find(".") == -1 else fmt[:fmt.index(".")]
		precis = fmt[:-2] if width == "" else fmt[fmt.index("."):-2]

		# do the precision bit first, so width/alignment works with the suffix
		t = ("{0:{1}f}"+mult[i]+suffix).format(v, precis)

		return "{0:{1}}".format(t,width) if width != "" else t
