#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Validation for Collaborative Fast & Slow Thinking Systems
"""

import os
import json
import argparse
import random
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

# Cấu hình
CONFIG = {
    "data_dir": "generated_data",
    "output_dir": "validation_results",
    "dataset_file": "final_dataset.json",
    "sample_size": 100,  # Số lượng mẫu để kiểm tra chi tiết
    "visualization_enabled": True
}

# Tạo thư mục đầu ra nếu chưa tồn tại
os.makedirs(CONFIG["output_dir"], exist_ok=True)

class DataValidator:
    """Lớp xác thực dữ liệu"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data = self._load_data()
        self.validation_results = {}
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Tải dữ liệu từ file"""
        dataset_path = os.path.join(self.config["data_dir"], self.config["dataset_file"])
        
        if not os.path.exists(dataset_path):
            print(f"Dataset file {dataset_path} not found.")
            # Tạo dữ liệu mẫu để kiểm tra
            return self._create_sample_data()
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_sample_data(self) -> List[Dict[str, Any]]:
        """Tạo dữ liệu mẫu để kiểm tra"""
        print("Creating sample data for validation...")
        
        sample_data = []
        strategies = ["fast_only", "slow_only", "fast_then_slow", "parallel", "iterative"]
        task_types = ["math", "logic", "creative", "qa", "decision", "programming", "reasoning"]
        domains = ["math", "logic", "language", "science", "programming", "common_sense", "decision_making"]
        difficulties = ["easy", "medium", "hard", "expert"]
        
        for i in range(200):  # Tạo 200 mẫu
            strategy = random.choice(strategies)
            task_type = random.choice(task_types)
            domain = random.choice(domains)
            difficulty = random.choice(difficulties)
            
            # Tạo complexity_score dựa trên difficulty
            complexity_map = {"easy": (0.0, 0.3), "medium": (0.3, 0.6), "hard": (0.6, 0.8), "expert": (0.8, 1.0)}
            complexity_range = complexity_map[difficulty]
            complexity_score = round(random.uniform(complexity_range[0], complexity_range[1]), 2)
            
            # Tạo mẫu
            sample = {
                "id": f"sample_{i}",
                "task": {
                    "instruction": f"Sample task {i} for {task_type} in {domain}",
                    "input": "",
                    "context": ""
                },
                "analysis": {
                    "complexity_score": complexity_score,
                    "task_type": task_type,
                    "constraints": [],
                    "recommended_strategy": strategy
                },
                "thinking_processes": {
                    "fast_thinking": {
                        "process": "Sample fast thinking process" if strategy in ["fast_only", "fast_then_slow", "parallel", "iterative"] else "",
                        "simplified_task": "Sample simplified task" if strategy in ["fast_only", "fast_then_slow", "parallel", "iterative"] else "",
                        "intermediate_result": "Sample intermediate result" if strategy in ["fast_only", "fast_then_slow", "parallel", "iterative"] else ""
                    },
                    "slow_thinking": {
                        "decomposition": ["Step 1", "Step 2", "Step 3"] if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"] else [],
                        "reasoning": ["Reasoning 1", "Reasoning 2", "Reasoning 3"] if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"] else [],
                        "verification": ["Verification 1", "Verification 2", "Verification 3"] if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"] else [],
                        "intermediate_result": "Sample intermediate result" if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"] else ""
                    }
                },
                "integration": {
                    "process": "Sample integration process",
                    "inspection": "Sample inspection process",
                    "corrections": []
                },
                "output": {
                    "final_answer": "Sample final answer",
                    "explanation": "Sample explanation"
                },
                "metadata": {
                    "domain": domain,
                    "difficulty": difficulty,
                    "source": random.choice(["benchmark", "synthetic", "augmented"]),
                    "quality_score": round(random.uniform(0.7, 1.0), 2),
                    "tags": [strategy, task_type, domain]
                }
            }
            
            # Thêm một số lỗi ngẫu nhiên để kiểm tra xác thực
            if random.random() < 0.1:  # 10% mẫu có lỗi
                error_type = random.choice(["missing_field", "inconsistent_strategy", "empty_required_field", "invalid_complexity"])
                
                if error_type == "missing_field":
                    if random.random() < 0.5:
                        del sample["thinking_processes"]["fast_thinking"]["process"]
                    else:
                        del sample["output"]["explanation"]
                
                elif error_type == "inconsistent_strategy":
                    if strategy == "fast_only":
                        sample["thinking_processes"]["slow_thinking"]["decomposition"] = ["Step 1", "Step 2"]
                    elif strategy == "slow_only":
                        sample["thinking_processes"]["fast_thinking"]["process"] = "Inconsistent fast thinking process"
                
                elif error_type == "empty_required_field":
                    if random.random() < 0.5:
                        sample["task"]["instruction"] = ""
                    else:
                        sample["output"]["final_answer"] = ""
                
                elif error_type == "invalid_complexity":
                    if strategy == "fast_only":
                        sample["analysis"]["complexity_score"] = 0.7  # Quá cao cho fast_only
                    elif strategy == "slow_only":
                        sample["analysis"]["complexity_score"] = 0.2  # Quá thấp cho slow_only
            
            sample_data.append(sample)
        
        return sample_data
    
    def validate(self) -> Dict[str, Any]:
        """Xác thực dữ liệu"""
        print(f"Validating {len(self.data)} samples...")
        
        # Kiểm tra tính đầy đủ
        completeness_results = self._validate_completeness()
        
        # Kiểm tra tính nhất quán
        consistency_results = self._validate_consistency()
        
        # Kiểm tra tính đa dạng
        diversity_results = self._validate_diversity()
        
        # Kiểm tra chất lượng
        quality_results = self._validate_quality()
        
        # Tổng hợp kết quả
        self.validation_results = {
            "completeness": completeness_results,
            "consistency": consistency_results,
            "diversity": diversity_results,
            "quality": quality_results,
            "overall": {
                "total_samples": len(self.data),
                "valid_samples": completeness_results["valid_samples"],
                "invalid_samples": completeness_results["invalid_samples"],
                "validity_rate": completeness_results["validity_rate"],
                "average_quality_score": quality_results["average_quality_score"]
            }
        }
        
        # Lưu kết quả
        self._save_results()
        
        # Tạo trực quan hóa
        if self.config["visualization_enabled"]:
            self._create_visualizations()
        
        return self.validation_results
    
    def _validate_completeness(self) -> Dict[str, Any]:
        """Kiểm tra tính đầy đủ của dữ liệu"""
        print("Validating completeness...")
        
        valid_samples = 0
        invalid_samples = 0
        missing_fields = {}
        
        for sample in tqdm(self.data, desc="Checking completeness"):
            is_valid = True
            
            # Kiểm tra các trường bắt buộc
            required_fields = [
                ("id", None),
                ("task", "instruction"),
                ("analysis", "complexity_score"),
                ("analysis", "recommended_strategy"),
                ("thinking_processes", "fast_thinking"),
                ("thinking_processes", "slow_thinking"),
                ("output", "final_answer")
            ]
            
            for field, subfield in required_fields:
                if field not in sample:
                    is_valid = False
                    missing_fields[field] = missing_fields.get(field, 0) + 1
                elif subfield and (subfield not in sample[field] or not sample[field][subfield]):
                    is_valid = False
                    missing_fields[f"{field}.{subfield}"] = missing_fields.get(f"{field}.{subfield}", 0) + 1
            
            # Kiểm tra các trường bắt buộc dựa trên chiến lược
            strategy = sample.get("analysis", {}).get("recommended_strategy", "")
            
            if strategy in ["fast_only", "fast_then_slow", "parallel", "iterative"]:
                fast_thinking = sample.get("thinking_processes", {}).get("fast_thinking", {})
                if not fast_thinking.get("process"):
                    is_valid = False
                    missing_fields["thinking_processes.fast_thinking.process"] = missing_fields.get("thinking_processes.fast_thinking.process", 0) + 1
            
            if strategy in ["slow_only", "fast_then_slow", "parallel", "iterative"]:
                slow_thinking = sample.get("thinking_processes", {}).get("slow_thinking", {})
                if not slow_thinking.get("decomposition"):
                    is_valid = False
                    missing_fields["thinking_processes.slow_thinking.decomposition"] = missing_fields.get("thinking_processes.slow_thinking.decomposition", 0) + 1
            
            if is_valid:
                valid_samples += 1
            else:
                invalid_samples += 1
        
        return {
            "valid_samples": valid_samples,
            "invalid_samples": invalid_samples,
            "validity_rate": round(valid_samples / len(self.data) * 100, 2) if self.data else 0,
            "missing_fields": missing_fields
        }
    
    def _validate_consistency(self) -> Dict[str, Any]:
        """Kiểm tra tính nhất quán của dữ liệu"""
        print("Validating consistency...")
        
        consistent_samples = 0
        inconsistent_samples = 0
        inconsistency_types = {}
        
        for sample in tqdm(self.data, desc="Checking consistency"):
            is_consistent = True
            
            # Kiểm tra tính nhất quán giữa complexity_score và recommended_strategy
            complexity_score = sample.get("analysis", {}).get("complexity_score", 0)
            strategy = sample.get("analysis", {}).get("recommended_strategy", "")
            
            if strategy == "fast_only" and complexity_score > 0.3:
                is_consistent = False
                inconsistency_types["high_complexity_fast_only"] = inconsistency_types.get("high_complexity_fast_only", 0) + 1
            
            elif strategy == "slow_only" and complexity_score < 0.6:
                is_consistent = False
                inconsistency_types["low_complexity_slow_only"] = inconsistency_types.get("low_complexity_slow_only", 0) + 1
            
            # Kiểm tra tính nhất quán giữa recommended_strategy và thinking_processes
            if strategy == "fast_only":
                slow_thinking = sample.get("thinking_processes", {}).get("slow_thinking", {})
                if slow_thinking.get("decomposition") or slow_thinking.get("reasoning") or slow_thinking.get("verification"):
                    is_consistent = False
                    inconsistency_types["slow_thinking_in_fast_only"] = inconsistency_types.get("slow_thinking_in_fast_only", 0) + 1
            
            elif strategy == "slow_only":
                fast_thinking = sample.get("thinking_processes", {}).get("fast_thinking", {})
                if fast_thinking.get("process") or fast_thinking.get("simplified_task") or fast_thinking.get("intermediate_result"):
                    is_consistent = False
                    inconsistency_types["fast_thinking_in_slow_only"] = inconsistency_types.get("fast_thinking_in_slow_only", 0) + 1
            
            # Kiểm tra tính nhất quán giữa complexity_score và difficulty
            difficulty = sample.get("metadata", {}).get("difficulty", "")
            
            if difficulty == "easy" and complexity_score > 0.3:
                is_consistent = False
                inconsistency_types["high_complexity_easy"] = inconsistency_types.get("high_complexity_easy", 0) + 1
            
            elif difficulty == "medium" and (complexity_score < 0.3 or complexity_score > 0.6):
                is_consistent = False
                inconsistency_types["wrong_complexity_medium"] = inconsistency_types.get("wrong_complexity_medium", 0) + 1
            
            elif difficulty == "hard" and (complexity_score < 0.6 or complexity_score > 0.8):
                is_consistent = False
                inconsistency_types["wrong_complexity_hard"] = inconsistency_types.get("wrong_complexity_hard", 0) + 1
            
            elif difficulty == "expert" and complexity_score < 0.8:
                is_consistent = False
                inconsistency_types["low_complexity_expert"] = inconsistency_types.get("low_complexity_expert", 0) + 1
            
            if is_consistent:
                consistent_samples += 1
            else:
                inconsistent_samples += 1
        
        return {
            "consistent_samples": consistent_samples,
            "inconsistent_samples": inconsistent_samples,
            "consistency_rate": round(consistent_samples / len(self.data) * 100, 2) if self.data else 0,
            "inconsistency_types": inconsistency_types
        }
    
    def _validate_diversity(self) -> Dict[str, Any]:
        """Kiểm tra tính đa dạng của dữ liệu"""
        print("Validating diversity...")
        
        # Thống kê phân phối
        strategy_distribution = {}
        task_type_distribution = {}
        domain_distribution = {}
        difficulty_distribution = {}
        complexity_distribution = {
            "simple": 0,
            "medium": 0,
            "complex": 0,
            "very_complex": 0
        }
        source_distribution = {}
        
        for sample in tqdm(self.data, desc="Checking diversity"):
            # Thống kê chiến lược
            strategy = sample.get("analysis", {}).get("recommended_strategy", "unknown")
            strategy_distribution[strategy] = strategy_distribution.get(strategy, 0) + 1
            
            # Thống kê loại nhiệm vụ
            task_type = sample.get("analysis", {}).get("task_type", "unknown")
            task_type_distribution[task_type] = task_type_distribution.get(task_type, 0) + 1
            
            # Thống kê lĩnh vực
            domain = sample.get("metadata", {}).get("domain", "unknown")
            domain_distribution[domain] = domain_distribution.get(domain, 0) + 1
            
            # Thống kê độ khó
            difficulty = sample.get("metadata", {}).get("difficulty", "unknown")
            difficulty_distribution[difficulty] = difficulty_distribution.get(difficulty, 0) + 1
            
            # Thống kê độ phức tạp
            complexity_score = sample.get("analysis", {}).get("complexity_score", 0)
            if complexity_score < 0.3:
                complexity_distribution["simple"] += 1
            elif complexity_score < 0.6:
                complexity_distribution["medium"] += 1
            elif complexity_score < 0.8:
                complexity_distribution["complex"] += 1
            else:
                complexity_distribution["very_complex"] += 1
            
            # Thống kê nguồn
            source = sample.get("metadata", {}).get("source", "unknown")
            source_distribution[source] = source_distribution.get(source, 0) + 1
        
        # Tính chỉ số đa dạng (entropy)
        strategy_entropy = self._calculate_entropy(list(strategy_distribution.values()))
        task_type_entropy = self._calculate_entropy(list(task_type_distribution.values()))
        domain_entropy = self._calculate_entropy(list(domain_distribution.values()))
        difficulty_entropy = self._calculate_entropy(list(difficulty_distribution.values()))
        complexity_entropy = self._calculate_entropy(list(complexity_distribution.values()))
        source_entropy = self._calculate_entropy(list(source_distribution.values()))
        
        # Tính chỉ số đa dạng tổng thể
        overall_entropy = (strategy_entropy + task_type_entropy + domain_entropy + 
                          difficulty_entropy + complexity_entropy + source_entropy) / 6
        
        return {
            "strategy_distribution": strategy_distribution,
            "task_type_distribution": task_type_distribution,
            "domain_distribution": domain_distribution,
            "difficulty_distribution": difficulty_distribution,
            "complexity_distribution": complexity_distribution,
            "source_distribution": source_distribution,
            "entropy": {
                "strategy_entropy": strategy_entropy,
                "task_type_entropy": task_type_entropy,
                "domain_entropy": domain_entropy,
                "difficulty_entropy": difficulty_entropy,
                "complexity_entropy": complexity_entropy,
                "source_entropy": source_entropy,
                "overall_entropy": overall_entropy
            }
        }
    
    def _calculate_entropy(self, distribution: List[int]) -> float:
        """Tính entropy của một phân phối"""
        if not distribution or sum(distribution) == 0:
            return 0
        
        total = sum(distribution)
        probabilities = [count / total for count in distribution]
        entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in probabilities)
        
        # Chuẩn hóa entropy (chia cho log2(n) để có giá trị từ 0 đến 1)
        max_entropy = np.log2(len(distribution)) if len(distribution) > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return round(normalized_entropy, 4)
    
    def _validate_quality(self) -> Dict[str, Any]:
        """Kiểm tra chất lượng của dữ liệu"""
        print("Validating quality...")
        
        quality_scores = []
        low_quality_samples = 0
        high_quality_samples = 0
        
        # Thống kê chất lượng
        for sample in tqdm(self.data, desc="Checking quality"):
            quality_score = sample.get("metadata", {}).get("quality_score", 0)
            quality_scores.append(quality_score)
            
            if quality_score < 0.7:
                low_quality_samples += 1
            else:
                high_quality_samples += 1
        
        # Kiểm tra chi tiết một số mẫu ngẫu nhiên
        detailed_samples = []
        if self.data:
            sample_size = min(self.config["sample_size"], len(self.data))
            sampled_indices = random.sample(range(len(self.data)), sample_size)
            
            for idx in sampled_indices:
                sample = self.data[idx]
                
                # Đánh giá chi tiết
                detailed_evaluation = self._evaluate_sample_quality(sample)
                
                detailed_samples.append({
                    "id": sample.get("id", ""),
                    "task": sample.get("task", {}).get("instruction", ""),
                    "strategy": sample.get("analysis", {}).get("recommended_strategy", ""),
                    "quality_score": sample.get("metadata", {}).get("quality_score", 0),
                    "detailed_evaluation": detailed_evaluation
                })
        
        return {
            "average_quality_score": round(sum(quality_scores) / len(quality_scores), 4) if quality_scores else 0,
            "median_quality_score": round(np.median(quality_scores), 4) if quality_scores else 0,
            "min_quality_score": round(min(quality_scores), 4) if quality_scores else 0,
            "max_quality_score": round(max(quality_scores), 4) if quality_scores else 0,
            "low_quality_samples": low_quality_samples,
            "high_quality_samples": high_quality_samples,
            "detailed_samples": detailed_samples
        }
    
    def _evaluate_sample_quality(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Đánh giá chất lượng chi tiết của một mẫu"""
        evaluation = {}
        
        # Đánh giá instruction
        instruction = sample.get("task", {}).get("instruction", "")
        instruction_length = len(instruction)
        evaluation["instruction"] = {
            "length": instruction_length,
            "quality": "good" if instruction_length >= 10 else "poor"
        }
        
        # Đánh giá fast_thinking
        fast_thinking = sample.get("thinking_processes", {}).get("fast_thinking", {})
        fast_thinking_process = fast_thinking.get("process", "")
        evaluation["fast_thinking"] = {
            "length": len(fast_thinking_process),
            "quality": "good" if len(fast_thinking_process) >= 20 else "poor" if fast_thinking_process else "n/a"
        }
        
        # Đánh giá slow_thinking
        slow_thinking = sample.get("thinking_processes", {}).get("slow_thinking", {})
        decomposition = slow_thinking.get("decomposition", [])
        reasoning = slow_thinking.get("reasoning", [])
        verification = slow_thinking.get("verification", [])
        
        evaluation["slow_thinking"] = {
            "decomposition_steps": len(decomposition),
            "reasoning_steps": len(reasoning),
            "verification_steps": len(verification),
            "quality": "good" if len(decomposition) >= 3 and len(reasoning) >= 3 else "poor" if decomposition else "n/a"
        }
        
        # Đánh giá output
        final_answer = sample.get("output", {}).get("final_answer", "")
        explanation = sample.get("output", {}).get("explanation", "")
        
        evaluation["output"] = {
            "final_answer_length": len(final_answer),
            "explanation_length": len(explanation),
            "quality": "good" if len(final_answer) >= 5 and len(explanation) >= 10 else "poor"
        }
        
        # Đánh giá tổng thể
        good_count = sum(1 for v in evaluation.values() if v.get("quality") == "good")
        total_count = sum(1 for v in evaluation.values() if v.get("quality") in ["good", "poor"])
        
        evaluation["overall"] = {
            "good_ratio": round(good_count / total_count, 2) if total_count > 0 else 0,
            "quality": "good" if good_count / total_count >= 0.7 if total_count > 0 else 0 else "poor"
        }
        
        return evaluation
    
    def _save_results(self) -> None:
        """Lưu kết quả xác thực"""
        output_path = os.path.join(self.config["output_dir"], "validation_results.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, ensure_ascii=False, indent=2)
        
        print(f"Saved validation results to {output_path}")
        
        # Lưu báo cáo tóm tắt
        summary_path = os.path.join(self.config["output_dir"], "validation_summary.txt")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=== VALIDATION SUMMARY ===\n\n")
            
            f.write("OVERALL STATISTICS:\n")
            f.write(f"Total samples: {self.validation_results['overall']['total_samples']}\n")
            f.write(f"Valid samples: {self.validation_results['overall']['valid_samples']} ({self.validation_results['overall']['validity_rate']}%)\n")
            f.write(f"Invalid samples: {self.validation_results['overall']['invalid_samples']}\n")
            f.write(f"Average quality score: {self.validation_results['overall']['average_quality_score']}\n\n")
            
            f.write("COMPLETENESS:\n")
            f.write(f"Valid samples: {self.validation_results['completeness']['valid_samples']} ({self.validation_results['completeness']['validity_rate']}%)\n")
            f.write(f"Invalid samples: {self.validation_results['completeness']['invalid_samples']}\n")
            f.write("Missing fields:\n")
            for field, count in self.validation_results['completeness']['missing_fields'].items():
                f.write(f"  - {field}: {count}\n")
            f.write("\n")
            
            f.write("CONSISTENCY:\n")
            f.write(f"Consistent samples: {self.validation_results['consistency']['consistent_samples']} ({self.validation_results['consistency']['consistency_rate']}%)\n")
            f.write(f"Inconsistent samples: {self.validation_results['consistency']['inconsistent_samples']}\n")
            f.write("Inconsistency types:\n")
            for type_, count in self.validation_results['consistency']['inconsistency_types'].items():
                f.write(f"  - {type_}: {count}\n")
            f.write("\n")
            
            f.write("DIVERSITY:\n")
            f.write("Strategy distribution:\n")
            for strategy, count in self.validation_results['diversity']['strategy_distribution'].items():
                f.write(f"  - {strategy}: {count}\n")
            f.write("Task type distribution:\n")
            for task_type, count in self.validation_results['diversity']['task_type_distribution'].items():
                f.write(f"  - {task_type}: {count}\n")
            f.write("Domain distribution:\n")
            for domain, count in self.validation_results['diversity']['domain_distribution'].items():
                f.write(f"  - {domain}: {count}\n")
            f.write("Difficulty distribution:\n")
            for difficulty, count in self.validation_results['diversity']['difficulty_distribution'].items():
                f.write(f"  - {difficulty}: {count}\n")
            f.write("Complexity distribution:\n")
            for complexity, count in self.validation_results['diversity']['complexity_distribution'].items():
                f.write(f"  - {complexity}: {count}\n")
            f.write("Source distribution:\n")
            for source, count in self.validation_results['diversity']['source_distribution'].items():
                f.write(f"  - {source}: {count}\n")
            f.write("\n")
            
            f.write("Entropy (diversity score, 0-1):\n")
            for key, value in self.validation_results['diversity']['entropy'].items():
                f.write(f"  - {key}: {value}\n")
            f.write("\n")
            
            f.write("QUALITY:\n")
            f.write(f"Average quality score: {self.validation_results['quality']['average_quality_score']}\n")
            f.write(f"Median quality score: {self.validation_results['quality']['median_quality_score']}\n")
            f.write(f"Min quality score: {self.validation_results['quality']['min_quality_score']}\n")
            f.write(f"Max quality score: {self.validation_results['quality']['max_quality_score']}\n")
            f.write(f"Low quality samples: {self.validation_results['quality']['low_quality_samples']}\n")
            f.write(f"High quality samples: {self.validation_results['quality']['high_quality_samples']}\n")
        
        print(f"Saved validation summary to {summary_path}")
    
    def _create_visualizations(self) -> None:
        """Tạo trực quan hóa cho kết quả xác thực"""
        print("Creating visualizations...")
        
        # Tạo thư mục cho trực quan hóa
        viz_dir = os.path.join(self.config["output_dir"], "visualizations")
        os.makedirs(viz_dir, exist_ok=True)
        
        # Trực quan hóa tính đầy đủ
        self._visualize_completeness(viz_dir)
        
        # Trực quan hóa tính nhất quán
        self._visualize_consistency(viz_dir)
        
        # Trực quan hóa tính đa dạng
        self._visualize_diversity(viz_dir)
        
        # Trực quan hóa chất lượng
        self._visualize_quality(viz_dir)
        
        print(f"Saved visualizations to {viz_dir}")
    
    def _visualize_completeness(self, viz_dir: str) -> None:
        """Trực quan hóa tính đầy đủ"""
        # Biểu đồ tròn cho tỷ lệ mẫu hợp lệ/không hợp lệ
        plt.figure(figsize=(10, 6))
        labels = ['Valid', 'Invalid']
        sizes = [self.validation_results['completeness']['valid_samples'], 
                self.validation_results['completeness']['invalid_samples']]
        colors = ['#66b3ff', '#ff9999']
        explode = (0.1, 0)  # Tách phần "Valid" ra một chút
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')
        plt.title('Sample Validity')
        plt.savefig(os.path.join(viz_dir, 'completeness_validity.png'))
        plt.close()
        
        # Biểu đồ cột cho các trường bị thiếu
        if self.validation_results['completeness']['missing_fields']:
            plt.figure(figsize=(12, 8))
            fields = list(self.validation_results['completeness']['missing_fields'].keys())
            counts = list(self.validation_results['completeness']['missing_fields'].values())
            
            # Sắp xếp theo số lượng giảm dần
            sorted_indices = np.argsort(counts)[::-1]
            fields = [fields[i] for i in sorted_indices]
            counts = [counts[i] for i in sorted_indices]
            
            plt.bar(fields, counts, color='#ff9999')
            plt.xlabel('Missing Fields')
            plt.ylabel('Count')
            plt.title('Missing Fields Distribution')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, 'completeness_missing_fields.png'))
            plt.close()
    
    def _visualize_consistency(self, viz_dir: str) -> None:
        """Trực quan hóa tính nhất quán"""
        # Biểu đồ tròn cho tỷ lệ mẫu nhất quán/không nhất quán
        plt.figure(figsize=(10, 6))
        labels = ['Consistent', 'Inconsistent']
        sizes = [self.validation_results['consistency']['consistent_samples'], 
                self.validation_results['consistency']['inconsistent_samples']]
        colors = ['#66b3ff', '#ff9999']
        explode = (0.1, 0)  # Tách phần "Consistent" ra một chút
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')
        plt.title('Sample Consistency')
        plt.savefig(os.path.join(viz_dir, 'consistency_ratio.png'))
        plt.close()
        
        # Biểu đồ cột cho các loại không nhất quán
        if self.validation_results['consistency']['inconsistency_types']:
            plt.figure(figsize=(12, 8))
            types = list(self.validation_results['consistency']['inconsistency_types'].keys())
            counts = list(self.validation_results['consistency']['inconsistency_types'].values())
            
            # Sắp xếp theo số lượng giảm dần
            sorted_indices = np.argsort(counts)[::-1]
            types = [types[i] for i in sorted_indices]
            counts = [counts[i] for i in sorted_indices]
            
            plt.bar(types, counts, color='#ff9999')
            plt.xlabel('Inconsistency Types')
            plt.ylabel('Count')
            plt.title('Inconsistency Types Distribution')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, 'consistency_types.png'))
            plt.close()
    
    def _visualize_diversity(self, viz_dir: str) -> None:
        """Trực quan hóa tính đa dạng"""
        # Biểu đồ cột cho phân phối chiến lược
        plt.figure(figsize=(12, 8))
        strategies = list(self.validation_results['diversity']['strategy_distribution'].keys())
        counts = list(self.validation_results['diversity']['strategy_distribution'].values())
        
        plt.bar(strategies, counts, color='#66b3ff')
        plt.xlabel('Strategy')
        plt.ylabel('Count')
        plt.title('Strategy Distribution')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, 'diversity_strategy.png'))
        plt.close()
        
        # Biểu đồ cột cho phân phối loại nhiệm vụ
        plt.figure(figsize=(12, 8))
        task_types = list(self.validation_results['diversity']['task_type_distribution'].keys())
        counts = list(self.validation_results['diversity']['task_type_distribution'].values())
        
        plt.bar(task_types, counts, color='#66b3ff')
        plt.xlabel('Task Type')
        plt.ylabel('Count')
        plt.title('Task Type Distribution')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, 'diversity_task_type.png'))
        plt.close()
        
        # Biểu đồ cột cho phân phối độ phức tạp
        plt.figure(figsize=(12, 8))
        complexities = list(self.validation_results['diversity']['complexity_distribution'].keys())
        counts = list(self.validation_results['diversity']['complexity_distribution'].values())
        
        plt.bar(complexities, counts, color='#66b3ff')
        plt.xlabel('Complexity')
        plt.ylabel('Count')
        plt.title('Complexity Distribution')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, 'diversity_complexity.png'))
        plt.close()
        
        # Biểu đồ radar cho entropy
        plt.figure(figsize=(10, 10))
        categories = ['Strategy', 'Task Type', 'Domain', 'Difficulty', 'Complexity', 'Source']
        values = [
            self.validation_results['diversity']['entropy']['strategy_entropy'],
            self.validation_results['diversity']['entropy']['task_type_entropy'],
            self.validation_results['diversity']['entropy']['domain_entropy'],
            self.validation_results['diversity']['entropy']['difficulty_entropy'],
            self.validation_results['diversity']['entropy']['complexity_entropy'],
            self.validation_results['diversity']['entropy']['source_entropy']
        ]
        
        # Số lượng biến
        N = len(categories)
        
        # Góc của mỗi trục
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        
        # Thêm giá trị đầu tiên vào cuối để khép kín đa giác
        values += values[:1]
        
        # Vẽ biểu đồ
        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], categories, color='grey', size=10)
        plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ['0.2', '0.4', '0.6', '0.8', '1.0'], color='grey', size=10)
        plt.ylim(0, 1)
        
        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'b', alpha=0.1)
        
        plt.title('Diversity Entropy (0-1)')
        plt.savefig(os.path.join(viz_dir, 'diversity_entropy.png'))
        plt.close()
    
    def _visualize_quality(self, viz_dir: str) -> None:
        """Trực quan hóa chất lượng"""
        # Biểu đồ histogram cho phân phối điểm chất lượng
        quality_scores = [sample.get("metadata", {}).get("quality_score", 0) for sample in self.data]
        
        plt.figure(figsize=(10, 6))
        plt.hist(quality_scores, bins=20, color='#66b3ff', edgecolor='black')
        plt.xlabel('Quality Score')
        plt.ylabel('Count')
        plt.title('Quality Score Distribution')
        plt.axvline(x=0.7, color='r', linestyle='--', label='Threshold (0.7)')
        plt.legend()
        plt.savefig(os.path.join(viz_dir, 'quality_distribution.png'))
        plt.close()
        
        # Biểu đồ cột cho tỷ lệ mẫu chất lượng cao/thấp
        plt.figure(figsize=(8, 6))
        labels = ['High Quality', 'Low Quality']
        counts = [self.validation_results['quality']['high_quality_samples'], 
                 self.validation_results['quality']['low_quality_samples']]
        
        plt.bar(labels, counts, color=['#66b3ff', '#ff9999'])
        plt.xlabel('Quality Category')
        plt.ylabel('Count')
        plt.title('Sample Quality Distribution')
        plt.savefig(os.path.join(viz_dir, 'quality_categories.png'))
        plt.close()
        
        # Biểu đồ box plot cho điểm chất lượng theo chiến lược
        if self.data:
            # Tạo DataFrame từ dữ liệu
            data = []
            for sample in self.data:
                strategy = sample.get("analysis", {}).get("recommended_strategy", "unknown")
                quality_score = sample.get("metadata", {}).get("quality_score", 0)
                data.append({"strategy": strategy, "quality_score": quality_score})
            
            df = pd.DataFrame(data)
            
            plt.figure(figsize=(12, 8))
            df.boxplot(column='quality_score', by='strategy', grid=False)
            plt.suptitle('')
            plt.title('Quality Score by Strategy')
            plt.xlabel('Strategy')
            plt.ylabel('Quality Score')
            plt.savefig(os.path.join(viz_dir, 'quality_by_strategy.png'))
            plt.close()

