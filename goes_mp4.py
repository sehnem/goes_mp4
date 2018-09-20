from download import get_goes
from datetime import datetime
from satpy import Scene
from glob import glob
from satpy.multiscene import MultiScene

path = './data/'
start = datetime(2018,9,18,14)
end = datetime(2018,9,18,19)

files = get_goes(16, 'Rad', 'M1', start=start, end=end, bands=[1,2,3], path=path)

all_filenames = [glob(fn.replace('C01', 'C0[123]*')[:len(path) + 50] + '*.nc') for fn in sorted([f for f in files if 'C01' in f])]
scenes = [Scene(reader='abi_l1b', filenames=filenames) for filenames in all_filenames]

mscn = MultiScene(scenes)
mscn.load(['true_color'])
new_mscn = mscn.resample(resampler='native')
new_mscn.save_animation('./{name}_{start_time:%Y%m%d_%H%M%S}.mp4', fps=5)
