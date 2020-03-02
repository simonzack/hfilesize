import unittest

from hfilesize import FileSize, Format


class TestHFileSize(unittest.TestCase):
    def test_parse(self):
        # basic tests on integers with no units
        self.assertEqual(FileSize(1), 1)
        self.assertEqual(FileSize('1'), 1)
        self.assertEqual(FileSize('-1'), -1)

        # int base
        self.assertEqual(FileSize('0x12', 16), 0x12)

        # case sensitive
        self.assertEqual(FileSize('1k'), 1000)
        self.assertEqual(FileSize('1K'), 1024)
        self.assertEqual(FileSize('1kib'), 1024)
        self.assertEqual(FileSize('1kIB'), 1024)
        self.assertEqual(FileSize('1kb'), 1000)
        self.assertEqual(FileSize('1kB'), 1000)
        self.assertEqual(FileSize('1Kb'), 1024)
        self.assertEqual(FileSize('1KB'), 1024)

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

        # case insensitive
        self.assertEqual(FileSize('1K', default_binary=False, case_sensitive=False), 1000**1)
        self.assertEqual(FileSize('1K', default_binary=True, case_sensitive=False), 1024**1)

        # spacing
        self.assertEqual(FileSize('1 k'), 1000)

        # invalid values
        with self.assertRaises(ValueError):
            FileSize(1.1)
        with self.assertRaises(ValueError):
            FileSize('1.1')
        with self.assertRaises(ValueError):
            FileSize('1kibb')

    def test_format(self):
        # base guessing
        self.assertEqual(FileSize(1024).format(size_fmt=Format.casing), '1 KB')
        with self.assertRaises(ValueError):
            self.assertEqual(FileSize(1024).format(size_fmt=Format.si), '1 KB')

        # plural
        self.assertEqual(FileSize(0).format(base=1024, size_fmt=Format.casing), '0 bytes')
        self.assertEqual(FileSize(1).format(base=1024, size_fmt=Format.casing), '1 byte')
        self.assertEqual(FileSize(2).format(base=1024, size_fmt=Format.casing), '2 bytes')
        self.assertEqual(FileSize(1024).format(base=1024, size_fmt=Format.casing_verbose), '1 kilobyte')
        self.assertEqual(FileSize(1025).format(base=1024, size_fmt=Format.casing_verbose), '1.00 kilobytes')
        self.assertEqual(FileSize(2048).format(base=1024, size_fmt=Format.casing_verbose), '2 kilobytes')

        # float formatting
        self.assertEqual(FileSize(1024).format(base=1024, size_fmt=Format.casing), '1 KB')
        self.assertEqual(FileSize(1025).format(base=1024, size_fmt=Format.casing), '1.00 KB')
        self.assertEqual(FileSize(2048).format(base=1024, size_fmt=Format.casing), '2 KB')

        # exponent
        self.assertEqual(FileSize(1024).format(base=1024, size_fmt=Format.casing, exponent=0), '1024 bytes')

        # exponent bounds check
        with self.assertRaises(ValueError):
            FileSize(1024).format(base=1024, size_fmt=Format.casing, exponent=100)
        with self.assertRaises(ValueError):
            FileSize(1024).format(base=1024, size_fmt=Format.casing, exponent=-1)

    def test_str_format(self):
        self.assertEqual('{:d}'.format(FileSize(1024)), '1024')
        self.assertEqual('{:.02fH}'.format(FileSize(1024)), '1 KB')
        self.assertEqual('{:.02fhs}'.format(FileSize(1000)), '1 KB')
        self.assertEqual('{:.02fhs^0}'.format(FileSize(1000)), '1000 B')
        self.assertEqual('{:.02fHcv}'.format(FileSize(1024)), '1 kilobyte')
        self.assertEqual('{: >10.02fH}'.format(FileSize(1024)), '1 KB'.rjust(10))
