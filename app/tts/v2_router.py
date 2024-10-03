import base64

import logging

from fastapi import APIRouter
from fastapi.responses import Response
from fastapi import HTTPException

from app import mq_connector, api_config
from . import Config, Speaker, Request, ErrorMessage, ResponseContent

LOGGER = logging.getLogger(__name__)

v2_router = APIRouter(tags=["v2"])


@v2_router.get('/', include_in_schema=False)
@v2_router.get('', response_model=Config, description="Get the configuration of available models and speakers.")
async def get_config():
    config = Config(speakers=[Speaker(
        name=name,
        languages=speaker.languages
    )
        for name, speaker in api_config.speakers.items()])
    return config


@v2_router.post('/', include_in_schema=False)
@v2_router.post('', response_class=Response,
                description="Submit a text-to-speech request.",
                responses={
                    200: {"content": {"audio/wav": {}}, "description": "Returns the synthesized audio."},
                    422: {"model": ErrorMessage},
                    408: {"model": ErrorMessage},
                    500: {"model": ErrorMessage}
                })
async def synthesis(body: Request):
    content, correlation_id = await mq_connector.publish_request(body, body.speaker)
    audio = base64.b64decode(content['audio'])
    response = Response(
        content=audio,
        media_type="audio/wav",
        headers={'Content-Disposition': f'attachment; filename="{correlation_id}.wav"'}
    )
    return response


@v2_router.post('/verbose', response_model=ResponseContent,
                description="Submit a text-to-speech request and return only some information about the output.",
                responses={
                    200: {"content": {"audio/wav": {}}, "description": "Returns the synthesized audio."},
                    422: {"model": ErrorMessage},
                    408: {"model": ErrorMessage},
                    500: {"model": ErrorMessage}
                })
async def synthesis_info(body: Request):
    content, correlation_id = await mq_connector.publish_request(body, body.speaker)
    return content



@v2_router.post('/stream_with_headers', include_in_schema=False,
                response_class=Response,
                description="Submit a text-to-speech request and stream audio with additional metadata in headers.",
                responses={
                    200: {"content": {"audio/wav": {}}, "description": "Returns the synthesized audio with headers containing metadata."},
                    422: {"model": ErrorMessage},
                    408: {"model": ErrorMessage},
                    500: {"model": ErrorMessage}
                })
async def stream_with_headers(body: Request):
    try:
        content, correlation_id = await mq_connector.publish_request(body, body.speaker)
        audio = base64.b64decode(content['audio'])
        
        response = Response(
            content=audio,
            media_type="audio/wav",
            headers={
                'Content-Disposition': f'attachment; filename="{correlation_id}.wav"',
                'Original-Text': base64.b64encode(body.text.encode('utf-8')).decode('utf-8'),
                'Normalized-Text': base64.b64encode(content['text'].encode('utf-8')).decode('utf-8'),
                'Duration-Frames': base64.b64encode(str(content.get('duration_frames', '')).encode('utf-8')).decode('utf-8'),
                'Sampling-Rate': f"{content.get('sampling_rate', '')}",
                'Win-Length': f"{content.get('win_length', '')}",
                'Hop-Length': f"{content.get('hop_length', '')}",
            }
        )
        return response
    except Exception as e:
        LOGGER.error(f"Error creating the streaming response: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while processing the request.")
