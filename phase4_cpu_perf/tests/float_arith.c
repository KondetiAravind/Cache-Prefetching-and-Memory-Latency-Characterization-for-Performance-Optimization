#include <stdio.h>
#include <math.h>
#include <time.h>

int main() {
    volatile double x = 0.5, y = 1.3, z = 2.7;
    const unsigned long N = 40000000UL;
    clock_t start = clock();

    for (unsigned long i = 0; i < N; i++) {
        x = sin(y) * cos(z) + tanh(x);
        y = x * 1.0000001 + y * 0.9999999;
        z = sqrt(x*x + y*y + 1.0);
    }

    clock_t end = clock();
    double seconds = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Floating arithmetic complete. x=%f  Time=%.3f s\n", x, seconds);
    return 0;
}
