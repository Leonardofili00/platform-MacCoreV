# MacCoreV
### Descrizione
[...]
---
### Modifiche da fare:
- [x] platform.json --> le keywords
- [x] /boards/myboard.json --> modificare i dettagli della board
- [x] /builder/main.py --> prefisso della toolchain; eventuali flag speciali
- [x] /framework-MacCoreV/package.json --> I dettagli generali
- [x] /framework-MacCoreV/src/... --> aggiungere: crt0.S, linker.ld, syscalls.c, eventuali startup .c/.s
- [x] /toolchain-MacCoreV/package.json --> Il nome e il contenuto del campo bin, se diverso
- [x] /toolchain-MacCoreV/bin/... --> aggiungere riscv32-unknown-elf-gcc (e altri binari: as, objcopy, ld, ecc.) oppure riscv32-mycpu-elf-gcc se hai un prefisso diverso (in tal caso aggiorna anche main.py!)

    - [ ] Cosa ci va dentro di preciso? Servono tutti i binari della toolchain?
  
---
  
### Cose da chiarire
- [ ] Come si fa per installare il package?
- [ ] Come fare a creare un loader per questa board?
      
    In questo caso il loader sarebbe uno script di python (che ho già) che in sostanza legge il file *.elf generato e lo converte un un file header in una cartella che sarebbe da definire nell'environment di PlatformIO (di seguito PIO)

- [ ] Come faccio a digli di compilare le SysCall (nel file `framework-MacCoreV/src/syscalls.c`) e di usare la funzione `_init` (definita in `framework-MacCoreV/src/startup.c`) come codice di startup?

- [x]  Dove trovo, e dove devo copiare i file della NewLib affinchè usi le nano spech?
    
    > Ho risolto io!! 

