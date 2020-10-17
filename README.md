# Underground Chat Cli

Asynchronous client saving a web chat history into a file.

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

To run the script on Linux enter the command:

```bash
$ python main.py --host minechat.dvmn.org --port 5000 --history test
```
It is possible to get the values of input arguments from environment variables. 
See `python main.py --help` for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
