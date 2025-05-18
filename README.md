# MacCoreV
## Descrizione
[...]
---
## Modifiche da fare al codice:
- [x] platform.json --> le keywords
- [x] /boards/myboard.json --> modificare i dettagli della board
- [x] /builder/main.py --> prefisso della toolchain; eventuali flag speciali
- [x] /framework-MacCoreV/package.json --> I dettagli generali
- [x] /framework-MacCoreV/src/... --> aggiungere: crt0.S, linker.ld, syscalls.c, eventuali startup .c/.s
- [x] /toolchain-MacCoreV/package.json --> Il nome e il contenuto del campo bin, se diverso
- [x] /toolchain-MacCoreV/bin/... --> icludere i binari essenziali riportati di seguito. **ASSICURARSI CHE I NOMI CORRISPONDANO NEL `builder/main.py`**  
*Non includere tool inutili come gdb, readelf, nm, ecc. se non li usi.*
    - `riscv32-unknown-elf-gcc` compilatore C
    - `riscv32-unknown-elf-g++` compilatore C++ (se usi C++)
    - `riscv32-unknown-elf-as` assembler
    - `riscv32-unknown-elf-ld` linker (opzionale, GCC lo chiama da sé)
    - `riscv32-unknown-elf-objcopy` conversione bin/hex
    - `riscv32-unknown-elf-objdump` disassemblaggio (debug opzionale)
    - `riscv32-unknown-elf-size` stampa dimensioni binario
    - `riscv32-unknown-elf-ar` crea archivi .a
    - `riscv32-unknown-elf-ranlib` indicizza .a
---

## Installazione
OPZIONI:
### 1. Stai usando una piattaforma PlatformIO personalizzata (come la tua platform-mycore)
- Non bisogna installare nulla con `pio pkg install`
- Nel progetto PlatformIO nel file platformio.ini impostare:
    > [env:myboard]  
    platform = file:///percorso/assoluto/o/relativo/platform-mycore  
    board = myboard
    framework = mycore

### 2. Vuoi installare un pacchetto da testare separatamente (toolchain o framework)

**Questo metodo è utile solo se vuoi riutilizzare il pacchetto in più piattaforme.**

Vai nella cartella del tuo pacchetto (es. toolchain-mycore):

`cd toolchain-mycore`

Installa localmente:

`pio pkg pack`

Questo crea un file tipo:

`toolchain-mycore-1.0.0.tar.gz`

Poi:

`pio pkg install --global --storage-dir ~/.platformio/packages --package toolchain-mycore-1.0.0.tar.gz`

oppure per framework:

`pio pkg install --global --storage-dir ~/.platformio/packages --package framework-m`

---

## Creare un loader per la board

Nel tuo progetto crea una cartella (che per esempio chiamiamo `convert`) contenente lo script `run_after_built.py`

Codice `run_after_built.py`

```
Import("env")
import os
import subprocess

def run_loader(source, target, env):
elf_file = str(target[0])  # il file ELF generato
output_dir = os.path.join(env["PROJECT_DIR"], "include", "generated")

os.makedirs(output_dir, exist_ok=True)

script_path = os.path.join(env["PROJECT_DIR"], "convert", "convert_elf_to_header.py")

print(f"[LOADER] Eseguo: {script_path}")
print(f"[LOADER] ELF: {elf_file}")
print(f"[LOADER] Output: {output_dir}")

result = subprocess.run(["python3", script_path, elf_file, output_dir], capture_output=True, text=True)

if result.returncode != 0:
    print("[LOADER] Errore:")
    print(result.stderr)
    raise Exception("Errore nel loader")
else:
    print("[LOADER] Fatto.")
    print(result.stdout)

env.AddPostAction("buildprog", run_loader)


in `platformio.ini`:
> [env:myboard]
platform = file://../platform-MacCoreV
board = myboard
framework = MacCoreV

extra_scripts = post:convert/run_after_build.py
```

Successivamente nella cartella `convert` aggiungiamo lo script da eseguire.

**`run_after_built.py` collega il loader personalizzato al processo di build di PlatformIO**

---

## Compilare le SysCall come codice di start up

Assicurarti che in startup.c la funzione sia definita così

```
void _init(void) {  
    // codice di inizializzazione, chiamata a main() ecc.  
}
```

Per il linker aggiungere nel `builder/main.py` lo script
> env.Replace(LDSCRIPT_PATH=join(framework_dir, "src", "linker_script.ld"))

**NON HO MODIFICATO IL TUO CODICE DATO CHE PREFERISCO CHE TU FACCIA UNA VALUTAZIONE DEI CAMBIAMENTI**

## Cose da chiarire

- [x] Come si fa per installare il package?
- [x] Come fare a creare un loader per questa board?
      
    In questo caso il loader sarebbe uno script di python (che ho già) che in sostanza legge il file *.elf generato e lo converte un un file header in una cartella che sarebbe da definire nell'environment di PlatformIO (di seguito PIO)

- [x] Come faccio a digli di compilare le SysCall (nel file `framework-MacCoreV/src/syscalls.c`) e di usare la funzione `_init` (definita in `framework-MacCoreV/src/startup.c`) come codice di startup?

- [x]  Dove trovo, e dove devo copiare i file della NewLib affinchè usi le nano spech?