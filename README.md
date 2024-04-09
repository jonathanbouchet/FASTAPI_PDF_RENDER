# FASTAPI_PDF_RENDER
test of api endpoint for uploading pdf files on Render

There are 3 endpoints example:
- `upload_body`: 
    - upload multiple files with extra parameters
    - this endpoint has an `oauth` verification using `APIKeyHeader`
- `uploadfile`: upload 1 file
- `uploadfiles`: upload multiple files
    - `uploadfile` and `uploadfiles` can be used directly on `Swagger`. 


The motivation of `upload_body` is because when using a `post` request using the `UploadFile` class creates temporary names when the source of the pdf is not the current folder.
My use case was using `streamlit` where I needed to use the `NamedTemporaryFile` class that saved in memory the pdf file.

```python
uploaded_files = st.sidebar.file_uploader(
    label="Upload PDF files", type=["pdf"], 
    accept_multiple_files=True
    )
... 
for file in uploaded_files: 
    filenames.append(file.name)
    with NamedTemporaryFile(dir='.', suffix='.pdf') as f:
        print(f"original file :{file.name}, path: {Path(file.name).resolve()}")
        print(f"temporary file :{f.name}, path: {Path(f.name).resolve()}")
        f.write(file.getbuffer())
        filesToUpload.append(('files', open(f.name, 'rb')))
```

The example of a post request is in the `test_upload_request_example` script
In short, you pass a `data` dictionary containing the names and a `files` list containing the pdf buffers.
I've added the `X-API-Key` for later use.

```python
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
```