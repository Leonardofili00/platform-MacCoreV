extern void main(int argc, char const *argv[]);

__attribute__((naked, section(".init")))
void _init(){
    __asm__ volatile(
        ".option norelax\n\t"
        "la gp, __global_pointer$\n\t"
        "la sp, __stack_start\n\t"
        "li t0, 0x40010000\n\t"
        "lw a0, 4(t0)\n\t"
        "lw a1, 8(t0)\n\t"
        "call main\n\t"
    );
}
