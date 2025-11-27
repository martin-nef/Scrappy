.PHONY: build run

all: build run

build:
	podman build -t scrappy .

run: build manual-control

manual-control: build
	podman run --network=host -p 8889:8889/udp -p 8890:8890/udp --rm -it scrappy python manual-control.py

console: build
	podman run --network=host -p 8889:8889/udp -p 8890:8890/udp -p 11111:11111/udp -p 5000:5000 --rm -it scrappy python 

stream: build
	podman run --network=host -p 11111:11111/udp -p 5000:5000 --rm -it scrappy python stream_server.py

