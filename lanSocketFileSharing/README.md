# Simple socket file transfer implementation

You can modify parameters in [conf.ini](./conf.ini).

## How to run

- create download folder and set it as parameter `DOWNLOAD_DIR` in [conf.ini](./conf.ini)
- set `fp` variable to desired file path in `main` function of [client.py](./src/client.py)

Start server:
> bash run-server.sh

Run client script:
> bash run-client.sh

Ckeck download folder that you have made for a new file.