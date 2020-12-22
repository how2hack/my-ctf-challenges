#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *f;
    char flag[0x100];
    char buf[0x100];

    f = fopen("/flag", "r");
    fgets(flag, 0xff, f);
    fgets(buf, 0xff, stdin);
    printf(buf);

    return 0;
}