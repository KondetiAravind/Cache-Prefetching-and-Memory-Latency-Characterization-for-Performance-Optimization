#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
    const size_t N = 32 * 1024 * 1024;   // 32 MB
    char *src = malloc(N);
    char *dst = malloc(N);
    if (!src || !dst) return 1;

    for (size_t i = 0; i < N; i++) src[i] = (char)(i & 0xFF);

    clock_t start = clock();
    for (int r = 0; r < 50; r++) memcpy(dst, src, N);
    clock_t end = clock();

    double sec = (double)(end - start)/CLOCKS_PER_SEC;
    double mb = (double)N*50/(1024.0*1024.0);
    printf("Memory copy complete: %.1f MB in %.3f s (%.2f MB/s)\n",
           mb, sec, mb/sec);

    free(src); free(dst);
    return 0;
}
