# YouTube Playlist Summarizer & Guide Generator

This is a command-line tool written in Python that generates summaries or step-by-step guides for all videos in a given YouTube playlist.

## Features

- **Two Modes:** Choose between generating a standard prose summary or a structured step-by-step guide.
- **Playlist Processing:** Simply provide a URL to a public YouTube playlist.
- **NLP-Powered Analysis:**
    - **Summarizer:** Uses Latent Semantic Analysis (LSA) to extract the most important sentences from a video's transcript.
    - **Guide Generator:** Uses Part-of-Speech (POS) tagging to identify instructional sentences (e.g., those starting with a verb) to create a list of steps.
- **File Output:** Saves the generated content for the entire playlist to a single `summary.txt` file.

## Setup and Installation

1.  **Prerequisites:** Make sure you have Python 3.8 or higher installed on your system.

2.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

3.  **Install dependencies:**
    The required Python libraries are listed in `requirements.txt`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
    The first time you run the script, it may also automatically download necessary data packages from the NLTK library.

## How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the project directory.
3.  Run the script:
    ```bash
    python summarizer.py
    ```
4.  The script will prompt you to enter the URL of the YouTube playlist you want to process.
5.  Next, it will ask you to select a mode: `(1)` for a standard summary or `(2)` for a step-by-step guide.
6.  The script will then process each video in the playlist. The final output will be saved in a file named `summary.txt` in the same directory.

## Important Note on Usage

This tool relies on fetching public video transcripts from YouTube. YouTube may block requests from IP addresses associated with cloud computing providers (like AWS, Google Cloud, etc.).

If you run this script from such a server, you may encounter errors. The script is designed to handle these errors gracefully, but it will be unable to retrieve the transcripts. **For best results, run this script from a personal computer on a residential network.**
