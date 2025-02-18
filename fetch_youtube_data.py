
from pytube import extract
# youtube_transcript_api is for fetching the transcript
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable




def extract_id(URL):
    try:
        ID = extract.video_id(URL)
    except:
        return "Not a valid Youtube link"
    else:
        return ID



'''
Returns data from the video in the following format:

{
    'text': 'Hey there',
    'start': 7.58,
    'duration': 6.13
},
{
    'text': 'how are you',
    'start': 14.08,
    'duration': 7.58
},
# ...
'''
def fetch_transcript(URL):
    try:
        TRANSCRIPT = YouTubeTranscriptApi.get_transcript(URL)
    except TranscriptsDisabled:
        return "ERROR"
    except NoTranscriptFound:
        return "ERROR"
    except VideoUnavailable:
        return "ERROR"
    except Exception:
        return f"ERROR"
    else:
        return TRANSCRIPT



def fetch_youtube_transcipt(url:str):

    URL_ID = extract_id(url)

    if URL_ID == "Not a valid Youtube link":
        return "Not a valid Youtube Link"
    else:
        TRANSCRIPT = fetch_transcript(URL_ID)

        try:
            TRANSCRIPT = [line['text'] for line in TRANSCRIPT]
            TRANSCRIPT = ' '.join(TRANSCRIPT)
        except Exception:
            return TRANSCRIPT
        else:
            return TRANSCRIPT   