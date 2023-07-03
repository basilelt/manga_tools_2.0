import os
import subprocess
import shutil
from PIL import Image
import math
import statistics

## ! Install requirements.txt with pip !


## Get working directory
name = os.path.basename(__file__)
current_path = __file__.replace(name, "")
os.chdir(current_path)

waifu_path = os.path.join(current_path, "waifu2x", "waifu2x-ncnn-vulkan.exe")
path_stitcher = os.path.join(current_path, "SmartStitch", "SmartStitchConsole.py")
oxipng_path = os.path.join(current_path, "oxipng", "oxipng.exe")
mangadex_path = os.path.join(current_path, "mangadex_bulk_uploader", "md_uploader.py")
path_fmd = os.path.join(current_path, "fmd", "fmd.exe")
path_mogrify = os.path.join(current_path, "image_magick", "mogrify.exe")
path_magick = os.path.join(current_path, "image_magick", "magick.exe")

download_path = os.path.join(current_path, "download")
denoise_path = os.path.join(current_path, "denoise")
stitched_path = os.path.join(current_path, "stiched")
upload_path = os.path.join(current_path, "mangadex_bulk_uploader", "to_upload")
uploaded_path = os.path.join(current_path, "mangadex_bulk_uploader", "uploaded")
drive_path = r'D:\Gdrive\.shortcut-targets-by-id\1dp1NNqw9AuMIHcOgoY8TJT6c75HwHBpn\Zero Scans Projects' ## Change to your need


## Downloading chapters
subprocess.run([path_fmd])

## To modify to match your raws and drive folders
raw_lst =["来自深渊的我今天也要拯救人类", "我只想安静地打游戏", "我必须成为怪物", "只靠防御称霸诸天", "魔石异世录——艾莎的救赎", "恶龙转生，复仇从五岁开始！", "失业魔王", "我困在这一天已三千年", "斩月"]
name_lst = ["Abyss", "I Just Want to Play the Game Quietly", "I Must Become A Monster", "Dominate the World Only by Defense", "Aisha's Salvation", "My Dragon System", "The Demon King Who Lost His Job", "I’ve Been Trapped on the Same Day for Over 3000 Years", "Moon Slayer"]
to_denoise = raw_lst + ['我真不是邪神走狗']


## Renaming weird chars
for manga in os.listdir(download_path):
	manga_path = os.path.join(download_path, manga)
	if manga == "I’ve Been Trapped on the Same Day for Over 3000 Years":
		manga = "Ive Been Trapped on the Same Day for Over 3000 Years"
		os.rename(os.path.join(manga_path), os.path.join(download_path, manga))
		manga_path = os.path.join(download_path, manga)
	
	for chapter in os.listdir(manga_path):
		chapter_path = os.path.join(manga_path, chapter)
		if "I’ve Been Trapped on the Same Day for Over 3000 Years" in chapter:
			chapter = chapter.replace("I’ve Been Trapped on the Same Day for Over 3000 Years", "Ive Been Trapped on the Same Day for Over 3000 Years")
			os.rename(os.path.join(chapter_path), os.path.join(manga_path, chapter))
			chapter_path = os.path.join(manga_path, chapter)


## Denoising resizing		
for manga in os.listdir(download_path):
	manga_path = os.path.join(download_path, manga)
	denoise_out = os.path.join(denoise_path, manga)

	for chapter in os.listdir(manga_path):
		chapter_path = os.path.join(manga_path, chapter)
		chapter_out_path = os.path.join(denoise_out, chapter)
		os.makedirs(chapter_out_path)

		width_lst = []
		for img in os.listdir(chapter_path):
			img_path = os.path.join(chapter_path, img)
			subprocess.run([path_mogrify, '-format', 'png', img_path])
			if "jpg" in img_path:
				os.remove(img_path)
				img_path = img_path.replace("jpg", "png")

			elif "jpeg" in img_path:
				os.remove(img_path)
				img_path = img_path.replace("jpeg", "png")

			elif "webp" in img_path:
				os.remove(img_path)
				img_path = img_path.replace("webp", "png")


			im = Image.open(img_path)
			width_lst = width + [im.size[0]]
			im.close()

		median = int(statistics.median(width_lst))
		
		for img in os.listdir(chapter_path):
			img_path = os.path.join(chapter_path, img)
			img_out_path = os.path.join(chapter_out_path, img)
			
			im = Image.open(img_path)
			width = im.size[0]
			im.close()
			no_waifu = True

			if width < median:
				ratio = median / width
				if int(ratio) not in [1, 2, 4, 8, 16, 32, 64, 128]:
					i = 2
					while i < ratio:
						i *= 2
					ratio = i
				ratio = str(ratio)

				subprocess.run([waifu_path, '-i', img_path, '-o', img_out_path, '-n', '3', '-s', ratio, '-x', '-f', 'png'])
				size = str(median) + "x"
				subprocess.run([path_magick, img_out_path, "-resize", size, img_out_path])
				no_waifu = False

			elif width > median:
				size = str(median) + "x"
				subprocess.run([path_magick, img_path, "-resize", size, img_out_path])
				os.remove(img_path)

			if manga in to_denoise and no_waifu:
				subprocess.run([waifu_path, '-i', img_path, '-o', img_out_path, '-n', '3', '-s', '1', '-x', '-f', 'png'])

			else:
				shutil.move(img_path, img_out_path)

	shutil.rmtree(manga_path)


