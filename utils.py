from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import UploadFile


async def get_multiple_documents(uploaded_files: list[UploadFile]) -> dict[str, int]:
    """split documents into chunks

    :param uploaded_files:
    """
    print(f"uploaded files length:{len(uploaded_files)}, type: {type(uploaded_files)}")
    text = ""
    for uploaded_file in uploaded_files:
        print(f"current: {uploaded_file}, type:{type(uploaded_file)}")
        pdf_reader = PdfReader(uploaded_file.file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20, length_function=len)

    chunks = text_splitter.split_text(text)

    print(f"number of chunks: {len(chunks)}")
    for i in range(0,3):
        print(f"chunk: {i}: {chunks[i]}")
    return {"number of chunks": len(chunks)}


async def get_document(uploaded_file) -> dict[str, int]:
    """split documents into chunks

    :param uploaded_files:
    """
    print(f"uploaded file, type: {type(uploaded_file)}")
    text = ""
    pdf_reader = PdfReader(uploaded_file.file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20, length_function=len)
    chunks = text_splitter.split_text(text)
    return {"number of chunks": len(chunks)}