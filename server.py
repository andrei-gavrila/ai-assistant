import streamlit as st

st.title("AI Assistant :monkey:")

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
