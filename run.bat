@echo off
CALL conda activate gemini
python D:\PythonWorkSpace\git\side\main.py >> D:\PythonWorkSpace\git\side\log.txt
CALL conda deactivate
