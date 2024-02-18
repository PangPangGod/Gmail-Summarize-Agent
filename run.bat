@echo off
CALL conda activate gemini
set PYTHONIOENCODING=utf-8
python main.py >> log.md
CALL conda deactivate
