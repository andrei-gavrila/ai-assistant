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

### Development Containers

An open specification for enriching containers with development specific content and settings.

Website: [Development Containers](https://containers.dev)

### EditorConfig

EditorConfig helps maintain consistent coding styles for multiple developers working on the same project across various editors and IDEs.

Website: [EditorConfig](https://editorconfig.org)

### GitHub

The complete developer platform to build, scale, and deliver secure software.

Website: [GitHub](https://github.com/about)

### GitHub Actions

GitHub Actions makes it easy to automate all your software workflows, now with world-class CI/CD. Build, test, and deploy your code right from GitHub. Make code reviews, branch management, and issue triaging work the way you want.

Website: [GitHub Actions](https://github.com/features/actions)

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

The container used above has support for multiple architectures: https://hub.docker.com/r/weastur/poetry/tags.

### Visual Studio Code

Download and install the proper version based on your environment: https://code.visualstudio.com/Download.

Based on the used development setup (local or remote) the following plugins are required: **Dev Containers** (local and remote) and **Remote - SSH** (only for remote).

### Run the application

Clone the project (the example uses ssh with key)

```bash
git clone git@github.com:andrei-gavrila/ai-assistant.git
```

switch to the cloned folder

```bash
cd ai-assistant
```

then open the project in Visual Studio Code

```bash
code .
```

Once **Visual Studio Code** opened the project, the **Dev Containers** extension asks to **Reopen in Container** (if the question is missed, use the command palette to trigger **Dev Containers: Reopen in Container**).

The **Dev Container** contains a postcreate command to install the project dependencies. However, if a dependency is added manually (not recommended, use ```poetry add```), running this in the project root folder may be required:

```bash
poetry install
```

Note: On certain conditions, **Visual Studio Code** doesn't detect the proper **Python** interpreter (eg. packages are not recognized). If this happens, select the interpreter in the ```.venv``` folder by clicking the correspnding entry in the footer file on the bottom right side of the **Visual Studio Code** window while a **Python** file is opened.

To run the application simply use the defined launch configuration - this has full debugging support (breakpoints, variables, ...). Alternatevly, the application can also be started from the **Terminal** (without debugging support):

```bash
poetry run streamlit run main.py
```

Note: Additional parameters may be added to the command above and in the *launch.json* configuration (base URL, server host and port, ...).

Once the application is started, the port is automatically forwarded by **Visual Studio Code** and (based on configuration) a browser window is opened with the URL http://localhost:8501/ (this is the default port used by **Streamlit**).
