@echo off
CALL conda activate gemini
python main.py >> log.txt
CALL conda deactivate
