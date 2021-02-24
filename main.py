""" 
This Module is the Main Module for the EpubToAudiobook Application that uses the Google Cloud Text-To-Speech functionality to output 
easy-listening Audiobooks from Epub Input
"""
import argparse
import click
import os

@click.command()
# Required Args
@click.option('--epub-file',required=True, help='The URI to the ePub file that is being processed into the AudioBook')
# Optional Args
@click.option('--voice', help='', default="en-AU-Wavenet-B")
@click.option('--gcloud-credentials', help='Google Credentials JSON File')
def CreateAudioBook(epub_file, voice, gcloud_credentials):
    """ This method creates performs Text-To-Speech using Google Cloud to create an Audiobook from an ePub and writes this to a new directory within the current path """
    
    # Configure Google Credentials
    if gcloud_credentials:
        print(f'Using Google Credentials located at {gcloud_credentials}')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcloud_credentials

    # Importing Utilities here to use new value of GOOGLE_APPLICATION_CREDENTIALS
    from utilities import GetEPubHTML, kubernetesBookProcessing, TextToSpeech, WriteAudioFile

    # Get Book Content
    chapter_text = GetEPubHTML(epub_file, kubernetesBookProcessing)
    # Make Dir
    _, filename = os.path.split(epub_file)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    new_dir_path = os.path.join(dir_path, filename+"_dir")

    try:
        os.makedirs(new_dir_path, exist_ok=True)
    except OSError:
        print ("Creation of the directory %s failed" % new_dir_path)
        return

    # Write each chapter to the folder
    for index, chapter in enumerate(chapter_text):
        audio = TextToSpeech(voice, chapter)
        
        # Store the chapter in the New Folder 
        filename = os.path.join(new_dir_path, "chapter"+str(index))
        WriteAudioFile(filename=filename, file_contents=audio)

if __name__ == '__main__':
    CreateAudioBook()