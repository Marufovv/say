"""WIUT official interface; inference is entirely local. See README for class coverage."""
from src.events import OFFICIAL_CLASSES
from src.pipeline import analyze

CLASSES=list(OFFICIAL_CLASSES)
RISK_HORIZON_SEC=5.0

def detect_events(video_path: str) -> list[list]:
    return analyze(video_path,collect=False)['events']

class RiskEstimator:
    """Optional Part B is intentionally the unchanged zero-risk strategy.
    No file opening, future-frame access, or Part A cache reuse.
    """
    def reset(self,meta:dict)->None:
        self.meta=dict(meta)
    def step(self,frame,t_sec:float)->float:
        return 0.0
