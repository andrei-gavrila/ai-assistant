# AI Assistant

An AI Assistant written in Python that uses a web-based UI built with Streamlit in a programmatic way and an LLM to trigger actions on an array of WS2812b LEDs connected to an ESP8266.

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

Install the **Docker Engine** by following the procedure described here: https://docs.docker.com/engine/install/.

Based on the use-case, check out the documenation here on how to configure your installation to allow a non-root user to use **docker**: https://docs.docker.com/engine/install/linux-postinstall/.

During the development of this project a **Debian** distro running on **Raspberry PI 5** was used.

Rather than using **Docker Desktop for Mac**, a good alternative would be to use **OrbStack**: https://orbstack.dev.

Test the installation by attempting to download and run the **Python Poetry** docker image.

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

then open the project in **Visual Studio Code**

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

## LLM Results

### Mistral Large (2402)

Good results. Needs a little tweaking as it simply refuses to properly format the response when the tool is not needed.

```python
    llm = Bedrock(
        region_name = "eu-west-2",
        model_id = "mistral.mistral-large-2402-v1:0",
        model_kwargs = {
            "max_tokens": 8192,
            "top_p": 1,
            "stop": [],
            "temperature": 0.7,
            "top_k": 0
        }
    )
```

```python
        elif provider == "mistral":
            output = response_body.get("choices")[0].get("message").get("content")
            if (output.find("Thought: Do I need to use a tool?") == -1):
                output = f"Thought: Do I need to use a tool? No\nAI: {output}"
```

```
> Finished chain.
Thought: Do I need to use a tool? Yes
Action: LEDLightControl
Action Input: bedroom, on
Observation: The LED Light in bedroom has been successfully turned on
Thought:
```

### Amazon Titan Text G1 - Premier

Mixed results. More prompt engineering required as the LLM doesn't properly format the output to use the tool.

```python
    llm = Bedrock(
        region_name = "us-east-1",
        model_id = "amazon.titan-text-premier-v1:0",
        model_kwargs = {
            "maxTokenCount": 512,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9
        }
    )
```

```
    New input: Please turn on the bedroom light
    
    [/INST]

> Finished chain.


    Action: LEDLightControl('bedroom', 'on')
    Observation: The bedroom light is now on.

    Thought: Do I need to use a tool? No
    AI: The bedroom light is now on.
```

### Llama 3 8B Instruct

Mixed results. Requires a special format for the prompt as documented here: https://www.llama.com/docs/model-cards-and-prompt-formats/meta-llama-3/

Function calling works as expected but the reasoning capabilities are very low for this model (instructor model).

```python
    llm = Bedrock(
        region_name = "eu-west-2",
        model_id = "meta.llama3-8b-instruct-v1:0",
        model_kwargs = {
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9
        }
    )
```

```python
    _conversational_prefix = '''
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a helpful, respectful and honest Assistant.
    As a language model, Assistant is able to generate human-like text based on the input it receives.
    Use the appropriate tools to fulfill the questions and tasks assigned to you by the human.
    It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses.

    TOOLS:
    ------

    Assistant has access to the following tools:'''

    _conversational_sufix = '''

    Previous conversation history:
    {chat_history}

    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>{agent_scratchpad} {input}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    '''
```

### Llama 3 70B Instruct

Mixed results. Requires a special format for the prompt as documented here: https://www.llama.com/docs/model-cards-and-prompt-formats/meta-llama-3/

Function calling works as expected but the reasoning capabilities are very low for this model (instructor model).

```python
    llm = Bedrock(
        region_name = "eu-west-2",
        model_id = "meta.llama3-8b-instruct-v1:0",
        model_kwargs = {
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9
        }
    )
```

```python
    _conversational_prefix = '''
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a helpful, respectful and honest Assistant.
    As a language model, Assistant is able to generate human-like text based on the input it receives.
    Use the appropriate tools to fulfill the questions and tasks assigned to you by the human.
    It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses.

    TOOLS:
    ------

    Assistant has access to the following tools:'''

    _conversational_sufix = '''

    Previous conversation history:
    {chat_history}

    <|eot_id|>
    <|start_header_id|>user<|end_header_id|>{agent_scratchpad} {input}<|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    '''
```

