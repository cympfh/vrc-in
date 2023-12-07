import logging

from fastapi import FastAPI
from pydantic import BaseModel

from util.mount import MountFiles
from util.translate import Translate

app = FastAPI()
logger = logging.getLogger("uvicorn")


class SubmitData(BaseModel):
    text: str
    translate_en: bool
    translate_zh: bool
    translate_ko: bool
    translate_ja: bool


@app.post("/api/submit")
async def submit(data: SubmitData):
    targets = []
    if data.translate_en:
        targets.append("en")
    if data.translate_zh:
        targets.append("zh")
    if data.translate_ko:
        targets.append("ko")
    if data.translate_ja:
        targets.append("ja")

    if len(targets) > 0:
        translated = Translate().run(data.text, targets)
    else:
        translated = None

    text = data.text
    if translated:
        text = translated + " / " + data.text

    return {
        "status": "ok",
        "targets": targets,
        "text": text,
    }


app.mount("/", MountFiles(directory="web/public", html=True), name="static")
