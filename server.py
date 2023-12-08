import logging
import subprocess

from fastapi import FastAPI
from pydantic import BaseModel
from pythonosc import udp_client

from util.mount import MountFiles
from util.translate import Translate

logger = logging.getLogger("uvicorn")


class VRC:
    def __init__(self, port: int = 9000):
        res = subprocess.run("ipwin", capture_output=True)
        ip = res.stdout.decode()
        logger.info("VRC.__init__; ip=%s, port=%s", ip, port)
        self.client = udp_client.SimpleUDPClient(ip, port)

    def send(self, message: str):
        logger.info("VRC.send_message; message=%s", repr(message))
        self.client.send_message("/chatbox/input", [message, True, True])


app = FastAPI()
vrc = VRC()


class SubmitData(BaseModel):
    text: str
    translate_en: bool
    translate_zh: bool
    translate_ko: bool
    translate_ja: bool


@app.post("/api/submit")
async def submit(data: SubmitData):
    data.text = data.text.strip()
    logger.info("data={%s}", data)

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
        translated = Translate().run(data.text, targets).strip()
    else:
        translated = None
    logger.info("translated=%s", repr(translated))

    text = data.text
    if translated:
        text = translated + " / " + data.text

    vrc.send(text)

    return {
        "status": "ok",
        "targets": targets,
        "text": text,
    }


app.mount("/", MountFiles(directory="web/public", html=True), name="static")
