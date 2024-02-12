import streamlit as st
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os
import cohere
from cohere.responses.chat import StreamEvent
import random
import time
co = cohere.Client(os.environ.get("COHERE_API_KEY"))
st.title("William's bot")
# with st.chat_message("user"):
#     st.write("hello")
#     st.bar_chart(np.random.rand(30,3))
def response_generator():
    responses=[
        "Hello there!How can i assist you today",
        "I'm there to help,What do you need",
        "Hey! what can i do for u"
        "Hi what do you need help with me"

    ]
    response  = random.choice(responses)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
def cohere_res_generator(prompt):
    chat_history = list(map(lambda x:{
        "user_name": "user" if x["role"]=="user" else "Chatbot",
        "text": x["content"]
        },st.session_state.messages))
    for event in co.chat(
        message=f"{prompt}.Answer in less than 20 words",
        chat_history=chat_history,
        stream=True):
        if event.event_type == StreamEvent.TEXT_GENERATION:
            yield event.text
        elif event.event_type == StreamEvent.STREAM_END:
            return""
def cohere_response_generator(prompt):
    for event in co.chat(prompt,stream=True):
        if event.event_type == StreamEvent.TEXT_GENERATION:
            yield event.text
        elif event.event_type == StreamEvent.STREAM_END:
            return""

#intialize a chat history
if "messages" not in st.session_state:
    st.session_state.messages=[]

#Display the chat messgaes from the chat history
for message in st.session_state.messages:
    # st.write(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something...,") :
    #Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    #Add the user message to the chat history
    st.session_state.messages.append({"role":"user","content":prompt})
    response  = f"Echo : {prompt}"


    #Diplay the assistant reponse in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(cohere_response_generator(prompt))
        #stream = co.chat(prompt, streamimg=True)
    #Add the assistant response to the chat history
        st.session_state.messages.append( {"role": "assistant", "content": response} )

    
    
    
    # user_message = st.chat_message("user")
    # user_message.write(prompt)