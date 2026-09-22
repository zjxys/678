from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Optional

from ..models import AnalysisResult


class BaseAnalyzer(ABC):
    """分析器基类，所有维度分析器继承此类。"""

    def __init__(self, name: str, max_score: float):
        self.name = name
        self.max_score = max_score

    @abstractmethod
    def analyze(self, text: str, title: str = "") -> AnalysisResult:
        pass

    def _count_keywords(self, text: str, keywords: list[str]) -> int:
        count = 0
        for kw in keywords:
            count += text.count(kw)
        return count

    def _count_any(self, text: str, keywords: list[str]) -> int:
        return sum(1 for kw in keywords if kw in text)

    def _split_paragraphs(self, text: str) -> list[str]:
        paragraphs = [p.strip() for p in re.split(r"[\n\r]+", text) if p.strip()]
        return paragraphs

    def _split_sentences(self, text: str) -> list[str]:
        sentences = re.split(r"[。！？；!?;]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _clamp(self, value: float, low: float = 0, high: float = None) -> float:
        high = high if high is not None else self.max_score
        return max(low, min(high, value))
