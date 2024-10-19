# AI Assistant

## Overview

![Overview Diagram](docs/diagrams/overview.svg)

## Technology stack

### Python

Python is a programming language that lets you work quickly and integrate systems more effectively.

Website: [Python](https://www.python.org)

### Python Poetry

Python packaging and dependency management made easy.

Website: [Python Poetry](https://python-poetry.org)

### Streamlit

Streamlit turns data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience required.

Website: [Streamlit](https://streamlit.io)

### LangChain

LangChain is a framework to build with LLMs by chaining interoperable components. LangGraph is the framework for building controllable agentic workflows.

Website: [LangChain](https://www.langchain.com)

## Development

### Docker Engine

Install the Docker Engine by following the procedure described here: https://docs.docker.com/engine/install/.

Based on the use-case, check out the documenation here on how to configure your installation to allow a non-root user to use docker: https://docs.docker.com/engine/install/linux-postinstall/.

During the development of this project a Debian distro running on Raspberry PI 5 was used.

Rather than using Docker Desktop for Mac, a good alternative would be to use OrbStack: https://orbstack.dev.

Test the installation by attempting to download and run the Python Poetry docker image.

```bash
docker run -it weastur/poetry:1.8.3-python-3.9.19-bookworm /bin/bash
```

The cotainer used above has support for multiple architectures: https://hub.docker.com/r/weastur/poetry/tags.

### Visual Studio Code

Download and install the proper version based on your environment: https://code.visualstudio.com/Download.
