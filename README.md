# 高考语文作文自动批改框架

一个基于规则分析与自然语言处理的高考语文作文自动批改框架，提供 Web 界面，可快速部署为在线评分网站。

## 评分标准

参照全国高考语文作文评分标准，总分 **60 分**：

| 等级 | 维度 | 分值 | 说明 |
|------|------|------|------|
| 基础等级 | 内容 | 20 分 | 题意、中心、内容、感情 |
| 基础等级 | 表达 | 20 分 | 文体、结构、语言、字迹 |
| 发展等级 | 发展 | 20 分 | 深刻、丰富、有文采、有创新 |

## 项目结构

```
gaokao-essay-grader/
├── app.py                    # Flask Web 应用入口
├── config.py                 # 配置文件
├── requirements.txt          # 依赖列表
├── core/                     # 核心评分引擎
│   ├── grader.py             # 评分调度器
│   ├── criteria.py           # 评分标准定义
│   ├── models.py             # 数据模型
│   └── analyzers/            # 各维度分析器
│       ├── content_analyzer.py       # 内容分析
│       ├── structure_analyzer.py     # 结构分析
│       ├── language_analyzer.py      # 语言分析
│       └── development_analyzer.py   # 发展等级分析
├── templates/                # HTML 模板
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/                   # 静态资源
│   ├── css/style.css
│   └── js/main.js
├── tests/                    # 测试
│   └── test_grader.py
└── examples/                 # 示例
    └── sample_essays.json
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动 Web 服务

```bash
python app.py
```

浏览器访问 `http://127.0.0.1:5000` 即可使用。

### 作为 API 调用

```python
from core.grader import EssayGrader

grader = EssayGrader()
result = grader.grade("你的作文内容", title="作文题目")

print(f"总分: {result.total_score}")
print(f"内容: {result.content_score}")
print(f"表达: {result.expression_score}")
print(f"发展: {result.development_score}")
for item in result.feedback:
    print(f"- {item}")
```

## 扩展自定义分析器

```python
from core.analyzers.base import BaseAnalyzer
from core.models import AnalysisResult

class MyAnalyzer(BaseAnalyzer):
    def analyze(self, text: str, title: str = "") -> AnalysisResult:
        score = self._calculate(text)
        feedback = self._generate_feedback(text)
        return AnalysisResult(score=score, max_score=20, feedback=feedback)

    def _calculate(self, text: str) -> float:
        # 你的评分逻辑
        return 15.0
```

然后在 `grader.py` 中注册：

```python
self.analyzers["custom"] = MyAnalyzer()
```

## 技术栈

- **后端**: Python + Flask
- **NLP**: jieba 分词 + 规则引擎
- **前端**: HTML5 + CSS3 + 原生 JavaScript

## License

MIT
