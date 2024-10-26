import streamlit as st

from bedrock import Bedrock

from langchain.agents import ConversationalAgent
from langchain.chains import LLMChain
from langchain.agents import ConversationalAgent
from langchain.agents import AgentExecutor

from tools.led_light_control import LEDLightControl

import requests

led_light_control = LEDLightControl()

tools = [led_light_control]

from langchain.agents import ConversationalAgent

def create_prompt(tools):
    """  """
    _conversational_prefix = '''
You are a helpful, respectful and honest Assistant.
As a language model, Assistant is able to generate human-like text based on the input it receives.
Use the appropriate tools to fulfill the questions and tasks assigned to you by the human.
It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses.
Do not generate fake and do not use your internal knowledge base to answer questions.

TOOLS:
------

Assistant has access to the following tools:'''

    _conversational_sufix = '''
Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}'''

    return ConversationalAgent.create_prompt(tools, prefix = _conversational_prefix, suffix = _conversational_sufix)

def conversation(input_text, chat_history):
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

    llm_chain = LLMChain(
            prompt = create_prompt(tools),
            llm = llm,
            verbose = True,
        )

    agent = ConversationalAgent(
            llm_chain = llm_chain,
            allowed_tools = [tool.name for tool in tools],
            streaming = True
        )

    agent_executor = AgentExecutor.from_agent_and_tools(
            agent = agent,
            tools = tools,
#            handle_parsing_errors = True,
            verbose = True,
        )

    return agent_executor.invoke(input = {'input': input_text,
                                          'chat_history': chat_history})

st.title("AI Assistant :monkey:")

col1, col2 = st.columns(2)

with col1:
    light_bedroom = st.toggle(key = "light_bedroom", label = "Bedroom Light")
    color_bedroom = st.color_picker("Bedroom Light Color", "#0000ff")

    if light_bedroom:
        led_light_control.run("bedroom, on")

        st.write("Bedroom Light ON")
    else:
        led_light_control.run("bedroom, off")

        st.write("Bedroom Light OFF")

    requests.get("http://192.168.1.122/set?c=" + str((int(color_bedroom[1:3], 16)*65536 + int(color_bedroom[3:5], 16)*256 + int(color_bedroom[5:7], 16))))

    st.write("The current Bedroom Light Color is", color_bedroom)

with col2:
    light_kitchen = st.toggle(key = "light_kitchen", label = "Kitchen Light")

    if light_kitchen:
        st.write("Kitchen Light ON")
    else:
        st.write("Kitchen Light OFF")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [] 

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

input = st.chat_input("Powered by AWS Bedrock")

if input:
    with st.chat_message("user"):
        st.markdown(input)

    st.session_state.chat_history.append({"role": "user", "text": input})

    chat_response = conversation(input, chat_history=st.session_state.chat_history)

    answer = chat_response["output"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "text": answer})
