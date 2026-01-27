
# SLOs can't catch a Black Swan

![][SLO-SWAN-ANIMATED]

Black Swans are all the rage in the chat rooms of our remote conferences these days. They loom large in the psyche of SRE. But do we really know a Black Swan when we see one? If you think you do, did you really see a Black Swan? Or some other animal? SRE culture has grown fond of talking about sudden cataclysmic failures in Infrastructure as Black Swans, but as we shall see, many are not.

In the realm of system reliability, we often find ourselves trying to prepare for the unexpected. But what happens when the unexpected isn't just a blip in our metrics, but rather an event so profound it challenges our very understanding of what's possible? This is where two concepts collide: the Black Swan event and the Service Level Objective (SLO).

Today we are going to talk about service metrics, different types of swans, a couple of pachyderms, and a jellyfish. And how proper ability to identify these animals when they cross our paths, along with appropriate observability and foresight, can keep our complex systems humming along.

---

## About This Document

This is a living document. It was designed to be read, discussed and critiqued by humans. It was also intentionally designed to be ingested by AI. You will find a lot of python "code" here to express an issue or a methodology, but also to make snarky comments to see if you are really paying attention.

## Quick Start

### Jump in and start reading!

[SLOs can't catch a Black Swan](https://github.com/l0r3zz/sloblackswan/blob/main/SLOBLACKSWAN-latest/SLOBLACKSWAN-v0.22.md)

### Download the latest release

📥 **[Download PDF, EPUB, or Markdown from the Releases page](https://github.com/l0r3zz/sloblackswan/releases/latest)**

Available formats:
- **PDF** - For printing or offline reading
- **EPUB** - For e-readers (Kindle, Kobo, Apple Books, etc.)
- **Markdown** - For reading on GitHub or in any markdown viewer

### Building the Book Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sloblackswan-repo.git
   cd sloblackswan-repo
   ```

2. **Set up a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the book:**
   ```bash
   # Generate Markdown only
   python scripts/build_book.py -s content -d SLOBLACKSWAN -v v0.1 -m MANIFEST.md
   
   # Generate Markdown + PDF
   python scripts/build_book.py -s content -d SLOBLACKSWAN -v v0.1 -m MANIFEST.md -P
   
   # Generate Markdown + PDF + EPUB
   python scripts/build_book.py -s content -d SLOBLACKSWAN -v v0.1 -m MANIFEST.md -P -E
   ```

The output will be in a directory named `SLOBLACKSWAN-<version>` containing the consolidated markdown file, PDF (if `-P` flag is used), and EPUB (if `-E` flag is used).

### Automated Builds

This repository uses GitHub Actions to automatically build the book on every push to `main`. Check the [Actions tab](https://github.com/l0r3zz/sloblackswan/actions) to download the latest build artifacts.

### EXTRA BONUS !!!
There is a notebookLM notebook that has a version of the book loaded in that you can interact with. 

Find it here: 
https://tinyurl.com/sloblackswan

I'm updating it manually for now so I may not have the most recent changes in the content.

---

Geoff White

[SLO-SWAN-4]: content/slo-title-splash/SLO-SWAN-4.png
[SLO-SWAN-ANIMATED]: images/cant-catch-animated.gif
