cd src
pyinstaller --onefile -w code_metrics.py
rmdir /s .\build
del *.spec
cd ..
move src\dist\code_metrics.exe .\dist
rmdir src\dist
