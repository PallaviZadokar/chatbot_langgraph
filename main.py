import os
import configparser
import random
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

config = configparser.ConfigParser()
config.read("config.ini")

groq_api_key = config["SETTINGS"].get("GROQ_API_KEY")
sendgrid_api_key = config["SETTINGS"].get("APIKEY")
sender_email = config["SETTINGS"].get("FROM")

ssl._create_default_https_context = ssl._create_unverified_context

if not sendgrid_api_key or not sender_email or not groq_api_key:
    print("Error: Missing API key(s). Check config.ini.")
    exit(1)

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_email: str
    otp: str
    otp_verified: bool


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(email, otp):
    subject = "Email Verification OTP"
    html_content = f"<p>Your OTP is: <strong>{otp}</strong></p>"
    message = Mail(from_email=sender_email, to_emails=email, subject=subject, html_content=html_content)
    
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        return "OTP sent successfully!"
    except Exception as e:
        return f"Error sending OTP: {e}"
    

def chatbot(state: State):
    response = llm.invoke(state['messages'])
    return {"messages": response}


def ask_for_email(state: State):
    last_message_obj = state["messages"][-1] if state["messages"] else None

    # Ensure it's a string (handle different object types)
    if hasattr(last_message_obj, "content"):
        last_message = last_message_obj.content.lower()
    else:
        last_message = str(last_message_obj).lower() if last_message_obj else ""

    trigger_keywords = ["historical places", "places to visit", "travel", "monument", "recommendation"]
    
    if any(keyword in last_message for keyword in trigger_keywords):
        email = input("Assistant: Would you like more details via email? \nUser: ")

        if email.lower() in ["no", "n", "skip"]:
            return {"messages": ["No worries! Have a great day!"]}

        state["user_email"] = email  # Store user email
        return {"messages": [f"Thanks! I'll send a verification code to {state['user_email']}."], "user_email": state["user_email"]}

    return {}


def send_otp_node(state: State):
    email = state.get("user_email")

    if not email:
        return {}

    otp = generate_otp()
    state["otp"] = otp  
    response = send_otp(email, otp)
    return {"messages": "I have sent a 6-digit code to your email. Please verify it.", "otp": otp}

def verify_otp(state: State):
    user_otp = input("Enter OTP: ")

    if user_otp == state['otp']:
        state['otp_verified'] = True
        return {"messages": "Great, OTP verified! I'll email you soon."}
    else:
        return {"messages": "Incorrect OTP. Please try again."}
    

    
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("ask_for_email", ask_for_email)
graph_builder.add_node("send_otp", send_otp_node)
graph_builder.add_node("verify_otp", verify_otp)

graph_builder.add_edge(START, "chatbot")  
graph_builder.add_edge("chatbot", "ask_for_email")  
graph_builder.add_edge("ask_for_email", "send_otp")  
graph_builder.add_edge("send_otp", "verify_otp")  
graph_builder.add_edge("verify_otp", END)

graph = graph_builder.compile()


while True:
    user_input = input("User: ")
    
    if user_input.lower() in ["quit", "q"]:
        print("Goodbye!")
        break
    
    state = {"messages": [("user", user_input)], "user_email": "", "otp": "", "otp_verified": False}
    
    for event in graph.stream(state):
        for value in event.values():
            if value and isinstance(value, dict) and "messages" in value and value["messages"]:
                if isinstance(value["messages"], list):
                    for msg in value["messages"]:
                        print("Assistant:", msg.content if hasattr(msg, "content") else msg)
                else:
                    print("Assistant:", value["messages"].content if hasattr(value["messages"], "content") else value["messages"])
