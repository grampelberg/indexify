# Audio Transcription 

1. The extraction graph creates an endpoint which accepts audio files and transcribes them using OpenAI's Whisper model
2. You can continuously transcribe audio with this pipeline by uploading audio files to indexify server.
3. You can run 1000s of instances of the extractors in parallel transcribe audio in a fault tolerant manner.

## Code Reference

[Link to Code](https://github.com/tensorlakeai/indexify/tree/main/examples/audio/transcription)

1. `graph.yaml` - contains the extraction graph.
2. `setup_graph.py` - Sets up the extraction graph in Indexify Server
3. `upload_and_retrieve.py` - Uploads audio into the extraction graph, waits for extraction and finally retrieves from the endpoint.

## Download & Start Indexify Server
```bash title="Terminal 1"
curl https://getindexify.ai | sh
./indexify server -d
```

## Download & Join Indexify Extractors 
```bash title="Terminal 2"
virtualenv ve
source ve/bin/activate

pip install indexify-extractor-sdk
indexify-extractor download tensorlake/whisper-asr
indexify-extractor join-server
```

## Setup the Graph 
```bash title="Terminal 3"
python setup_graph.py
```

<img src="https://docs.getindexify.ai/example_code/audio/transcription/carbon.png" width="600"/>

## Upload Data and Retrieve 
The next step is to upload an audio file and retrieve the transcript

```bash title="Terminal 3"
python upload_and_retrieve.py
```

<img src="https://docs.getindexify.ai/example_code/audio/transcription/output.png" width="800"/>
