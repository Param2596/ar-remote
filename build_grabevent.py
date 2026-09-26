"""Build a tiny arm64 program that grabs the remote so the phone ignores it.

The program opens the input device, takes exclusive access, and writes one
text line per key ("103 1") so adb can flush each press immediately. When it
exits, the kernel releases the grab and the phone sees the remote again.
"""

from __future__ import annotations

import struct
from pathlib import Path

from keystone import KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN, Ks

LOAD = 0x400000
CODE_ADDR = LOAD + 0x100
BUF_ADDR = 0x410000

SOURCE = r"""
_start:
    ldr x20, [sp, #16]
    cbz x20, open_fail
    ldrb w5, [x20]
    cmp w5, #45
    b.ne open_dev
    mov w3, #103
    mov w4, #1
    bl emit
    b done

open_dev:
    mov x0, #-100
    mov x1, x20
    mov x2, #0
    mov x8, #56
    svc #0
    cmp x0, #0
    b.lt open_fail
    mov x19, x0

    mov x0, x19
    movz x1, #0x4590
    movk x1, #0x4004, lsl #16
    mov x2, #1
    mov x8, #29
    svc #0
    cmp x0, #0
    b.lt grab_fail

    movz x21, #0x0000
    movk x21, #0x0041, lsl #16

loop:
    mov x0, x19
    mov x1, x21
    mov x2, #24
    mov x8, #63
    svc #0
    cmp x0, #24
    b.ne done
    ldrh w2, [x21, #16]
    cmp w2, #1
    b.ne loop
    ldrh w3, [x21, #18]
    ldr w4, [x21, #20]
    bl emit
    b loop

emit:
    stp x30, x23, [sp, #-16]!
    movz x23, #0x0100
    movk x23, #0x0041, lsl #16
    mov x1, x23
    mov w0, w3
    bl utoa
    mov w5, #32
    strb w5, [x1], #1
    mov w0, w4
    bl utoa
    mov w5, #10
    strb w5, [x1], #1
    sub x2, x1, x23
    mov x0, #1
    mov x1, x23
    mov x8, #64
    svc #0
    ldp x30, x23, [sp], #16
    ret

utoa:
    cbz w0, utoa_zero
    stp x30, xzr, [sp, #-16]!
    sub sp, sp, #32
    mov x6, sp
    mov x7, sp
utoa_div:
    mov w9, #10
    udiv w10, w0, w9
    msub w11, w10, w9, w0
    add w11, w11, #48
    strb w11, [x7], #1
    mov w0, w10
    cbnz w0, utoa_div
utoa_rev:
    cmp x7, x6
    b.eq utoa_rev_done
    sub x7, x7, #1
    ldrb w11, [x7]
    strb w11, [x1], #1
    b utoa_rev
utoa_rev_done:
    add sp, sp, #48
    ret
utoa_zero:
    mov w11, #48
    strb w11, [x1], #1
    ret

done:
    mov x0, #0
    mov x8, #93
    svc #0
open_fail:
    mov x0, #1
    mov x8, #93
    svc #0
grab_fail:
    mov x0, #2
    mov x8, #93
    svc #0
"""


def elf(code: bytes) -> bytes:
    code_off = CODE_ADDR - LOAD
    file_size = code_off + len(code)
    image = bytearray(file_size)
    ident = bytearray(16)
    ident[0:4] = b"\x7fELF"
    ident[4] = 2
    ident[5] = 1
    ident[6] = 1
    header = struct.pack(
        "<16sHHIQQQIHHHHHH",
        bytes(ident),
        2,  # ET_EXEC
        183,  # EM_AARCH64
        1,
        CODE_ADDR,
        64,  # program header offset
        0,
        0,
        64,
        56,
        2,
        0,
        0,
        0,
    )
    image[0:64] = header

    def phdr(offset: int, vaddr: int, filesz: int, memsz: int, flags: int) -> bytes:
        return struct.pack(
            "<IIQQQQQQ",
            1,  # PT_LOAD
            flags,
            offset,
            vaddr,
            vaddr,
            filesz,
            memsz,
            0x1000,
        )

    image[64:120] = phdr(0, LOAD, file_size, file_size, 5)  # RX
    image[120:176] = phdr(0, BUF_ADDR, 0, 0x1000, 6)  # RW buffer
    image[code_off:file_size] = code
    return bytes(image)


def main() -> None:
    encoding, _count = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN).asm(SOURCE, CODE_ADDR)
    code = bytes(encoding)
    out = Path(__file__).with_name("grabevent")
    out.write_bytes(elf(code))
    print(f"wrote {out} ({out.stat().st_size} bytes, code {len(code)})")


if __name__ == "__main__":
    main()
