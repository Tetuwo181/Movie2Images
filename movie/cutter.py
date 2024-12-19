import cv2
import os
from datetime import datetime
from typing import Union, Optional, List, Tuple, Callable
from .frame import FrameCalculator


ImgPositions = Tuple[int, int, int, int]


class Movie2Img(object):

    def __init__(self, interval: int = 1, ext: str = "jpg", cut_pos: Optional[ImgPositions] = None):

        self.__ext = ext
        self.__record_img = build_img_recorder(cut_pos)
        self.__frame_calculator = FrameCalculator(interval)

    def save_a_frame(self,
                     capture: cv2.VideoCapture,
                     frame_num: int,
                     result_dir: str,
                     result_basename: str) -> Union[str, bool]:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = capture.read()
        if ret:
            result_path = self.build_result_path(result_dir, result_basename, frame_num)
            self.__record_img(result_path, frame)
            return result_path
        return False

    def save_frames(self,
                    video_path: str,
                    result_dir: str,
                    result_basename: str,
                    start_time: int = 0,
                    end_time: Optional[int] = None
                    ) -> List[str]:
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            return False
        os.makedirs(result_dir, exist_ok=True)
        pickup_frames = self.__frame_calculator.build_cut_frames(capture, start_time, end_time)
        results = (self.save_a_frame(capture, frame, result_dir, result_basename) for frame
                   in pickup_frames)
        return [result for result in results if type(result) is str]

    def build_result_path(self,
                          result_dir: str,
                          result_basename: str,
                          frame_num: int):
        return os.path.join(result_dir, result_basename + str(frame_num) + "." + self.__ext)


def build_img_recorder(cut_pos: Optional[ImgPositions]) -> Callable[[str, cv2.VideoCapture], None]:
    def non_trim_image(image_path, frame): \
            return cv2.imwrite(image_path, frame)

    if cut_pos is None:
        return non_trim_image

    def trim_and_record(image_path, frame):
        trimmed = frame[cut_pos[0]: cut_pos[1], cut_pos[2]: cut_pos[3]]
        cv2.imwrite(image_path, trimmed)

    return trim_and_record
