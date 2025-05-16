from os.path import join
from SCons.Script import DefaultEnvironment

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

framework_dir = env.PioPlatform().get_package_dir("framework-mycore")

env.Append(
    # CFLAGS = -ffreestanding -Os --specs=nano.specs -ffunction-sections -Wl,--gc-sections
    # LDFLAGS = -T $(LINKER) -e main 
    CCFLAGS=["-ffreestanding", "-Os", "--specs=nano.specs", "-ffunction-sections", "-Wl,--gc-sections"],
    LINKFLAGS=["-T", join(framework_dir, "src", "linker_script.ld")],
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
