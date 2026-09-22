from __future__ import annotations

import re

from .base import BaseAnalyzer
from ..models import AnalysisResult
from ..criteria import CONTENT_KEYWORDS


class LanguageAnalyzer(BaseAnalyzer):
    """语言维度分析器（满分 10 分，属于表达维度）。

    子维度：语言（5 分）、卷面/格式（5 分）。
    """

    def __init__(self):
        super().__init__("language", 10)

    def analyze(self, text: str, title: str = "") -> AnalysisResult:
        feedback = []
        details = {}

        language_score = self._analyze_language(text)
        format_score = self._analyze_format(text)

        details["language"] = {"score": language_score, "max": 5}
        details["format"] = {"score": format_score, "max": 5}

        if language_score < 3:
            feedback.append("语言表达有待提升，建议注意语句通顺和用词准确。")
        elif language_score >= 4:
            feedback.append("语言流畅，表达准确。")

        if format_score < 3:
            feedback.append("标点或段落格式存在瑕疵，建议检查标点使用是否规范。")

        total = language_score + format_score
        return AnalysisResult(
            score=total,
            max_score=self.max_score,
            dimension="表达·语言",
            feedback=feedback,
            details=details,
        )

    def _analyze_language(self, text: str) -> float:
        score = 2.0
        sentences = self._split_sentences(text)
        if not sentences:
            return 1.0

        avg_len = sum(len(s) for s in sentences) / len(sentences)
        if 15 <= avg_len <= 40:
            score += 1.0
        elif avg_len < 10:
            feedback_note = True
        else:
            score += 0.5

        transition_count = self._count_any(text, CONTENT_KEYWORDS["transition"])
        if transition_count >= 2:
            score += 1.0
        elif transition_count >= 1:
            score += 0.5

        rhetoric_count = self._count_any(text, CONTENT_KEYWORDS["rhetoric"])
        if rhetoric_count >= 2:
            score += 1.0
        elif rhetoric_count >= 1:
            score += 0.5

        return self._clamp(score)

    def _analyze_format(self, text: str) -> float:
        score = 3.0
        punctuation_count = len(re.findall(r"[，。！？；：、""''《》（）—…]", text))
        char_count = len(text.replace(" ", "").replace("\n", ""))
        if char_count > 0:
            ratio = punctuation_count / char_count
            if 0.03 <= ratio <= 0.08:
                score += 1.5
            elif ratio < 0.02:
                score -= 1.0
            elif ratio > 0.10:
                score -= 0.5

        mixed_punct = len(re.findall(r"[,.!?;:]", text))
        if mixed_punct > punctuation_count * 0.3 and punctuation_count > 5:
            score -= 0.5

        paragraphs = self._split_paragraphs(text)
        if len(paragraphs) >= 3:
            score += 0.5

        return self._clamp(score)
