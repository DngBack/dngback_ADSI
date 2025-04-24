#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Generation Implementation for Collaborative Fast & Slow Thinking Systems
"""

import os
import json
import random
import argparse
import uuid
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# Thư viện cần thiết - cần cài đặt trước khi chạy
# pip install requests tqdm numpy pandas openai

import requests
import numpy as np
import pandas as pd
from tqdm import tqdm

# Cấu hình
CONFIG = {
    "output_dir": "generated_data",
    "benchmark_data_dir": "benchmark_data",
    "llm_api_key": os.environ.get("OPENAI_API_KEY", ""),
    "llm_model": "gpt-4",
    "num_samples": {
        "fast_only": 100,
        "slow_only": 100,
        "fast_then_slow": 150,
        "parallel": 75,
        "iterative": 75
    },
    "complexity_thresholds": {
        "simple": (0.0, 0.3),
        "medium": (0.3, 0.6),
        "complex": (0.6, 0.8),
        "very_complex": (0.8, 1.0)
    },
    "task_types": [
        "reasoning", "creative", "qa", "decision", "programming", "math", "logic", "language"
    ],
    "domains": [
        "math", "logic", "language", "science", "programming", "common_sense", "decision_making"
    ]
}

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(CONFIG["output_dir"], exist_ok=True)
os.makedirs(CONFIG["benchmark_data_dir"], exist_ok=True)

# Lớp cơ sở cho việc tạo dữ liệu
class DataGenerator:
    """Lớp cơ sở cho việc tạo dữ liệu"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.generated_data = []
    
    def generate(self, num_samples: int) -> List[Dict[str, Any]]:
        """Phương thức tạo dữ liệu cơ bản"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def save(self, filename: str) -> None:
        """Lưu dữ liệu đã tạo vào file JSON"""
        output_path = os.path.join(self.config["output_dir"], filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.generated_data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(self.generated_data)} samples to {output_path}")

# Lớp tạo dữ liệu từ benchmark có sẵn
class BenchmarkDataGenerator(DataGenerator):
    """Lớp tạo dữ liệu từ benchmark có sẵn"""
    
    def __init__(self, config: Dict[str, Any], benchmark_name: str):
        super().__init__(config)
        self.benchmark_name = benchmark_name
        self.benchmark_data = self._load_benchmark_data()
    
    def _load_benchmark_data(self) -> List[Dict[str, Any]]:
        """Tải dữ liệu benchmark từ file"""
        benchmark_path = os.path.join(self.config["benchmark_data_dir"], f"{self.benchmark_name}.json")
        if not os.path.exists(benchmark_path):
            print(f"Benchmark file {benchmark_path} not found. Creating empty dataset.")
            return []
        
        with open(benchmark_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate(self, num_samples: int) -> List[Dict[str, Any]]:
        """Chuyển đổi dữ liệu benchmark sang định dạng mới"""
        if not self.benchmark_data:
            print(f"No benchmark data available for {self.benchmark_name}")
            return []
        
        # Lấy mẫu ngẫu nhiên từ benchmark data
        samples = random.sample(self.benchmark_data, min(num_samples, len(self.benchmark_data)))
        
        for sample in tqdm(samples, desc=f"Converting {self.benchmark_name} data"):
            converted_sample = self._convert_sample(sample)
            self.generated_data.append(converted_sample)
        
        return self.generated_data
    
    def _convert_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Chuyển đổi một mẫu từ benchmark sang định dạng mới"""
        # Triển khai cụ thể tùy thuộc vào loại benchmark
        # Đây là một ví dụ chung
        
        # Phân tích độ phức tạp
        complexity_score = self._analyze_complexity(sample)
        task_type = self._determine_task_type(sample)
        constraints = self._extract_constraints(sample)
        strategy = self._recommend_strategy(complexity_score, task_type)
        
        # Tạo quá trình tư duy
        fast_thinking = self._generate_fast_thinking(sample) if strategy in ["fast_only", "fast_then_slow", "parallel", "iterative"] else {"process": "", "simplified_task": "", "intermediate_result": ""}
        slow_thinking = self._generate_slow_thinking(sample) if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"] else {"decomposition": [], "reasoning": [], "verification": [], "intermediate_result": ""}
        
        # Tạo quá trình tích hợp
        integration = self._generate_integration(sample, fast_thinking, slow_thinking, strategy)
        
        # Tạo kết quả cuối cùng
        output = {
            "final_answer": sample.get("answer", ""),
            "explanation": sample.get("explanation", "")
        }
        
        # Tạo metadata
        metadata = {
            "domain": self._determine_domain(sample),
            "difficulty": self._determine_difficulty(complexity_score),
            "source": f"benchmark_{self.benchmark_name}",
            "quality_score": random.uniform(0.8, 1.0),
            "tags": self._generate_tags(sample, task_type, strategy)
        }
        
        # Tạo mẫu hoàn chỉnh
        converted_sample = {
            "id": f"{self.benchmark_name}_{str(uuid.uuid4())[:8]}",
            "task": {
                "instruction": sample.get("question", sample.get("instruction", "")),
                "input": sample.get("input", ""),
                "context": sample.get("context", "")
            },
            "analysis": {
                "complexity_score": complexity_score,
                "task_type": task_type,
                "constraints": constraints,
                "recommended_strategy": strategy
            },
            "thinking_processes": {
                "fast_thinking": fast_thinking,
                "slow_thinking": slow_thinking
            },
            "integration": integration,
            "output": output,
            "metadata": metadata
        }
        
        return converted_sample
    
    def _analyze_complexity(self, sample: Dict[str, Any]) -> float:
        """Phân tích độ phức tạp của mẫu"""
        # Triển khai phân tích độ phức tạp dựa trên các đặc điểm của mẫu
        # Đây là một ví dụ đơn giản
        
        complexity_indicators = {
            "length": len(str(sample.get("question", sample.get("instruction", "")))),
            "has_constraints": 1 if "constraints" in sample else 0,
            "has_context": 1 if sample.get("context", "") else 0,
            "difficulty": sample.get("difficulty", "medium")
        }
        
        # Tính điểm độ phức tạp dựa trên các chỉ số
        length_score = min(complexity_indicators["length"] / 500, 1.0)
        constraint_score = complexity_indicators["has_constraints"] * 0.2
        context_score = complexity_indicators["has_context"] * 0.2
        
        difficulty_map = {"easy": 0.2, "medium": 0.5, "hard": 0.8, "expert": 1.0}
        difficulty_score = difficulty_map.get(complexity_indicators["difficulty"], 0.5)
        
        # Tính điểm tổng hợp
        complexity_score = (length_score * 0.3 + constraint_score * 0.2 + context_score * 0.2 + difficulty_score * 0.3)
        
        return round(min(max(complexity_score, 0.0), 1.0), 2)
    
    def _determine_task_type(self, sample: Dict[str, Any]) -> str:
        """Xác định loại nhiệm vụ của mẫu"""
        # Triển khai xác định loại nhiệm vụ dựa trên các đặc điểm của mẫu
        # Đây là một ví dụ đơn giản
        
        task_type = sample.get("task_type", "")
        if task_type and task_type in self.config["task_types"]:
            return task_type
        
        # Nếu không có task_type, thử phân tích từ nội dung
        instruction = sample.get("question", sample.get("instruction", "")).lower()
        
        if any(kw in instruction for kw in ["calculate", "solve", "compute", "find the value", "equation"]):
            return "math"
        elif any(kw in instruction for kw in ["write", "create", "compose", "story", "essay"]):
            return "creative"
        elif any(kw in instruction for kw in ["explain", "why", "how", "what is"]):
            return "qa"
        elif any(kw in instruction for kw in ["decide", "choose", "select", "best option"]):
            return "decision"
        elif any(kw in instruction for kw in ["code", "program", "function", "algorithm"]):
            return "programming"
        elif any(kw in instruction for kw in ["logic", "valid", "conclusion", "inference"]):
            return "logic"
        else:
            return "reasoning"
    
    def _extract_constraints(self, sample: Dict[str, Any]) -> List[str]:
        """Trích xuất các ràng buộc từ mẫu"""
        # Triển khai trích xuất ràng buộc dựa trên các đặc điểm của mẫu
        # Đây là một ví dụ đơn giản
        
        constraints = sample.get("constraints", [])
        if constraints:
            return constraints
        
        # Nếu không có constraints, thử trích xuất từ nội dung
        instruction = sample.get("question", sample.get("instruction", ""))
        
        # Tìm các cụm từ chỉ ràng buộc
        constraint_phrases = [
            "must include", "should contain", "required to", "make sure to",
            "ensure that", "do not", "avoid", "limit to", "maximum", "minimum"
        ]
        
        extracted_constraints = []
        for phrase in constraint_phrases:
            if phrase in instruction.lower():
                # Tìm vị trí của cụm từ
                start_idx = instruction.lower().find(phrase)
                if start_idx != -1:
                    # Trích xuất câu chứa cụm từ
                    sentence_end = instruction.find(".", start_idx)
                    if sentence_end == -1:
                        sentence_end = len(instruction)
                    constraint = instruction[start_idx:sentence_end].strip()
                    extracted_constraints.append(constraint)
        
        return extracted_constraints
    
    def _recommend_strategy(self, complexity_score: float, task_type: str) -> str:
        """Đề xuất chiến lược tư duy dựa trên độ phức tạp và loại nhiệm vụ"""
        # Triển khai đề xuất chiến lược dựa trên độ phức tạp và loại nhiệm vụ
        # Đây là một ví dụ đơn giản
        
        if complexity_score < 0.3:
            return "fast_only"
        elif complexity_score > 0.8:
            return "slow_only"
        elif 0.3 <= complexity_score < 0.6:
            if task_type in ["creative", "qa"]:
                return "fast_then_slow"
            else:
                return "parallel"
        else:  # 0.6 <= complexity_score <= 0.8
            if task_type in ["math", "logic", "programming"]:
                return "slow_only"
            elif task_type in ["decision"]:
                return "iterative"
            else:
                return "fast_then_slow"
    
    def _generate_fast_thinking(self, sample: Dict[str, Any]) -> Dict[str, str]:
        """Tạo quá trình fast thinking"""
        # Triển khai tạo quá trình fast thinking dựa trên mẫu
        # Đây là một ví dụ đơn giản
        
        instruction = sample.get("question", sample.get("instruction", ""))
        
        # Đơn giản hóa nhiệm vụ
        simplified_task = self._simplify_task(instruction)
        
        # Tạo quá trình tư duy nhanh
        process = f"Đây là một nhiệm vụ về {self._determine_task_type(sample)}. Tôi sẽ giải quyết nhanh chóng bằng cách {self._get_fast_thinking_approach(sample)}."
        
        # Tạo kết quả trung gian
        intermediate_result = sample.get("answer", "")
        if not intermediate_result:
            intermediate_result = "Kết quả trung gian từ fast thinking"
        
        return {
            "process": process,
            "simplified_task": simplified_task,
            "intermediate_result": intermediate_result
        }
    
    def _simplify_task(self, instruction: str) -> str:
        """Đơn giản hóa nhiệm vụ"""
        # Triển khai đơn giản hóa nhiệm vụ
        # Đây là một ví dụ đơn giản
        
        # Loại bỏ các chi tiết phức tạp
        simplified = instruction
        
        # Loại bỏ các cụm từ chỉ ràng buộc
        constraint_phrases = [
            "must include", "should contain", "required to", "make sure to",
            "ensure that", "do not", "avoid", "limit to", "maximum", "minimum"
        ]
        
        for phrase in constraint_phrases:
            if phrase in simplified.lower():
                # Tìm vị trí của cụm từ
                start_idx = simplified.lower().find(phrase)
                if start_idx != -1:
                    # Tìm kết thúc của câu chứa cụm từ
                    sentence_end = simplified.find(".", start_idx)
                    if sentence_end == -1:
                        sentence_end = len(simplified)
                    # Loại bỏ câu chứa cụm từ
                    simplified = simplified[:start_idx] + simplified[sentence_end+1:]
        
        # Rút gọn câu dài
        if len(simplified) > 100:
            simplified = simplified[:100] + "..."
        
        return simplified.strip()
    
    def _get_fast_thinking_approach(self, sample: Dict[str, Any]) -> str:
        """Lấy cách tiếp cận fast thinking dựa trên loại nhiệm vụ"""
        task_type = self._determine_task_type(sample)
        
        approaches = {
            "math": "áp dụng công thức trực tiếp",
            "creative": "brainstorming ý tưởng chính",
            "qa": "truy xuất thông tin liên quan",
            "decision": "đánh giá nhanh các lựa chọn",
            "programming": "phác thảo giải pháp tổng quát",
            "logic": "áp dụng quy tắc logic cơ bản",
            "reasoning": "sử dụng trực giác và kinh nghiệm",
            "language": "phân tích ngữ cảnh và từ khóa chính"
        }
        
        return approaches.get(task_type, "xử lý thông tin nhanh chóng")
    
    def _generate_slow_thinking(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo quá trình slow thinking"""
        # Triển khai tạo quá trình slow thinking dựa trên mẫu
        # Đây là một ví dụ đơn giản
        
        task_type = self._determine_task_type(sample)
        
        # Tạo các bước phân rã
        decomposition = self._generate_decomposition_steps(sample)
        
        # Tạo các bước suy luận
        reasoning = []
        for step in decomposition:
            reasoning.append(f"Suy luận cho {step.lower()}")
        
        # Tạo các bước xác thực
        verification = []
        for step in decomposition:
            verification.append(f"Xác thực kết quả của {step.lower()}")
        
        # Tạo kết quả trung gian
        intermediate_result = sample.get("answer", "")
        if not intermediate_result:
            intermediate_result = "Kết quả trung gian từ slow thinking"
        
        return {
            "decomposition": decomposition,
            "reasoning": reasoning,
            "verification": verification,
            "intermediate_result": intermediate_result
        }
    
    def _generate_decomposition_steps(self, sample: Dict[str, Any]) -> List[str]:
        """Tạo các bước phân rã cho slow thinking"""
        task_type = self._determine_task_type(sample)
        
        # Các bước phân rã mẫu cho từng loại nhiệm vụ
        decomposition_templates = {
            "math": [
                "Bước 1: Xác định các biến và ràng buộc",
                "Bước 2: Thiết lập phương trình hoặc hệ phương trình",
                "Bước 3: Giải phương trình",
                "Bước 4: Kiểm tra kết quả"
            ],
            "creative": [
                "Bước 1: Xác định yêu cầu và ràng buộc",
                "Bước 2: Brainstorming ý tưởng",
                "Bước 3: Phát triển ý tưởng chính",
                "Bước 4: Hoàn thiện và kiểm tra"
            ],
            "qa": [
                "Bước 1: Phân tích câu hỏi",
                "Bước 2: Truy xuất thông tin liên quan",
                "Bước 3: Tổng hợp thông tin",
                "Bước 4: Xây dựng câu trả lời"
            ],
            "decision": [
                "Bước 1: Xác định các lựa chọn",
                "Bước 2: Xác định tiêu chí đánh giá",
                "Bước 3: Đánh giá từng lựa chọn",
                "Bước 4: So sánh và đưa ra quyết định"
            ],
            "programming": [
                "Bước 1: Phân tích yêu cầu",
                "Bước 2: Thiết kế thuật toán",
                "Bước 3: Triển khai mã",
                "Bước 4: Kiểm tra và gỡ lỗi"
            ],
            "logic": [
                "Bước 1: Xác định các tiền đề",
                "Bước 2: Áp dụng quy tắc suy luận",
                "Bước 3: Kiểm tra tính hợp lệ",
                "Bước 4: Đưa ra kết luận"
            ]
        }
        
        # Lấy template phù hợp hoặc template mặc định
        steps = decomposition_templates.get(task_type, [
            "Bước 1: Phân tích nhiệm vụ",
            "Bước 2: Xác định phương pháp giải quyết",
            "Bước 3: Thực hiện giải pháp",
            "Bước 4: Kiểm tra kết quả"
        ])
        
        return steps
    
    def _generate_integration(self, sample: Dict[str, Any], fast_thinking: Dict[str, str], slow_thinking: Dict[str, Any], strategy: str) -> Dict[str, Any]:
        """Tạo quá trình tích hợp"""
        # Triển khai tạo quá trình tích hợp dựa trên mẫu và kết quả từ fast thinking và slow thinking
        # Đây là một ví dụ đơn giản
        
        if strategy == "fast_only":
            process = "Kết quả từ fast thinking là đủ chính xác."
            inspection = "Kiểm tra nhanh tính hợp lý của kết quả."
        elif strategy == "slow_only":
            process = "Kết quả từ slow thinking là đủ chính xác."
            inspection = "Đã kiểm tra kỹ lưỡng tính chính xác của từng bước."
        elif strategy == "fast_then_slow":
            process = "Kết hợp ý tưởng ban đầu từ fast thinking với phiên bản được cải thiện từ slow thinking."
            inspection = "Kiểm tra lại kết quả để đảm bảo nó đáp ứng tất cả các yêu cầu."
        elif strategy == "parallel":
            process = "Kết hợp kết quả từ cả fast thinking và slow thinking."
            inspection = "So sánh và tích hợp kết quả từ cả hai quá trình tư duy."
        else:  # iterative
            process = "Lặp lại quá trình fast-slow nhiều lần, mỗi lần cải thiện kết quả."
            inspection = "Kiểm tra sự hội tụ của kết quả qua các vòng lặp."
        
        # Tạo các sửa lỗi (nếu có)
        corrections = []
        if random.random() < 0.3:  # 30% khả năng có sửa lỗi
            corrections.append("Sửa lỗi nhỏ trong kết quả")
        
        return {
            "process": process,
            "inspection": inspection,
            "corrections": corrections
        }
    
    def _determine_domain(self, sample: Dict[str, Any]) -> str:
        """Xác định lĩnh vực của mẫu"""
        domain = sample.get("domain", "")
        if domain and domain in self.config["domains"]:
            return domain
        
        # Nếu không có domain, thử suy ra từ task_type
        task_type = self._determine_task_type(sample)
        
        domain_mapping = {
            "math": "math",
            "logic": "logic",
            "creative": "language",
            "qa": "language",
            "programming": "programming",
            "decision": "decision_making"
        }
        
        return domain_mapping.get(task_type, "common_sense")
    
    def _determine_difficulty(self, complexity_score: float) -> str:
        """Xác định độ khó dựa trên điểm độ phức tạp"""
        if complexity_score < 0.3:
            return "easy"
        elif 0.3 <= complexity_score < 0.6:
            return "medium"
        elif 0.6 <= complexity_score < 0.8:
            return "hard"
        else:
            return "expert"
    
    def _generate_tags(self, sample: Dict[str, Any], task_type: str, strategy: str) -> List[str]:
        """Tạo các tag cho mẫu"""
        tags = [task_type, strategy]
        
        # Thêm domain
        domain = self._determine_domain(sample)
        if domain:
            tags.append(domain)
        
        # Thêm các tag từ mẫu gốc
        original_tags = sample.get("tags", [])
        tags.extend(original_tags)
        
        # Loại bỏ trùng lặp
        return list(set(tags))

# Lớp tạo dữ liệu tổng hợp bằng LLM
class LLMDataGenerator(DataGenerator):
    """Lớp tạo dữ liệu tổng hợp bằng LLM"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config["llm_api_key"]
        self.model = config["llm_model"]
    
    def generate(self, num_samples: int, strategy: str = "fast_then_slow") -> List[Dict[str, Any]]:
        """Tạo dữ liệu tổng hợp bằng LLM"""
        if not self.api_key:
            print("LLM API key not provided. Skipping LLM data generation.")
            return []
        
        print(f"Generating {num_samples} samples with strategy: {strategy}")
        
        for i in tqdm(range(num_samples), desc=f"Generating {strategy} data"):
            # Tạo nhiệm vụ ngẫu nhiên
            task = self._generate_random_task(strategy)
            
            # Tạo mẫu hoàn chỉnh bằng LLM
            sample = self._generate_sample_with_llm(task, strategy)
            
            if sample:
                self.generated_data.append(sample)
        
        return self.generated_data
    
    def _generate_random_task(self, strategy: str) -> Dict[str, str]:
        """Tạo nhiệm vụ ngẫu nhiên dựa trên chiến lược"""
        # Chọn loại nhiệm vụ dựa trên chiến lược
        task_types_by_strategy = {
            "fast_only": ["qa", "decision", "language"],
            "slow_only": ["math", "logic", "programming"],
            "fast_then_slow": ["creative", "reasoning", "qa"],
            "parallel": ["decision", "reasoning"],
            "iterative": ["creative", "programming", "math"]
        }
        
        task_type = random.choice(task_types_by_strategy.get(strategy, self.config["task_types"]))
        
        # Chọn độ phức tạp dựa trên chiến lược
        complexity_by_strategy = {
            "fast_only": "simple",
            "slow_only": "complex",
            "fast_then_slow": "medium",
            "parallel": "medium",
            "iterative": "very_complex"
        }
        
        complexity = complexity_by_strategy.get(strategy, "medium")
        
        # Tạo nhiệm vụ dựa trên loại và độ phức tạp
        task = self._create_task_by_type(task_type, complexity)
        
        return task
    
    def _create_task_by_type(self, task_type: str, complexity: str) -> Dict[str, str]:
        """Tạo nhiệm vụ dựa trên loại và độ phức tạp"""
        # Các template nhiệm vụ cho từng loại
        task_templates = {
            "math": {
                "simple": "Tính tổng của {a} và {b}.",
                "medium": "Giải phương trình bậc hai: {a}x² + {b}x + {c} = 0",
                "complex": "Tìm giá trị lớn nhất của hàm số f(x) = {a}x² + {b}x + {c} trong khoảng [{d}, {e}].",
                "very_complex": "Tìm tất cả các giá trị của x thỏa mãn: {a}sin(x) + {b}cos(x) = {c}, với x thuộc khoảng [0, 2π]."
            },
            "logic": {
                "simple": "Nếu {premise1}, thì {conclusion1} đúng hay sai?",
                "medium": "Nếu {premise1} và {premise2}, thì {conclusion1} đúng hay sai?",
                "complex": "Cho các tiền đề: {premise1}, {premise2}, và {premise3}. Kết luận {conclusion1} có hợp lệ không?",
                "very_complex": "Cho các tiền đề: {premise1}, {premise2}, {premise3}, và {premise4}. Kết luận nào trong số sau đây là hợp lệ: {conclusion1}, {conclusion2}, hay {conclusion3}?"
            },
            "creative": {
                "simple": "Viết một câu chuyện ngắn về {topic}.",
                "medium": "Viết một câu chuyện ngắn (khoảng 100 từ) về {topic}, bao gồm các từ: {word1}, {word2}, và {word3}.",
                "complex": "Viết một câu chuyện ngắn (khoảng 200 từ) về {topic}, bao gồm các từ: {word1}, {word2}, {word3}, và {word4}. Câu chuyện phải có {character} là nhân vật chính và diễn ra ở {setting}.",
                "very_complex": "Viết một câu chuyện ngắn (khoảng 300 từ) về {topic}, bao gồm các từ: {word1}, {word2}, {word3}, {word4}, và {word5}. Câu chuyện phải có {character} là nhân vật chính, diễn ra ở {setting}, và phải có một bài học về {moral}."
            },
            "qa": {
                "simple": "Ai là {person}?",
                "medium": "Giải thích {concept} là gì và tại sao nó quan trọng?",
                "complex": "So sánh và đối chiếu {concept1} và {concept2}. Chúng giống và khác nhau như thế nào?",
                "very_complex": "Phân tích tác động của {event} đối với {domain} trong ngắn hạn và dài hạn. Đưa ra các ví dụ cụ thể và dữ liệu để hỗ trợ phân tích của bạn."
            },
            "decision": {
                "simple": "Nên chọn {option1} hay {option2}?",
                "medium": "Đánh giá ưu và nhược điểm của {option1} và {option2}. Nên chọn cái nào?",
                "complex": "Đánh giá các lựa chọn sau dựa trên các tiêu chí {criterion1}, {criterion2}, và {criterion3}: {option1}, {option2}, và {option3}. Đề xuất lựa chọn tốt nhất và giải thích lý do.",
                "very_complex": "Một {organization} đang cân nhắc các chiến lược sau: {option1}, {option2}, {option3}, và {option4}. Đánh giá mỗi chiến lược dựa trên các tiêu chí {criterion1}, {criterion2}, {criterion3}, và {criterion4}. Đề xuất chiến lược tốt nhất và một kế hoạch triển khai chi tiết."
            },
            "programming": {
                "simple": "Viết một hàm để {task_description}.",
                "medium": "Viết một hàm để {task_description} với các ràng buộc sau: {constraint1} và {constraint2}.",
                "complex": "Viết một chương trình để {task_description} với các ràng buộc sau: {constraint1}, {constraint2}, và {constraint3}. Chương trình phải xử lý các trường hợp ngoại lệ sau: {exception1} và {exception2}.",
                "very_complex": "Thiết kế và triển khai một thuật toán để {task_description} với độ phức tạp thời gian tốt nhất có thể. Thuật toán phải xử lý các trường hợp đặc biệt sau: {special_case1}, {special_case2}, và {special_case3}. Phân tích độ phức tạp thời gian và không gian của thuật toán của bạn."
            },
            "reasoning": {
                "simple": "Giải thích tại sao {phenomenon} xảy ra.",
                "medium": "Phân tích nguyên nhân và hệ quả của {phenomenon}.",
                "complex": "Phân tích mối quan hệ giữa {factor1}, {factor2}, và {factor3} trong {phenomenon}. Yếu tố nào có ảnh hưởng lớn nhất và tại sao?",
                "very_complex": "Đánh giá các lý thuyết cạnh tranh giải thích {phenomenon}: {theory1}, {theory2}, và {theory3}. Lý thuyết nào giải thích hiện tượng tốt nhất dựa trên bằng chứng hiện có? Có những khoảng trống nào trong hiểu biết hiện tại và làm thế nào để giải quyết chúng?"
            },
            "language": {
                "simple": "Dịch câu sau sang {language}: '{sentence}'",
                "medium": "Viết lại câu sau theo phong cách {style}: '{sentence}'",
                "complex": "Viết lại đoạn văn sau để nó phù hợp với đối tượng {audience} và giữ nguyên ý nghĩa chính: '{paragraph}'",
                "very_complex": "Phân tích văn bản sau về mặt ngữ điệu, phong cách, và hiệu quả tu từ. Đề xuất các cách để cải thiện nó cho đối tượng {audience} mà vẫn giữ nguyên thông điệp chính: '{text}'"
            }
        }
        
        # Lấy template phù hợp
        template = task_templates.get(task_type, {}).get(complexity, "Giải quyết vấn đề sau: {problem}")
        
        # Tạo các giá trị ngẫu nhiên để điền vào template
        values = self._generate_random_values(task_type, complexity)
        
        # Điền giá trị vào template
        instruction = template.format(**values)
        
        return {
            "instruction": instruction,
            "task_type": task_type,
            "complexity": complexity,
            "values": values
        }
    
    def _generate_random_values(self, task_type: str, complexity: str) -> Dict[str, Any]:
        """Tạo các giá trị ngẫu nhiên cho template nhiệm vụ"""
        values = {}
        
        if task_type == "math":
            values["a"] = random.randint(-10, 10)
            values["b"] = random.randint(-10, 10)
            values["c"] = random.randint(-10, 10)
            values["d"] = random.randint(-5, 0)
            values["e"] = random.randint(1, 5)
        
        elif task_type == "logic":
            premises = [
                "tất cả các con mèo đều có lông",
                "một số động vật có lông",
                "không có con chó nào là mèo",
                "tất cả các con chim đều biết bay",
                "một số động vật biết bơi",
                "tất cả các con cá đều sống dưới nước"
            ]
            conclusions = [
                "một số động vật có lông là mèo",
                "tất cả các con mèo đều là động vật",
                "một số con chó biết bơi",
                "không có con cá nào biết bay",
                "một số động vật biết bay và biết bơi"
            ]
            
            random.shuffle(premises)
            random.shuffle(conclusions)
            
            for i in range(1, 5):
                if i <= len(premises):
                    values[f"premise{i}"] = premises[i-1]
            
            for i in range(1, 4):
                if i <= len(conclusions):
                    values[f"conclusion{i}"] = conclusions[i-1]
        
        elif task_type == "creative":
            topics = ["một cuộc phiêu lưu", "một ngày mưa", "một kỳ nghỉ", "một người bạn", "một giấc mơ"]
            words = ["cửa sổ", "mưa", "sách", "ánh sáng", "bóng tối", "nụ cười", "nước mắt", "thời gian", "kỷ niệm", "hy vọng"]
            characters = ["một đứa trẻ", "một người già", "một chú mèo", "một chú chó", "một nhà thám hiểm"]
            settings = ["một thành phố nhỏ", "một hòn đảo hoang", "một khu rừng", "một ngôi nhà cũ", "một trường học"]
            morals = ["lòng tốt", "sự kiên nhẫn", "tình bạn", "sự trung thực", "lòng dũng cảm"]
            
            values["topic"] = random.choice(topics)
            random.shuffle(words)
            for i in range(1, 6):
                if i <= len(words):
                    values[f"word{i}"] = words[i-1]
            
            values["character"] = random.choice(characters)
            values["setting"] = random.choice(settings)
            values["moral"] = random.choice(morals)
        
        elif task_type == "qa":
            people = ["Albert Einstein", "Marie Curie", "Isaac Newton", "Ada Lovelace", "Charles Darwin"]
            concepts = ["trí tuệ nhân tạo", "biến đổi khí hậu", "năng lượng tái tạo", "học máy", "blockchain", "lượng tử điện toán"]
            events = ["cách mạng công nghiệp", "cuộc cách mạng kỹ thuật số", "đại dịch COVID-19", "sự phát triển của internet", "cuộc khủng hoảng tài chính 2008"]
            domains = ["kinh tế", "xã hội", "công nghệ", "giáo dục", "y tế", "môi trường"]
            
            values["person"] = random.choice(people)
            random.shuffle(concepts)
            for i in range(1, 3):
                if i <= len(concepts):
                    values[f"concept{i}"] = concepts[i-1]
            
            values["event"] = random.choice(events)
            values["domain"] = random.choice(domains)
        
        elif task_type == "decision":
            options = ["đầu tư vào cổ phiếu", "đầu tư vào bất động sản", "tiết kiệm tiền", "mở rộng kinh doanh", "phát triển sản phẩm mới", "tham gia thị trường mới"]
            criteria = ["chi phí", "lợi nhuận", "rủi ro", "thời gian", "tính bền vững", "tác động xã hội"]
            organizations = ["công ty khởi nghiệp", "tập đoàn đa quốc gia", "tổ chức phi lợi nhuận", "cơ quan chính phủ", "trường đại học"]
            
            random.shuffle(options)
            for i in range(1, 5):
                if i <= len(options):
                    values[f"option{i}"] = options[i-1]
            
            random.shuffle(criteria)
            for i in range(1, 5):
                if i <= len(criteria):
                    values[f"criterion{i}"] = criteria[i-1]
            
            values["organization"] = random.choice(organizations)
        
        elif task_type == "programming":
            tasks = [
                "tính tổng của một mảng số nguyên",
                "tìm số lớn nhất trong một mảng",
                "kiểm tra một chuỗi có phải là palindrome",
                "sắp xếp một mảng theo thứ tự tăng dần",
                "tìm tất cả các số nguyên tố trong một khoảng",
                "đảo ngược một chuỗi",
                "tính giai thừa của một số"
            ]
            constraints = [
                "không sử dụng vòng lặp",
                "không sử dụng biến tạm",
                "độ phức tạp thời gian O(n)",
                "độ phức tạp không gian O(1)",
                "sử dụng đệ quy",
                "không sử dụng thư viện chuẩn"
            ]
            exceptions = [
                "đầu vào rỗng",
                "đầu vào âm",
                "đầu vào quá lớn",
                "đầu vào không hợp lệ",
                "tràn bộ nhớ"
            ]
            special_cases = [
                "mảng đã được sắp xếp",
                "mảng chỉ có một phần tử",
                "mảng có các phần tử trùng lặp",
                "chuỗi chỉ có một ký tự",
                "số quá lớn"
            ]
            
            values["task_description"] = random.choice(tasks)
            
            random.shuffle(constraints)
            for i in range(1, 4):
                if i <= len(constraints):
                    values[f"constraint{i}"] = constraints[i-1]
            
            random.shuffle(exceptions)
            for i in range(1, 3):
                if i <= len(exceptions):
                    values[f"exception{i}"] = exceptions[i-1]
            
            random.shuffle(special_cases)
            for i in range(1, 4):
                if i <= len(special_cases):
                    values[f"special_case{i}"] = special_cases[i-1]
        
        elif task_type == "reasoning":
            phenomena = [
                "biến đổi khí hậu",
                "bất bình đẳng kinh tế",
                "sự phát triển của trí tuệ nhân tạo",
                "sự gia tăng của các bệnh không lây nhiễm",
                "sự suy giảm đa dạng sinh học"
            ]
            factors = [
                "chính sách của chính phủ",
                "hành vi của người tiêu dùng",
                "tiến bộ công nghệ",
                "yếu tố văn hóa",
                "điều kiện kinh tế",
                "yếu tố môi trường"
            ]
            theories = [
                "lý thuyết hệ thống",
                "lý thuyết tiến hóa",
                "lý thuyết kinh tế tân cổ điển",
                "lý thuyết xã hội học",
                "lý thuyết tâm lý học nhận thức"
            ]
            
            values["phenomenon"] = random.choice(phenomena)
            
            random.shuffle(factors)
            for i in range(1, 4):
                if i <= len(factors):
                    values[f"factor{i}"] = factors[i-1]
            
            random.shuffle(theories)
            for i in range(1, 4):
                if i <= len(theories):
                    values[f"theory{i}"] = theories[i-1]
        
        elif task_type == "language":
            languages = ["tiếng Anh", "tiếng Pháp", "tiếng Đức", "tiếng Tây Ban Nha", "tiếng Trung"]
            styles = ["trang trọng", "thân mật", "hài hước", "khoa học", "thơ ca"]
            audiences = ["trẻ em", "thanh thiếu niên", "người trưởng thành", "chuyên gia", "người học ngôn ngữ"]
            sentences = [
                "Hôm nay trời đẹp quá.",
                "Tôi rất thích học ngôn ngữ mới.",
                "Cuộc sống đầy những điều bất ngờ.",
                "Công nghệ đang thay đổi cách chúng ta sống."
            ]
            paragraphs = [
                "Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc và sống. Nó mang lại nhiều cơ hội mới nhưng cũng đặt ra nhiều thách thức. Chúng ta cần chuẩn bị để thích nghi với những thay đổi này.",
                "Biến đổi khí hậu là một trong những thách thức lớn nhất của thời đại chúng ta. Nó ảnh hưởng đến mọi khía cạnh của cuộc sống, từ thời tiết đến nông nghiệp, từ sức khỏe đến kinh tế."
            ]
            
            values["language"] = random.choice(languages)
            values["style"] = random.choice(styles)
            values["audience"] = random.choice(audiences)
            values["sentence"] = random.choice(sentences)
            values["paragraph"] = random.choice(paragraphs)
            values["text"] = random.choice(paragraphs)
        
        return values
    
    def _generate_sample_with_llm(self, task: Dict[str, str], strategy: str) -> Optional[Dict[str, Any]]:
        """Tạo mẫu hoàn chỉnh bằng LLM"""
        try:
            # Tạo prompt cho LLM
            prompt = self._create_prompt_for_llm(task, strategy)
            
            # Gọi API của LLM
            response = self._call_llm_api(prompt)
            
            if not response:
                return None
            
            # Phân tích phản hồi từ LLM
            sample = self._parse_llm_response(response, task, strategy)
            
            return sample
        
        except Exception as e:
            print(f"Error generating sample with LLM: {e}")
            return None
    
    def _create_prompt_for_llm(self, task: Dict[str, str], strategy: str) -> str:
        """Tạo prompt cho LLM"""
        # Tạo prompt dựa trên chiến lược
        prompt_templates = {
            "fast_only": """
            Tạo một mẫu dữ liệu cho mô hình Collaborative Fast & Slow Thinking Systems với chiến lược Fast-Only.
            
            Nhiệm vụ: {instruction}
            
            Hãy tạo một mẫu dữ liệu JSON hoàn chỉnh với cấu trúc sau:
            {{
              "id": "unique_id",
              "task": {{
                "instruction": "Nhiệm vụ cần giải quyết",
                "input": "Dữ liệu đầu vào (nếu có)",
                "context": "Ngữ cảnh bổ sung (nếu có)"
              }},
              "analysis": {{
                "complexity_score": 0.75,
                "task_type": "reasoning|creative|qa|decision|...",
                "constraints": ["Ràng buộc 1", "Ràng buộc 2", ...],
                "recommended_strategy": "fast_only"
              }},
              "thinking_processes": {{
                "fast_thinking": {{
                  "process": "Quá trình tư duy nhanh, trực giác",
                  "simplified_task": "Nhiệm vụ đã được đơn giản hóa",
                  "intermediate_result": "Kết quả trung gian từ fast thinking"
                }},
                "slow_thinking": {{
                  "decomposition": [],
                  "reasoning": [],
                  "verification": [],
                  "intermediate_result": ""
                }}
              }},
              "integration": {{
                "process": "Quá trình tích hợp kết quả từ fast thinking và slow thinking",
                "inspection": "Quá trình kiểm tra tính chính xác của kết quả",
                "corrections": ["Sửa lỗi 1", "Sửa lỗi 2", ...]
              }},
              "output": {{
                "final_answer": "Câu trả lời cuối cùng",
                "explanation": "Giải thích cho câu trả lời"
              }},
              "metadata": {{
                "domain": "math|logic|language|science|...",
                "difficulty": "easy|medium|hard|expert",
                "source": "synthetic",
                "quality_score": 0.95,
                "tags": ["Tag 1", "Tag 2", ...]
              }}
            }}
            
            Lưu ý:
            - Đây là chiến lược Fast-Only, nên phần fast_thinking phải đầy đủ và chi tiết, còn phần slow_thinking để trống.
            - Complexity_score phải nhỏ hơn 0.3 vì đây là nhiệm vụ đơn giản phù hợp với fast thinking.
            - Đảm bảo câu trả lời cuối cùng chính xác và phù hợp với nhiệm vụ.
            
            Chỉ trả về JSON, không cần giải thích thêm.
            """,
            
            "slow_only": """
            Tạo một mẫu dữ liệu cho mô hình Collaborative Fast & Slow Thinking Systems với chiến lược Slow-Only.
            
            Nhiệm vụ: {instruction}
            
            Hãy tạo một mẫu dữ liệu JSON hoàn chỉnh với cấu trúc sau:
            {{
              "id": "unique_id",
              "task": {{
                "instruction": "Nhiệm vụ cần giải quyết",
                "input": "Dữ liệu đầu vào (nếu có)",
                "context": "Ngữ cảnh bổ sung (nếu có)"
              }},
              "analysis": {{
                "complexity_score": 0.75,
                "task_type": "reasoning|creative|qa|decision|...",
                "constraints": ["Ràng buộc 1", "Ràng buộc 2", ...],
                "recommended_strategy": "slow_only"
              }},
              "thinking_processes": {{
                "fast_thinking": {{
                  "process": "",
                  "simplified_task": "",
                  "intermediate_result": ""
                }},
                "slow_thinking": {{
                  "decomposition": ["Bước 1", "Bước 2", ...],
                  "reasoning": ["Suy luận cho bước 1", "Suy luận cho bước 2", ...],
                  "verification": ["Xác thực kết quả bước 1", "Xác thực kết quả bước 2", ...],
                  "intermediate_result": "Kết quả trung gian từ slow thinking"
                }}
              }},
              "integration": {{
                "process": "Quá trình tích hợp kết quả từ fast thinking và slow thinking",
                "inspection": "Quá trình kiểm tra tính chính xác của kết quả",
                "corrections": ["Sửa lỗi 1", "Sửa lỗi 2", ...]
              }},
              "output": {{
                "final_answer": "Câu trả lời cuối cùng",
                "explanation": "Giải thích cho câu trả lời"
              }},
              "metadata": {{
                "domain": "math|logic|language|science|...",
                "difficulty": "easy|medium|hard|expert",
                "source": "synthetic",
                "quality_score": 0.95,
                "tags": ["Tag 1", "Tag 2", ...]
              }}
            }}
            
            Lưu ý:
            - Đây là chiến lược Slow-Only, nên phần slow_thinking phải đầy đủ và chi tiết, còn phần fast_thinking để trống.
            - Complexity_score phải lớn hơn 0.6 vì đây là nhiệm vụ phức tạp phù hợp với slow thinking.
            - Đảm bảo câu trả lời cuối cùng chính xác và phù hợp với nhiệm vụ.
            - Phần decomposition, reasoning, và verification phải có ít nhất 3 bước.
            
            Chỉ trả về JSON, không cần giải thích thêm.
            """,
            
            "fast_then_slow": """
            Tạo một mẫu dữ liệu cho mô hình Collaborative Fast & Slow Thinking Systems với chiến lược Fast-then-Slow.
            
            Nhiệm vụ: {instruction}
            
            Hãy tạo một mẫu dữ liệu JSON hoàn chỉnh với cấu trúc sau:
            {{
              "id": "unique_id",
              "task": {{
                "instruction": "Nhiệm vụ cần giải quyết",
                "input": "Dữ liệu đầu vào (nếu có)",
                "context": "Ngữ cảnh bổ sung (nếu có)"
              }},
              "analysis": {{
                "complexity_score": 0.75,
                "task_type": "reasoning|creative|qa|decision|...",
                "constraints": ["Ràng buộc 1", "Ràng buộc 2", ...],
                "recommended_strategy": "fast_then_slow"
              }},
              "thinking_processes": {{
                "fast_thinking": {{
                  "process": "Quá trình tư duy nhanh, trực giác",
                  "simplified_task": "Nhiệm vụ đã được đơn giản hóa",
                  "intermediate_result": "Kết quả trung gian từ fast thinking"
                }},
                "slow_thinking": {{
                  "decomposition": ["Bước 1", "Bước 2", ...],
                  "reasoning": ["Suy luận cho bước 1", "Suy luận cho bước 2", ...],
                  "verification": ["Xác thực kết quả bước 1", "Xác thực kết quả bước 2", ...],
                  "intermediate_result": "Kết quả trung gian từ slow thinking"
                }}
              }},
              "integration": {{
                "process": "Quá trình tích hợp kết quả từ fast thinking và slow thinking",
                "inspection": "Quá trình kiểm tra tính chính xác của kết quả",
                "corrections": ["Sửa lỗi 1", "Sửa lỗi 2", ...]
              }},
              "output": {{
                "final_answer": "Câu trả lời cuối cùng",
                "explanation": "Giải thích cho câu trả lời"
              }},
              "metadata": {{
                "domain": "math|logic|language|science|...",
                "difficulty": "easy|medium|hard|expert",
                "source": "synthetic",
                "quality_score": 0.95,
                "tags": ["Tag 1", "Tag 2", ...]
              }}
            }}
            
            Lưu ý:
            - Đây là chiến lược Fast-then-Slow, nên cả phần fast_thinking và slow_thinking đều phải đầy đủ và chi tiết.
            - Phần fast_thinking phải tạo ra một kết quả trung gian đơn giản.
            - Phần slow_thinking phải cải thiện kết quả từ fast_thinking bằng cách phân tích chi tiết.
            - Complexity_score nên trong khoảng 0.3-0.6 vì đây là nhiệm vụ có độ phức tạp trung bình.
            - Đảm bảo câu trả lời cuối cùng chính xác và phù hợp với nhiệm vụ.
            
            Chỉ trả về JSON, không cần giải thích thêm.
            """,
            
            "parallel": """
            Tạo một mẫu dữ liệu cho mô hình Collaborative Fast & Slow Thinking Systems với chiến lược Parallel.
            
            Nhiệm vụ: {instruction}
            
            Hãy tạo một mẫu dữ liệu JSON hoàn chỉnh với cấu trúc sau:
            {{
              "id": "unique_id",
              "task": {{
                "instruction": "Nhiệm vụ cần giải quyết",
                "input": "Dữ liệu đầu vào (nếu có)",
                "context": "Ngữ cảnh bổ sung (nếu có)"
              }},
              "analysis": {{
                "complexity_score": 0.75,
                "task_type": "reasoning|creative|qa|decision|...",
                "constraints": ["Ràng buộc 1", "Ràng buộc 2", ...],
                "recommended_strategy": "parallel"
              }},
              "thinking_processes": {{
                "fast_thinking": {{
                  "process": "Quá trình tư duy nhanh, trực giác",
                  "simplified_task": "Nhiệm vụ đã được đơn giản hóa",
                  "intermediate_result": "Kết quả trung gian từ fast thinking"
                }},
                "slow_thinking": {{
                  "decomposition": ["Bước 1", "Bước 2", ...],
                  "reasoning": ["Suy luận cho bước 1", "Suy luận cho bước 2", ...],
                  "verification": ["Xác thực kết quả bước 1", "Xác thực kết quả bước 2", ...],
                  "intermediate_result": "Kết quả trung gian từ slow thinking"
                }}
              }},
              "integration": {{
                "process": "Quá trình tích hợp kết quả từ fast thinking và slow thinking",
                "inspection": "Quá trình kiểm tra tính chính xác của kết quả",
                "corrections": ["Sửa lỗi 1", "Sửa lỗi 2", ...]
              }},
              "output": {{
                "final_answer": "Câu trả lời cuối cùng",
                "explanation": "Giải thích cho câu trả lời"
              }},
              "metadata": {{
                "domain": "math|logic|language|science|...",
                "difficulty": "easy|medium|hard|expert",
                "source": "synthetic",
                "quality_score": 0.95,
                "tags": ["Tag 1", "Tag 2", ...]
              }}
            }}
            
            Lưu ý:
            - Đây là chiến lược Parallel, nên cả phần fast_thinking và slow_thinking đều phải đầy đủ và chi tiết.
            - Phần fast_thinking và slow_thinking phải tạo ra các kết quả trung gian khác nhau.
            - Phần integration phải kết hợp kết quả từ cả hai quá trình tư duy.
            - Complexity_score nên trong khoảng 0.3-0.6 vì đây là nhiệm vụ có độ phức tạp trung bình.
            - Đảm bảo câu trả lời cuối cùng chính xác và phù hợp với nhiệm vụ.
            
            Chỉ trả về JSON, không cần giải thích thêm.
            """,
            
            "iterative": """
            Tạo một mẫu dữ liệu cho mô hình Collaborative Fast & Slow Thinking Systems với chiến lược Iterative.
            
            Nhiệm vụ: {instruction}
            
            Hãy tạo một mẫu dữ liệu JSON hoàn chỉnh với cấu trúc sau:
            {{
              "id": "unique_id",
              "task": {{
                "instruction": "Nhiệm vụ cần giải quyết",
                "input": "Dữ liệu đầu vào (nếu có)",
                "context": "Ngữ cảnh bổ sung (nếu có)"
              }},
              "analysis": {{
                "complexity_score": 0.75,
                "task_type": "reasoning|creative|qa|decision|...",
                "constraints": ["Ràng buộc 1", "Ràng buộc 2", ...],
                "recommended_strategy": "iterative"
              }},
              "thinking_processes": {{
                "fast_thinking": {{
                  "process": "Quá trình tư duy nhanh, trực giác",
                  "simplified_task": "Nhiệm vụ đã được đơn giản hóa",
                  "intermediate_result": "Kết quả trung gian từ fast thinking"
                }},
                "slow_thinking": {{
                  "decomposition": ["Bước 1", "Bước 2", ...],
                  "reasoning": ["Suy luận cho bước 1", "Suy luận cho bước 2", ...],
                  "verification": ["Xác thực kết quả bước 1", "Xác thực kết quả bước 2", ...],
                  "intermediate_result": "Kết quả trung gian từ slow thinking"
                }}
              }},
              "integration": {{
                "process": "Quá trình tích hợp kết quả từ fast thinking và slow thinking",
                "inspection": "Quá trình kiểm tra tính chính xác của kết quả",
                "corrections": ["Sửa lỗi 1", "Sửa lỗi 2", ...]
              }},
              "output": {{
                "final_answer": "Câu trả lời cuối cùng",
                "explanation": "Giải thích cho câu trả lời"
              }},
              "metadata": {{
                "domain": "math|logic|language|science|...",
                "difficulty": "easy|medium|hard|expert",
                "source": "synthetic",
                "quality_score": 0.95,
                "tags": ["Tag 1", "Tag 2", ...]
              }}
            }}
            
            Lưu ý:
            - Đây là chiến lược Iterative, nên cả phần fast_thinking và slow_thinking đều phải đầy đủ và chi tiết.
            - Phần fast_thinking phải tạo ra một kết quả trung gian ban đầu.
            - Phần slow_thinking phải cải thiện kết quả từ fast_thinking qua nhiều vòng lặp.
            - Phần integration phải mô tả quá trình lặp đi lặp lại và cải thiện dần dần.
            - Complexity_score nên lớn hơn 0.6 vì đây là nhiệm vụ phức tạp.
            - Đảm bảo câu trả lời cuối cùng chính xác và phù hợp với nhiệm vụ.
            
            Chỉ trả về JSON, không cần giải thích thêm.
            """
        }
        
        # Lấy template phù hợp
        template = prompt_templates.get(strategy, prompt_templates["fast_then_slow"])
        
        # Điền giá trị vào template
        prompt = template.format(instruction=task["instruction"])
        
        return prompt
    
    def _call_llm_api(self, prompt: str) -> Optional[str]:
        """Gọi API của LLM"""
        # Đây là một ví dụ đơn giản sử dụng OpenAI API
        # Trong thực tế, bạn cần thay thế bằng API của LLM mà bạn sử dụng
        
        try:
            # Giả lập gọi API
            # Trong thực tế, bạn sẽ sử dụng thư viện của LLM provider
            # Ví dụ: import openai; response = openai.ChatCompletion.create(...)
            
            # Giả lập phản hồi từ LLM
            # Trong thực tế, phản hồi sẽ được trả về từ API
            response = """
            {
              "id": "synthetic_12345678",
              "task": {
                "instruction": "Tính tổng của 15 và 27.",
                "input": "",
                "context": ""
              },
              "analysis": {
                "complexity_score": 0.1,
                "task_type": "math",
                "constraints": [],
                "recommended_strategy": "fast_only"
              },
              "thinking_processes": {
                "fast_thinking": {
                  "process": "Đây là một phép tính cộng đơn giản. Tôi sẽ cộng trực tiếp 15 và 27.",
                  "simplified_task": "Tính 15 + 27",
                  "intermediate_result": "42"
                },
                "slow_thinking": {
                  "decomposition": [],
                  "reasoning": [],
                  "verification": [],
                  "intermediate_result": ""
                }
              },
              "integration": {
                "process": "Kết quả từ fast thinking là đủ chính xác.",
                "inspection": "Kiểm tra: 15 + 27 = 42. Đúng.",
                "corrections": []
              },
              "output": {
                "final_answer": "42",
                "explanation": "Tổng của 15 và 27 là 42."
              },
              "metadata": {
                "domain": "math",
                "difficulty": "easy",
                "source": "synthetic",
                "quality_score": 0.98,
                "tags": ["math", "addition", "fast_thinking"]
              }
            }
            """
            
            return response
        
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return None
    
    def _parse_llm_response(self, response: str, task: Dict[str, str], strategy: str) -> Dict[str, Any]:
        """Phân tích phản hồi từ LLM"""
        try:
            # Tìm và trích xuất JSON từ phản hồi
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            
            # Phân tích JSON
            sample = json.loads(json_str)
            
            # Đảm bảo ID là duy nhất
            sample["id"] = f"{strategy}_{str(uuid.uuid4())[:8]}"
            
            # Đảm bảo instruction khớp với nhiệm vụ gốc
            sample["task"]["instruction"] = task["instruction"]
            
            # Đảm bảo recommended_strategy khớp với chiến lược
            sample["analysis"]["recommended_strategy"] = strategy
            
            return sample
        
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            # Trả về mẫu mặc định nếu có lỗi
            return self._create_default_sample(task, strategy)
    
    def _create_default_sample(self, task: Dict[str, str], strategy: str) -> Dict[str, Any]:
        """Tạo mẫu mặc định nếu có lỗi"""
        # Tạo mẫu mặc định dựa trên chiến lược
        sample = {
            "id": f"{strategy}_{str(uuid.uuid4())[:8]}",
            "task": {
                "instruction": task["instruction"],
                "input": "",
                "context": ""
            },
            "analysis": {
                "complexity_score": 0.5,
                "task_type": task.get("task_type", "reasoning"),
                "constraints": [],
                "recommended_strategy": strategy
            },
            "thinking_processes": {
                "fast_thinking": {
                    "process": "Quá trình tư duy nhanh mặc định.",
                    "simplified_task": "Nhiệm vụ đã được đơn giản hóa.",
                    "intermediate_result": "Kết quả trung gian từ fast thinking."
                },
                "slow_thinking": {
                    "decomposition": ["Bước 1: Phân tích nhiệm vụ", "Bước 2: Giải quyết vấn đề", "Bước 3: Kiểm tra kết quả"],
                    "reasoning": ["Suy luận cho bước 1", "Suy luận cho bước 2", "Suy luận cho bước 3"],
                    "verification": ["Xác thực kết quả bước 1", "Xác thực kết quả bước 2", "Xác thực kết quả bước 3"],
                    "intermediate_result": "Kết quả trung gian từ slow thinking."
                }
            },
            "integration": {
                "process": "Quá trình tích hợp kết quả mặc định.",
                "inspection": "Quá trình kiểm tra tính chính xác mặc định.",
                "corrections": []
            },
            "output": {
                "final_answer": "Câu trả lời mặc định.",
                "explanation": "Giải thích mặc định."
            },
            "metadata": {
                "domain": "general",
                "difficulty": "medium",
                "source": "synthetic",
                "quality_score": 0.7,
                "tags": [strategy, "default"]
            }
        }
        
        # Điều chỉnh mẫu dựa trên chiến lược
        if strategy == "fast_only":
            sample["analysis"]["complexity_score"] = 0.2
            sample["thinking_processes"]["slow_thinking"] = {
                "decomposition": [],
                "reasoning": [],
                "verification": [],
                "intermediate_result": ""
            }
            sample["metadata"]["difficulty"] = "easy"
        
        elif strategy == "slow_only":
            sample["analysis"]["complexity_score"] = 0.7
            sample["thinking_processes"]["fast_thinking"] = {
                "process": "",
                "simplified_task": "",
                "intermediate_result": ""
            }
            sample["metadata"]["difficulty"] = "hard"
        
        return sample

# Lớp tạo dữ liệu tăng cường
class AugmentedDataGenerator(DataGenerator):
    """Lớp tạo dữ liệu tăng cường"""
    
    def __init__(self, config: Dict[str, Any], base_data: List[Dict[str, Any]]):
        super().__init__(config)
        self.base_data = base_data
    
    def generate(self, num_samples: int) -> List[Dict[str, Any]]:
        """Tạo dữ liệu tăng cường từ dữ liệu cơ sở"""
        if not self.base_data:
            print("No base data available for augmentation")
            return []
        
        # Lấy mẫu ngẫu nhiên từ base data
        samples = random.sample(self.base_data, min(num_samples, len(self.base_data)))
        
        for sample in tqdm(samples, desc="Augmenting data"):
            augmented_sample = self._augment_sample(sample)
            self.generated_data.append(augmented_sample)
        
        return self.generated_data
    
    def _augment_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Tăng cường một mẫu"""
        # Chọn ngẫu nhiên một phương pháp tăng cường
        augmentation_methods = [
            self._change_context,
            self._change_complexity,
            self._change_format,
            self._create_adversarial
        ]
        
        method = random.choice(augmentation_methods)
        
        # Áp dụng phương pháp tăng cường
        augmented_sample = method(sample)
        
        # Đảm bảo ID là duy nhất
        augmented_sample["id"] = f"augmented_{str(uuid.uuid4())[:8]}"
        
        # Cập nhật metadata
        augmented_sample["metadata"]["source"] = "augmented"
        augmented_sample["metadata"]["tags"].append("augmented")
        
        return augmented_sample
    
    def _change_context(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Thay đổi ngữ cảnh của mẫu"""
        # Tạo một bản sao sâu của mẫu
        augmented_sample = json.loads(json.dumps(sample))
        
        # Thay đổi ngữ cảnh
        contexts = [
            "Trong một cuộc phỏng vấn việc làm",
            "Trong một lớp học đại học",
            "Trong một cuộc họp kinh doanh",
            "Trong một cuộc trò chuyện với bạn bè",
            "Trong một bài kiểm tra"
        ]
        
        augmented_sample["task"]["context"] = random.choice(contexts)
        
        # Cập nhật tags
        augmented_sample["metadata"]["tags"].append("context_changed")
        
        return augmented_sample
    
    def _change_complexity(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Thay đổi độ phức tạp của mẫu"""
        # Tạo một bản sao sâu của mẫu
        augmented_sample = json.loads(json.dumps(sample))
        
        # Thay đổi độ phức tạp
        current_complexity = sample["analysis"]["complexity_score"]
        
        # Tăng hoặc giảm độ phức tạp
        if current_complexity < 0.5:
            # Tăng độ phức tạp
            new_complexity = min(current_complexity + random.uniform(0.2, 0.4), 1.0)
            
            # Thêm ràng buộc
            constraints = [
                "Phải hoàn thành trong 5 phút",
                "Không được sử dụng máy tính",
                "Phải giải thích từng bước",
                "Phải sử dụng ít nhất 3 ví dụ",
                "Không được sử dụng từ khóa X"
            ]
            
            augmented_sample["analysis"]["constraints"].append(random.choice(constraints))
            
            # Cập nhật chiến lược tư duy
            if new_complexity > 0.6:
                augmented_sample["analysis"]["recommended_strategy"] = "slow_only"
            elif new_complexity > 0.3:
                augmented_sample["analysis"]["recommended_strategy"] = "fast_then_slow"
        else:
            # Giảm độ phức tạp
            new_complexity = max(current_complexity - random.uniform(0.2, 0.4), 0.0)
            
            # Loại bỏ một số ràng buộc
            if augmented_sample["analysis"]["constraints"]:
                augmented_sample["analysis"]["constraints"] = augmented_sample["analysis"]["constraints"][:-1]
            
            # Cập nhật chiến lược tư duy
            if new_complexity < 0.3:
                augmented_sample["analysis"]["recommended_strategy"] = "fast_only"
            elif new_complexity < 0.6:
                augmented_sample["analysis"]["recommended_strategy"] = "fast_then_slow"
        
        augmented_sample["analysis"]["complexity_score"] = round(new_complexity, 2)
        
        # Cập nhật difficulty
        if new_complexity < 0.3:
            augmented_sample["metadata"]["difficulty"] = "easy"
        elif new_complexity < 0.6:
            augmented_sample["metadata"]["difficulty"] = "medium"
        elif new_complexity < 0.8:
            augmented_sample["metadata"]["difficulty"] = "hard"
        else:
            augmented_sample["metadata"]["difficulty"] = "expert"
        
        # Cập nhật tags
        augmented_sample["metadata"]["tags"].append("complexity_changed")
        
        return augmented_sample
    
    def _change_format(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Thay đổi định dạng của mẫu"""
        # Tạo một bản sao sâu của mẫu
        augmented_sample = json.loads(json.dumps(sample))
        
        # Thay đổi định dạng của instruction
        instruction = sample["task"]["instruction"]
        
        formats = [
            # Thêm dấu hỏi
            lambda x: f"{x}?" if not x.endswith("?") else x,
            # Thêm yêu cầu lịch sự
            lambda x: f"Làm ơn {x.lower()}" if not x.lower().startswith("làm ơn") else x,
            # Thêm ngữ cảnh
            lambda x: f"Giả sử bạn là một chuyên gia, {x.lower()}",
            # Thêm giới hạn thời gian
            lambda x: f"{x} Hãy trả lời trong vòng 2 phút.",
            # Thêm yêu cầu giải thích
            lambda x: f"{x} Hãy giải thích chi tiết."
        ]
        
        new_instruction = random.choice(formats)(instruction)
        augmented_sample["task"]["instruction"] = new_instruction
        
        # Cập nhật tags
        augmented_sample["metadata"]["tags"].append("format_changed")
        
        return augmented_sample
    
    def _create_adversarial(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo mẫu đối nghịch"""
        # Tạo một bản sao sâu của mẫu
        augmented_sample = json.loads(json.dumps(sample))
        
        # Tạo mẫu đối nghịch
        instruction = sample["task"]["instruction"]
        
        adversarial_transformations = [
            # Thêm thông tin gây nhiễu
            lambda x: f"{x} Lưu ý rằng có một số thông tin không liên quan như sau: X = 42, Y = 'hello', Z = [1, 2, 3].",
            # Thêm yêu cầu mâu thuẫn
            lambda x: f"{x} Hãy trả lời ngắn gọn nhưng phải giải thích chi tiết.",
            # Thêm ràng buộc khó
            lambda x: f"{x} Hãy trả lời mà không sử dụng các từ: 'là', 'và', 'của'.",
            # Đảo ngược yêu cầu
            lambda x: f"Đừng {x.lower()}" if not x.lower().startswith("đừng") else x,
            # Thêm nhiễu ngữ nghĩa
            lambda x: f"{x} Câu trả lời phải bao gồm một ví dụ về con mèo, ngay cả khi nó không liên quan."
        ]
        
        new_instruction = random.choice(adversarial_transformations)(instruction)
        augmented_sample["task"]["instruction"] = new_instruction
        
        # Cập nhật complexity_score
        augmented_sample["analysis"]["complexity_score"] = min(sample["analysis"]["complexity_score"] + 0.2, 1.0)
        
        # Thêm ràng buộc
        adversarial_constraints = [
            "Không được sử dụng từ X",
            "Phải bao gồm một ví dụ không liên quan",
            "Phải trả lời trong dưới 50 từ",
            "Phải bao gồm một câu hỏi ngược lại",
            "Phải sử dụng ít nhất 3 từ hiếm"
        ]
        
        augmented_sample["analysis"]["constraints"].append(random.choice(adversarial_constraints))
        
        # Cập nhật tags
        augmented_sample["metadata"]["tags"].append("adversarial")
        
        return augmented_sample

# Lớp kiểm tra chất lượng dữ liệu
class DataQualityChecker:
    """Lớp kiểm tra chất lượng dữ liệu"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def check_quality(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Kiểm tra chất lượng của dữ liệu"""
        if not data:
            return []
        
        filtered_data = []
        
        for sample in tqdm(data, desc="Checking data quality"):
            if self._is_valid_sample(sample):
                # Tính điểm chất lượng
                quality_score = self._calculate_quality_score(sample)
                
                # Cập nhật điểm chất lượng
                sample["metadata"]["quality_score"] = quality_score
                
                # Chỉ giữ lại các mẫu có chất lượng tốt
                if quality_score >= 0.7:
                    filtered_data.append(sample)
        
        print(f"Filtered {len(data) - len(filtered_data)} low-quality samples")
        
        return filtered_data
    
    def _is_valid_sample(self, sample: Dict[str, Any]) -> bool:
        """Kiểm tra tính hợp lệ của mẫu"""
        # Kiểm tra các trường bắt buộc
        required_fields = [
            "id", "task", "analysis", "thinking_processes", "integration", "output", "metadata"
        ]
        
        for field in required_fields:
            if field not in sample:
                return False
        
        # Kiểm tra task
        if "instruction" not in sample["task"]:
            return False
        
        # Kiểm tra analysis
        if "complexity_score" not in sample["analysis"] or "recommended_strategy" not in sample["analysis"]:
            return False
        
        # Kiểm tra thinking_processes
        if "fast_thinking" not in sample["thinking_processes"] or "slow_thinking" not in sample["thinking_processes"]:
            return False
        
        # Kiểm tra output
        if "final_answer" not in sample["output"]:
            return False
        
        return True
    
    def _calculate_quality_score(self, sample: Dict[str, Any]) -> float:
        """Tính điểm chất lượng của mẫu"""
        scores = []
        
        # Điểm cho instruction
        instruction_length = len(sample["task"]["instruction"])
        if instruction_length < 10:
            scores.append(0.3)
        elif instruction_length < 50:
            scores.append(0.7)
        else:
            scores.append(1.0)
        
        # Điểm cho fast_thinking
        strategy = sample["analysis"]["recommended_strategy"]
        if strategy in ["fast_only", "fast_then_slow", "parallel", "iterative"]:
            fast_thinking = sample["thinking_processes"]["fast_thinking"]
            if not fast_thinking["process"]:
                scores.append(0.0)
            elif len(fast_thinking["process"]) < 20:
                scores.append(0.5)
            else:
                scores.append(1.0)
        else:
            scores.append(1.0)
        
        # Điểm cho slow_thinking
        if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"]:
            slow_thinking = sample["thinking_processes"]["slow_thinking"]
            if not slow_thinking["decomposition"]:
                scores.append(0.0)
            elif len(slow_thinking["decomposition"]) < 2:
                scores.append(0.5)
            else:
                scores.append(1.0)
        else:
            scores.append(1.0)
        
        # Điểm cho final_answer
        final_answer = sample["output"]["final_answer"]
        if not final_answer:
            scores.append(0.0)
        elif len(final_answer) < 5:
            scores.append(0.5)
        else:
            scores.append(1.0)
        
        # Tính điểm trung bình
        return round(sum(scores) / len(scores), 2)

# Hàm chính để tạo dữ liệu
def generate_data(config: Dict[str, Any], num_samples: Dict[str, int]) -> List[Dict[str, Any]]:
    """Hàm chính để tạo dữ liệu"""
    all_data = []
    
    # Tạo dữ liệu từ benchmark
    benchmark_names = ["gsm8k", "math", "logiqa", "big_bench", "mmlu", "humaneval", "commongen"]
    
    for benchmark in benchmark_names:
        generator = BenchmarkDataGenerator(config, benchmark)
        data = generator.generate(100)  # Tạo 100 mẫu từ mỗi benchmark
        all_data.extend(data)
        
        # Lưu dữ liệu
        if data:
            generator.save(f"{benchmark}_converted.json")
    
    # Tạo dữ liệu tổng hợp bằng LLM
    llm_generator = LLMDataGenerator(config)
    
    for strategy, count in num_samples.items():
        data = llm_generator.generate(count, strategy)
        all_data.extend(data)
        
        # Lưu dữ liệu
        if data:
            llm_generator.save(f"llm_generated_{strategy}.json")
    
    # Tạo dữ liệu tăng cường
    if all_data:
        augmented_generator = AugmentedDataGenerator(config, all_data)
        augmented_data = augmented_generator.generate(int(len(all_data) * 0.3))  # Tăng cường 30% dữ liệu
        all_data.extend(augmented_data)
        
        # Lưu dữ liệu
        if augmented_data:
            augmented_generator.save("augmented_data.json")
    
    # Kiểm tra chất lượng dữ liệu
    quality_checker = DataQualityChecker(config)
    filtered_data = quality_checker.check_quality(all_data)
    
    # Lưu dữ liệu cuối cùng
    if filtered_data:
        output_path = os.path.join(config["output_dir"], "final_dataset.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(filtered_data)} samples to {output_path}")
    
    return filtered_data

# Hàm main
def main():
    """Hàm main"""
    parser = argparse.ArgumentParser(description="Generate data for Collaborative Fast & Slow Thinking Systems")
    parser.add_argument("--output_dir", type=str, default=CONFIG["output_dir"], help="Output directory")
    parser.add_argument("--benchmark_data_dir", type=str, default=CONFIG["benchmark_data_dir"], help="Benchmark data directory")
    parser.add_argument("--llm_api_key", type=str, default=CONFIG["llm_api_key"], help="LLM API key")
    parser.add_argument("--llm_model", type=str, default=CONFIG["llm_model"], help="LLM model")
    parser.add_argument("--fast_only", type=int, default=CONFIG["num_samples"]["fast_only"], help="Number of fast_only samples")
    parser.add_argument("--slow_only", type=int, default=CONFIG["num_samples"]["slow_only"], help="Number of slow_only samples")
    parser.add_argument("--fast_then_slow", type=int, default=CONFIG["num_samples"]["fast_then_slow"], help="Number of fast_then_slow samples")
    parser.add_argument("--parallel", type=int, default=CONFIG["num_samples"]["parallel"], help="Number of parallel samples")
    parser.add_argument("--iterative", type=int, default=CONFIG["num_samples"]["iterative"], help="Number of iterative samples")
    
    args = parser.parse_args()
    
    # Cập nhật cấu hình
    config = CONFIG.copy()
    config["output_dir"] = args.output_dir
    config["benchmark_data_dir"] = args.benchmark_data_dir
    config["llm_api_key"] = args.llm_api_key
    config["llm_model"] = args.llm_model
    
    num_samples = {
        "fast_only": args.fast_only,
        "slow_only": args.slow_only,
        "fast_then_slow": args.fast_then_slow,
        "parallel": args.parallel,
        "iterative": args.iterative
    }
    
    # Tạo dữ liệu
    generate_data(config, num_samples)

if __name__ == "__main__":
    main()
