#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "machbooks.h"

void init_library()
{
    uint32_t idx;
    Status *stat;
    library = (Book *)calloc(MAX_BOOK_NUM, sizeof(Book));
    stat = (Status *)calloc(MAX_BOOK_NUM, sizeof(Status));
    for (idx = 0; idx < MAX_BOOK_NUM; idx++)
    {
        library[idx].stat = &stat[idx];
        library[idx].stat->status = SET_ISFREE(library[idx].stat->status);
    }
}

void edit_book_name()
{
    uint32_t idx;

    printf("Book index: ");
    scanf("%u", &idx);

    if (idx >= MAX_BOOK_NUM || library[idx].is_bookname_edited)
    {
        puts("Invalid index");
        return;
    }

    printf("Book new name: ");
    read_input(library[idx].name, strlen(library[idx].name));
    library[idx].is_bookname_edited = 1;
}

void add_book_chapter()
{
    uint32_t idx;
    Chapter *chapter;

    printf("Book index: ");
    scanf("%u", &idx);  

    if (idx >= MAX_BOOK_NUM || !GET_INUSE(library[idx].stat->status) || GET_ISFREE(library[idx].stat->status))
    {
        puts("Invalid index");
        return;
    }

    chapter = (Chapter *)calloc(1, sizeof(Chapter));

    printf("Chapter title: ");
    read_input(chapter->title, MAX_TITLE_BUF);

    printf("Chapter content: ");
    read_input(chapter->content, MAX_CONTENT_BUF);

    chapter->next = library[idx].chapter;
    library[idx].chapter = chapter;
}

void create_book()
{
    uint32_t idx;

    printf("Book index: ");
    scanf("%u", &idx);

    if (idx >= MAX_BOOK_NUM || GET_INUSE(library[idx].stat->status))
    {
        puts("Invalid index");
        return;
    }

    printf("Book name: ");
    read_input(library[idx].name, MAX_NAME_BUF-1);

    library[idx].stat->status = SET_INUSE(0);
}

void edit_book()
{
    uint32_t choice;

    book_menu();
    printf("> ");
    scanf("%u", &choice);

    switch (choice)
    {
        case 1:
            edit_book_name();
            break;
        case 2:
            add_book_chapter();
            break;
        default:
            puts("invalid choice");
            break;
    }
}

void read_book()
{
    uint32_t idx;
    Chapter *cur;

    printf("Book index: ");
    scanf("%u", &idx); 

    if (idx >= MAX_BOOK_NUM || !GET_INUSE(library[idx].stat->status) || GET_ISFREE(library[idx].stat->status))
    {
        puts("Invalid index");
        return;
    }

    printf("Book %u: %s\n", idx, library[idx].name);
    
    cur = library[idx].chapter;
    while (cur)
    {
        printf("Chapter %s: %s\n", cur->title, cur->content);
        cur = cur->next;
    }
}

void remove_book()
{
    uint32_t idx;

    printf("Book index: ");
    scanf("%u", &idx);   

    if (idx >= MAX_BOOK_NUM || !GET_INUSE(library[idx].stat->status) || GET_ISFREE(library[idx].stat->status))
    {
        puts("Invalid index");
        return;
    } 

    library[idx].stat->status = SET_ISFREE(library[idx].stat->status);

    if (library[idx].fp)
    {
        fclose(library[idx].fp);
        library[idx].fp = NULL;
    }
}

void save_book()
{
    uint32_t idx;
    uint32_t count_chapter;
    FILE *fp;
    Chapter *cur;

    printf("Book index: ");
    scanf("%u", &idx);   

    if (idx >= MAX_BOOK_NUM || !GET_INUSE(library[idx].stat->status) || GET_ISFREE(library[idx].stat->status))
    {
        puts("Invalid index");
        return;
    }

    if (!waf_filename(library[idx].name))
    {
        puts("Invalid filename");
        return;
    }

    if (access(library[idx].name, F_OK) == 0)
    {
        puts("File exists");
        return;
    }

    fp = fopen(library[idx].name, "wb");
    if (!fp)
    {
        puts("fopen error");
        exit(-1);
    }
    write_file(library[idx].name, MAX_NAME_BUF, fp);

    count_chapter = 0;
    cur = library[idx].chapter;
    while (cur)
    {
        count_chapter++;
        cur = cur->next;
    }
    fprintf(fp, "%u\n", count_chapter);

    cur = library[idx].chapter;
    while (cur)
    {
        write_file(cur->title, MAX_TITLE_BUF, fp);
        write_file(cur->content, MAX_CONTENT_BUF, fp);
        cur = cur->next;
    }

    fclose(fp);
}

