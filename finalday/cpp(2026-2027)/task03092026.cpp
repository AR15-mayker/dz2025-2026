#include <stdio.h>

int main(void) {
    char name[64];
    int age;
    scanf("%63s", name);
    scanf("%d", &age);
    printf("Hello, %s! you are %d years old. \n" name , age);
    return 0;
}