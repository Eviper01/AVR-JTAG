.include "m328pdef.inc"

LDI R16, 0x20
out DDRB, R16
LDI R16, 0x20
out PINB, R16
kill:
jmp kill
