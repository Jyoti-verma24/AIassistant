








































import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def gemini_generate_summary(prompt_text, api_key, temperature=0.3):
    """
    Generates a summary using LangChain and the Gemini model,
    allowing for temperature control.
    """
    try:
        # Use the temperature value from the slider
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key, temperature=temperature)

        prompt = PromptTemplate.from_template(prompt_text)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        summary = chain.run({})
        return summary

    except Exception as e:
        print(f"GEMINI API ERROR: {e}")
        return f"⚠️ An error occurred with the AI model: {e}"

