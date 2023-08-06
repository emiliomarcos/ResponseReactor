import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

def run():
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    pdf_file = PyPDFLoader("./great_work.pdf")
    pdf_data = pdf_file.load()

    pdf_text = ""

    for page in pdf_data:
        pdf_text += page.page_content

    questions_text_splitter = TokenTextSplitter(model_name="gpt-3.5-turbo", chunk_size=10000, chunk_overlap=200)
    questions_text_chunks = questions_text_splitter.split_text(pdf_text)

    questions_documents = [Document(page_content=t) for t in questions_text_chunks]

    answers_text_splitter = TokenTextSplitter(model_name="gpt-3.5-turbo", chunk_size=500, chunk_overlap=100)
    answers_documents = answers_text_splitter.split_documents(questions_documents)

    questions_llm = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-3.5-turbo", temperature=0.5)

    prompt_template = """
    Take the role of an experienced creator of practice questions from study material. Aim to provide the most valuable questions for an exam
    from the following text:
    {text}
    Questions:
    """

    refine_prompt_template = """
    Take the role of an experienced creator of practice questions from study material. We have the following questions: {current_questions}
    Improve the questions if you find in necessary and if not just provide the original questions. We are trying to study the most valuable
    questions from the following text:
    {text}
    Questions:
    """

    questions_prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    refine_questions_prompt = PromptTemplate(template=refine_prompt_template, input_variables=["text", "current_questions"])
    questions_chain = load_summarize_chain(llm = questions_llm, chain_type="refine", verbose=True, question_prompt=questions_prompt, refine_prompt=refine_questions_prompt)

    questions = questions_chain(questions_documents)
    print(questions)
