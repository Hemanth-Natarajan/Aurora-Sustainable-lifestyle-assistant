import streamlit as st
import streamlit as st
import base64
import os
import time
from groq import Groq
from pinecone import Pinecone, ServerlessSpec
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch




# Load the tokenizer and model

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
    
def generate_response(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def display_typing_effect(text, role="assistant"):
    message_placeholder = st.empty()  # Create an empty placeholder for messages
    current_text = ""
    for char in text:
        current_text += char
        message_placeholder.markdown(f"**{role}:** {current_text}")  # Update placeholder content
        time.sleep(0.005)  # Simulate typing delay
    return current_text

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

background_image = get_base64_image("C:\\Users\\TUF GAMING\\Downloads\\wallpaperflare.com_wallpaper.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    @keyframes flyIn {
        0% {
            transform: translateX(-100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0%);
            opacity: 1;
        }
    }
    
    .glowing-fade-title {
        font-family: 'Roboto', sans-serif; /* Use the custom font */
        color: #FFFFF;
        font-size: 3em;
        text-align: center;
        opacity: 0; /* Start hidden */
        animation: fadeInGlow 1s forwards, glow 1.5s infinite alternate;
        animation-delay: 2.5s; 
    }

    .subheading {
        animation: flyIn 2s ease-out forwards; /* Forward so it maintains the final state */
        color: #808080;
        text-align: center;
        font-size: 1.5em;
        opacity: 0; /* Start hidden */
        animation-delay: 2.5s; 
    }

    @keyframes fadeInGlow {
        0% {
            opacity: 0;
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #FFE5B4, 0 0 20px #FFE5B4, 0 0 25px #FFE5B4, 0 0 30px #FFE5B4, 0 0 35px #FFE5B4;
        }
        100% {
            opacity: 1;
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #FFE5B4, 0 0 40px #FFE5B4, 0 0 50px #FFE5B4, 0 0 60px #FFE5B4, 0 0 70px #FFE5B4;
        }
    }

    @keyframes glow {
        0% {
            text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #FFE5B4, 0 0 40px #FFE5B4, 0 0 50px #FFE5B4, 0 0 60px #FFE5B4, 0 0 70px #FFE5B4;
        }
        100% {
            text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #FFE5B4, 0 0 20px #FFE5B4, 0 0 25px #FFE5B4, 0 0 30px #FFE5B4, 0 0 35px #FFE5B4;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Title
st.markdown("<h1 class='glowing-fade-title'>Aurora</h1>", unsafe_allow_html=True)

# Subheading
st.markdown("<h2 class='subheading'>Your personal guidance to a sustainable lifestyle</h2>", unsafe_allow_html=True)


conversation_history = ""

def generate_response_with_context(user_input):
    global conversation_history
    conversation_history += f"User: {user_input}\n"
    response = generate_response(conversation_history)
    conversation_history += f"Bot: {response}\n"
    return response


st.markdown("""
    <style>
    .glowing-box {
        border-radius: 30px;
        padding: 30px;
        background-color: #FFFFF;
        color: white;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.6), 0 0 30px rgba(255, 255, 255, 0.4), 0 0 40px rgba(255, 0, 255, 0.3);
        transition: box-shadow 0.3s ease-in-out;
    }

    .glowing-box:hover {
        box-shadow: 0 0 40px rgba(255, 255, 255, 0.8), 0 0 60px rgba(255, 0, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

client = Groq(
    # This is the default and can be omitted
    api_key="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",
)
pc = Pinecone("52eb674a-0527-4ccb-80b5-baacd6e6a1e7")
index = pc.Index("quickstart")

st.session_state.api_key = "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"

# Only show the API key input if the key is not already set
if not st.session_state.api_key:
    # Ask the user's API key if it doesn't exist
    api_key = st.text_input("Enter API Key", type="password")
    
    # Store the API key in the session state once provided
    if api_key:
        st.session_state.api_key = api_key
        st.rerun()  # Refresh the app once the key is entered to remove the input field
else:
    # If the API key exists, show the chat app
    # Center the title using HTML and Markdown
    
    

    # Initialize the chat message list in session state if it doesn't exist
    if "chat_messages" not in st.session_state:
        st.session_state.groq_chat_messages = [{"role": "system", "content": "You are Aurora, an ai chatbot made specifically for providing information related to sustainable lifestyle . You are required to answer for all the questions or queries asked by user. If enough information isn't provided by the user ,you are required to ask the user for appropriate queries, but if the user greets you or thanks you, respond them nicely.Also if the user asks questions other than sustainable lifestyle , give answers for those too but remember you are an ai chatbot specifically designed for assisting the user for having a sustainable lifestyle"}]
        st.session_state.chat_messages = []
        
    # Display previous chat messages
    for messages in st.session_state.chat_messages:
        if messages["role"] in ["user", "assistant"]:
            with st.chat_message(messages["role"]):
                st.markdown(messages["content"])
    
    # Define a function to simulate chat interaction (you would replace this with an actual API call)
    def get_chat():
        embedding = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[st.session_state.chat_messages[-1]["content"]],
            parameters={
                "input_type": "query"
            }
        )
        results = index.query(
            namespace="ns1",
            vector=embedding[0].values,
            top_k=3,
            include_values=False,
            include_metadata=True
        )
        context = ""
        for result in results.matches:
            if result['score'] > 0.8:
                context += result['metadata']['text']
            
        st.session_state.groq_chat_messages[-1]["content"] = f"User Query: {st.session_state.chat_messages[-1]['content']} \n Retrieved Content (optional): {context}"
        chat_completion = client.chat.completions.create(
            messages=st.session_state.groq_chat_messages,
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content

    # Handle user input
    if prompt := st.chat_input("Ask Aurora someting or say hi to her"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.session_state.groq_chat_messages.append({"role": "user", "content": prompt})
        # Get the assistant's response (in this case, it's just echoing the prompt)
        with st.spinner("Aurora is working on it.."):
            response = get_chat()
        with st.chat_message("Aurora"):
            final_response = display_typing_effect(response)

           
   
        
        
        # Add user message and assistant response to chat history
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.session_state.groq_chat_messages.append({"role": "assistant", "content": response})

     