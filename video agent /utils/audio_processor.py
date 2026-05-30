import yt_dlp
from pydub import AudioSegment
import os

DOWNLODED_DIR = "downloads"
os.makedirs(DOWNLODED_DIR, exist_ok=True)

def download_youtube_audio(url:str)->str:
    """
    Download YouTube audio as MP3 using yt-dlp
    """

    output_path = os.path.join(DOWNLODED_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,

        # Convert to wav
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],

        # Optional
        "quiet": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
           info = ydl.extract_info(url, download=True)
           filename = ydl.prepare_filename(info).replace('.webm','.wav').replace('.m4a','.wav')

        return filename 

    except Exception as e:
        print(f"Error: {e}")





def convert_to_wav(input_path:str)->str:

    try:
        output_path = os.path.splitext(input_path)[0] + "_converted.wav"
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        print(f"Error: {e}")




#chunck audio in 10 minite 

def chunck_audio(wav_path: str , chunk_minint : int = 10)-> list:
    audio = AudioSegment.from_wav(wav_path)
    chunck_ms = chunk_minint * 60 *1000
    chunks = []

    for i , start in enumerate(range(0,len(audio),chunck_ms)):
        chunck = audio[start: start + chunck_ms]

        chunck_path = f"{wav_path}_chunck_{i}.wav"
        chunck.export(chunck_path, format="wav")
        chunks.append(chunck_path)

    return chunks




#Trigaring function 

def process_input(source : str )-> list:
    if source.startswith("http://") or source.startswith("https://"):
        wav_path = download_youtube_audio(source)
        print("Downloading audio")
    else:
        #local file path 
        wav_path = convert_to_wav(source)
        print("Converting audio to wav")
    
    #chunking the audio function call

    chunks = chunck_audio(wav_path)
    print("Chunking audio in 10 minite")

    return chunks
    