from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import google_sheet_pusher
import message_parser
import json

app = FastAPI()

interesting_groups = [
    "טרמפיסטים #2 עוזרים לחיילים",
    "טרמפיסטים 1# עוזרים לחיילים",
    "guyandroi",
    "test"
]
par = message_parser.MessageParser()
config = json.load(open("/root/whatsapp_google_sheet_integration/config.json", "rb"))
sheet_pusher = google_sheet_pusher.SpreadSheetCommunicator(config)


class MessageRequest(BaseModel):
    group_id: str
    group_name: str
    message: str
    phone_number: str
    stopped: bool


@app.post("/")
async def process_message(message_request: MessageRequest):
    try:
        # not an interesting group
        if message_request.group_name not in interesting_groups:
            return {"ack_needed": False}

        # message parsed successfully
        if handled_message(message_request.message, message_request.stopped):
            return {"ack_needed": True}

        # couldnt parse the message
        return {"ack_needed": False}

    except Exception as exc:
        logging.error(f"Failed to process message request: {message_request}")
        raise HTTPException(status_code=500, detail=str(exc))


def handled_message(message, stopped = True):
    try:
        message_dict = par.pattern_match(message)
        logging.info(f"Parsed message: {message_dict}")

        sheet_pusher.communicate_message(message_dict, stopped)

        return True

    except ValueError as exc:
        # Couldn't parse the message
        logging.error(f"Failed to parse message: {message}")
        logging.error(f"Error: {exc}")
        return False


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=2001)
