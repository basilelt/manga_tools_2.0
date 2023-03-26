cd /D "%~dp0"

git update-git-for-windows

python -m pip install --upgrade pip
python -m pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}

cd SmartStich
git pull origin master
cd ..

cd mangadex_bulk_uploader
git pull origin master
cd ..

powershell -Command "Invoke-WebRequest -Uri ((Invoke-WebRequest -Uri https://api.github.com/repos/shssoichiro/oxipng/releases/latest | ConvertFrom-Json).assets | Where-Object { $_.name -like 'oxipng*windows*.zip' } | Select-Object -First 1).browser_download_url -OutFile oxipng.zip"
mkdir oxipng
tar -xf .\oxipng.zip -C oxipng
del .\oxipng.zip

powershell -Command "Invoke-WebRequest -Uri ((Invoke-WebRequest -Uri https://api.github.com/repos/nihui/waifu2x-ncnn-vulkan/releases/latest | ConvertFrom-Json).assets | Where-Object { $_.name -like 'waifu2x-ncnn-vulkan-*-windows.zip' } | Select-Object -First 1).browser_download_url -OutFile waifu2x-ncnn-vulkan-windows.zip"  
tar -xf .\waifu2x-ncnn-vulkan-windows.zip
del .\waifu2x-ncnn-vulkan-windows.zip
powershell -Command "Get-ChildItem -Directory -Filter 'waifu2x*' | Rename-Item -NewName 'waifu2x' -Force"