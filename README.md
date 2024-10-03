# Text-to-Speech API

## Overview
This API provides text-to-speech (TTS) services. You can submit text and receive synthesized audio in response.

## Endpoints

### `GET /v2`
Retrieve the configuration of available models and speakers.

**Response:**
- `200 OK`: Returns the configuration of available models and speakers.

### `POST /v2`
Submit a text-to-speech request.

**Request Body:**
- `text` (string): The text to be synthesized.
- `speaker` (string): The speaker to use for synthesis.

**Responses:**
- `200 OK`: Returns the synthesized audio.
- `422 Unprocessable Entity`: Invalid input.
- `408 Request Timeout`: Request timed out.
- `500 Internal Server Error`: Server error.

### `POST /v2/verbose`
Submit a text-to-speech request and return only some information about the output.

**Request Body:**
- `text` (string): The text to be synthesized.
- `speaker` (string): The speaker to use for synthesis.

**Responses:**
- `200 OK`: Returns information about the synthesized audio.
- `422 Unprocessable Entity`: Invalid input.
- `408 Request Timeout`: Request timed out.
- `500 Internal Server Error`: Server error.

### `POST /v2/stream_with_headers`
Submit a text-to-speech request and stream audio with additional metadata in headers.

**Request Body:**
- `text` (string): The text to be synthesized.
- `speaker` (string): The speaker to use for synthesis.

**Responses:**
- `200 OK`: Returns the synthesized audio with headers containing metadata.
- `422 Unprocessable Entity`: Invalid input.
- `408 Request Timeout`: Request timed out.
- `500 Internal Server Error`: Server error.

## Example Requests

### Get Configuration