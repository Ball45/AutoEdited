import auditok
region = auditok.load("media\\time3.wav")  # returns an AudioRegion object
regions = region.split_and_plot(...)  # or just region.splitp()
