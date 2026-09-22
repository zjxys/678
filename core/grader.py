from __future__ import annotations

import jieba

from .models import Essay, GradeResult, AnalysisResult
from .analyzers import (
    ContentAnalyzer,
    StructureAnalyzer,
    LanguageAnalyzer,
    DevelopmentAnalyzer,
)


class EssayGrader:
    """高考语文作文评分调度器。

    整合四大分析器，输出完整的评分结果：
      - 内容维度（20 分）
      - 表达维度（20 分）= 结构（10 分）+ 语言（10 分）
      - 发展等级（20 分）
    总分 60 分。
    """

    def __init__(self):
        self.analyzers = {
            "content": ContentAnalyzer(),
            "structure": StructureAnalyzer(),
            "language": LanguageAnalyzer(),
            "development": DevelopmentAnalyzer(),
        }
        jieba.setLogLevel(20)

    def grade(self, text: str, title: str = "") -> GradeResult:
        text = text.strip()
        title = title.strip()

        essay = Essay(title=title, body=text)
        char_count = essay.char_count

        if char_count < 50:
            return self._too_short_result(essay)

        content_result = self.analyzers["content"].analyze(text, title)
        structure_result = self.analyzers["structure"].analyze(text, title)
        language_result = self.analyzers["language"].analyze(text, title)
        development_result = self.analyzers["development"].analyze(text, title)

        expression_score = structure_result.score + language_result.score
        expression_score = min(expression_score, 20.0)

        total = content_result.score + expression_score + development_result.score

        all_feedback = []
        for r in [content_result, structure_result, language_result, development_result]:
            all_feedback.extend(r.feedback)

        suggestions = self._generate_suggestions(
            content_result, structure_result, language_result, development_result, char_count
        )

        dimension_results = {
            "content": content_result,
            "structure": structure_result,
            "language": language_result,
            "development": development_result,
        }

        return GradeResult(
            total_score=total,
            content_score=content_result.score,
            expression_score=expression_score,
            development_score=development_result.score,
            max_total=60.0,
            max_content=20.0,
            max_expression=20.0,
            max_development=20.0,
            feedback=all_feedback,
            dimension_results=dimension_results,
            essay=essay,
            suggestions=suggestions,
        )

    def _too_short_result(self, essay: Essay) -> GradeResult:
        return GradeResult(
            total_score=5.0,
            content_score=2.0,
            expression_score=2.0,
            development_score=1.0,
            feedback=["文章字数过少，无法进行有效评分，请输入完整的作文内容。"],
            essay=essay,
            suggestions=["请确保作文不少于 800 字。"],
        )

    def _generate_suggestions(
        self,
        content: AnalysisResult,
        structure: AnalysisResult,
        language: AnalysisResult,
        development: AnalysisResult,
        char_count: int,
    ) -> list[str]:
        suggestions = []

        if char_count < 800:
            suggestions.append(
                f"当前字数 {char_count} 字，建议扩充至 800 字以上。"
            )

        if content.ratio < 0.7:
            suggestions.append("加强审题训练，确保文章内容紧扣题目要求。")
        if structure.ratio < 0.7:
            suggestions.append('练习使用"引论—本论—结论"的三段式结构。')
        if language.ratio < 0.7:
            suggestions.append("多阅读优秀范文，积累好词好句，提升语言表达力。")
        if development.ratio < 0.7:
            suggestions.append("在论述中尝试从多个角度深入分析，增强思想的深刻性和创新性。")

        if not suggestions:
            suggestions.append("整体表现良好，继续保持！可进一步提升文采和创新性。")

        return suggestions
