from dumpulator.native import *
from enum import IntEnum
from unicorn import *
from unicorn.unicorn_const import *
from typing import Callable


class Breakpoint:
    def __init__(self, address: int, callback: Callable, info: any):
        self.address = address
        self.original: Optional[bytes] = None
        self.callback = callback
        self.info = info


class ExceptionInfo:
    def __init__(self):
        self.type: ExceptionType = ExceptionType.NoException
        self.code: Exceptions = Exceptions.NoException
        self.memory_address = 0
        self.memory_size = 0
        self.memory_value = 0
        self.interrupt_number = 0
        self.code_hook_h: Optional[int] = None  # TODO: should be unicorn.uc_hook_h, but type error
        self.context: Optional[unicorn.UcContext] = None
        self.tb_start = 0
        self.tb_size = 0
        self.tb_icount = 0
        self.step_count = 0
        self.final = False
        self.handling = False

    def __str__(self):
        return f"{self.code:x}, ({hex(self.tb_start)}, {hex(self.tb_size)}, {self.tb_icount})"


class ExceptionType(IntEnum):
    NoException = 0x0000
    Memory = 0x1000
    Interrupt = 0x2000
    ContextSwitch = 0x4000
    Error = 0x8000


class MemoryFlags(IntEnum):
    Read = 0x10
    Write = 0x20
    Execute = 0x40
    Unmapped = 0x100
    Unaligned = 0x200
    Protection = 0x400
    After = 0x800


