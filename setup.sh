#!/bin/bash
mkdir -p ~/.streamlit/
echo "[server]\nheadless = true\nport = $PORT\nenableCORS = false\n
" > ~/.streamlit/config.toml
streamlit run adaptive_learning_app.py
