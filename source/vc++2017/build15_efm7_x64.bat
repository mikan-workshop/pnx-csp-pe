echo off

if exist "%ProgramFiles(x86)%" goto is_x64
set path="%ProgramFiles%\Microsoft Visual Studio\2017\WDExpress\MSBuild\15.0\Bin";%PATH%
goto start

:is_x64
set path="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\WDExpress\MSBuild\15.0\Bin";%PATH%

:start
rmdir /s /q build_vc15
mkdir build_vc15

msbuild.exe fm7.vcxproj /t:clean;rebuild /p:Configuration=Release;Platform="x64"
msbuild.exe fm77.vcxproj /t:clean;rebuild /p:Configuration=Release;Platform="x64"
msbuild.exe fm77l4.vcxproj /t:clean;rebuild /p:Configuration=Release;Platform="x64"
msbuild.exe fm77av.vcxproj /t:clean;rebuild /p:Configuration=Release;Platform="x64"
mkdir build_vc15\fm7
copy bin\x64\Release\fm7.exe build_vc15\fm7\.
copy bin\x64\Release\fm77.exe build_vc15\fm7\.
copy bin\x64\Release\fm77l4.exe build_vc15\fm7\.
copy bin\x64\Release\fm77av.exe build_vc15\fm7\.

pause
echo on
exit /b