# TODO: could be Flag instead of IntEnum and combine with ExceptionType to have 1 Enum Flag
class Exceptions(IntEnum):
    # No Exception
    NoException = ExceptionType.NoException
    Memory = ExceptionType.Memory
    Interrupt = ExceptionType.Interrupt
    ContextSwitch = ExceptionType.ContextSwitch
    Error = ExceptionType.Error

    # Memory Exceptions
    MemRead = ExceptionType.Memory | MemoryFlags.Read
    MemWrite = ExceptionType.Memory | MemoryFlags.Write
    MemExecute = ExceptionType.Memory | MemoryFlags.Execute
    MemReadUnmapped = ExceptionType.Memory | MemoryFlags.Read | MemoryFlags.Unmapped
    MemWriteUnmapped = ExceptionType.Memory | MemoryFlags.Write | MemoryFlags.Unmapped
    MemExecuteUnmapped = ExceptionType.Memory | MemoryFlags.Execute | MemoryFlags.Unmapped
    MemReadProt = ExceptionType.Memory | MemoryFlags.Read | MemoryFlags.Protection
    MemWriteProt = ExceptionType.Memory | MemoryFlags.Write | MemoryFlags.Protection
    MemExecuteProt = ExceptionType.Memory | MemoryFlags.Execute | MemoryFlags.Protection
    MemReadAfter = ExceptionType.Memory | MemoryFlags.Execute | MemoryFlags.After

    # Interrupts
    Interrupt_1 = ExceptionType.Interrupt | 1
    Interrupt_2 = ExceptionType.Interrupt | 2
    Interrupt_3 = ExceptionType.Interrupt | 3
    Interrupt_4 = ExceptionType.Interrupt | 4
    Interrupt_5 = ExceptionType.Interrupt | 5
    Interrupt_6 = ExceptionType.Interrupt | 6
    Interrupt_7 = ExceptionType.Interrupt | 7
    Interrupt_8 = ExceptionType.Interrupt | 8
    Interrupt_9 = ExceptionType.Interrupt | 9
    Interrupt_A = ExceptionType.Interrupt | 10
    Interrupt_B = ExceptionType.Interrupt | 11
    Interrupt_C = ExceptionType.Interrupt | 12
    Interrupt_D = ExceptionType.Interrupt | 13
    Interrupt_E = ExceptionType.Interrupt | 14
    Interrupt_F = ExceptionType.Interrupt | 15
    Interrupt_10 = ExceptionType.Interrupt | 16
    Interrupt_11 = ExceptionType.Interrupt | 17
    Interrupt_12 = ExceptionType.Interrupt | 18
    Interrupt_13 = ExceptionType.Interrupt | 19
    Interrupt_14 = ExceptionType.Interrupt | 20
    Interrupt_15 = ExceptionType.Interrupt | 21
    Interrupt_16 = ExceptionType.Interrupt | 22
    Interrupt_17 = ExceptionType.Interrupt | 23
    Interrupt_18 = ExceptionType.Interrupt | 24
    Interrupt_19 = ExceptionType.Interrupt | 25
    Interrupt_1A = ExceptionType.Interrupt | 26
    Interrupt_1B = ExceptionType.Interrupt | 27
    Interrupt_1C = ExceptionType.Interrupt | 28
    Interrupt_1D = ExceptionType.Interrupt | 29
    Interrupt_1E = ExceptionType.Interrupt | 30
    Interrupt_1F = ExceptionType.Interrupt | 31
    Interrupt_20 = ExceptionType.Interrupt | 32
    Interrupt_21 = ExceptionType.Interrupt | 33
    Interrupt_22 = ExceptionType.Interrupt | 34
    Interrupt_23 = ExceptionType.Interrupt | 35
    Interrupt_24 = ExceptionType.Interrupt | 36
    Interrupt_25 = ExceptionType.Interrupt | 37
    Interrupt_26 = ExceptionType.Interrupt | 38
    Interrupt_27 = ExceptionType.Interrupt | 39
    Interrupt_28 = ExceptionType.Interrupt | 40
    Interrupt_29 = ExceptionType.Interrupt | 41
    Interrupt_2A = ExceptionType.Interrupt | 42
    Interrupt_2B = ExceptionType.Interrupt | 43
    Interrupt_2C = ExceptionType.Interrupt | 44
    Interrupt_2D = ExceptionType.Interrupt | 45
    Interrupt_2E = ExceptionType.Interrupt | 46
    Interrupt_2F = ExceptionType.Interrupt | 47
    Interrupt_30 = ExceptionType.Interrupt | 48
    Interrupt_31 = ExceptionType.Interrupt | 49
    Interrupt_32 = ExceptionType.Interrupt | 50
    Interrupt_33 = ExceptionType.Interrupt | 51
    Interrupt_34 = ExceptionType.Interrupt | 52
    Interrupt_35 = ExceptionType.Interrupt | 53
    Interrupt_36 = ExceptionType.Interrupt | 54
    Interrupt_37 = ExceptionType.Interrupt | 55
    Interrupt_38 = ExceptionType.Interrupt | 56
    Interrupt_39 = ExceptionType.Interrupt | 57
    Interrupt_3A = ExceptionType.Interrupt | 58
    Interrupt_3B = ExceptionType.Interrupt | 59
    Interrupt_3C = ExceptionType.Interrupt | 60
    Interrupt_3D = ExceptionType.Interrupt | 61
    Interrupt_3E = ExceptionType.Interrupt | 62
    Interrupt_3F = ExceptionType.Interrupt | 63
    Interrupt_40 = ExceptionType.Interrupt | 64
    Interrupt_41 = ExceptionType.Interrupt | 65
    Interrupt_42 = ExceptionType.Interrupt | 66
    Interrupt_43 = ExceptionType.Interrupt | 67
    Interrupt_44 = ExceptionType.Interrupt | 68
    Interrupt_45 = ExceptionType.Interrupt | 69
    Interrupt_46 = ExceptionType.Interrupt | 70
    Interrupt_47 = ExceptionType.Interrupt | 71
    Interrupt_48 = ExceptionType.Interrupt | 72
    Interrupt_49 = ExceptionType.Interrupt | 73
    Interrupt_4A = ExceptionType.Interrupt | 74
    Interrupt_4B = ExceptionType.Interrupt | 75
    Interrupt_4C = ExceptionType.Interrupt | 76
    Interrupt_4D = ExceptionType.Interrupt | 77
    Interrupt_4E = ExceptionType.Interrupt | 78
    Interrupt_4F = ExceptionType.Interrupt | 79
    Interrupt_50 = ExceptionType.Interrupt | 80
    Interrupt_51 = ExceptionType.Interrupt | 81
    Interrupt_52 = ExceptionType.Interrupt | 82
    Interrupt_53 = ExceptionType.Interrupt | 83
    Interrupt_54 = ExceptionType.Interrupt | 84
    Interrupt_55 = ExceptionType.Interrupt | 85
    Interrupt_56 = ExceptionType.Interrupt | 86
    Interrupt_57 = ExceptionType.Interrupt | 87
    Interrupt_58 = ExceptionType.Interrupt | 88
    Interrupt_59 = ExceptionType.Interrupt | 89
    Interrupt_5A = ExceptionType.Interrupt | 90
    Interrupt_5B = ExceptionType.Interrupt | 91
    Interrupt_5C = ExceptionType.Interrupt | 92
    Interrupt_5D = ExceptionType.Interrupt | 93
    Interrupt_5E = ExceptionType.Interrupt | 94
    Interrupt_5F = ExceptionType.Interrupt | 95
    Interrupt_60 = ExceptionType.Interrupt | 96
    Interrupt_61 = ExceptionType.Interrupt | 97
    Interrupt_62 = ExceptionType.Interrupt | 98
    Interrupt_63 = ExceptionType.Interrupt | 99
    Interrupt_64 = ExceptionType.Interrupt | 100
    Interrupt_65 = ExceptionType.Interrupt | 101
    Interrupt_66 = ExceptionType.Interrupt | 102
    Interrupt_67 = ExceptionType.Interrupt | 103
    Interrupt_68 = ExceptionType.Interrupt | 104
    Interrupt_69 = ExceptionType.Interrupt | 105
    Interrupt_6A = ExceptionType.Interrupt | 106
    Interrupt_6B = ExceptionType.Interrupt | 107
    Interrupt_6C = ExceptionType.Interrupt | 108
    Interrupt_6D = ExceptionType.Interrupt | 109
    Interrupt_6E = ExceptionType.Interrupt | 110
    Interrupt_6F = ExceptionType.Interrupt | 111
    Interrupt_70 = ExceptionType.Interrupt | 112
    Interrupt_71 = ExceptionType.Interrupt | 113
    Interrupt_72 = ExceptionType.Interrupt | 114
    Interrupt_73 = ExceptionType.Interrupt | 115
    Interrupt_74 = ExceptionType.Interrupt | 116
    Interrupt_75 = ExceptionType.Interrupt | 117
    Interrupt_76 = ExceptionType.Interrupt | 118
    Interrupt_77 = ExceptionType.Interrupt | 119
    Interrupt_78 = ExceptionType.Interrupt | 120
    Interrupt_79 = ExceptionType.Interrupt | 121
    Interrupt_7A = ExceptionType.Interrupt | 122
    Interrupt_7B = ExceptionType.Interrupt | 123
    Interrupt_7C = ExceptionType.Interrupt | 124
    Interrupt_7D = ExceptionType.Interrupt | 125
    Interrupt_7E = ExceptionType.Interrupt | 126
    Interrupt_7F = ExceptionType.Interrupt | 127
    Interrupt_80 = ExceptionType.Interrupt | 128
    Interrupt_81 = ExceptionType.Interrupt | 129
    Interrupt_82 = ExceptionType.Interrupt | 130
    Interrupt_83 = ExceptionType.Interrupt | 131
    Interrupt_84 = ExceptionType.Interrupt | 132
    Interrupt_85 = ExceptionType.Interrupt | 133
    Interrupt_86 = ExceptionType.Interrupt | 134
    Interrupt_87 = ExceptionType.Interrupt | 135
    Interrupt_88 = ExceptionType.Interrupt | 136
    Interrupt_89 = ExceptionType.Interrupt | 137
    Interrupt_8A = ExceptionType.Interrupt | 138
    Interrupt_8B = ExceptionType.Interrupt | 139
    Interrupt_8C = ExceptionType.Interrupt | 140
    Interrupt_8D = ExceptionType.Interrupt | 141
    Interrupt_8E = ExceptionType.Interrupt | 142
    Interrupt_8F = ExceptionType.Interrupt | 143
    Interrupt_90 = ExceptionType.Interrupt | 144
    Interrupt_91 = ExceptionType.Interrupt | 145
    Interrupt_92 = ExceptionType.Interrupt | 146
    Interrupt_93 = ExceptionType.Interrupt | 147
    Interrupt_94 = ExceptionType.Interrupt | 148
    Interrupt_95 = ExceptionType.Interrupt | 149
    Interrupt_96 = ExceptionType.Interrupt | 150
    Interrupt_97 = ExceptionType.Interrupt | 151
    Interrupt_98 = ExceptionType.Interrupt | 152
    Interrupt_99 = ExceptionType.Interrupt | 153
    Interrupt_9A = ExceptionType.Interrupt | 154
    Interrupt_9B = ExceptionType.Interrupt | 155
    Interrupt_9C = ExceptionType.Interrupt | 156
    Interrupt_9D = ExceptionType.Interrupt | 157
    Interrupt_9E = ExceptionType.Interrupt | 158
    Interrupt_9F = ExceptionType.Interrupt | 159
    Interrupt_A0 = ExceptionType.Interrupt | 160
    Interrupt_A1 = ExceptionType.Interrupt | 161
    Interrupt_A2 = ExceptionType.Interrupt | 162
    Interrupt_A3 = ExceptionType.Interrupt | 163
    Interrupt_A4 = ExceptionType.Interrupt | 164
    Interrupt_A5 = ExceptionType.Interrupt | 165
    Interrupt_A6 = ExceptionType.Interrupt | 166
    Interrupt_A7 = ExceptionType.Interrupt | 167
    Interrupt_A8 = ExceptionType.Interrupt | 168
    Interrupt_A9 = ExceptionType.Interrupt | 169
    Interrupt_AA = ExceptionType.Interrupt | 170
    Interrupt_AB = ExceptionType.Interrupt | 171
    Interrupt_AC = ExceptionType.Interrupt | 172
    Interrupt_AD = ExceptionType.Interrupt | 173
    Interrupt_AE = ExceptionType.Interrupt | 174
    Interrupt_AF = ExceptionType.Interrupt | 175
    Interrupt_B0 = ExceptionType.Interrupt | 176
    Interrupt_B1 = ExceptionType.Interrupt | 177
    Interrupt_B2 = ExceptionType.Interrupt | 178
    Interrupt_B3 = ExceptionType.Interrupt | 179
    Interrupt_B4 = ExceptionType.Interrupt | 180
    Interrupt_B5 = ExceptionType.Interrupt | 181
    Interrupt_B6 = ExceptionType.Interrupt | 182
    Interrupt_B7 = ExceptionType.Interrupt | 183
    Interrupt_B8 = ExceptionType.Interrupt | 184
    Interrupt_B9 = ExceptionType.Interrupt | 185
    Interrupt_BA = ExceptionType.Interrupt | 186
    Interrupt_BB = ExceptionType.Interrupt | 187
    Interrupt_BC = ExceptionType.Interrupt | 188
    Interrupt_BD = ExceptionType.Interrupt | 189
    Interrupt_BE = ExceptionType.Interrupt | 190
    Interrupt_BF = ExceptionType.Interrupt | 191
    Interrupt_C0 = ExceptionType.Interrupt | 192
    Interrupt_C1 = ExceptionType.Interrupt | 193
    Interrupt_C2 = ExceptionType.Interrupt | 194
    Interrupt_C3 = ExceptionType.Interrupt | 195
    Interrupt_C4 = ExceptionType.Interrupt | 196
    Interrupt_C5 = ExceptionType.Interrupt | 197
    Interrupt_C6 = ExceptionType.Interrupt | 198
    Interrupt_C7 = ExceptionType.Interrupt | 199
    Interrupt_C8 = ExceptionType.Interrupt | 200
    Interrupt_C9 = ExceptionType.Interrupt | 201
    Interrupt_CA = ExceptionType.Interrupt | 202
    Interrupt_CB = ExceptionType.Interrupt | 203
    Interrupt_CC = ExceptionType.Interrupt | 204
    Interrupt_CD = ExceptionType.Interrupt | 205
    Interrupt_CE = ExceptionType.Interrupt | 206
    Interrupt_CF = ExceptionType.Interrupt | 207
    Interrupt_D0 = ExceptionType.Interrupt | 208
    Interrupt_D1 = ExceptionType.Interrupt | 209
    Interrupt_D2 = ExceptionType.Interrupt | 210
    Interrupt_D3 = ExceptionType.Interrupt | 211
    Interrupt_D4 = ExceptionType.Interrupt | 212
    Interrupt_D5 = ExceptionType.Interrupt | 213
    Interrupt_D6 = ExceptionType.Interrupt | 214
    Interrupt_D7 = ExceptionType.Interrupt | 215
    Interrupt_D8 = ExceptionType.Interrupt | 216
    Interrupt_D9 = ExceptionType.Interrupt | 217
    Interrupt_DA = ExceptionType.Interrupt | 218
    Interrupt_DB = ExceptionType.Interrupt | 219
    Interrupt_DC = ExceptionType.Interrupt | 220
    Interrupt_DD = ExceptionType.Interrupt | 221
    Interrupt_DE = ExceptionType.Interrupt | 222
    Interrupt_DF = ExceptionType.Interrupt | 223
    Interrupt_E0 = ExceptionType.Interrupt | 224
    Interrupt_E1 = ExceptionType.Interrupt | 225
    Interrupt_E2 = ExceptionType.Interrupt | 226
    Interrupt_E3 = ExceptionType.Interrupt | 227
    Interrupt_E4 = ExceptionType.Interrupt | 228
    Interrupt_E5 = ExceptionType.Interrupt | 229
    Interrupt_E6 = ExceptionType.Interrupt | 230
    Interrupt_E7 = ExceptionType.Interrupt | 231
    Interrupt_E8 = ExceptionType.Interrupt | 232
    Interrupt_E9 = ExceptionType.Interrupt | 233
    Interrupt_EA = ExceptionType.Interrupt | 234
    Interrupt_EB = ExceptionType.Interrupt | 235
    Interrupt_EC = ExceptionType.Interrupt | 236
    Interrupt_ED = ExceptionType.Interrupt | 237
    Interrupt_EE = ExceptionType.Interrupt | 238
    Interrupt_EF = ExceptionType.Interrupt | 239
    Interrupt_F0 = ExceptionType.Interrupt | 240
    Interrupt_F1 = ExceptionType.Interrupt | 241
    Interrupt_F2 = ExceptionType.Interrupt | 242
    Interrupt_F3 = ExceptionType.Interrupt | 243
    Interrupt_F4 = ExceptionType.Interrupt | 244
    Interrupt_F5 = ExceptionType.Interrupt | 245
    Interrupt_F6 = ExceptionType.Interrupt | 246
    Interrupt_F7 = ExceptionType.Interrupt | 247
    Interrupt_F8 = ExceptionType.Interrupt | 248
    Interrupt_F9 = ExceptionType.Interrupt | 249
    Interrupt_FA = ExceptionType.Interrupt | 250
    Interrupt_FB = ExceptionType.Interrupt | 251
    Interrupt_FC = ExceptionType.Interrupt | 252
    Interrupt_FD = ExceptionType.Interrupt | 253
    Interrupt_FE = ExceptionType.Interrupt | 254
    Interrupt_FF = ExceptionType.Interrupt | 255

    # UC Errors
    ErrNoMem = ExceptionType.Error | 1
    ErrArch = ExceptionType.Error | 2
    ErrHandle = ExceptionType.Error | 3
    ErrMode = ExceptionType.Error | 4
    ErrVersion = ExceptionType.Error | 5
    ErrHook = ExceptionType.Error | 6
    ErrInsnInvalid = ExceptionType.Error | 7
    ErrMap = ExceptionType.Error | 8
    ErrArg = ExceptionType.Error | 9
    ErrHookExists = ExceptionType.Error | 10
    ErrResource = ExceptionType.Error | 11
    ErrException = ExceptionType.Error | 12

    # UC Memory Errors
    ErrReadUnmapped = ExceptionType.Error | MemoryFlags.Read | MemoryFlags.Unmapped
    ErrWriteUnmapped = ExceptionType.Error | MemoryFlags.Write | MemoryFlags.Unmapped
    ErrExecuteUnmapped = ExceptionType.Error | MemoryFlags.Execute | MemoryFlags.Unmapped
    ErrReadProt = ExceptionType.Error | MemoryFlags.Read | MemoryFlags.Protection
    ErrWriteProt = ExceptionType.Error | MemoryFlags.Write | MemoryFlags.Protection
    ErrExecuteProt = ExceptionType.Error | MemoryFlags.Execute | MemoryFlags.Protection
    ErrReadUnaligned = ExceptionType.Error | MemoryFlags.Read | MemoryFlags.Unaligned
    ErrWriteUnaligned = ExceptionType.Error | MemoryFlags.Write | MemoryFlags.Unaligned
    ErrExecuteUnaligned = ExceptionType.Error | MemoryFlags.Execute | MemoryFlags.Unaligned

    def type(self) -> [ExceptionType, int]:
        return ExceptionType(self & 0xF000)

    def memory_access(self) -> MemoryFlags:
        assert self.type() == ExceptionType.Memory
        return MemoryFlags(self & 0xF0)

    def to_memory_fault(self) -> int:
        assert self.type() == ExceptionType.Memory, f'Exception is not type of Memory, code: {self}.'
        types = {
            MemoryFlags.Read: EXCEPTION_READ_FAULT,
            MemoryFlags.Write: EXCEPTION_WRITE_FAULT,
            MemoryFlags.Execute: EXCEPTION_EXECUTE_FAULT
        }
        return types[MemoryFlags(self.memory_access())]

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}.{self.name}'

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'{cls_name}.{self.name}'


