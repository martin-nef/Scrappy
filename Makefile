.PHONY: build run

all: build run

build:
	podman build -t scrappy .

run:
	podman run --network=host --rm -it scrappy

manual-control: build
	podman run --network=host --rm -it scrappy python manual-control.py

console: build
	podman run --network=host --rm -it scrappy python 
