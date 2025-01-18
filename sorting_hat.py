import streamlit as st

st.set_page_config(page_title="재미로 하는 뜨개인 테스트", page_icon="🧶", layout="centered")

QUESTIONS = [
    "나는 뜨개질로...",
    "왠지 마음이 끌리는 편물은?",
    "나는 무언가에 도전할 때...",
]


STITCH_IMAGES = {
    "짧은뜨기": "assets/crochet.jpg",
    "메리야스": "assets/knit.jpeg",
}

GRIP_IMAGES = {
    "아메리칸": "assets/american.gif",
    "컨티넨탈": "assets/continental.gif",
    "펜 그립": "assets/pen_grip.jpeg",
    "나이프 그립": "assets/knife_grip.jpeg"
}

OPTIONS = [
    ["스웨터나 가디건 👕을 만들고 싶어!", "키링이나 가방 👜을 만들고 싶어!"],
    ["짧은뜨기", "메리야스"],
    ["이왕이면 빨리빨리 🐰 해보고 싶어!", "느려도 괜찮아 🐢 언젠가 완성하겠지!"],
]

HOUSES = {
    "대바늘": 0,
    "코바늘": 0,
}

KNITTING_STYLES = {
    "대바늘": ["아메리칸", "컨티넨탈"],
    "코바늘": ["나이프 그립", "펜 그립"]
}


def initialize_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "quiz"  # quiz, wand, style, result, hidden
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "house_points" not in st.session_state:
        st.session_state.house_points = HOUSES.copy()
    if "house_type" not in st.session_state:
        st.session_state.house_type = None
    if "wand_type" not in st.session_state:
        st.session_state.wand_type = None
    if "knitting_type" not in st.session_state:
        st.session_state.knitting_type = None


def reset_quiz():
    st.session_state.page = "quiz"
    st.session_state.current_question = 0
    st.session_state.house_points = HOUSES.copy()
    st.session_state.house_type = None
    st.session_state.wand_type = None
    st.session_state.knitting_type = None

def show_stitch_option(col, stitch_name):
    col.image(STITCH_IMAGES[stitch_name], use_container_width=True)
    if col.button("💗", key=f"select_{stitch_name}"):
        if stitch_name == "짧은뜨기":
            st.session_state.house_points["코바늘"] += 1
        else:
            st.session_state.house_points["대바늘"] += 1
        handle_question_answered()


def show_grip_option(col, grip_name):
    col.image(GRIP_IMAGES[grip_name], use_container_width=True)
    if col.button("💗", key=f"select_{grip_name}"):
        st.session_state.knitting_type = grip_name
        st.session_state.page = "result"
        st.rerun()


def show_quiz():
    st.title("재미로 하는 뜨개인 테스트 🧶")
    st.subheader(QUESTIONS[st.session_state.current_question])

    current_options = OPTIONS[st.session_state.current_question]

    if st.session_state.current_question == 1:
        col1, col2 = st.columns(2)
        with col1:
            show_stitch_option(col1, "짧은뜨기")
        with col2:
            show_stitch_option(col2, "메리야스")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(current_options[0], key=f"option1_{st.session_state.current_question}"):
                if st.session_state.current_question == 0:
                    st.session_state.house_points["대바늘"] += 1
                else:
                    st.session_state.house_points["코바늘"] += 1
                handle_question_answered()
        with col2:
            if st.button(current_options[1], key=f"option2_{st.session_state.current_question}"):
                if st.session_state.current_question == 0:
                    st.session_state.house_points["코바늘"] += 1
                else:
                    st.session_state.house_points["대바늘"] += 1
                handle_question_answered()


def handle_question_answered():
    if st.session_state.current_question < len(QUESTIONS) - 1:
        st.session_state.current_question += 1
    else:
        sorted_houses = sorted(
            st.session_state.house_points.items(),
            key=lambda x: x[1],
            reverse=True
        )
        st.session_state.house_type = sorted_houses[0][0]
        st.session_state.page = "wand"
    st.rerun()


def show_wand_selection():
    st.title("재미로 하는 뜨개인 테스트 🧶")
    st.subheader("이상하게 더 끌리는 바늘은?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("부드럽고 포근한 나무 🪵", key="wand_wood"):
            st.session_state.wand_type = "나무바늘"
            st.session_state.page = "style"
            st.rerun()
    with col2:
        if st.button("매끄럽고 튼튼한 스틸 🪙", key="wand_steel"):
            st.session_state.wand_type = "스틸바늘"
            st.session_state.page = "style"
            st.rerun()


def show_style_selection():
    st.title("재미로 하는 뜨개인 테스트 🧶")
    st.subheader("뜨개질 마법, 어떻게 해볼까?")

    styles = KNITTING_STYLES[st.session_state.house_type]
    col1, col2 = st.columns(2)

    with col1:
        show_grip_option(col1, styles[0])
    with col2:
        show_grip_option(col2, styles[1])

def show_result():
    if (
            st.session_state.house_type == "대바늘" and
            st.session_state.wand_type == "스틸바늘" and
            st.session_state.knitting_type == "컨티넨탈"
    ):
        st.session_state.page = "hidden"
        st.rerun()

    st.title("당신은 이런 뜨개인이에요!")
    st.image("assets/knitters_high.jpg")

    st.markdown(
        f"""
            🎩 **<u>{st.session_state.house_type}</u>** 뜨개로 시작해 보는 건 어떨까요? 

            🪄 운명의 바늘은 **<u>{st.session_state.wand_type}</u>** 이예요.  

            💗 **<u>{st.session_state.knitting_type}</u>** 방법으로 바늘을 잡아보는 걸 추천해요!
            """,
        unsafe_allow_html=True
    )

    if (
            st.session_state.house_type == "대바늘" and
            st.session_state.wand_type == "스틸바늘" and
            st.session_state.knitting_type == "컨티넨탈"
    ):
        st.session_state.page = "hidden"
        st.rerun()

    if st.button("다시 시작하기"):
        reset_quiz()
        st.rerun()

def hidden_page():
    st.title("🍀저랑 통하셨군요!")
    st.image("assets/winner.png")
    st.markdown(
        f"""
                저도 <u>{st.session_state.house_type}</u> 뜨개를 가장 좋아해요!
                
                <u>{st.session_state.wand_type}</u>이 제 손에 맞아서 바늘 세트를 들였어요 😎
                
                <u>{st.session_state.knitting_type}</u> 기법을 가장 많이 써요. 가끔은 플리킹도..!
                """,
        unsafe_allow_html=True
    )

    if st.button("다시 시작하기"):
        reset_quiz()
        st.rerun()


def main():
    initialize_session_state()

    # Route the app to the appropriate page
    if st.session_state.page == "quiz":
        show_quiz()
    elif st.session_state.page == "wand":
        show_wand_selection()
    elif st.session_state.page == "style":
        show_style_selection()
    elif st.session_state.page == "result":
        show_result()
    elif st.session_state.page == "hidden":
        hidden_page()


if __name__ == "__main__":
    main()