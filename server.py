from typing import List
from fastapi import FastAPI, UploadFile, Depends, Request, HTTPException, status
from starlette.datastructures import FormData
import utils, oauth

app = FastAPI(title="pdf uploader")

async def get_body(request: Request):
    """check the content of the uploaded file

    :param Request request:
    :return _type_: _description_
    """
    content_type = request.headers.get('Content-Type')
    print(f"from server, content :{content_type}")
    if content_type is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Content-Type provided")
    elif content_type == "application/x-www-form-urlencoded" or content_type.startswith('multipart/form-data'):
        try:
            return await request.form()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Form data: {e}')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Content-Type not supported!')


@app.get("/", tags=["health check"])
async def root() -> dict[str, str]:
    return {"msg": "Hello World"}

@app.post('/upload_body', tags=["pdf upload"], dependencies=[Depends(oauth.api_auth_key)])
async def main(body = Depends(get_body)):
    """endpoint to upload pdf file(s)) with extra parameters

    :param body: pdf multi pages, filename

    :return: None
    """
    if isinstance(body, FormData):  # if Form/File data received
        files: list = body.getlist('files')  # returns a list of UploadFile objects
        filenames = body.get("filenames")
        print(f"filename: {filenames}")
        if files:
            await utils.get_multiple_documents(uploaded_files=files)
        return {"msg": f"file {filenames} successfully uploaded to server"}
    

@app.post("/uploadfile/", tags=["pdf upload"])
async def create_upload_file(file: UploadFile):
    """upload a single file

    :param UploadFile file:
    """
    res = await utils.get_document(uploaded_file=file)
    return {"filename": file.filename, "data": res}


@app.post("/uploadfiles/", tags=["pdf upload"])
async def create_upload_files(files: List[UploadFile]):
    """upload multiple files

    :param List[UploadFile] files:

    """
    res = await utils.get_multiple_documents(uploaded_files=files)
    return {"filenames": [file.filename for file in files], "data": res}
