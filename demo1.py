import easyocr
import streamlit as st
import openai

from PIL import Image
import cv2
import numpy as np
import time
import os
import speech_recognition as sr



lang_map = {
    "한국어": "ko",
    "영어": "en",
    "스페인어": "spa",
    "프랑스어": "fra",
    "이탈리아어": "ita",
    "태국어": "tha",
    '일본어':'jpn'

}

def process_image(file, tesseract_lang):   # we change the format of the language input later
    img = Image.open(file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    # Convert to RGB
    image = np.array(img)
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
    reader = easyocr.Reader(tesseract_lang) # this needs to run only once to load the model into memory
    text = reader.readtext(image, detail = 0, paragraph=True)
    st.text(text)
    return text

# def process_speech():
#     r = sr.Recognizer()
#     audio = ""
#     with sr.Microphone() as source:
#         st.text("무엇을 도와드릴까요?")
#         try:
#             speech = r.listen(source)
#             time.sleep(5)
#             #noise 제거
#             r.adjust_for_ambient_noise(source)
#         except sr.WaitTimeoutError:
#             st.text("Timeout error occurred")
#             return ""

#     try:    
#         audio = r.recognize_google(speech, language="ko-KR")
#         st.text("Your speech thinks like\n " + audio)
        
#     except sr.UnknownValueError:
#         st.text("Your speech can not understand")
#     except sr.RequestError as e:
#         st.text("Request Error!; {0}".format(e))
#     return audio

def process_speech():
    audio = "what is it?"
    st.text("Virtual Speech : What is it?")
    return audio


def process_chatgpt(audio, text):
    # https://www.daleseo.com/chatgpt-python/
    #API 입력
    openai.api_key = 'aaa'
    st.text(audio)
    st.text(text)
    input_text = ['한국어로 대답해줘']+ [audio] + text
    input_text = ' '.join(input_text)
    st.text(input_text)
    

    model = "gpt-3.5-turbo" # https://platform.openai.com/docs/api-reference/chat/create
        
        # 질문 작성하기
    # query = "텍스트를 입력받아 이미지를 생성하는 방법을 알려주세요."
        
        # 메시지 설정하기
    messages = [
                # {"role": "system", "content": "input_text"},
                {"role": "user", "content": "input_text"}
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
   
lang_choice = st.selectbox("Choose the language of the text", list(lang_map.keys()))
tesseract_lang = [lang_map[lang_choice] , 'en']

uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg'])


if "audio_text" not in st.session_state:
    st.session_state.audio_text = ""

if "image_text" not in st.session_state:
    st.session_state.image_text = ""

if uploaded_file is not None:
    if st.checkbox('Process Image'):
        st.session_state.image_text = process_image(uploaded_file,tesseract_lang)

if st.checkbox('Process Speech'):
    st.session_state.audio_text = process_speech()

if st.checkbox('Process BardAPI'):
    process_chatgpt(st.session_state.audio_text, st.session_state.image_text)

