import re
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

# NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    print("Downloading required NLTK data...")
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')

def get_transcript_text(video_url):
    """
    Fetches and formats the transcript for a given video URL.
    Returns the transcript text, or an error string if it fails.
    """
    try:
        video_id_match = re.search(r"v=([^&]+)", video_url)
        if not video_id_match:
            return f"Could not extract video ID from {video_url}"
        video_id = video_id_match.group(1)

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['en'])
        full_transcript_data = transcript.fetch()

        if not full_transcript_data:
            return "No transcript content found."

        formatter = TextFormatter()
        return formatter.format_transcript(full_transcript_data)
    except Exception as e:
        if "TranscriptsDisabled" in str(e) or "No transcripts were found" in str(e):
            return "Transcripts are disabled or not available for this video."
        return f"An error occurred: {e}"

def get_summary(full_transcript_text):
    """
    Generates a summary from a block of text.
    """
    if full_transcript_text.startswith("Could not") or full_transcript_text.startswith("An error"):
        return full_transcript_text

    parser = PlaintextParser.from_string(full_transcript_text, Tokenizer("english"))
    stemmer = Stemmer("english")
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")
    summary_sentences = summarizer(parser.document, 5)
    return " ".join([str(sentence) for sentence in summary_sentences])

def create_step_by_step_guide(full_transcript_text):
    """
    Identifies instructional sentences from a transcript to create a guide.
    """
    if full_transcript_text.startswith("Could not") or full_transcript_text.startswith("An error"):
        return full_transcript_text

    sentences = nltk.sent_tokenize(full_transcript_text)
    instructional_sentences = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        if not words:
            continue

        tagged_words = nltk.pos_tag(words)
        first_word_tag = tagged_words[0][1]
        if first_word_tag.startswith('VB'): # Catches VB, VBP, VBG, etc.
            instructional_sentences.append(sentence)

    if not instructional_sentences:
        return "No clear step-by-step instructions were identified in the transcript."

    return "\n".join(f"{i+1}. {s}" for i, s in enumerate(instructional_sentences))

def get_playlist_info(url):
    """
    Retrieves the title and video URLs from a YouTube playlist.
    """
    try:
        playlist = Playlist(url)
        title = playlist.title
        video_urls = list(playlist.video_urls)
        if not video_urls:
            print("Error: Could not retrieve videos from playlist. It might be empty or private.")
            return None, None
        return title, video_urls
    except Exception as e:
        print(f"An error occurred while fetching the playlist: {e}")
        return None, None

def main():
    """
    Main function to run the summarizer.
    """
    playlist_url = input("Please enter the YouTube playlist URL: ")
    if not playlist_url:
        print("No URL entered. Exiting.")
        return

    mode = ''
    while mode not in ['1', '2']:
        mode = input("Select mode: (1) Standard Summary (2) Step-by-step Guide: ")
        if mode not in ['1', '2']:
            print("Invalid selection. Please enter 1 or 2.")

    print("\nFetching playlist information...")
    playlist_title, video_urls = get_playlist_info(playlist_url)

    if playlist_title and video_urls:
        print(f"Successfully fetched playlist: '{playlist_title}'")
        print(f"Found {len(video_urls)} videos. This may take a while...")

        results = []
        for i, url in enumerate(video_urls):
            print(f"\n--- Processing Video {i+1}/{len(video_urls)}: {url} ---")
            transcript_text = get_transcript_text(url)

            if mode == '1':
                output = get_summary(transcript_text)
                output_label = "Summary"
            else: # mode == '2'
                output = create_step_by_step_guide(transcript_text)
                output_label = "Step-by-step Guide"

            results.append((url, output_label, output))

        output_filename = "summary.txt"
        print(f"\n--- Writing all results to {output_filename} ---")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"Playlist: {playlist_title}\n")
            f.write("=" * 40 + "\n\n")
            for url, label, result_text in results:
                f.write(f"Video URL: {url}\n")
                f.write(f"{label}:\n{result_text}\n\n")

        print("--- Done. ---")

if __name__ == "__main__":
    main()
