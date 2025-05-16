from os.path import join
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

env.Replace(
    AS="riscv32-unknown-elf-as",
    CC="riscv32-unknown-elf-gcc",
    CXX="riscv32-unknown-elf-g++",
    AR="riscv32-unknown-elf-ar",
    OBJCOPY="riscv32-unknown-elf-objcopy",
    RANLIB="riscv32-unknown-elf-ranlib",
    SIZETOOL="riscv32-unknown-elf-size",

    SIZEFLAGS="--format=berkeley"
)

env.Append(
    LINKFLAGS=["-nostartfiles", "-Wl,--gc-sections"],
    CPPDEFINES=["F_CPU=" + board.get("build.f_cpu")],
    CPPPATH=[join("$PROJECT_DIR", "include")],
    LIBSOURCE_DIRS=[join(env.subst("$PROJECT_DIR"), "lib")],
)

env.Append(BUILDERS=dict(
    ElfToHex=Builder(
        action="riscv32-unknown-elf-objcopy -O ihex $SOURCE $TARGET",
        suffix=".hex"
    )
))
