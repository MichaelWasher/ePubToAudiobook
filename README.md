# ePubToAudiobook
This is a small Python tool created to convert ePub files into Audiobooks using Googles Text-to-Speech. 

I wrote this to convert the Google's [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) and [The Go Programming Language](https://www.gopl.io/) ePubs to listen whilst commuting. This may work for other ePubs too.

If there are specific formatting requirements for a book, the `processingFunction` parameter in the `GetEPubHTML` function can be used to perform custom preprocessing of the ePub HTML using BeautifulSoup. I find this is a need sometimes as classes are regularly used instead of H-tags for headers and I find it easier to follow the book when there are pauses (full-stops) at the end of headings.

## How to use this tool:
To use this tool, gCloud API credentials must be passed to the application. This is achieved by collecting service-account credentials in the form of a JSON token and using the `--gcloud-credentials` parameter. 

If the gCloud SDK is installed and configured correctly then this flag is not required as the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set and is used for authentication with the Google services.

## Example Command:
~~~
python3 ./main.py --epub-file=./book.epub --gcloud-credentials=/webtoken.json
~~~
