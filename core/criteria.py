SCORING_CRITERIA = {
    "content": {
        "name": "内容",
        "max_score": 20,
        "sub_dimensions": {
            "theme": {"name": "题意", "max_score": 5},
            "center": {"name": "中心", "max_score": 5},
            "material": {"name": "内容", "max_score": 5},
            "emotion": {"name": "感情", "max_score": 5},
        },
    },
    "expression": {
        "name": "表达",
        "max_score": 20,
        "sub_dimensions": {
            "genre": {"name": "文体", "max_score": 5},
            "structure": {"name": "结构", "max_score": 5},
            "language": {"name": "语言", "max_score": 5},
            "handwriting": {"name": "卷面", "max_score": 5},
        },
    },
    "development": {
        "name": "发展等级",
        "max_score": 20,
        "sub_dimensions": {
            "profound": {"name": "深刻", "max_score": 5},
            "rich": {"name": "丰富", "max_score": 5},
            "literary": {"name": "有文采", "max_score": 5},
            "innovative": {"name": "有创新", "max_score": 5},
        },
    },
}

CONTENT_KEYWORDS = {
    "positive_emotion": [
        "热爱", "感恩", "感动", "幸福", "快乐", "希望", "梦想",
        "温暖", "美好", "珍惜", "敬畏", "坚守", "担当", "奋斗",
    ],
    "negative_emotion": [
        "悲伤", "痛苦", "绝望", "愤怒", "恐惧", "孤独", "迷茫",
        "焦虑", "无奈", "遗憾",
    ],
    "argumentation": [
        "因此", "所以", "由此", "可见", "综上", "总之", "显然",
        "不难看出", "事实上", "毋庸置疑", "归根结底",
    ],
    "transition": [
        "然而", "但是", "不过", "与此相反", "另一方面", "诚然",
        "尽管如此", "换言之", "与此同时", "诚然", "固然",
    ],
    "rhetoric": [
        "如同一", "仿佛", "宛如", "好似", "犹如",
        "不是...而是", "既...又", "不仅...而且",
    ],
    "literary_devices": [
        "排比", "比喻", "拟人", "对偶", "反问", "设问",
        "引用", "夸张", "借代", "双关",
    ],
    "deep_thinking": [
        "本质", "根源", "内在", "深处", "背后", "底层",
        "究其原因", "追本溯源", "透过现象", "辩证", "反思",
    ],
    "innovation": [
        "独特", "新颖", "别具一格", "另辟蹊径", "独树一帜",
        "前所未有", "打破常规", "与众不同",
    ],
    "classical_quotes": [
        "古人云", "正如", "曾言", "有诗云", "所谓",
        "孔子曰", "孟子曰", "老子曰", "庄子曰", "《", "》",
    ],
}

STRUCTURE_PATTERNS = {
    "paragraph_starters": [
        "首先", "其次", "再次", "最后", "其一", "其二",
        "一方面", "另一方面", "第一", "第二", "第三",
    ],
    "conclusion_starters": [
        "总而言之", "综上所述", "综上", "由此可见",
        "归根结底", "总之", "由此观之",
    ],
    "opening_patterns": [
        "在", "从", "当今", "如今", "纵观", "放眼",
        "时光", "岁月", "历史", "人生",
    ],
}

DEVELOPMENT_INDICATORS = {
    "profound": {
        "keywords": ["本质", "根源", "规律", "必然", "内在联系", "辩证"],
        "description": "透过现象看本质，揭示事物内在关系",
    },
    "rich": {
        "keywords": ["丰富", "充实", "多元", "广博", "引经据典"],
        "description": "材料丰富，论据充实",
    },
    "literary": {
        "keywords": ["文采", "生动", "优美", "典雅", "凝练"],
        "description": "用词贴切，句式灵活，善用修辞",
    },
    "innovative": {
        "keywords": ["独特", "新颖", "别具一格", "独辟蹊径", "突破"],
        "description": "见解新颖，材料新鲜，构思新巧",
    },
}


def get_criteria_summary() -> dict:
    return {
        dim: {
            "name": info["name"],
            "max_score": info["max_score"],
            "sub_dimensions": {
                k: v["name"] for k, v in info["sub_dimensions"].items()
            },
        }
        for dim, info in SCORING_CRITERIA.items()
    }
