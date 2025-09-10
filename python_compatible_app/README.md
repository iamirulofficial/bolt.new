# Python PrototypeAI App

This example combines the `prototype_ai` backend with a small
client/executor that consumes streaming responses, parses
`<prototypeArtifact>` instructions and applies them to a local
workspace.

## Usage

1. Start the backend server:
   ```bash
   uvicorn prototype_ai.server.chat:app --reload
   ```
2. In another terminal run the interactive client:
   ```bash
   python -m python_compatible_app.run
   ```
3. Enter natural language prompts. When the model responds with
   `prototypeAction` blocks, the client will write files and execute
   shell commands accordingly.

The client also tracks file changes and sends them back as diffs on the
next prompt so the model stays aware of the current project state.
