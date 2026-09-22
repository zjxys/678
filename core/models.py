from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Essay:
    title: str
    body: str
    grade_level: str = "高中"

    @property
    def char_count(self) -> int:
        return len(self.body.replace(" ", "").replace("\n", "").replace("\r", ""))


@dataclass
class AnalysisResult:
    score: float
    max_score: float
    dimension: str
    feedback: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    @property
    def ratio(self) -> float:
        if self.max_score == 0:
            return 0.0
        return self.score / self.max_score


@dataclass
class GradeResult:
    total_score: float
    content_score: float
    expression_score: float
    development_score: float
    max_total: float = 60.0
    max_content: float = 20.0
    max_expression: float = 20.0
    max_development: float = 20.0
    feedback: list[str] = field(default_factory=list)
    dimension_results: dict[str, AnalysisResult] = field(default_factory=dict)
    essay: Optional[Essay] = None
    grade_level_label: str = ""
    suggestions: list[str] = field(default_factory=list)

    @property
    def grade_label(self) -> str:
        ratio = self.total_score / self.max_total
        if ratio >= 0.90:
            return "一类文"
        elif ratio >= 0.80:
            return "二类文"
        elif ratio >= 0.70:
            return "三类文"
        elif ratio >= 0.60:
            return "四类文"
        else:
            return "五类文"

    def to_dict(self) -> dict:
        return {
            "total_score": round(self.total_score, 1),
            "content_score": round(self.content_score, 1),
            "expression_score": round(self.expression_score, 1),
            "development_score": round(self.development_score, 1),
            "max_total": self.max_total,
            "max_content": self.max_content,
            "max_expression": self.max_expression,
            "max_development": self.max_development,
            "grade_label": self.grade_label,
            "feedback": self.feedback,
            "suggestions": self.suggestions,
            "char_count": self.essay.char_count if self.essay else 0,
            "dimensions": {
                k: {
                    "score": round(v.score, 1),
                    "max_score": v.max_score,
                    "feedback": v.feedback,
                    "details": v.details,
                }
                for k, v in self.dimension_results.items()
            },
        }
