import os
import subprocess
import shutil
import cv2

## ! Install requirements.txt with pip !


## Downloading chapters
subprocess.run([path_fmd])


## Get working directory
name = os.path.basename(__file__)
current_path = __file__.replace(name, "")
os.chdir(current_path)

waifu_path = os.path.join(current_path, "waifu2x", "waifu2x-ncnn-vulkan.exe")
path_stitcher = os.path.join(current_path, "SmartStitch", "SmartStitchConsole.py")
oxipng_path = os.path.join(current_path, "oxipng", "oxipng.exe")
mangadex_path = os.path.join(current_path, "mangadex_bulk_uploader", "md_uploader.py")
path_fmd = os.path.join(current_path, "fmd", "fmd.exe")

download_path = os.path.join(current_path, "download")
denoise_path = os.path.join(current_path, "denoise")
stitched_path = os.path.join(current_path, "stiched")
upload_path = os.path.join(current_path, "mangadex_bulk_uploader", "to_upload")
uploaded_path = os.path.join(current_path, "mangadex_bulk_uploader", "uploaded")
drive_path = r'D:\Gdrive\.shortcut-targets-by-id\1dp1NNqw9AuMIHcOgoY8TJT6c75HwHBpn\Zero Scans Projects' ## Change to your need


## Denoising resizing
for manga in os.listdir(download_path):
	manga_path = os.path.join(download_path, manga)
	denoise_out = os.path.join(denoise_path, manga)

	for chapter in os.listdir(manga_path):
		chapter_path = os.path.join(manga_path, chapter)
		chapter_out_path = os.path.join(denoise_out, chapter)
		os.makedirs(chapter_out_path)

		max_width = 0
		for img in os.listdir(chapter_path):
			img_path = os.path.join(chapter_path, img)
			im = cv2.imread(img_path)
			width = im.shape[1]

			if max_width < width:
				max_width = width
		
		for img in os.listdir(chapter_path):
			img_path = os.path.join(chapter_path, img)
			img_out_path = os.path.join(chapter_out_path, img)
			
			im = cv2.imread(img_path)
			width = im.shape[1]

			if width < max_width:
				ratio = str(max_width / width)
				subprocess.run([waifu_path, '-i', img_path, '-o', img_out_path, '-n', '3', '-s', ratio, '-x'])
			else:
				subprocess.run([waifu_path, '-i', img_path, '-o', img_out_path, '-n', '3', '-s', '1', '-x'])

	shutil.rmtree(manga_path)


no_stitch = ["魔石异世录——艾莎的救赎", "Star Martial God Technique", "The Demon King Who Lost His Job"] ## To modify to match your paged series
raw = ["来自深渊的我今天也要拯救人类", "我只想安静地打游戏", "我必须成为怪物", "只靠防御称霸诸天", "我真不是邪神走狗"] ## To modify to match your raws (different stitch size than upload)

## Stitching chapters
for manga in os.listdir(denoise_path):
	manga_path = os.path.join(denoise_path, manga)
	
	if manga in no_stitch: ## Paged series
		print(f"{manga} does not need stitching")
	
	elif manga in raw:
		subprocess.run(['python', path_stitcher, '-i', manga_path, '-sh', '10000', '-t', '.png', '-dt', '90', '-sl', '15'])
		shutil.rmtree(manga_path)
		os.rename(os.path.join(manga_path, "[stitched]"), manga_path)

	else:
		subprocess.run(['python', path_stitcher, '-i', manga_path, '-sh', '2000', '-t', '.png', '-dt', 'none', '-sl', '50'])
		shutil.rmtree(manga_path)
		os.rename(manga_path + " [stitched]", manga_path)


## Optimizing images
subprocess.run([oxipng_path, denoise_path, '-o', 'max', '-r', '--strip', 'all', '-a', '-i', '0', '--fix', '-Z', '-t', '512'])
## '-f', '0,9', '-zc', '12'


## To modify to match your raws and drive folders
raw_lst =["来自深渊的我今天也要拯救人类", "我只想安静地打游戏", "我必须成为怪物", "只靠防御称霸诸天", "魔石异世录——艾莎的救赎"]
name_lst = ["Abyss", "I Just Want to Play the Game Quietly", "I Must Become A Monster", "Dominate the World Only by Defense", "Aisha's Salvation"]

## Moving Output to Drive directory
for manga in os.listdir(denoise_path):
	manga_path = os.path.join(denoise_path, manga)

	if manga in raw_lst:
		for i in range(len(raw_lst)):
			if manga == raw_lst[i]:
				title = name_lst[i]
				folder_raw = r'1. Project RAWs'
			
				for chapter in os.listdir(manga_path):
					chapter_path = os.path.join(manga_path, chapter)
					raw_path = os.path.join(drive_path, title, folder_raw, chapters)
					
					shutil.move(chapter_path, raw_path)
			
				shutil.rmtree(manga_path)
				break

	## Other path
	elif manga == '我真不是邪神走狗':
		for chapter in os.listdir(manga_path):
			chapter_path = os.path.join(manga_path, chapter)
			raw_path = os.path.join(r'D:\Gdrive\My Drive\RAW', chapter) ## Outside tree folder
			
			shutil.move(chapter_path, raw_path)
		
		shutil.rmtree(manga_path)

	else:
		for chapter in os.listdir(manga_path):
			chapter_path = os.path.join(manga_path, chapter)
			raw_path = os.path.join(upload_path, chapter.replace("Chapter ", "c"))
			
			shutil.move(chapter_path, raw_path)
		
		shutil.rmtree(manga_path)


## Upload chapter to mangadex
subprocess.run(['python', mangadex_path])
shutil.rmtree(manga_path)

print("done")