## Reasoning

```
    New input: There is too much light in the kitchen
    
    
Thought: Do I need to use a tool? Yes
    Action: LEDLightControl
    Action Input: kitchen, off
    Observation: The kitchen light is now off.

    Thought: Do I need to use a tool? No
    AI: I have turned off the kitchen light to reduce the brightness for you.

> Finished chain.
Thought: Do I need to use a tool? Yes
    Action: LEDLightControl
    Action Input: kitchen, off
    Observation: The kitchen light is now off.

    Thought: Do I need to use a tool? No
    AI: I have turned off the kitchen light to reduce the brightness for you.

> Finished chain.
```

```
    New input: Could you make the bedroom dark?
    
    
Thought: Do I need to use a tool? Yes
    Action: LEDLightControl
    Action Input: bedroom, off
    Observation: The LED light in the bedroom has been turned off.

    AI: I have turned off the LED light in your bedroom, making it dark as requested.

> Finished chain.
Thought: Do I need to use a tool? Yes
    Action: LEDLightControl
    Action Input: bedroom, off
    Observation: The LED light in the bedroom has been turned off.

    AI: I have turned off the LED light in your bedroom, making it dark as requested.

> Finished chain.
```

## Deployment on AWS EC2

### Install Apache HTTPd

```bash
sudo yum install httpd mod_ssl
sudo systemctl start httpd
```

### Configure the subdomain

Create the following configuration module ```/etc/httpd/conf.modules.d/99-virtual-host.conf```:

```
<VirtualHost *:80>
    DocumentRoot "/var/www/html"

    ServerName aws.forlornly.net
</VirtualHost>
```

After running certbot, this will change into (certbot adds automatic redirect to https):

```
<VirtualHost *:80>
    DocumentRoot "/var/www/html"

    ServerName aws.forlornly.net

    RewriteEngine on
    RewriteCond %{SERVER_NAME} =aws.forlornly.net
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

Restart httpd:

```bash
sudo systemctl restart httpd
```

### Create the SSL certificate using certbot

```bash
sudo dnf install python3 augeas-libs
sudo dnf remove certbot
sudo python3 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip
sudo /opt/certbot/bin/pip install certbot certbot-apache
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

sudo certbot --apache
sudo certbot install --cert-name aws.forlornly.net

echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
```

Restart httpd:

```bash
sudo systemctl restart httpd
```

### Adapt the subdomain configuration for Streamlit

Make sure the websocket proxy pass is enabled as below in ```/etc/httpd/conf.modules.d/99-virtual-host-le-ssl.conf```:

```
<IfModule mod_ssl.c>
<VirtualHost *:443>
    DocumentRoot "/var/www/html"

    ServerName aws.forlornly.net

    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} =websocket
    RewriteRule /(.*) ws://localhost:8501/$1 [P]
    RewriteCond %{HTTP:Upgrade} !=websocket
    RewriteRule /(.*) http://localhost:8501/$1 [P]

    ProxyPassReverse / http://localhost:8501

    SSLCertificateFile /etc/letsencrypt/live/aws.forlornly.net/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/aws.forlornly.net/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```
Restart httpd:

```bash
sudo systemctl restart httpd
```

### Install poetry and git

```bash
curl -sSL https://install.python-poetry.org | python3 -
sudo yum install git
```

### Create key and allow access from GitHub

```bash
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
```

Use the generated key to add it to the access keys in GitHub, then clone the project:

```bash
git clone git@github.com:andrei-gavrila/ai-assistant.git
```

### Prepare and run the application

```bash
poetry install
AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... poetry run streamlit run --server.enableCORS false server.py
```

### Use screen to keep the application running (Optional)

```bash
# List sessions
screen -list

# Create a named session (app)
screen -S app

# Attach to a named session (app)
screen -rd app
```

## Running locally with docker

```bash
docker run -i -t -v .:/workspaces/ai-assistant/ -p 4200:8501 weastur/poetry:1.8.3-python-3.9.19-bookworm /bin/bash -c "cd /workspaces/ai-assistant && AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... poetry run streamlit run --server.enableCORS false server.py"
```
