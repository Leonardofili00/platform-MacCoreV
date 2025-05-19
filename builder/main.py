from os.path import join
from SCons.Script import DefaultEnvironment, Builder

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

toolchain_dir = platform.get_package_dir("toolchain-maccorev")
framework_dir = platform.get_package_dir("framework-maccorev")
loader_dir = platform.get_package_dir("loader-maccorev")

assert toolchain_dir and framework_dir

env.PrependENVPath("PATH", join(toolchain_dir, "bin"))

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

env.Append(
    CCFLAGS=["-ffreestanding", "-Os", "--specs=nano.specs", "-ffunction-sections", "-Wl,--gc-sections"],
    LINKFLAGS=["-Wl,-e,_init", "-T", join(framework_dir, "src", "linker_script.ld")],
    CPPDEFINES=["F_CPU=" + str(board.get("build.f_cpu", "0"))],
    CPPPATH=[join(framework_dir, "src")]
)

env.Append(BUILDERS=dict(
    ElfToHex=Builder(
        action="riscv32-unknown-elf-objcopy -O ihex $SOURCE $TARGET",
        suffix=".hex",
        src_suffix=".elf"
    )
))

env.BuildSources(
join("$BUILD_DIR", "FrameworkMacCoreV"),
join(framework_dir, "src")
)

if loader_dir:
    env.AddPostAction("$BUILD_DIR/${PROGNAME}.elf", f"python3 {join(loader_dir, 'scripts', 'run_after_build.py')} $BUILD_DIR/${{PROGNAME}}.elf")