# Hàm main
def main():
    """Hàm main"""
    parser = argparse.ArgumentParser(description="Validate data for Collaborative Fast & Slow Thinking Systems")
    parser.add_argument("--data_dir", type=str, default=CONFIG["data_dir"], help="Data directory")
    parser.add_argument("--output_dir", type=str, default=CONFIG["output_dir"], help="Output directory")
    parser.add_argument("--dataset_file", type=str, default=CONFIG["dataset_file"], help="Dataset file name")
    parser.add_argument("--sample_size", type=int, default=CONFIG["sample_size"], help="Number of samples for detailed check")
    parser.add_argument("--no_visualization", action="store_true", help="Disable visualization")
    
    args = parser.parse_args()
    
    # Cập nhật cấu hình
    config = CONFIG.copy()
    config["data_dir"] = args.data_dir
    config["output_dir"] = args.output_dir
    config["dataset_file"] = args.dataset_file
    config["sample_size"] = args.sample_size
    config["visualization_enabled"] = not args.no_visualization
    
    # Xác thực dữ liệu
    validator = DataValidator(config)
    results = validator.validate()
    
    # In tóm tắt kết quả
    print("\n=== VALIDATION SUMMARY ===")
    print(f"Total samples: {results['overall']['total_samples']}")
    print(f"Valid samples: {results['overall']['valid_samples']} ({results['overall']['validity_rate']}%)")
    print(f"Consistent samples: {results['consistency']['consistent_samples']} ({results['consistency']['consistency_rate']}%)")
    print(f"Average quality score: {results['overall']['average_quality_score']}")
    print(f"Overall diversity score: {results['diversity']['entropy']['overall_entropy']}")
    print(f"Results saved to {config['output_dir']}")

if __name__ == "__main__":
    main()
