from flask import Flask, render_template
import concurrent.futures
from assets.Analyzer import summarizer
import assets.FileOperations as fo
# from assets.whisperRealtimeOffline import transcribe, load_model

from deepgram import Deepgram
from typing import Dict, Callable
import os
from flask_sockets import Sockets
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
import asyncio

  
WDS_SOCKET_PORT=0
app = Flask('aioflask')


# @app.route("/")
# def index():
#     return render_template("index.html")

@app.after_request
def add_header(response): # I know this is brute force. But I like brute force.
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/summary", methods=["GET"])
def get_summary():
    # return "1\n2\n3"
    return fo.get_file_contents("files/summary.txt", "summary")

@app.route("/transcript", methods=["GET"])
def get_transcript():
    transcript_file = fo.get_file_contents("files/transcript.txt")
    print(transcript_file)
    transcript_file = transcript_file.split(" ")
    return " ".join(transcript_file)

# DEEPGRAM START.
DEEPGRAM_API_KEY = 'fee4f0ae75f7f8a55637098f3b6db47d32d3a23b'
dg_client = Deepgram(DEEPGRAM_API_KEY)


async def process_audio(fast_socket: web.WebSocketResponse):
    async def get_transcript(data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']
        
            if transcript:
                await fast_socket.send_str(transcript)

    deepgram_socket = await connect_to_deepgram(get_transcript)

    return deepgram_socket

async def connect_to_deepgram(transcript_received_handler: Callable[[Dict], None]) -> str:
    try:
        socket = await dg_client.transcription.live({'punctuate': True, 'interim_results': False})
        socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, transcript_received_handler)

        return socket
    except Exception as e:
        raise Exception(f'Could not open socket: {e}')

@app.route('/')
def index():
    return render_template('index.html')

async def socket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request) 

    deepgram_socket = await process_audio(ws)

    while True:
        data = await ws.receive_bytes()
        deepgram_socket.send(data)
        
# DEEPGRAM END

def main():
    fo.get_settings()
    fo.clear_files()
    # model = load_model(fo.model_name)

    executor = concurrent.futures.ThreadPoolExecutor()
    # executor.submit(app.run, port=WDS_SOCKET_PORT)

    # Start the summarizer.
    executor.submit(summarizer, fo.openai_api_key, fo.summarize_threshold, fo.max_tokens, fo.max_lines)
    # transcribe(model, fo.pause_threshold)



    loop = asyncio.get_event_loop()
    aio_app = web.Application()
    wsgi = WSGIHandler(app)
    aio_app.router.add_route('*', '/{path_info: *}', wsgi.handle_request)
    aio_app.router.add_route('GET', '/listen', socket)
    web.run_app(aio_app, port=5555)


if __name__ == "__main__":
    main()