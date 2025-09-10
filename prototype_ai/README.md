# PrototypeAI Backend

PrototypeAI is a minimal Python backend demonstrating an LLM‑driven system that can
generate files and run commands. It is *LLM agnostic* and can speak to OpenAI, Azure
OpenAI, or Google Gemini through a shared interface.

## Architecture

* **LLM clients** – provider‑specific wrappers implement a common `BaseClient` interface.
* **Switchable stream** – supports continuation when the model reaches a token limit.
* **FastAPI route** – `POST /api/chat` streams text from the selected model and handles
  continuation prompts.

## Generating files & running commands

Model responses are expected to contain `<prototypeArtifact>` blocks. Each block may hold
multiple `<prototypeAction>` elements:

* `<prototypeAction type="file" filePath="path/to/file">` – write or update files.
* `<prototypeAction type="shell">` – run shell commands to install dependencies or start
  processes.

Files are written relative to a workspace directory (e.g. the project root) so the
generated application can be executed immediately after the model finishes.

## Running the server

1. Set `LLM_PROVIDER` to `openai`, `azure`, or `gemini` and export the matching API
   credentials in your environment.
2. Change into this directory and start the FastAPI app:

   ```bash
   cd prototype_ai
   uvicorn server.chat:app --reload
   ```

3. Send chat requests to `POST /api/chat` with a list of `{role, content}` messages.

The route streams the model output and automatically requests continuation when needed.
