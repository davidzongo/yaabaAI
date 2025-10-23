#!/bin/bash#!/bin/bash



mkdir -p ~/.streamlit/mkdir -p ~/.streamlit/



echo "\echo "\

[general]\n\[general]\n\

email = \"yaaba-ai@go-ai-corp.com\"\n\email = \"yaaba-ai@go-ai-corp.com\"\n\

" > ~/.streamlit/credentials.toml" > ~/.streamlit/credentials.toml



echo "\echo "\

[server]\n\[server]\n\

headless = true\n\headless = true\n\

enableCORS = false\n\enableCORS = false\n\

port = $PORT\n\port = $PORT\n\

address = 0.0.0.0\n\address = 0.0.0.0\n\

[theme]\n\[theme]\n\

primaryColor = \"#667eea\"\n\primaryColor = \"#667eea\"\n\

backgroundColor = \"#ffffff\"\n\backgroundColor = \"#ffffff\"\n\

secondaryBackgroundColor = \"#f8f9fa\"\n\secondaryBackgroundColor = \"#f8f9fa\"\n\

textColor = \"#555555\"\n\textColor = \"#555555\"\n\

" > ~/.streamlit/config.toml" > ~/.streamlit/config.toml