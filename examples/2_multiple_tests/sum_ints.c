#include "sum_ints.h"

static int sum = 0;

int sum_ints(const int kNum)
{
    return (sum += kNum);
}
