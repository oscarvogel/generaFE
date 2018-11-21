rd /S /Q dist\main
pyinstaller --clean --version-file=version.txt --windowed -F --icon=imagenes\logo.ico main.py -p H:\envs\FE\Lib\site-packages\PyQt4