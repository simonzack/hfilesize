
import math
import string
import re

class Format:
	# We do not provide a lower case 1024 format to minimize ambiguity.
	casing = [
		(1, (' byte', ' bytes')),

		(1024 ** 1, ' KB'),
		(1024 ** 2, ' MB'),
		(1024 ** 3, ' GB'),
		(1024 ** 4, ' TB'),
		(1024 ** 5, ' PB'),
		(1024 ** 6, ' EB'),
		(1024 ** 7, ' ZB'),
		(1024 ** 8, ' YB'),

		(1000 ** 1, ' kb'),
		(1000 ** 2, ' mb'),
		(1000 ** 3, ' gb'),
		(1000 ** 4, ' tb'),
		(1000 ** 5, ' pb'),
		(1000 ** 6, ' eb'),
		(1000 ** 7, ' zb'),
		(1000 ** 8, ' yb'),
	]

	casing_short = [
		(1, ''),

		(1024 ** 1, 'K'),
		(1024 ** 2, 'M'),
		(1024 ** 3, 'G'),
		(1024 ** 4, 'T'),
		(1024 ** 5, 'P'),
		(1024 ** 6, 'E'),
		(1024 ** 7, 'Z'),
		(1024 ** 8, 'Y'),

		(1000 ** 1, ' kb'),
		(1000 ** 2, ' mb'),
		(1000 ** 3, ' gb'),
		(1000 ** 4, ' tb'),
		(1000 ** 5, ' pb'),
		(1000 ** 6, ' eb'),
		(1000 ** 7, ' zb'),
		(1000 ** 8, ' yb'),
	]

	casing_verbose = [
		(1024 ** 0, (' byte', ' bytes')),
		(1024 ** 1, (' kilobyte', ' kilobytes')),
		(1024 ** 2, (' megabyte', ' megabytes')),
		(1024 ** 3, (' gigabyte', ' gigabytes')),
		(1024 ** 4, (' terabyte', ' terabytes')),
		(1024 ** 5, (' petabyte', ' petabytes')),
		(1024 ** 6, (' exabyte', ' exabytes')),
		(1024 ** 7, (' zettabyte', ' zettabytes')),
		(1024 ** 8, (' yottabyte', ' yottabytes')),
	]

	iec = [
		(1024 ** 0, ''),
		(1024 ** 1, 'KiB'),
		(1024 ** 2, 'MiB'),
		(1024 ** 3, 'GiB'),
		(1024 ** 4, 'TiB'),
		(1024 ** 5, 'PiB'),
		(1024 ** 6, 'EiB'),
		(1024 ** 7, 'ZiB'),
		(1024 ** 8, 'YiB'),
	]

	iec_verbose = [
		(1024 ** 0, (' byte', ' bytes')),
		(1024 ** 1, (' kibibyte', 'kibibytes')),
		(1024 ** 2, (' mebibyte', 'mebibytes')),
		(1024 ** 3, (' gibibyte', 'gibibytes')),
		(1024 ** 4, (' tebibyte', 'tebibytes')),
		(1024 ** 5, (' pebibyte', 'pebibytes')),
		(1024 ** 6, (' exbibyte', 'exbibytes')),
		(1024 ** 7, (' zebibyte', 'zebibytes')),
		(1024 ** 8, (' yobibyte', 'yobibytes')),
	]

	si = [
		(1000 ** 0, 'B'),
		(1000 ** 1, 'KB'),
		(1000 ** 2, 'MB'),
		(1000 ** 3, 'GB'),
		(1000 ** 4, 'TB'),
		(1000 ** 5, 'PB'),
		(1000 ** 6, 'EB'),
		(1000 ** 7, 'ZB'),
		(1000 ** 8, 'YB'),
	]

	si_verbose = [
		(1000 ** 0, (' byte', ' bytes')),
		(1000 ** 1, (' kilobyte', ' kilobytes')),
		(1000 ** 2, (' megabyte', ' megabytes')),
		(1000 ** 3, (' gigabyte', ' gigabytes')),
		(1000 ** 4, (' terabyte', ' terabytes')),
		(1000 ** 5, (' petabyte', ' petabytes')),
		(1000 ** 6, (' exabyte', ' exabytes')),
		(1000 ** 7, (' zettabyte', ' zettabytes')),
		(1000 ** 8, (' yottabyte', ' yottabytes')),
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

	def format(self, float_fmt, date_fmt=Format.casing, exponent=None):
		if exponent is None:
			exponent =

		pass

	def __format__(self, fmt):
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
