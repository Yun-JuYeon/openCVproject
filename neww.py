import glob
import os.path

files = glob.glob('*.m4a')
for x in files:
 if not os.path.isdir(x):
  filename = os.path.splitext(x)
  os.rename(x, filename[0] + '.wav')