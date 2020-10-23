# Underground Chat Cli

The asynchronous CLI client of the web chat.

## Project Goal
This is the educational project created to improve the skills of asynchronous code.
The training courses for web-developers - [dvmn.org](https://dvmn.org/).

## Getting Started

### How to Install

1. Download this repository.
2. Python v3.8 should be already installed. Afterwards use pip to install dependencies:
```bash
$ pip install -r requirements.txt
```
It is recommended to use a virtual environment for better isolation.

### Quick Start

The repository contains the two independent scripts.
A Linux command to run the script collecting a chat history:
```bash
$ python read_chat.py --host chat_host.org --port 1234 --history history.txt
```
A Linux command to run the script sending a message to the chat:
```bash
$ python send_message.py --host chat_host.org --port 1234 --token token --message Hello Everyone! 
```
User can set input arguments as environment variables. 
See `python main.py --help` for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
