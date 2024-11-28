#!/usr/bin/env python
# coding: utf-8

import getpass
import os

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key:")

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama3-8b-8192",        # Using LLaMA 3.0 8B model or LLaMA 3B as needed
    temperature=0.3,                # Lower temperature for deterministic, focused output
    max_tokens=500,                 # Moderate token limit for concise, detailed answers
    max_retries=3,                  # Retries up to 3 times in case of failure
    timeout=60,                     # 60 seconds to allow for complex tasks        
)

system_message = """
You are a health assistant trained to provide accurate information on health-related topics.
Your tasks include:

1. Providing information on medical conditions, treatments, and wellness.
2. Offering advice on fitness, nutrition, and general health concerns.
3. Addressing queries related to mental health and emotional well-being.

Your Goals:
- Answer health-related questions with accuracy, based on reliable medical information.
- Avoid responding to non-health-related queries, such as entertainment, technology, or unrelated topics.
- Always prioritize user safety and well-being in your responses.
- Do not provide advice on any non-health-related matters.
-Answer in one or two lines (concise and to the point).
"""

from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        ("human", "Please respond to the following health-related query: {task_description}"),
    ]
)
chain = prompt | llm

def get_response_with_dynamic_chain(prompt):
    conversation_history = ""
    
    # Append the user prompt to the conversation history
    conversation_history += f"User: {prompt}\n"
    
    # Get the model's response
    response = chain.invoke(conversation_history)
    
    # Append the model's response to the conversation history
    conversation_history += f"Assistant: {response.content}\n"
    
    # Return the response content
    return response.content




