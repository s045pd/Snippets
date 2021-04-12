from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import List

app = FastAPI()


@app.get("/maps/")
async def api_map():
    return {
        _.path: {"name": _.name, "desc": getattr(_, "description", "")}
        for _ in app.routes
    }


@app.post("/single/")
async def single_files(file: UploadFile = File(...)):
    def stream_process(file):
        for line in file.file:
            ...
            yield line
    return StreamingResponse(stream_process(file))


@app.post("/multiple/")
async def multiple_files(files: List[UploadFile] = File(...)):
	return [_.file for _ in files]


# uvicorn api:app
# upload single file
# curl -N -F "file=@A.csv" 127.0.0.1/single/

# upload multiple files
# curl -N -F "files=@xx.txt" -F "files=@xxx.txt"   127.0.0.1/multiple/