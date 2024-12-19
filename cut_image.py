from movie.cutter import Movie2Img
from datetime import datetime
import os


positions = None
#positions = (0, 530, 0, 1280)

base_name = "test"
test_data = os.path.join("test_data", base_name + ".mp4")
output_dir = os.path.join("result", base_name)

movie_2_img = Movie2Img(interval=1, cut_pos=positions)

movie_2_img.save_frames(test_data, output_dir, base_name)
