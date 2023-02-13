from deepgram import Deepgram
import json

def deepgramTranscribe(api_key):
    # The API key we created in step 3

    # Hosted sample file
    AUDIO_URL = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"

    def main():
        # Initializes the Deepgram SDK
        dg_client = Deepgram(api_key)
        source = {'url': AUDIO_URL}
        options = { "punctuate": True, "model": "general", "language": "en-US", "tier": "enhanced" }

        print('Requesting transcript...')
        print('Your file may take up to a couple minutes to process.')
        print('While you wait, did you know that Deepgram accepts over 40 audio file formats? Even MP4s.')
        print('To learn more about customizing your transcripts check out developers.deepgram.com')

        response = dg_client.transcription.sync_prerecorded(source, options)
        print(json.dumps(response, indent=4))

    main()