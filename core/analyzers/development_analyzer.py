from __future__ import annotations

import re

from .base import BaseAnalyzer
from ..models import AnalysisResult
from ..criteria import CONTENT_KEYWORDS, DEVELOPMENT_INDICATORS


class DevelopmentAnalyzer(BaseAnalyzer):
    """发展等级分析器（满分 20 分）。

    子维度：深刻、丰富、有文采、有创新。
    """

    def __init__(self):
        super().__init__("development", 20)

    def analyze(self, text: str, title: str = "") -> AnalysisResult:
        feedback = []
        details = {}

        profound_score = self._analyze_profound(text)
        rich_score = self._analyze_rich(text)
        literary_score = self._analyze_literary(text)
        innovative_score = self._analyze_innovative(text)

        details["profound"] = {"score": profound_score, "max": 5}
        details["rich"] = {"score": rich_score, "max": 5}
        details["literary"] = {"score": literary_score, "max": 5}
        details["innovative"] = {"score": innovative_score, "max": 5}

        if profound_score >= 4:
            feedback.append("论述深刻，能透过现象看本质。")
        elif profound_score < 3:
            feedback.append("思想深度有待提升，建议多从本质和规律层面思考问题。")

        if rich_score >= 4:
            feedback.append("材料丰富，论据充实有力。")
        elif rich_score < 3:
            feedback.append("内容略显单薄，建议增加多元素材。")

        if literary_score >= 4:
            feedback.append("语言富有文采，修辞运用得当。")
        elif literary_score < 3:
            feedback.append("文采方面有待加强，可尝试使用比喻、排比等修辞手法。")

        if innovative_score >= 4:
            feedback.append("见解新颖，构思巧妙。")
        elif innovative_score < 3:
            feedback.append("创新性不足，可尝试从独特视角立意。")

        total = profound_score + rich_score + literary_score + innovative_score
        return AnalysisResult(
            score=total,
            max_score=self.max_score,
            dimension="发展等级",
            feedback=feedback,
            details=details,
        )

    def _analyze_profound(self, text: str) -> float:
        deep_words = CONTENT_KEYWORDS["deep_thinking"]
        count = self._count_any(text, deep_words)
        if count >= 4:
            return 5.0
        elif count >= 3:
            return 4.0
        elif count >= 2:
            return 3.0
        elif count >= 1:
            return 2.5
        return 2.0

    def _analyze_rich(self, text: str) -> float:
        score = 2.0
        quotes = len(re.findall(r"[《""]", text))
        if quotes >= 4:
            score += 1.5
        elif quotes >= 2:
            score += 1.0
        elif quotes >= 1:
            score += 0.5

        examples = self._count_any(text, ["例如", "比如", "譬如", "以", "正如", "曾", "譬如"])
        if examples >= 3:
            score += 1.5
        elif examples >= 2:
            score += 1.0
        elif examples >= 1:
            score += 0.5

        return self._clamp(score)

    def _analyze_literary(self, text: str) -> float:
        score = 2.0
        rhetoric_count = self._count_any(text, CONTENT_KEYWORDS["rhetoric"])
        if rhetoric_count >= 3:
            score += 2.0
        elif rhetoric_count >= 2:
            score += 1.5
        elif rhetoric_count >= 1:
            score += 1.0

        classical = self._count_any(text, CONTENT_KEYWORDS["classical_quotes"])
        if classical >= 2:
            score += 1.0
        elif classical >= 1:
            score += 0.5

        return self._clamp(score)

    def _analyze_innovative(self, text: str) -> float:
        score = 2.0
        innovation_words = CONTENT_KEYWORDS["innovation"]
        count = self._count_any(text, innovation_words)
        if count >= 2:
            score += 2.0
        elif count >= 1:
            score += 1.0

        question_marks = text.count("？") + text.count("?")
        if question_marks >= 3:
            score += 1.0
        elif question_marks >= 1:
            score += 0.5

        transition_words = CONTENT_KEYWORDS["transition"]
        if self._count_any(text, transition_words) >= 2:
            score += 0.5

        return self._clamp(score)
