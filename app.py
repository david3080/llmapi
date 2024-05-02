import openai
import streamlit as st

if "all_text" not in st.session_state:
    st.session_state.all_text = []

with st.sidebar:
    st.title("AIチャット")
    api_key = st.text_input("OPEN_AI_KEY", type="password")

if api_key:
    openai.api_key = api_key
    user_prompt = st.chat_input("user:")
    assistant_text = ""
    for text_info in st.session_state.all_text:
        with st.chat_message(text_info["role"], avatar=text_info["role"]):
            st.write(text_info["role"] + ":\n\n" + text_info["content"])

    if user_prompt:
        with st.chat_message("user", avatar="user"):
            st.write("user" + ":\n\n" + user_prompt)

        st.session_state.all_text.append({"role": "user", "content": user_prompt})

        if len(st.session_state.all_text) > 10:
            st.session_state.all_text.pop(1)

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.all_text,
            stream=True,
        )
        with st.chat_message("assistant", avatar="assistant"):
            place = st.empty()
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    assistant_text += content
                    place.write("assistant" + ":\n\n" + assistant_text)

        st.session_state.all_text.append(
            {"role": "assistant", "content": assistant_text}
        )
else:
    st.info("👈OPEN_AI_KEYを入力してください。")
