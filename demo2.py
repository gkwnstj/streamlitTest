import easyocr
import streamlit as st
import openai

from PIL import Image
import cv2
import numpy as np
import time
import os
import speech_recognition as sr


# Language List
# https://www.jaided.ai/easyocr/

lang_map = {
    "한국어": "ko",
    "영어": "en",
    "스페인어": "es",
    "프랑스어": "fr",
    "이탈리아어": "it",
    "태국어": "th",
    '일본어':'ja'

}

lang_list = ["ko", "en", "es", "fr", "it", "th", "ja"]

def process_image(tesseract_lang):   # we change the format of the language input later
    # img = Image.open(file)
    # st.image(img, caption="Uploaded Image", use_column_width=True)
    st.text("Processing...")
    
    # Convert to RGB
    image = np.array(img)
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
    reader = easyocr.Reader(tesseract_lang) # this needs to run only once to load the model into memory
    text = reader.readtext(image, detail = 0, paragraph=True)
    return text

# def process_speech():
#     audio = "-> 이 제품은 뭐야?"
#     st.text("Virtual Speech : -> 이 제품은 뭐야?")
#     return audio


def process_chatgpt(audio, text):
    st.text("Processing...")
    # https://www.daleseo.com/chatgpt-python/
    #API 입력
    openai.api_key = st.secrets["api_key"]
    # st.text("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")
    # st.text(audio)
    # st.text(text)
    input_text = ['한국어로 대답해줘. ']+ text + [" -> 이 제품은 뭐야?"]
    input_text = ' '.join(input_text)
    # input_text = st.text_area(input_text)
    # st.text(input_text)
    

    model = "gpt-3.5-turbo" # https://platform.openai.com/docs/api-reference/chat/create
        
        # 질문 작성하기
    # query = "텍스트를 입력받아 이미지를 생성하는 방법을 알려주세요."
        
        # 메시지 설정하기
    messages = [
                # {"role": "system", "content": "input_text"},
                {"role": "user", "content": input_text}
                ]
        
        # ChatGPT API 호출하기
    answer = openai.ChatCompletion.create(
                model=model,
                messages=messages
                )
    st.markdown(answer.choices[0].message.content)


    # response = bardapi.core.Bard().get_answer(input_text)
    # for i , choice in enumerate(response['choices']):
    #     li.append(choice['content'][0])
    # st.markdown(li[0])

image_text = ""
audio_text = ""
   
# lang_choice = st.selectbox("Choose the language of the text", list(lang_map.keys()))
# tesseract_lang = [lang_map[lang_choice] , 'en']  # It is impossible to adjust much more than 2. We have to consider about the combination all of them

uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg'])


if "audio_text" not in st.session_state:
    st.session_state.audio_text = ""

if "image_text" not in st.session_state:
    st.session_state.image_text = ""

a = []

if uploaded_file is not None:
    if st.checkbox('Process Image'):
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        # st.session_state.image_text = process_image(uploaded_file,[tesseract_lang, "en"])
        for i in range(7):
            try:
                b = st.session_state.image_text = process_image([lang_list[i], "en"])   # English is the global language, so it is adopted
                # st.text(st.session_state.image_text)
                a.append(b[0])
            except:
                st.text("Searching appropraite language")

        # st.text(a)
        # st.text(a)
        intp = ",".join(a)
        # st.text(intp)

        st.text("Done!")

# if st.checkbox('Process Speech'):
#     st.session_state.audio_text = process_speech()

if st.checkbox('Process ChatGPT_API'):
    process_chatgpt(st.session_state.audio_text, [intp])#st.session_state.image_text)
