from os.path import join
from SCons.Script import DefaultEnvironment, Builder

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

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

framework_dir = platform.get_package_dir("framework-maccorev")
assert framework_dir, "framework-maccorev non trovato!"

env.Append(
    CCFLAGS=[
        "-ffreestanding",
        "-Os",
        "--specs=nano.specs",
        "-ffunction-sections",
        "-Wl,--gc-sections"
    ],
    LINKFLAGS=[
        "-Wl,-e,_init",
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

env.Append(BUILDERS=dict(
    ElfToHex=Builder(
        action="riscv32-unknown-elf-objcopy -O ihex $SOURCE $TARGET",
        suffix=".hex",
        src_suffix=".elf"
    )
))

# Qui definisci la variabile sources
sources = env.Glob(join(framework_dir, "src", "*.c"))

program = env.Program(
    target=join("$BUILD_DIR", "firmware.elf"),
    source=sources
)

env.Alias("buildprog", program)
env.AlwaysBuild(program)

# Definisci default target per PlatformIO
Default(program)
