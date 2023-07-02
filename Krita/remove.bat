set NAME=incrementalsave
set ZIP="%PROGRAMFILES%\7-Zip\7z.exe"
set KRITA="%PROGRAMFILES%\Krita (x64)\bin\krita.com"

del /S /Q %appdata%\krita\pykrita\%NAME%
del /Q %appdata%\krita\pykrita\%NAME%.desktop
del /Q %appdata%\krita\actions\%NAME%.action
del /Q .\%NAME%.zip

%KRITA%