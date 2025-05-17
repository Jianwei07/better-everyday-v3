#!/bin/bash
# Example script to run a local LLM server (TGI) for Eva backend
# Requires Docker and a GPU for best performance

MODEL_ID="microsoft/phi-2"
PORT=8001

docker run --rm -it \
  -p $PORT:8001 \
  -e MODEL_ID=$MODEL_ID \
  -v $(pwd)/models:/data/models \
  ghcr.io/huggingface/text-generation-inference:latest

# For llama.cpp or vLLM, see their docs for equivalent server launch commands
