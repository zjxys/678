from __future__ import annotations

import jieba
import re

from .base import BaseAnalyzer
from ..models import AnalysisResult
from ..criteria import CONTENT_KEYWORDS


class ContentAnalyzer(BaseAnalyzer):
    """内容维度分析器（满分 20 分）。

    子维度：题意、中心、内容、感情。
    """

    def __init__(self):
        super().__init__("content", 20)

    def analyze(self, text: str, title: str = "") -> AnalysisResult:
        feedback = []
        details = {}

        theme_score = self._analyze_theme(text, title)
        center_score = self._analyze_center(text)
        material_score = self._analyze_material(text)
        emotion_score = self._analyze_emotion(text)

        details["theme"] = {"score": theme_score, "max": 5}
        details["center"] = {"score": center_score, "max": 5}
        details["material"] = {"score": material_score, "max": 5}
        details["emotion"] = {"score": emotion_score, "max": 5}

        if title:
            title_words = set(jieba.cut(title))
            title_words = {w for w in title_words if len(w) > 1}
            body_hits = sum(1 for w in title_words if w in text)
            coverage = body_hits / max(len(title_words), 1)
            if coverage < 0.3:
                feedback.append("文章与题目关联度较低，建议紧扣题意展开论述。")
            elif coverage >= 0.7:
                feedback.append("文章紧扣题意，主题切合度高。")

        if center_score < 3:
            feedback.append("中心论点不够明确，建议在文章开头或结尾点明主旨。")
        elif center_score >= 4:
            feedback.append("中心思想明确突出。")

        if material_score < 3:
            feedback.append("论据和素材偏少，建议增加具体事例或引用来充实内容。")
        elif material_score >= 4:
            feedback.append("内容充实，素材运用得当。")

        if emotion_score < 3:
            feedback.append("情感表达不够充分，建议融入更真挚的情感体验。")

        total = theme_score + center_score + material_score + emotion_score
        return AnalysisResult(
            score=total,
            max_score=self.max_score,
            dimension="内容",
            feedback=feedback,
            details=details,
        )

    def _analyze_theme(self, text: str, title: str) -> float:
        if not title:
            return 3.5
        title_words = set(jieba.cut(title))
        title_words = {w for w in title_words if len(w) > 1}
        if not title_words:
            return 3.5
        body_hits = sum(1 for w in title_words if w in text)
        coverage = body_hits / len(title_words)
        if coverage >= 0.7:
            return 5.0
        elif coverage >= 0.5:
            return 4.0
        elif coverage >= 0.3:
            return 3.0
        else:
            return 2.0

    def _analyze_center(self, text: str) -> float:
        first_para = text[:200]
        last_para = text[-200:]
        center_indicators = [
            "我认为", "在我看来", "本文", "总之", "归根结底",
            "核心", "关键", "根本", "本质", "主旨", "意在",
        ]
        first_hits = self._count_any(first_para, center_indicators)
        last_hits = self._count_any(last_para, center_indicators)
        total_hits = first_hits + last_hits
        if total_hits >= 3:
            return 5.0
        elif total_hits >= 2:
            return 4.0
        elif total_hits >= 1:
            return 3.5
        else:
            arg_words = CONTENT_KEYWORDS["argumentation"]
            if self._count_any(text, arg_words) >= 3:
                return 4.0
            return 2.5

    def _analyze_material(self, text: str) -> float:
        score = 1.5
        char_count = len(text.replace(" ", "").replace("\n", ""))
        if char_count >= 800:
            score += 1.0
        elif char_count >= 600:
            score += 0.5
        quotes = len(re.findall(r"[《""]", text))
        if quotes >= 2:
            score += 1.0
        elif quotes >= 1:
            score += 0.5
        examples = self._count_any(text, ["例如", "比如", "譬如", "以", "正如", "曾"])
        if examples >= 3:
            score += 1.0
        elif examples >= 1:
            score += 0.5
        return self._clamp(score)

    def _analyze_emotion(self, text: str) -> float:
        positive = self._count_keywords(text, CONTENT_KEYWORDS["positive_emotion"])
        negative = self._count_keywords(text, CONTENT_KEYWORDS["negative_emotion"])
        total = positive + negative
        if total >= 5:
            return 5.0
        elif total >= 3:
            return 4.0
        elif total >= 1:
            return 3.0
        else:
            return 2.0
