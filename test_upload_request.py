import requests
import json
url = "http://127.0.0.1:8000/upload_body"
headers = {"X-API-Key":"1234"}

data = {
    "filenames": [
        "my_pdf1.pdf", 
        "my_pdf_2.pdf"
        ]}
files = [
    ('files', open("/path_to_pdf_1.pdf", "rb")),
    ('files', open("/path_to_pdf_2.pdf", "rb"))
]

response = requests.post(
    url=url,
    files=files,
    headers=headers,
    data=data
)

print(response.json())