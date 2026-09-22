from __future__ import annotations

import re

from .base import BaseAnalyzer
from ..models import AnalysisResult
from ..criteria import STRUCTURE_PATTERNS


class StructureAnalyzer(BaseAnalyzer):
    """结构维度分析器（满分 10 分，属于表达维度）。

    子维度：文体（5 分）、结构（5 分）。
    """

    def __init__(self):
        super().__init__("structure", 10)

    def analyze(self, text: str, title: str = "") -> AnalysisResult:
        feedback = []
        details = {}

        genre_score = self._analyze_genre(text)
        structure_score = self._analyze_structure(text)

        details["genre"] = {"score": genre_score, "max": 5}
        details["structure"] = {"score": structure_score, "max": 5}

        if genre_score < 3:
            feedback.append("文体特征不够鲜明，建议明确议论文或记叙文的写作规范。")
        elif genre_score >= 4:
            feedback.append("文体特征鲜明，符合写作规范。")

        if structure_score < 3:
            feedback.append('文章结构不够清晰，建议使用"总—分—总"等常见结构框架。')
        elif structure_score >= 4:
            feedback.append("结构严谨，层次分明。")

        total = genre_score + structure_score
        return AnalysisResult(
            score=total,
            max_score=self.max_score,
            dimension="表达·结构",
            feedback=feedback,
            details=details,
        )

    def _analyze_genre(self, text: str) -> float:
        argumentation_markers = [
            "论点", "论据", "论证", "首先", "其次", "因此",
            "由此可见", "综上所述", "不难发现",
        ]
        narration_markers = [
            "那天", "记得", "小时候", "后来", "突然", "这时",
            "于是", "走到", "看到", "听到",
        ]
        arg_count = self._count_any(text, argumentation_markers)
        nar_count = self._count_any(text, narration_markers)
        if arg_count >= 3 and arg_count > nar_count:
            return 5.0
        elif nar_count >= 3 and nar_count > arg_count:
            return 4.5
        elif arg_count >= 2 or nar_count >= 2:
            return 3.5
        else:
            return 2.5

    def _analyze_structure(self, text: str) -> float:
        paragraphs = self._split_paragraphs(text)
        score = 1.5
        if len(paragraphs) >= 5:
            score += 1.5
        elif len(paragraphs) >= 3:
            score += 1.0
        elif len(paragraphs) >= 2:
            score += 0.5

        starters = STRUCTURE_PATTERNS["paragraph_starters"]
        has_ordered = self._count_any(text, starters)
        if has_ordered >= 2:
            score += 1.0
        elif has_ordered >= 1:
            score += 0.5

        conclusion = STRUCTURE_PATTERNS["conclusion_starters"]
        if self._count_any(text, conclusion) >= 1:
            score += 1.0

        opening = STRUCTURE_PATTERNS["opening_patterns"]
        if self._count_any(text, opening) >= 1:
            score += 0.5

        return self._clamp(score)
