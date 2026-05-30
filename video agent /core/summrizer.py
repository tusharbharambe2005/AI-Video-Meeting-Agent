from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from dotenv import load_dotenv
import os 

load_dotenv()


def getllm():
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.3
    )


def split_transcript(transcript: str)-> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= 3000,
        chunk_overlap = 200
    )
    return splitter.split_text(transcript)

#summarizer

def summarizer(transcript:str)->str:
    llm = getllm()

    map_prompt = ChatPromptTemplate.from_messages([
        ("system","summerizer the protion of a meeting transcript concisly and bullet point"),
        ("human", '{text}')
    ])

    map_chain = map_prompt | llm | StrOutputParser()
    chunks = split_transcript(transcript)

    chunk_summaries = [map_chain.invoke({"text": chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    combine_prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are the expert meeting summarizer. combine these summaries int oa single coherent bullet point summary"),
            ("human","{text}")
        ]
    )

    combine_chain = (
        RunnableLambda(lambda x: {"text": x}) | combine_prompt | llm | StrOutputParser()
    )

    return combine_chain.invoke(combined)



def generate_title(transcript:str)->str:
    llm = getllm()

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text":x}) | ChatPromptTemplate.from_messages([
            ("system", "You are an expert at crafting accurate, professional video titles. Generate a title no longer than 8 words based on the following transcript."),
            ("human", "{text}")
        ]) | llm | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])
    