no_stitch = ["魔石异世录——艾莎的救赎", "Star Martial God Technique", "The Demon King Who Lost His Job"] ## To modify to match your paged series
raw = ["来自深渊的我今天也要拯救人类", "我只想安静地打游戏", "我必须成为怪物", "只靠防御称霸诸天", "我真不是邪神走狗", "恶龙转生，复仇从五岁开始！", "失业魔王", "我老婆是魔王大人", "我困在这一天已三千年", "斩月"] ## To modify to match your raws (different stitch size than upload)

## Stitching chapters
for manga in os.listdir(denoise_path):
	manga_path = os.path.join(denoise_path, manga)
	
	if manga in no_stitch: ## Paged series
		print(f"{manga} does not need stitching")
	
	elif manga in raw:
		subprocess.run(['python', path_stitcher, '-i', manga_path, '-sh', '10000', '-t', '.png', '-s', '95', '-sl', '15'])
		shutil.rmtree(manga_path)
		os.rename(manga_path + " [stitched]", manga_path)

	else:
		subprocess.run(['python', path_stitcher, '-i', manga_path, '-sh', '2000', '-t', '.png', '-dt', 'none', '-sl', '50'])
		shutil.rmtree(manga_path)
		os.rename(manga_path + " [stitched]", manga_path)


## Optimizing images
subprocess.run([oxipng_path, denoise_path, '-o', '4', '-r', '--strip', 'all', '-a', '-i', '0', '-t', '32'])
## '-f', '0,9', '-zc', '12'
## '-o', 'max', '-Z', '--fix'


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
					raw_path = os.path.join(drive_path, title, folder_raw, chapter)
					
					shutil.move(chapter_path, raw_path)
			
				shutil.rmtree(manga_path)
				break

	## Other path
	elif manga == '我真不是邪神走狗':
		for chapter in os.listdir(manga_path):
			chapter_path = os.path.join(manga_path, chapter)
			raw_path = os.path.join(r'D:\Gdrive\My Drive\ZeroScans\RAW_demon_lackey', chapter) ## Outside tree folder
			
			shutil.move(chapter_path, raw_path)
		
		shutil.rmtree(manga_path)
		
	elif manga == '我老婆是魔王大人':
		for chapter in os.listdir(manga_path):
			chapter_path = os.path.join(manga_path, chapter)
			raw_path = os.path.join(r'D:\Gdrive\My Drive\ZeroScans\RAW_wife', chapter) ## Outside tree folder
			
			shutil.move(chapter_path, raw_path)
		
		shutil.rmtree(manga_path)

	else:
		for chapter in os.listdir(manga_path):
			chapter_path = os.path.join(manga_path, chapter)
			raw_path = os.path.join(upload_path, chapter.replace("Chapter ", "c"))
			
			if "Second Life Ranker" in raw_path:
				raw_path = raw_path.replace("[ZeroScans]", "(v3) [ZeroScans]")

			elif "The Undefeatable Swordsman" in raw_path:
				raw_path = raw_path.replace("[ZeroScans]", "(v2) [ZeroScans]")

			elif "Bowblade The Descendants of Bowblade" in raw_path:
				raw_path = raw_path.replace("[ZeroScans]", "(v2) [ZeroScans]")

			elif "I Was Planning to Become a Loyal Sword" in raw_path:
				raw_path = raw_path.replace("[ZeroScans]", "[Snowy Scans+ZeroScans]")

			shutil.move(chapter_path, raw_path)

		
		shutil.rmtree(manga_path)


## Upload chapter to mangadex
os.chdir(os.path.join(current_path, "mangadex_bulk_uploader"))
subprocess.run(['python', mangadex_path])
shutil.rmtree(uploaded_path)
os.mkdir(uploaded_path)

print("done")
