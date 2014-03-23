
import unittest
from hfilesize import FileSize

class TestHFileSize(unittest.TestCase):
	def test_parse(self):
		self.assertEqual(FileSize(1), 1)
		self.assertEqual(FileSize('1'), 1)
		self.assertEqual(FileSize('-1'), -1)
		self.assertEqual(FileSize('0x12', 16), 0x12)

		self.assertEqual(FileSize('1k'), 1000)
		self.assertEqual(FileSize('1K'), 1024)
		self.assertEqual(FileSize('1kib'), 1024)
		self.assertEqual(FileSize('1kIB'), 1024)
		self.assertEqual(FileSize('1kb'), 1000)
		self.assertEqual(FileSize('1kB'), 1000)
		self.assertEqual(FileSize('1Kb'), 1024)
		self.assertEqual(FileSize('1KB'), 1024)
		self.assertEqual(FileSize('1 k'), 1000)

		self.assertEqual(FileSize('1k'), 1000**1)
		self.assertEqual(FileSize('1m'), 1000**2)
		self.assertEqual(FileSize('1g'), 1000**3)
		self.assertEqual(FileSize('1t'), 1000**4)
		self.assertEqual(FileSize('1p'), 1000**5)
		self.assertEqual(FileSize('1e'), 1000**6)
		self.assertEqual(FileSize('1z'), 1000**7)
		self.assertEqual(FileSize('1y'), 1000**8)
		self.assertEqual(FileSize('1K'), 1024**1)
		self.assertEqual(FileSize('1M'), 1024**2)
		self.assertEqual(FileSize('1G'), 1024**3)
		self.assertEqual(FileSize('1T'), 1024**4)
		self.assertEqual(FileSize('1P'), 1024**5)
		self.assertEqual(FileSize('1E'), 1024**6)
		self.assertEqual(FileSize('1Z'), 1024**7)
		self.assertEqual(FileSize('1Y'), 1024**8)

		with self.assertRaises(ValueError):
			FileSize(1.1)
		with self.assertRaises(ValueError):
			FileSize('1.1')
		with self.assertRaises(ValueError):
			FileSize('1kibb')

	def test_format(self):
		pass
		#print('{:.2}'.format(FileSize(1)))
