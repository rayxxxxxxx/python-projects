# Terminal multi-client chat on sockets

You can modify parameters in [config](./config.conf).

## How to run

- set your LAN IP address as parameter `HOST` in [config](./config.conf) if you want your machine to be visible to other machines

> [SERVER]  
> HOST=localhost <--- "your local IP here, or leave localhost"  

- manually set `SERVER_HOST` and `SERVER_PORT` in `main` function of file [client.py](./src/client.py) in order to connect to other machine (constants in [config](./config.conf) used to serve your machine as server)

> SERVER_HOST = "ip_address_of_other_machine"  
> SERVER_PORT = port_number  

Start server:
> bash run-server.sh

Run client script:
> bash run-client.sh

## *Notice

In order to see other people messages, you need to omit input and just press `Enter`.