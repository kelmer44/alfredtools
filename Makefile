CC := gcc
# build with debug symbols for easier debugging in VSCode
CFLAGS := -g -O0 -std=c11 -Wall -Wextra
SRCDIR := src
BINDIR := bin
TARGET := $(BINDIR)/alfredcli

SOURCES := $(SRCDIR)/main.c $(SRCDIR)/lodepng.c $(SRCDIR)/alfred*.c $(SRCDIR)/functions.c

all: $(TARGET)

$(BINDIR):
	mkdir -p $(BINDIR)

$(TARGET): $(BINDIR) $(SOURCES)
	$(CC) $(CFLAGS) -o $@ $(SOURCES)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -rf $(BINDIR)

.PHONY: all clean run
