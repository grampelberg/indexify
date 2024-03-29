# Audio Extractors

#### [Whisper](https://github.com/tensorlakeai/indexify-extractors/tree/main/audio/whisper-asr)
This extractor converts extracts transcriptions from audio. The entire text and
chunks with timestamps are represented as metadata of the content.

==="bash"
    indexify-extractor download hub://audio/whisper-asr
==="docker"
    docker run -d tensorlake/whisper-asr

#### [Speaker Diarization](https://github.com/tensorlakeai/indexify-extractors/tree/main/audio/whisper-diarization)
This extractor indentifies the speaker for each sentence in the transcription generated by Whisper.

==="bash"
    indexify-extractor download hub://audio/whisper-diarization
==="docker"
    docker run -d tensorlake/whisper-diarization