#!/bin/bash

# Create necessary directories
mkdir -p /tmp/nltk_data

# Download required NLTK data
python -c "import nltk; nltk.download('punkt', download_dir='/tmp/nltk_data')"
python -c "import nltk; nltk.download('stopwords', download_dir='/tmp/nltk_data')"
python -c "import nltk; nltk.download('vader_lexicon', download_dir='/tmp/nltk_data')"

# Deploy to Vercel
vercel --prod 