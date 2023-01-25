from dumpulator import *
from dumpulator.dumpulator import *
from dumpulator.handles import *
from dumpulator.memory import *

@syscall
def ZwAllocateVirtualMemory(dp: Dumpulator,
                            ProcessHandle: HANDLE,
                            BaseAddress: P(PVOID),
                            ZeroBits: ULONG_PTR,
                            RegionSize: P(SIZE_T),
                            AllocationType: ULONG,
                            Protect: ULONG
                            ):
    assert ZeroBits == 0
    assert ProcessHandle == dp.NtCurrentProcess()
    base = dp.read_ptr(BaseAddress.ptr)
    assert base & 0xFFF == 0
    size = round_to_pages(dp.read_ptr(RegionSize.ptr))
    assert size != 0
    protect = MemoryProtect(Protect)
    if AllocationType == MEM_COMMIT:
        if base == 0:
            base = dp.memory.find_free(size)
            if protect == MemoryProtect.PAGE_EXECUTE_READWRITE:
                dp.memory.reserve(base, size, MemoryProtect.PAGE_READWRITE, info='rwx')
                print("found rwx commit")
            else:
                dp.memory.reserve(base, size, protect)
            BaseAddress.write_ptr(base)
            RegionSize.write_ptr(size)
        print(f"commit({hex(base)}[{hex(size)}], {protect})")
        if protect == MemoryProtect.PAGE_EXECUTE_READWRITE:
            dp.memory.commit(base, size, MemoryProtect.PAGE_READWRITE)
            print("found rwx commit")
        else:
            dp.memory.commit(base, size, protect)
    elif AllocationType == MEM_RESERVE:
        if base == 0:
            base = dp.memory.find_free(size)
            BaseAddress.write_ptr(base)
            RegionSize.write_ptr(size)
        print(f"reserve({hex(base)}[{hex(size)}], {protect})")
        if protect == MemoryProtect.PAGE_EXECUTE_READWRITE:
            dp.memory.reserve(base, size, MemoryProtect.PAGE_READWRITE, info='rwx')
            print("found rwx commit")
        else:
            dp.memory.reserve(base, size, protect)
    elif AllocationType == MEM_COMMIT | MEM_RESERVE:
        if base == 0:
            base = dp.memory.find_free(size)
            BaseAddress.write_ptr(base)
            RegionSize.write_ptr(size)
        print(f"reserve+commit({hex(base)}[{hex(size)}], {protect})")
        if protect == MemoryProtect.PAGE_EXECUTE_READWRITE:
            dp.memory.reserve(base, size, MemoryProtect.PAGE_READWRITE, info='rwx')
            print("found rwx commit")
        else:
            dp.memory.reserve(base, size, protect)
        dp.memory.commit(base, size)
    else:
        assert False
    return STATUS_SUCCESS

STOP_CODE = 0xDEADBEEF

def exception_hook(dp: Dumpulator, exception: ExceptionInfo):
    if exception.memory_access == MemoryException.ExecuteProtection:
        print(f'catching ExecuteProtection 0x{dp.regs.cip:x}')
        mem_region = dp.memory.find_region(dp.regs.cip)
        if mem_region.info == 'rwx':
            print(f'potential stage3 buffer {mem_region}')
            data = dp.memory.read(mem_region.start, mem_region.size)

            print(f'first bytes of region: {data[:0x20]}')
            mem_region.protect = MemoryProtect.PAGE_EXECUTE_READWRITE

            save_file = rf'E:/tmp/ramen_{mem_region.start:x}.bin'
            with open(save_file, 'wb') as f:
                f.write(data)
                print(f'Saved dump to "{save_file}"')
                return STOP_CODE


def test_bp(dp: Dumpulator, data: Breakpoint):
    print(f'we hit a bp! info: {data.info} address: {data.address:x} original: {data.original}')

dp = Dumpulator("E:/tmp/stage2.dmp", quiet=True)

dp.add_breakpoint(0x6CE352, test_bp, 'entrypoint bp')
dp.add_exception_hook(ExceptionType.Memory, exception_hook)

dp.start(dp.regs.eip, end=STOP_CODE)
