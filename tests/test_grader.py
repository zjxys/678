import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.grader import EssayGrader
from core.models import GradeResult, AnalysisResult


class TestEssayGrader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.grader = EssayGrader()

    def test_short_text_returns_low_score(self):
        result = self.grader.grade("这是一段很短的文字。")
        self.assertLess(result.total_score, 10)
        self.assertTrue(any("字数过少" in f for f in result.feedback))

    def test_normal_essay_returns_valid_result(self):
        essay = self._load_sample("good_essay")
        result = self.grader.grade(essay["body"], essay["title"])
        self.assertIsInstance(result, GradeResult)
        self.assertGreater(result.total_score, 20)
        self.assertLessEqual(result.total_score, 60)

    def test_scores_within_bounds(self):
        essay = self._load_sample("good_essay")
        result = self.grader.grade(essay["body"], essay["title"])
        self.assertGreaterEqual(result.content_score, 0)
        self.assertLessEqual(result.content_score, 20)
        self.assertGreaterEqual(result.expression_score, 0)
        self.assertLessEqual(result.expression_score, 20)
        self.assertGreaterEqual(result.development_score, 0)
        self.assertLessEqual(result.development_score, 20)

    def test_empty_title_works(self):
        result = self.grader.grade("这是一段测试文字，用于验证无标题时系统是否正常工作。" * 20)
        self.assertIsInstance(result, GradeResult)

    def test_to_dict_format(self):
        result = self.grader.grade("测试文字内容。" * 50, "测试")
        d = result.to_dict()
        self.assertIn("total_score", d)
        self.assertIn("content_score", d)
        self.assertIn("expression_score", d)
        self.assertIn("development_score", d)
        self.assertIn("feedback", d)
        self.assertIn("grade_label", d)

    def test_grade_label_classification(self):
        result = self.grader.grade("短", "短")
        self.assertIn(result.grade_label, ["一类文", "二类文", "三类文", "四类文", "五类文"])

    def _load_sample(self, key):
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "examples", "sample_essays.json"
        )
        with open(sample_path, encoding="utf-8") as f:
            data = json.load(f)
        return data[key]


class TestAnalyzers(unittest.TestCase):
    def setUp(self):
        from core.analyzers import (
            ContentAnalyzer, StructureAnalyzer,
            LanguageAnalyzer, DevelopmentAnalyzer
        )
        self.analyzers = {
            "content": ContentAnalyzer(),
            "structure": StructureAnalyzer(),
            "language": LanguageAnalyzer(),
            "development": DevelopmentAnalyzer(),
        }

    def test_analyzers_return_valid_results(self):
        text = "这是一段用于测试的文字。" * 30
        for name, analyzer in self.analyzers.items():
            result = analyzer.analyze(text, "测试")
            self.assertIsInstance(result, AnalysisResult)
            self.assertGreaterEqual(result.score, 0)
            self.assertLessEqual(result.score, result.max_score)


if __name__ == "__main__":
    unittest.main()
