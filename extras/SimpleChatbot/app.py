""" Simple Chatbot
@author: Nigel Gebodh
@email: nigel.gebodh@gmail.com

"""

import streamlit as st
from openai import OpenAI
import os
import sys
from dotenv import load_dotenv, dotenv_values
load_dotenv()





# initialize the client
client = OpenAI(
  base_url="https://api-inference.huggingface.co/v1",
  api_key=os.environ.get('HUGGINGFACEHUB_API_TOKEN')#"hf_xxx" # Replace with your token
) 




#Create supported models
model_links ={
    "Mistral":"mistralai/Mistral-7B-Instruct-v0.2",
    "Gemma-7B":"google/gemma-7b-it",
    "Gemma-2B":"google/gemma-2b-it",
    "Zephyr-7B-β":"HuggingFaceH4/zephyr-7b-beta",
    # "Llama-2":"meta-llama/Llama-2-7b-chat-hf"

}

#Pull info about the model to display
model_info ={
    "Mistral":
        {'description':"""The Mistral model is a **Large Language Model (LLM)** that's able to have question and answer interactions.\n \
            \nIt was created by the [**Mistral AI**](https://mistral.ai/news/announcing-mistral-7b/) team as has over  **7 billion parameters.** \n""",
        'logo':'https://mistral.ai/images/logo_hubc88c4ece131b91c7cb753f40e9e1cc5_2589_256x0_resize_q97_h2_lanczos_3.webp'},
    "Gemma-7B":        
        {'description':"""The Gemma model is a **Large Language Model (LLM)** that's able to have question and answer interactions.\n \
            \nIt was created by the [**Google's AI Team**](https://blog.google/technology/developers/gemma-open-models/) team as has over  **7 billion parameters.** \n""",
        'logo':'https://pbs.twimg.com/media/GG3sJg7X0AEaNIq.jpg'},
    "Gemma-2B":        
    {'description':"""The Gemma model is a **Large Language Model (LLM)** that's able to have question and answer interactions.\n \
        \nIt was created by the [**Google's AI Team**](https://blog.google/technology/developers/gemma-open-models/) team as has over  **2 billion parameters.** \n""",
    'logo':'https://pbs.twimg.com/media/GG3sJg7X0AEaNIq.jpg'},
    "Zephyr-7B":        
    {'description':"""The Zephyr model is a **Large Language Model (LLM)** that's able to have question and answer interactions.\n \
        \nFrom Huggingface: \n\
        Zephyr is a series of language models that are trained to act as helpful assistants. \
        [Zephyr 7B Gemma](https://huggingface.co/HuggingFaceH4/zephyr-7b-gemma-v0.1)\
        is the third model in the series, and is a fine-tuned version of google/gemma-7b \
        that was trained on on a mix of publicly available, synthetic datasets using Direct Preference Optimization (DPO)\n""",
    'logo':'https://huggingface.co/HuggingFaceH4/zephyr-7b-gemma-v0.1/resolve/main/thumbnail.png'},
    "Zephyr-7B-β":        
    {'description':"""The Zephyr model is a **Large Language Model (LLM)** that's able to have question and answer interactions.\n \
        \nFrom Huggingface: \n\
        Zephyr is a series of language models that are trained to act as helpful assistants. \
        [Zephyr-7B-β](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)\
        is the second model in the series, and is a fine-tuned version of mistralai/Mistral-7B-v0.1 \
        that was trained on on a mix of publicly available, synthetic datasets using Direct Preference Optimization (DPO)\n""",
    'logo':'https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha/resolve/main/thumbnail.png'},

}

def reset_conversation():
    '''
    Resets Conversation
    '''
    st.session_state.conversation = []
    st.session_state.messages = []
    return None
    



# Define the available models
models =[key for key in model_links.keys()]

# Create the sidebar with the dropdown for model selection
selected_model = st.sidebar.selectbox("Select Model", models)

#Create a temperature slider
temp_values = st.sidebar.slider('Select a temperature value', 0.0, 1.0, (0.5))


#Add reset button to clear conversation
st.sidebar.button('Reset Chat', on_click=reset_conversation) #Reset button


# Create model description
st.sidebar.write(f"You're now chatting with **{selected_model}**")
st.sidebar.markdown(model_info[selected_model]['description'])
st.sidebar.image(model_info[selected_model]['logo'])
st.sidebar.markdown("*Generated content may be inaccurate or false.*")




if "prev_option" not in st.session_state:
    st.session_state.prev_option = selected_model

if st.session_state.prev_option != selected_model:
    st.session_state.messages = []
    # st.write(f"Changed to {selected_model}")
    st.session_state.prev_option = selected_model
    reset_conversation()



#Pull in the model we want to use
repo_id = model_links[selected_model]


st.subheader(f'AI - {selected_model}')
# st.title(f'ChatBot Using {selected_model}')

# Set a default model
if selected_model not in st.session_state:
    st.session_state[selected_model] = model_links[selected_model] 

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# Accept user input
if prompt := st.chat_input(f"Hi I'm {selected_model}, ask me a question"):

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model_links[selected_model],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=temp_values,#0.5,
            stream=True,
            max_tokens=3000,
        )

        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})