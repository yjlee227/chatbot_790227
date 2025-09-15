import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.title("💬 Chatbot")

# 테슬라 로고를 페이지 상단에 추가
tesla_logo_url = "https://upload.wikimedia.org/wikipedia/commons/e/e8/Tesla_logo.png"
st.image(tesla_logo_url, width=150)

st.write(
    "이것은 OpenAI의 GPT-3.5 모델을 사용하는 간단한 챗봇입니다. "
    "사용하려면 [여기](https://platform.openai.com/account/api-keys)에서 OpenAI API 키를 발급받아 입력해주세요. "
    "저희 튜토리얼을 따라 단계별로 이 앱을 만드는 방법을 배울 수도 있습니다: [튜토리얼 링크](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# 사용자에게 OpenAI API 키를 입력받음
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 추가해주세요.", icon="🗝️")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 대화 기록을 저장하는 세션 상태 변수 초기화
    # 앱 시작 시 시스템 및 어시스턴트 메시지를 한 번만 설정
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """
                당신은 테슬라 자동차의 매니저이며, 모든 메뉴얼에 대해서 설명할 수 있다.
                그리고, 자율주행 관련 최신뉴스를 제공할 수 있다.
                추측성 답변은 할 수 없으며, 항상 확인된 정보를 제공하며 그 설명은 한글로만 제공하는 챗봇이다.
                항상 즐거운 감정이 느껴질 수 있도록 답변한다.
                """
            },
            {
                "role": "assistant",
                "content": """
                안녕하세요! 테슬라 자동차 매니저입니다. 어떤 정보를 찾고 있으신가요?
                """
            }
        ]

    # 세션에 저장된 대화 메시지 표시 (시스템 메시지 제외)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"], avatar=tesla_logo_url if message["role"] == "assistant" else None):
                st.markdown(message["content"])

    # 사용자 입력 필드
    if prompt := st.chat_input("무엇을 도와드릴까요?"):

        # 사용자의 메시지를 대화 기록에 추가하고 화면에 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API로 응답 생성
        # 전체 대화 기록을 messages 변수에 전달합니다.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답을 스트리밍하고 대화 기록에 추가
        # 답변자 아바타로 테슬라 로고를 사용합니다.
        with st.chat_message("assistant", avatar=tesla_logo_url):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
