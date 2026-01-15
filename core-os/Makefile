CC := gcc
CFLAGS := -std=c11 -Wall -Wextra -Wpedantic -Iinclude
LDFLAGS :=

TARGET := ai_integration
OBJS := ai_integration.o sha256.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

ai_integration.o: ai_integration.c include/sha256.h
	$(CC) $(CFLAGS) -c ai_integration.c

sha256.o: sha256.c include/sha256.h
	$(CC) $(CFLAGS) -c sha256.c

clean:
	rm -f $(TARGET) $(OBJS)

.PHONY: all clean
