#ActinableItem , Decision, Questions
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os 



def getllm():
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.2
    )

llm = getllm()

def build_prompt(system_prompt: str):
    return( RunnablePassthrough() | RunnableLambda(lambda x: {'text': x}) | ChatPromptTemplate([
        ("system", system_prompt),
        ("human", "{text}")
    ]) | llm | StrOutputParser()
    )

# Extract action items
def extract_action_items(transcribe: str) -> str:
    chain = build_prompt(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all action items. For each item include:\n"
        "- Task description\n"
        "- Owner (who is responsible)\n"
        "- Deadline (if mentioned, else write 'not specified')\n"
        "Format as a numbered list. If none found, say 'No action items found.'"
    )
    return chain.invoke(transcribe)

#extract key decisions
def extract_key_decisions(transcribe: str)-> str:
    chain = build_prompt(
        "You are an expert meeting analyst. From the meeting transcript, "
        "extract all key decisions made. Format as a numbered list. "
        "If none found say 'No key decisions found.'"
    )
    return chain.invoke(transcribe)


#extract Questions

def extract_questions(transcribe: str)-> str:
    chain = build_prompt(
        "From the meeting transcript, extract all unresolved questions "
        "or topics needing follow-up. Format as a numbered list. "
        "If none found say 'No open questions found.'"
    )

    return chain.invoke(transcribe)


