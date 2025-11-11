#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main() {
    const int N = 5000000;
    double *arr = malloc(sizeof(double) * N);
    for (int i = 0; i < N; i++) arr[i] = i * 0.001;

    double sum = 0.0;
    clock_t start = clock();
    for (int r = 0; r < 50; r++) {
        for (int i = 0; i < N; i++) {
            arr[i] = sin(arr[i]) + sqrt(arr[i]);
            sum += arr[i];
        }
    }
    clock_t end = clock();
    double sec = (double)(end - start)/CLOCKS_PER_SEC;
    printf("Mixed workload complete. sum=%f  Time=%.3f s\n", sum, sec);

    free(arr);
    return 0;
}
