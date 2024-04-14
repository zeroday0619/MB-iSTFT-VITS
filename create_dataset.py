import os
import argparse
import httpx


class SpeechRecognizer(object):
    def __init__(self, speech_recognition_language: str, file: str) -> None:
        self.file = file
        self.url = f"https://{os.environ['AZURE_REGION']}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        self.params = {
            "language": speech_recognition_language,
            "format": "detailed"
        }
        self.headers = {
            "Ocp-Apim-Subscription-Key": os.environ['AZURE_SPEECH_SERVICES_API_KEY'],
            "Content-Type": "audio/wav",
        }
    
    def recognize(self):
        session = httpx.Client(
            headers=self.headers
        )
        resp = session.post(self.url, data=open(self.file, "rb"), params=self.params)
        resp.raise_for_status()
        return resp.json()['DisplayText']
    
    def write_audio_text_filelist(self, name: str):
        with open(f"filelists/{name}_audio_text_filelist.txt", "+a") as f:
            f.write(f"{self.file}|"+self.recognize()+"\n")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Azure Speech Recognition & VITS Dataset Preparation"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="ja-JP",
        help="Speech recognition language"
    )
    parser.add_argument(
        "--file",
        type=str,
        default="dataset/mizuki-voice-00.wav",
        help="Audio file"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="mizuki",
        help="Name of the dataset"
    )
    args = parser.parse_args()
    source = SpeechRecognizer(
        speech_recognition_language=args.lang,
        file=args.file
    ).write_audio_text_filelist(args.name)