def translate_exception(uc_code: int) -> Exceptions:
    translation = {
        UC_ERR_OK: Exceptions.NoException,
        UC_ERR_NOMEM: Exceptions.ErrNoMem,
        UC_ERR_ARCH: Exceptions.ErrArch,
        UC_ERR_HANDLE: Exceptions.ErrHandle,
        UC_ERR_MODE: Exceptions.ErrMode,
        UC_ERR_VERSION: Exceptions.ErrVersion,
        UC_ERR_READ_UNMAPPED: Exceptions.ErrReadUnmapped,
        UC_ERR_WRITE_UNMAPPED: Exceptions.ErrWriteUnmapped,
        UC_ERR_FETCH_UNMAPPED: Exceptions.ErrExecuteUnmapped,
        UC_ERR_HOOK: Exceptions.ErrHook,
        UC_ERR_INSN_INVALID: Exceptions.ErrInsnInvalid,
        UC_ERR_MAP: Exceptions.ErrMap,
        UC_ERR_WRITE_PROT: Exceptions.ErrWriteProt,
        UC_ERR_READ_PROT: Exceptions.ErrReadProt,
        UC_ERR_FETCH_PROT: Exceptions.ErrExecuteProt,
        UC_ERR_ARG: Exceptions.ErrArg,
        UC_ERR_READ_UNALIGNED: Exceptions.ErrReadUnaligned,
        UC_ERR_WRITE_UNALIGNED: Exceptions.ErrWriteUnaligned,
        UC_ERR_FETCH_UNALIGNED: Exceptions.ErrExecuteUnaligned,
        UC_ERR_HOOK_EXIST: Exceptions.ErrHookExists,
        UC_ERR_RESOURCE: Exceptions.ErrResource,
        UC_ERR_EXCEPTION: Exceptions.ErrException,
        UC_MEM_READ: Exceptions.MemRead,
        UC_MEM_WRITE: Exceptions.MemWrite,
        UC_MEM_FETCH: Exceptions.MemExecute,
        UC_MEM_READ_UNMAPPED: Exceptions.MemReadUnmapped,
        UC_MEM_WRITE_UNMAPPED: Exceptions.MemWriteUnmapped,
        UC_MEM_FETCH_UNMAPPED: Exceptions.MemExecuteUnmapped,
        UC_MEM_WRITE_PROT: Exceptions.MemWriteProt,
        UC_MEM_READ_PROT: Exceptions.MemReadProt,
        UC_MEM_FETCH_PROT: Exceptions.MemExecuteProt,
        UC_MEM_READ_AFTER: Exceptions.MemReadAfter
    }
    assert uc_code in translation, f'Unknown UC code: {uc_code}.'
    return translation[uc_code]
