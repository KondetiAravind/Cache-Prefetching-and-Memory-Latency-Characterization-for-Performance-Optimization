#include <stdio.h>
#include <stdint.h>
#include <time.h>

int main() {
    volatile uint64_t sum = 0;
    const uint64_t N = 50000000ULL;
    clock_t start = clock();

    for (uint64_t i = 1; i <= N; i++) {
        sum += i * 13 + (i >> 2);
        sum ^= (sum << 3);
    }

    clock_t end = clock();
    double seconds = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Integer arithmetic complete. Sum=%llu  Time=%.3f s\n",
           (unsigned long long)sum, seconds);
    return 0;
}
