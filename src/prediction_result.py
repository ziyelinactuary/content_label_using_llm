from __future__ import annotations
from dataclasses import dataclass

@dataclass
class PredictionResult:
    """Class for keeping track of an item in inventory."""
    segments: [int]
    canonical_label: str
    raw_label: str
    true_positive: int = 0
    false_positive: int = 0
    true_negative: int = 0
    false_negative: int = 0

    def accumulate(self, prediction_result: PredictionResult) -> PredictionResult:
        self.segments = self.segments + prediction_result.segments
        self.true_positive += prediction_result.true_positive
        self.true_negative += prediction_result.true_negative
        self.false_positive += prediction_result.false_positive
        self.false_negative += prediction_result.false_negative
        return self