import streamlit as st
import random
import voice
import trans


if st.session_state.get("memoing") == None:
    st.session_state["memoing"] = False
if "word_audios" not in st.session_state:
    st.session_state["word_audios"] = {}
if "index" not in st.session_state:
    st.session_state["index"] = 0
else:
    if st.session_state["index"] >= len(st.session_state["words"]):
        st.session_state["index"] = 0
        st.session_state["memoing"] = False
if "translate_result" not in st.session_state:
    st.session_state["translate_result"] = {}

with st.expander(
    "All words",
):
    words_input = st.text_area(
        "",
        placeholder="input words, saperate by new line or ,",
        value=", ".join(st.session_state.get("words") or []),
    )

    def on_words_input_complete():
        s_words = [
            word.strip() for i in words_input.split("\n") for word in i.split(",")
        ]
        s_words = list(filter(lambda x: x != "" and x.isalnum, s_words))

        random.shuffle(s_words)
        st.session_state["words"] = s_words
        st.session_state["index"] = 0
        st.session_state["results"] = {}
        st.session_state["memoing"] = False

    st.button("complete", on_click=on_words_input_complete)


class Memoer:
    ModeENtoNative = 1
    ModeENVoiceToEN = 2
    ModeNativeToEN = 3

    def __init__(self, native_language="zh") -> None:
        self.mode = st.session_state.mode
        self.native_language = native_language

    def gen(self):
        if st.session_state.index >= len(st.session_state.words):
            return None
        batch_words = st.session_state.words[
            st.session_state.index : st.session_state.index
            + st.session_state.batch_size
        ]
        for index, word in enumerate(batch_words):
            result = self.component(index, word)
            st.session_state.results[word] = result
        return batch_words

    def component(self, index, word):
        if self.mode == self.ModeENtoNative:
            pass
        elif self.mode == self.ModeENVoiceToEN:
            if word not in st.session_state.word_audios:
                st.session_state.word_audios[word] = voice.text_to_speech(word)
            data = st.session_state.word_audios[word]
            st.audio(data, format="audio/mp3")
        elif self.mode == self.ModeNativeToEN:
            if word not in st.session_state.translate_result:
                st.session_state.translate_result[word] = trans.translate_en_to_zh(word)
            return st.text_input(label=st.session_state.translate_result[word])
        return st.text_input(
            label=word
            if self.mode == self.ModeENtoNative
            else str(st.session_state.index + index)
        )


with st.sidebar:
    st.slider(
        "batch size", key="batch_size", min_value=3, max_value=10, step=1, value=3
    )
    st.selectbox(
        "mode",
        options=[Memoer.ModeENtoNative, Memoer.ModeENVoiceToEN, Memoer.ModeNativeToEN],
        format_func=lambda x: {
            Memoer.ModeENtoNative: "EN to Native",
            Memoer.ModeENVoiceToEN: "EN Voice to EN",
            Memoer.ModeNativeToEN: "Native to EN",
        }[x],
        key="mode",
    )

    def on_start_click():
        st.session_state["memoing"] = True
        st.session_state["index"] = 0

    st.button("start memo!", on_click=on_start_click)


if st.session_state.memoing == True:
    percent = st.session_state.index / len(st.session_state.words)
    st.progress(
        percent if percent <= 1 else 1.0,
        text=f"progress {st.session_state.index if st.session_state.index < len(st.session_state.words) else len(st.session_state.words)} / {len(st.session_state.words)}",
    )
    memoer = Memoer()
    batch_words = memoer.gen()
    if batch_words:
        now_index = st.session_state.index + len(batch_words)
        if now_index < len(st.session_state.words):

            def next_click():
                st.session_state.index = st.session_state.index + len(batch_words)

            st.button("next", on_click=next_click)
        else:

            def on_done_click():
                st.session_state.memoing = False
                st.table(data=st.session_state.results.items())

            st.button("done", on_click=on_done_click)
