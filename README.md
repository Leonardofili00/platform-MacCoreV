# MacCoreV
### Descrizione
[...]
---
### Modifiche da fare:
- platform.json --> le keywords
- /boards/myboard.json --> modificare i dettagli della board
- /builder/main.py --> prefisso della toolchain; eventuali flag speciali
- /framework-MacCoreV/package.json --> I dettagli generali
- /framework-MacCoreV/src/... --> aggiungere: crt0.S, linker.ld, syscalls.c, eventuali startup .c/.s
- /toolchain-MacCoreV/package.json --> Il nome e il contenuto del campo bin, se diverso
- /toolchain-MacCoreV/bin/... --> aggiungere riscv32-unknown-elf-gcc (e altri binari: as, objcopy, ld, ecc.) oppure riscv32-mycpu-elf-gcc se hai un prefisso diverso (in tal caso aggiorna anche main.py!)

---