
import math
import string
import re

traditional = [
	(1024 ** 5, 'P'),
	(1024 ** 4, 'T'),
	(1024 ** 3, 'G'),
	(1024 ** 2, 'M'),
	(1024 ** 1, 'K'),
	(1024 ** 0, 'B'),
]

alternative = [
	(1024 ** 5, ' PB'),
	(1024 ** 4, ' TB'),
	(1024 ** 3, ' GB'),
	(1024 ** 2, ' MB'),
	(1024 ** 1, ' KB'),
	(1024 ** 0, (' byte', ' bytes')),
]

verbose = [
	(1024 ** 5, (' petabyte', ' petabytes')),
	(1024 ** 4, (' terabyte', ' terabytes')),
	(1024 ** 3, (' gigabyte', ' gigabytes')),
	(1024 ** 2, (' megabyte', ' megabytes')),
	(1024 ** 1, (' kilobyte', ' kilobytes')),
	(1024 ** 0, (' byte', ' bytes')),
]

iec = [
	(1024 ** 5, 'Pi'),
	(1024 ** 4, 'Ti'),
	(1024 ** 3, 'Gi'),
	(1024 ** 2, 'Mi'),
	(1024 ** 1, 'Ki'),
	(1024 ** 0, ''),
]

si = [
	(1000 ** 5, 'P'),
	(1000 ** 4, 'T'),
	(1000 ** 3, 'G'),
	(1000 ** 2, 'M'),
	(1000 ** 1, 'K'),
	(1000 ** 0, 'B'),
]

parse_dict = {
	#(exponent, case_char, base_if_certain)
	#base doesn't matter for bytes
	'':				(0, None, 1),
	'b':			(0, None, 1),
	'byte':			(0, None, 1),
	'bytes':		(0, None, 1),

	'k':			(1, 0, None),
	'm':			(2, 0, None),
	'g':			(3, 0, None),
	't':			(4, 0, None),
	'p':			(5, 0, None),
	'e':			(6, 0, None),
	'z':			(7, 0, None),
	'y':			(8, 0, None),

	'kb':			(1, 0, None),
	'mb':			(2, 0, None),
	'gb':			(3, 0, None),
	'tb':			(4, 0, None),
	'pb':			(5, 0, None),
	'eb':			(6, 0, None),
	'zb':			(7, 0, None),
	'yb':			(8, 0, None),

	'kib':			(1, None, 1024),
	'mib':			(2, None, 1024),
	'gib':			(3, None, 1024),
	'tib':			(4, None, 1024),
	'pib':			(5, None, 1024),
	'eib':			(6, None, 1024),
	'zib':			(7, None, 1024),
	'yib':			(8, None, 1024),

	'kilobyte':		(1, None, None),
	'megabyte':		(2, None, None),
	'gigabyte':		(3, None, None),
	'terabyte':		(4, None, None),
	'petabyte':		(5, None, None),
	'exabyte':		(6, None, None),
	'zettabyte':	(7, None, None),
	'yottabyte':	(8, None, None),

	'kilobytes':	(1, None, None),
	'megabytes':	(2, None, None),
	'gigabytes':	(3, None, None),
	'terabytes':	(4, None, None),
	'petabytes':	(5, None, None),
	'exabytes':		(6, None, None),
	'zettabytes':	(7, None, None),
	'yottabytes':	(8, None, None),

	'kibibyte':		(1, None, 1024),
	'mebibyte':		(2, None, 1024),
	'gibibyte':		(3, None, 1024),
	'tebibyte':		(4, None, 1024),
	'pebibyte':		(5, None, 1024),
	'exbibyte':		(6, None, 1024),
	'zebibyte':		(7, None, 1024),
	'yobibyte':		(8, None, 1024),

	'kibibytes':	(1, None, 1024),
	'mebibytes':	(2, None, 1024),
	'gibibytes':	(3, None, 1024),
	'tebibytes':	(4, None, 1024),
	'pebibytes':	(5, None, 1024),
	'exbibytes':	(6, None, 1024),
	'zebibytes':	(7, None, 1024),
	'yobibytes':	(8, None, 1024),
}

class FileSize(int):
	'''
	Subclass of int to allow parsing & custom file size formatting.
	'''

	def __new__(cls, value, base=10, default_binary=True, case_sensitive=True):
		'''
		Parse file size, only accept ints as float has loss of precision, and using it is usually a user error.
		Otherwise allow any string int() allows.
		Upper-case is treated as binary, as this is commonly done in linux utilites (e.g. dd).
		Bits are not used in file size descriptions hence ignored.

		args:
			case_sensitive:
				use 1024 for upper case and 1000 for lower case if casing exists

			default_binary:
				default base if it is not clear what the unit is (i.e. if it is not 'mib' or 'mebibytes')
		'''
		if isinstance(value, str):
			matches = re.match(r'^(.*\d)\s*([a-zA-Z]*)$', value)
			if not matches:
				raise ValueError
			size_str, unit_str = matches.groups()
			size = int(size_str, base)
			try:
				exponent, case_char, base_if_certain = parse_dict[unit_str.lower()]
			except KeyError:
				raise ValueError
			if base_if_certain is not None:
				is_binary = base_if_certain
			elif case_sensitive and case_char is not None:
				is_binary = unit_str[case_char].isupper()
			else:
				is_binary = default_binary
			size_base = 1024 if is_binary else 1000
			size *= size_base**exponent
			return super().__new__(cls, size)
		elif isinstance(value, int):
			return super().__new__(cls, value)
		else:
			raise ValueError

	def format(self, fmt):
		'''
		format specifiers:
			s:					use largest unit possible in base 1000, e.g. 1000, s -> '1kb'
			S:					use largest unit possible in base 1024, e.g. 1024, S -> '1KiB'
			sb:					always use whatever comes after s as the unit description, in base 1000
			S{b|ib}:			always use whatever comes after s as the unit description, in base 1024
			s[kmgtpezy]:		use the specified unit in base 1000
			S[kmgtpezy]:		use the specified unit in base 1024
			s[kmgtpezy]b:		always use whatever comes after s as the unit description, in base 1000
			S[kmgtpezy]{b|ib}:	always use whatever comes after s as the unit description, in base 1024
		'''
		# is it an empty format or not a special format for the size class
		if fmt == "" or fmt[-2:].lower() not in ["em","sm","cm"]:
			if fmt[-1].lower() in ['b','c','d','o','x','n','e','f','g','%']:
				# Numeric format.
				return int(self).__format__(fmt)
			else:
				return str(self).__format__(fmt)

		# work out the scale, suffix and base
		factor, suffix = (8, "b") if fmt[-1] in string.ascii_lowercase else (1,"B")
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
