from os.path import join
from SCons.Script import DefaultEnvironment, Builder

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

# Configura toolchain RISC-V
env.Replace(
    AS="riscv32-unknown-elf-as",
    AR="riscv32-unknown-elf-ar",
    CXX="riscv32-unknown-elf-g++",
    CC="riscv32-unknown-elf-gcc",
    LD="riscv32-unknown-elf-ld",
    OBJCOPY="riscv32-unknown-elf-objcopy",
    RANLIB="riscv32-unknown-elf-ranlib",
    SIZETOOL="riscv32-unknown-elf-size",
    SIZEFLAGS="--format=berkeley"
)

# Path al framework
framework_dir = platform.get_package_dir("framework-MacCoreV")
assert framework_dir, "framework-MacCoreV non trovato!"

# Aggiunge flags di compilazione/linking
env.Append(
    CCFLAGS=[
        "-ffreestanding",
        "-Os",
        "--specs=nano.specs",
        "-ffunction-sections",
        "-Wl,--gc-sections"
    ],
    LINKFLAGS=[
        "-Wl,-e,_init",  # Imposta _init come entry point
        "-T", join(framework_dir, "src", "linker_script.ld")
    ],
    CPPDEFINES=[
        "F_CPU=" + board.get("build.f_cpu")
    ],
    CPPPATH=[
        join("$PROJECT_DIR", "include"),
        join(framework_dir, "src")
    ],
    LIBSOURCE_DIRS=[
        join(env.subst("$PROJECT_DIR"), "lib")
    ]
)

# Builder per convertire ELF in HEX
env.Append(BUILDERS=dict(
    ElfToHex=Builder(
        action="riscv32-unknown-elf-objcopy -O ihex $SOURCE $TARGET",
        suffix=".hex",
        src_suffix=".elf"
    )
))

# Compila i file sorgente dal framework (syscalls.c, startup.c, ecc.)
env.BuildSources(
    join("$BUILD_DIR", "FrameworkMacCoreV"),
    join(framework_dir, "src")
)
