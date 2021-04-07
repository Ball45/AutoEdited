from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

# Load the image specifying the regions.
# im = ImageClip("../../ultracompositing/motif.png")

# Loacate the regions, return a list of ImageClips
regions = findObjects(im)


# Load 7 clips from the US National Parks. Public Domain :D
clips = [VideoFileClip(n, audio=False).subclip(0, 5) for n in
         ["media/0001 (1).mp4",
          "media/0001 (2).mp4",
          "media/0001 (3).mp4",
          "media/0001 (4).mp4",
          "media/0001 (5).mp4",
          "media/0001 (6).mp4",
          "media/0001 (7).mp4"]]

# fit each clip into its region
comp_clips = [c.resize(r.size)
              .set_mask(r.mask)
              .set_pos(r.screenpos)
              for c, r in zip(clips, regions)]

cc = CompositeVideoClip(comp_clips, im.size)
cc.resize(0.6).write_videofile("media/composition.mp4")

# Note that this particular composition takes quite a long time of
# rendering (about 20s on my computer for just 4s of video).
