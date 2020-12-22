#include <stdio.h>
#include <ctype.h>
#include <stdint.h>
#include <signal.h>
#include <string.h>

#define MAX_TITLE_BUF 0x20
#define MAX_NAME_BUF 0x20
#define MAX_CONTENT_BUF 0x500
#define MAX_BOOK_NUM 0x6
#define MAX_FILE_BUFFER 0x1000

#define GET_ISFREE(b) (((b) >> 4) & 0x0F)
#define GET_INUSE(b) ((b) & 0x0F)

#define SET_ISFREE(b) ((b) | 0x10)
#define SET_INUSE(b) ((b) | 0x1)

#define TIMEOUT 120

typedef struct _chapter
{
    char title[MAX_TITLE_BUF];
    struct _chapter *next;
    char content[MAX_CONTENT_BUF];
} Chapter;

typedef struct _status
{
    // inuse: LO(status)
    // isfree: HI(status)
    uint8_t status;
    uint8_t reserved1;
    uint16_t reserved2;
    uint32_t reserved3;
    uint64_t reserved4;
} Status;

typedef struct _book
{
    char name[MAX_NAME_BUF];
    Status *stat;
    FILE *fp;
    uint64_t is_bookname_edited;
    Chapter *chapter;
} Book;

static Book *library;
static uint64_t num_chapter;
char file_buffer[MAX_FILE_BUFFER];

void main_menu()
{
    puts("=======================");
    puts("   1. Create Book      ");
    puts("   2. Edit Book        ");
    puts("   3. Read Book        ");
    puts("   4. Remove Book      ");
    puts("   5. Mach Cloud       ");
    puts("   6. Exit             ");
    puts("=======================");
}

void book_menu()
{
    puts("=======================");
    puts("   1. Edit Book Name   ");
    puts("   2. Add Chapter      ");
    puts("=======================");
}

void cloud_menu()
{
    puts("=======================");
    puts("   1. Save Book        ");
    puts("   2. Load Book        ");
    puts("   3. Reload Book      ");
    puts("=======================");    
}

void handler(int sig)
{
    exit(-1);
}

void init_proc()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stderr, 0, _IONBF, 0);
    signal(SIGALRM, handler);
    alarm(TIMEOUT);
}

void read_input(char *buf, uint32_t size)
{
    uint32_t ret;

    ret = read(0, buf, size);
    if(ret <= 0)
    {
        puts("read error");
		exit(-1);
    }

    if(buf[ret-1] == '\n')
    {
        buf[ret-1] = '\x00';
    }
}

void read_file(char *buf, uint32_t size, FILE *fp)
{
    memset(file_buffer, 0, MAX_FILE_BUFFER);
    fgets(file_buffer, 0x510, fp);
    memcpy(buf, file_buffer, size);
}

void write_file(char *buf, uint32_t size, FILE *fp)
{
    uint32_t i;

    for (i = 0; i < size; i++)
    {
        if (buf[i] == '\x00')
        {
            break;
        }
        fputc(buf[i], fp);
    }
    fputc('\n', fp);
}

uint32_t waf_filename(char *buf)
{
    uint32_t i;
    uint32_t filename_length = strlen(buf);

    for (i = 0; i < filename_length; i++)
    {
        if (!isalnum(buf[i]))
        {
            return 0;
        }
    }

    return 1;
}
