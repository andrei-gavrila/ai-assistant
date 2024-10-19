import streamlit as st

st.title("AI Assistant :monkey:")

col1, col2 = st.columns(2)

with col1:
    light_bedroom = st.toggle(key = "light_bedroom", label = "Bedroom Light")
    color_bedroom = st.color_picker("Bedroom Light Color", "#0000ff")

    if light_bedroom:
        st.write("Bedroom Light ON")
    else:
        st.write("Bedroom Light OFF")

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

input = st.chat_input("Powered by AWS Bedrock LLAMA2")

if input:
    with st.chat_message("user"):
        st.markdown(input)

    st.session_state.chat_history.append({"role": "user", "text": input})

    chat_response = {"output": "input was: " + input}

    answer = chat_response["output"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append({"role": "assistant", "text": answer})
