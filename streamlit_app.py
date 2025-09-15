import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # 대화 메시지 리스트를 생성합니다.
            # 각 메시지는 'role'과 'content'로 이루어져 있습니다.
            messages = [
              {
                # 시스템 메시지는 모델의 기본 역할이나 성격을 정의합니다.
                # 모델에게 똑똑하고 창의적이라는 역할을 부여합니다.
                "role": "system",
                "content": 
                """
                당신은 테슬라 자동차의 매니저이며, 모든 메뉴얼에 대해서 설명할 수 있다.
                그리고, 자율주행 관련 최신뉴스를 제공할 수 있다. 
                추측성 답변은 할 수 없으며, 항상 확인된 정보를 제공하며 그 설명은 한글로만 제공하는 챗봇이다.  
                """
              },
              {
                "role": "assistant",
                "content":
                "답변은 항상 자연수를 사용하여 순번 1부터 시작한다."
                "두번째 답변은 순번 2로 시작한다.."
                "준비한 답변이 끝날때까지 순번을 사용한다."  
                },
              {
                # 'user'는 사용자가 모델에게 보내는 메시지를 나타냅니다.
                # 사용자가 '안녕하세요!'라고 인사합니다.
                    "role": "user",
                "content": 
                  "오토파일럿에 대해서 알려줘"
              }
            ],            
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
