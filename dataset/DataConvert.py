import json
import re

def contains_chinese(text):
    """检查字符串是否包含中文字符"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def convert_format(input_file, output_file):
    """
    转换数据格式并过滤中文
    :param input_file: 原始JSON文件路径
    :param output_file: 输出JSON文件路径
    """
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            original_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in input file")

    converted_data = []
    
    for item in original_data:
        prompt = item.get("prompt", "")
        prediction = item.get("prediction", "")
        
        # 跳过包含中文的条目
        if contains_chinese(prompt) or contains_chinese(prediction):
            continue
        
        # 构建新格式
        new_item = {
            "instruction": prompt.strip(),
            "input": "",
            "output": prediction.strip()
        }
        converted_data.append(new_item)
    
    # 保存转换后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, indent=2, ensure_ascii=False)
    
    print(f"转换完成！共处理 {len(original_data)} 条数据，保留 {len(converted_data)} 条英文数据")

# 使用示例
if __name__ == "__main__":
    convert_format("Condor_Refine_20k.json", "Condor_Refine_20k_new.json")