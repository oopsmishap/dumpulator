import unittest
from dumpulator.memory import *


class TestVirtualMemory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vm = VirtualMemory()

    def test_reserve(self):
        self.vm.reserve(0x7FFE0000, 0x1000)

    def test_release(self):
        self.vm.reserve(0x7FFE0000, 0x1000)
        self.vm.release(0x7FFE0000, 0x1000)


if __name__ == '__main__':
    unittest.main()
