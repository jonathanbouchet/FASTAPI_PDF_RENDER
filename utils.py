from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from fastapi import UploadFile
from typing import List, Tuple, Dict
import re


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


def parse_pdf(file: UploadFile, filename: str) -> Tuple[List[str], str]:
    pdf = PdfReader(file.file)
    output = []
    print(f"{filename} -> {len(pdf.pages)}")
    for page in pdf.pages:
        text = page.extract_text()
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output, filename


def text_to_docs(text: List[str], filename: str) -> List[Document]:
    if isinstance(text, str):
        text = [text]
    page_docs = [Document(page_content=page) for page in text]
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    doc_chunks: List[Document] = []
    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=20,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc.metadata["filename"] = filename  # Add filename to metadata
            doc_chunks.append(doc)
    return doc_chunks


async def create_vector_db(uploaded_files: list, filenames:list) -> Dict:
    documents = []
    for pdf_file, pdf_name in zip(uploaded_files, filenames):
        print(f"processing :{pdf_name}")
        text, filename = parse_pdf(pdf_file, pdf_name)
        print(f"text: {text}")
        print(f"filename: {filename}")
        documents = documents + text_to_docs(text, filename)
    print(f"number of documents: {len(documents)}")
    print(f"first doc")
    print(documents[-1])
    print(type(documents[0]))
    return {"number of chunks": len(documents), "sample chunk": documents[0]}