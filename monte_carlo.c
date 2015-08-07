
#include <stdio.h>
#include <stdlib.h>
#include <time.h>




int main() {
    int radius = 5000;
    int diameter = 2 * radius;

    srand(time(NULL));
    int i = rand();
    printf("%d\n", i % 100);

    return 0;
}
