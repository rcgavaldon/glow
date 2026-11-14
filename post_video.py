"""Post a finished lamp's timelapse to its order page.
  python post_video.py G002-6P47D                 -> newest video_*.mp4 in Downloads
  python post_video.py G002-6P47D path\to\video.mp4
Crops tight around the print (cuts off the door glass), shrinks it, encrypts it with the
order code, and saves it into the site. Then: git add -A && git commit -m "video" && git push"""
import glob,os,re,subprocess,sys
import imageio_ffmpeg
code=re.sub(r'[^A-Z0-9]','',sys.argv[1].upper())
src=sys.argv[2] if len(sys.argv)>2 else max(glob.glob(os.path.expanduser('~/Downloads/video_*.mp4')),key=os.path.getmtime)
os.makedirs('videos',exist_ok=True); out=f'videos/{code}.mp4'
CROP='crop=1000:750:470:120,scale=1280:960'   # P2S camera, lamp at plate centre
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',src,'-vf',CROP,'-an','-c:v','libx264','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',out],check=True)
print('cropped',src,'->',out)
subprocess.run([sys.executable,'publish.py',code,'--video',out],check=True)
