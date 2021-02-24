""" This Module contains utility functions for creating the AudioBook """
# Ebook Imports
import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

# Google Cloud Imports
from google.cloud import texttospeech
from google.cloud import texttospeech_v1

# NOTE: This is here to resolve the issues with the ProtoBuf size-restrictions with the Python implementation of the
# Google Cloud API and will hopefully not be required with future releases of this API
# See: https://github.com/googleapis/python-texttospeech/issues/5
from google.cloud.texttospeech_v1.services.text_to_speech.transports.grpc import (
    TextToSpeechGrpcTransport,
)

channel = TextToSpeechGrpcTransport.create_channel(
    options=[("grpc.max_receive_message_length", 24 * 1024 * 1024)]
)
transport = TextToSpeechGrpcTransport(channel=channel)
client = texttospeech_v1.TextToSpeechClient(transport=transport)


def TextToSpeech(voice_name, text):
    """ Processes the input text and returns the wav-encoded audio"""
    # TODO Check the Voice, OutputFilename and Text meet requirements
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech_v1.SynthesisInput(text=text)
    voice_params = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    return response.audio_content

def WriteAudioFile(filename, file_contents):
    """ Write the Audio to a file """
    output_filename = f"{filename}.wav"
    with open(output_filename, "wb") as out:
        out.write(file_contents)
        print(f'Audio content written to "{output_filename}"')



def GetEPubHTML(epub_path, processingFunction=(lambda book_text: book_text)):
    """ Outputs a list containing all test from the Book split by Chapters """
    book = epub.read_epub(epub_path)
    chapters = []

    for index, item in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
        soup = BeautifulSoup(item.get_content(), features="lxml")

        # Iterate all Headers and add full-stop
        for heading in soup.find_all([f'h{i}' for i in range(1,7) ]):
            if isinstance(heading.string, str):
                heading.string = heading.string + "."

        # Processing for a Specific Book
        soup = processingFunction(soup)

        # Strip Empty Lines / Chapters
        chapter_text = soup.get_text().strip()
        
        if chapter_text == "":
            continue

        chapter_text = "\n".join([line for line in chapter_text.split('\n') if line.strip() != ''])

        # Add Chapter to Book
        chapters.append(chapter_text)

    return chapters


# Special Processing for :
def goBookPreProcessing(soup):
    """ This is a pre-processing function that is targetted at The Go Programming Language - ePub. To ensure there are pauses at Headings and code-snippets are removed"""
    for div in soup.find_all("div", {'class': 'display'}):
        div.string = "Code Snippet Replaced."

    for heading in soup.find_all("div", {'class': 'calibre10'}):
        heading.string = heading.string + "."

    return soup