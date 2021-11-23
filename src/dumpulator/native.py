import struct
from enum import Enum, IntFlag
from typing import Optional
import ctypes


def make_global(t):
    globals().update(t.__members__)


class Architecture:
    def __init__(self, pointer_size):
        self.pointer_size = pointer_size

class Int:
    size = 0

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"0x{self:X}"

class ULONG(Int):
    size = 4

    def __init__(self, value):
        super().__init__(value & 0xFFFFFFFF)


class USHORT(Int):
    size = 2

    def __init__(self, value):
        super().__init__(value & 0xFFFF)

class HANDLE(Int):
    size = -1
    pass

class SIZE_T(Int):
    size = -1
    pass


class ULONG_PTR(Int):
    size = -1


class PVOID:
    def __init__(self, ptr, mem_read):
        self.ptr = ptr
        self.type: Optional[type] = None
        self.read = lambda size: mem_read(ptr, size)

    def __getitem__(self, index):
        return struct.unpack("<Q", self.read(8))

    def __int__(self):
        return self.ptr

    def __eq__(self, other):
        return self.ptr == other

    def __ne__(self, other):
        return self.ptr != other

    def __str__(self):
        return f"0x{self:X}"

    def read_str(self, size, encoding="utf8"):
        return self.read(size).decode(encoding)


def P(t):
    class P(PVOID):
        def __init__(self, ptr, mem_read):
            super().__init__(ptr, mem_read)
            self.type = t
    return P


class Structure:
    _pack_ = 1
    _fields_ = []

class UNICODE_STRING(Structure):
    _pack_ = 1
    _fields_ = [
        ("Length", )
    ]


"""
class UNICODE_STRING(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("Length", ctypes.c_ushort),
        ("MaximumLength", ctypes.c_ushort),
        ("Buffer", ctypes.c_void_p)
    ]
"""


STATUS_SUCCESS = 0
STATUS_NOT_IMPLEMENTED = 0xC0000002

class MEMORY_INFORMATION_CLASS(Enum):
    MemoryBasicInformation = 0
    MemoryWorkingSetInformation = 1
    MemoryMappedFilenameInformation = 2
    MemoryRegionInformation = 3
    MemoryWorkingSetExInformation = 4
    MemorySharedCommitInformation = 5
    MemoryImageInformation = 6
    MemoryRegionInformationEx = 7
make_global(MEMORY_INFORMATION_CLASS)

class THREADINFOCLASS(Enum):
    ThreadBasicInformation = 0
    ThreadTimes = 1
    ThreadPriority = 2
    ThreadBasePriority = 3
    ThreadAffinityMask = 4
    ThreadImpersonationToken = 5
    ThreadDescriptorTableEntry = 6
    ThreadEnableAlignmentFaultFixup = 7
    ThreadEventPair = 8
    ThreadQuerySetWin32StartAddress = 9
    ThreadZeroTlsCell = 10
    ThreadPerformanceCount = 11
    ThreadAmILastThread = 12
    ThreadIdealProcessor = 13
    ThreadPriorityBoost = 14
    ThreadSetTlsArrayAddress = 15
    ThreadIsIoPending = 16
    ThreadHideFromDebugger = 17
    ThreadBreakOnTermination = 18
    ThreadSwitchLegacyState = 19
    ThreadIsTerminated = 20
    ThreadLastSystemCall = 21
    ThreadIoPriority = 22
    ThreadCycleTime = 23
    ThreadPagePriority = 24
    ThreadActualBasePriority = 25
    ThreadTebInformation = 26
    ThreadCSwitchMon = 27
    ThreadCSwitchPmu = 28
    ThreadWow64Context = 29
    ThreadGroupInformation = 30
    ThreadUmsInformation = 31
    ThreadCounterProfiling = 32
    ThreadIdealProcessorEx = 33
    ThreadCpuAccountingInformation = 34
    ThreadSuspendCount = 35
    ThreadHeterogeneousCpuPolicy = 36
    ThreadContainerId = 37
    ThreadNameInformation = 38
    ThreadSelectedCpuSets = 39
    ThreadSystemThreadInformation = 40
    ThreadActualGroupAffinity = 41
    ThreadDynamicCodePolicyInfo = 42
    ThreadExplicitCaseSensitivity = 43
    ThreadWorkOnBehalfTicket = 44
    ThreadSubsystemInformation = 45
    ThreadDbgkWerReportActive = 46
    ThreadAttachContainer = 47
make_global(THREADINFOCLASS)

class FS_INFORMATION_CLASS(Enum):
    FileFsVolumeInformation = 1
    FileFsLabelInformation = 2
    FileFsSizeInformation = 3
    FileFsDeviceInformation = 4
    FileFsAttributeInformation = 5
    FileFsControlInformation = 6
    FileFsFullSizeInformation = 7
    FileFsObjectIdInformation = 8
    FileFsDriverPathInformation = 9
    FileFsVolumeFlagsInformation = 10
    FileFsSectorSizeInformation = 11
    FileFsDataCopyInformation = 12
    FileFsMetadataSizeInformation = 13
make_global(FS_INFORMATION_CLASS)


MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PAGE_READWRITE = 0x4

class ACCESS_MASK(ULONG):
    pass

class OBJECT_ATTRIBUTES(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("Length", ctypes.c_ulong),
        ("RootDirectory", ctypes.c_ulong),
        ("ObjectName", ctypes.c_ulong),
        ("Attributes", ctypes.c_ulong),
        ("SecurityDescriptor", ctypes.c_ulong),
        ("SecurityQualityOfService", ctypes.c_ulong)
    ]

class IO_APC_ROUTINE:
    pass


class IO_STATUS_BLOCK:
    pass


class LARGE_INTEGER:
    pass
