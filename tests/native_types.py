from dumpulator.native import *

def test():
    arch = Architecture(8)
    size = 4
    print(hex(~0 & 0xFFFFFFFFFFFFFFFF >> (64 - size * 8)))
    #x = ULONG(5)
    #print(x)

if __name__ == '__main__':
    test()
