import cv2
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FrameCalculator(object):

    interval: int

    def build_cut_frames(self,
                         cap: cv2.VideoCapture,
                         start_time: int = 0,
                         end_time: Optional[int] = None):
        time = start_time
        stop_time = cap.get(cv2.CAP_PROP_FRAME_COUNT) if end_time is None else end_time
        frames = []
        while time < stop_time:
            frames.append(time)
            time = time + self.interval
        return frames

