#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#include "include/sha256.h"

static void perform_secure_operations(void) {
    const char *filename = "secure_data.txt";
    const char *data = "Sensitive Data for AI Model";
    uint8_t hash[SHA256_BLOCK_SIZE];
    SHA256_CTX ctx;

    sha256_init(&ctx);
    sha256_update(&ctx, (const uint8_t *)data, strlen(data));
    sha256_final(&ctx, hash);

    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd < 0) {
        perror("Failed to open file for writing");
        return;
    }

    write(fd, hash, SHA256_BLOCK_SIZE);
    close(fd);

    printf("Secure operations completed and data written to %s\n", filename);
}

static void print_system_info(void) {
    struct sysinfo sys_info;
    if (sysinfo(&sys_info) != 0) {
        perror("sysinfo");
        return;
    }

    printf("System uptime: %ld seconds\n", sys_info.uptime);
    printf("Total RAM: %lu MB\n", sys_info.totalram / (1024 * 1024));
    printf("Free RAM: %lu MB\n", sys_info.freeram / (1024 * 1024));
    printf("Process count: %d\n", sys_info.procs);
}

static void monitor_performance(int iterations, int interval_seconds) {
    for (int i = 0; i < iterations; i++) {
        print_system_info();
        if (i < iterations - 1) {
            sleep((unsigned int)interval_seconds);
        }
    }
}

static int parse_int(const char *value, int fallback) {
    char *end = NULL;
    long result = strtol(value, &end, 10);
    if (end == value || result <= 0) {
        return fallback;
    }
    return (int)result;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <operation> [options]\n", argv[0]);
        fprintf(stderr, "Operations: secure, monitor\n");
        return 1;
    }

    if (strcmp(argv[1], "secure") == 0) {
        perform_secure_operations();
    } else if (strcmp(argv[1], "monitor") == 0) {
        int iterations = 2;
        int interval = 2;
        if (argc >= 3) {
            iterations = parse_int(argv[2], iterations);
        }
        if (argc >= 4) {
            interval = parse_int(argv[3], interval);
        }
        monitor_performance(iterations, interval);
    } else {
        fprintf(stderr, "Invalid operation: %s\n", argv[1]);
        return 1;
    }

    return 0;
}
