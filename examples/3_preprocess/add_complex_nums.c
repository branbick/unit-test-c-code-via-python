#include "add_complex_nums.h"

complex add_complex_nums(complex a, const complex kB)
{
    a.real += kB.real;
    a.imag += kB.imag;

    return a;
}
