# Description: 对meta_data根据category字段进行分层采样


import json
import random
from collections import defaultdict

def stratified_sampling_by_category(meta_data_path, samples_per_category=100, output_path=None, random_seed=42):
    """
    对meta_data根据category字段进行分层采样
    
    Args:
        meta_data_path: meta_data.json文件路径
        samples_per_category: 每个类别采样的数量
        output_path: 输出文件路径，如果为None则不保存文件
        random_seed: 随机种子
    
    Returns:
        dict: 采样后的数据
    """
    # 设置随机种子以确保结果可重现
    random.seed(random_seed)
    
    # 读取meta_data
    with open(meta_data_path, 'r', encoding='utf-8') as f:
        meta_data = json.load(f)
    
    # 按category分组
    category_groups = defaultdict(list)
    for key, value in meta_data.items():
        category = value.get('category')
        if category:
            category_groups[category].append(key)
    
    # 打印每个类别的统计信息
    print("类别统计信息:")
    for category, items in category_groups.items():
        print(f"  {category}: {len(items)} 个样本")
    
    # 对每个类别进行采样
    sampled_data = {}
    sampling_summary = {}
    
    for category, items in category_groups.items():
        # 如果该类别的样本数量少于要求的采样数量，则全部采用
        actual_sample_size = min(samples_per_category, len(items))
        sampled_items = random.sample(items, actual_sample_size)
        
        # 将采样的数据添加到结果中
        for item_key in sampled_items:
            sampled_data[item_key] = meta_data[item_key]
        
        sampling_summary[category] = {
            'original_count': len(items),
            'sampled_count': actual_sample_size
        }
    
    # 打印采样结果统计
    print("\n采样结果统计:")
    total_original = 0
    total_sampled = 0
    for category, summary in sampling_summary.items():
        print(f"  {category}: {summary['original_count']} -> {summary['sampled_count']}")
        total_original += summary['original_count']
        total_sampled += summary['sampled_count']
    
    print(f"\n总计: {total_original} -> {total_sampled}")
    
    # 如果指定了输出路径，保存采样结果
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sampled_data, f, ensure_ascii=False, indent=2)
        print(f"\n采样结果已保存到: {output_path}")
    
    return sampled_data

# 使用示例
if __name__ == "__main__":
    # 输入文件路径
    input_path = "/data2/hfc/datasets/MJHQ-30K/meta_data.json"
    
    # 输出文件路径
    output_path = "/data2/hfc/datasets/MJHQ-30K/meta_data_sampled.json"
    
    # 执行分层采样
    sampled_data = stratified_sampling_by_category(
        meta_data_path=input_path,
        samples_per_category=50,
        output_path=output_path,
        random_seed=42
    )
    
    print(f"\n采样完成！共采样了 {len(sampled_data)} 个样本")