void load_book()
{
    uint32_t idx;
    uint32_t i;
    uint32_t count_chapter;
    Chapter *chapter;
    char filename[MAX_NAME_BUF+0x10];
    char count_chapter_buf[MAX_NAME_BUF+0x10];

    printf("Book name: ");
    read_input(filename, MAX_NAME_BUF-1);

    if (!waf_filename(filename))
    {
        puts("Invalid filename");
        return;
    }

    if (access(filename, F_OK) == -1)
    {
        puts("File doesn't exist");
        return;
    }

    printf("Book index: ");
    scanf("%u", &idx);

    if (idx >= MAX_BOOK_NUM || GET_INUSE(library[idx].stat->status))
    {
        puts("Invalid index");
        return;
    }

    library[idx].fp = fopen(filename, "rb");
    if (!library[idx].fp)
    {
        puts("fopen error");
        exit(-1);
    }

    library[idx].chapter = NULL;
    read_file(library[idx].name, MAX_NAME_BUF, library[idx].fp);
    read_file(count_chapter_buf, MAX_NAME_BUF, library[idx].fp);
    count_chapter = atoi(count_chapter_buf);

    for (i = 0; i < count_chapter; i++)
    {
        chapter = (Chapter *)calloc(1, sizeof(Chapter));
        read_file(chapter->title, MAX_TITLE_BUF, library[idx].fp);
        read_file(chapter->content, MAX_CONTENT_BUF, library[idx].fp);

        chapter->next = library[idx].chapter;
        library[idx].chapter = chapter;
    }

    library[idx].stat->status = SET_INUSE(0);
}

void reload_book()
{
    uint32_t idx;
    uint32_t i;
    uint32_t count_chapter;
    Chapter *chapter;
    char count_chapter_buf[MAX_NAME_BUF+0x10];

    printf("Book index: ");
    scanf("%u", &idx);   

    if (idx >= MAX_BOOK_NUM || !GET_INUSE(library[idx].stat->status) || GET_ISFREE(library[idx].stat->status) || !library[idx].fp)
    {
        puts("Invalid index");
        return;
    }

    fseek(library[idx].fp, 0, SEEK_SET);
    memset(library[idx].name, 0, sizeof(library[idx].name));
    library[idx].chapter = NULL;

    read_file(library[idx].name, MAX_NAME_BUF, library[idx].fp);
    read_file(count_chapter_buf, MAX_NAME_BUF, library[idx].fp);
    count_chapter = atoi(count_chapter_buf);

    for (i = 0; i < count_chapter; i++)
    {
        chapter = (Chapter *)calloc(1, sizeof(Chapter));
        read_file(chapter->title, MAX_TITLE_BUF, library[idx].fp);
        read_file(chapter->content, MAX_CONTENT_BUF, library[idx].fp);

        chapter->next = library[idx].chapter;
        library[idx].chapter = chapter;
    }
}

void mach_cloud()
{
    uint32_t choice;

    cloud_menu();
    printf("> ");
    scanf("%u", &choice);

    switch (choice)
    {
        case 1:
            save_book();
            break;
        case 2:
            load_book();
            break;
        case 3:
            reload_book();
            break;
        default:
            puts("invalid choice");
            break;
    }
}

int main()
{   
    uint32_t choice;

    init_proc();
    init_library();

    while (1)
    {
        main_menu();
        printf("> ");
        scanf("%u", &choice);

        switch (choice)
        {
            case 1:
                create_book();  
                break;
            case 2:
                edit_book();
                break;
            case 3:
                read_book();
                break;
            case 4:
                remove_book();
                break;    
            case 5:
                mach_cloud();
                break;
            case 6:
                puts("bye~");
                return 0;
            default:
                puts("invalid choice");
                break;
        }
    }

    return 0;
}
