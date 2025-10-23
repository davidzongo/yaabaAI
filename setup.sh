#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"yaaba-ai@go-ai-corp.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
address = 0.0.0.0\n\
[theme]\n\
primaryColor = \"#667eea\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f8f9fa\"\n\
textColor = \"#555555\"\n\
" > ~/.streamlit/config.toml