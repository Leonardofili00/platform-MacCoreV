# MacCoreV
## Descrizione
[...]

---

## Modifiche da fare al codice:
- [X] platform.json: assicurarti che i nomi corrispondano ai tuoi package
- [x] toolchain-maccorev/package.json: Che il sistema operativo sia corretto
- [ ] loader-maccorev/scripts/run_after_build.py: inserire lo script che deve essere eseguito alla fine della build
    > Non ci occupiamo di questo ora, prima facciamolo compilare
- [x] Nel progetto in cui usi la piattaforma, il file platformio.ini deve specificare:
```
[env:myboard]
platform = /percorso/assoluto/o/nome_registrato/platform-maccorev
board = myboard
framework = maccorev
```

---

## Installazione
OPZIONI:
### 1. Installare una piattaforma PlatformIO personalizzata (come la tua platform-maccorev)
- Non bisogna installare nulla con `pio pkg install`
- Nel progetto PlatformIO nel file `platformio.ini` impostare:
    ```ini
    [env:myboard]  
    platform = file:///percorso/assoluto/o/relativo/platform-maccorev  
    board = myboard
    framework = maccorev
    ```

### 2. Installare un pacchetto da testare separatamente (toolchain o framework)

Vai nella cartella della tua platform (es. platform-maccorev):

```bash
cd platform-maccorev
```

Installa localmente:
```bash
pio pkg install --global -t ./toolchain-maccorev
```

oppure per framework:
```bash
pio pkg install --global -t ./framework-maccorev
```
---

## Cose da chiarire

- [x] Come si fa per installare il package?
- [x] Come fare a creare un loader per questa board?
      
    In questo caso il loader sarebbe uno script di python (che ho già) che in sostanza legge il file *.elf generato e lo converte un un file header in una cartella che sarebbe da definire nell'environment di PlatformIO (di seguito PIO)

- [x] Come faccio a digli di compilare le SysCall (nel file `framework-MacCoreV/src/syscalls.c`) e di usare la funzione `_init` (definita in `framework-MacCoreV/src/startup.c`) come codice di startup?

- [x]  Dove trovo, e dove devo copiare i file della NewLib affinchè usi le nano spech?