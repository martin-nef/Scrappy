.PHONY: build run

all: build run

build:
	podman build -t scrappy .

run:
	podman run --rm -it scrappy

manual-control: build
	podman run --rm -it scrappy python manual-control.py
