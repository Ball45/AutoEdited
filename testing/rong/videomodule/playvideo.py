import subprocess


vlc = "/Applications/VLC.app/Contents/MacOS/VLC"
outfile = "media/tetest_out.mp4"
p1 =subprocess.run ([''+vlc+'', ''+outfile+'',  'vlc://quit'])
#p1 = subprocess.run(['ls', '-la'])
print(p1)