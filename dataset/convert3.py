import json

def convert_rlhf_format(input_file, output_file):
    """
    转换RLHF数据格式
    :param input_file: 原始JSON文件路径
    :param output_file: 输出JSON文件路径
    """
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    converted_data = []
    
    for item in original_data:
        # 转换对话历史
        conversations = []
        for turn in item["context"]:
            role = "human" if turn["role"] == "human" else "gpt"
            conversations.append({
                "from": role,
                "value": turn["text"]
            })
        
        # 添加被选择和被拒绝的回答
        converted_item = {
            "conversations": conversations,
            "chosen": {
                "from": "gpt",
                "value": item["chosen"]["text"]
            },
            "rejected": {
                "from": "gpt",
                "value": item["rejected"]["text"]
            }
        }
        
        converted_data.append(converted_item)
    
    # 保存转换后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, indent=2, ensure_ascii=False)
    
    print(f"转换完成！共处理 {len(original_data)} 条数据")

# 使用示例
if __name__ == "__main__":
    convert_rlhf_format("original_rlhf_data.json", "converted_rlhf_data.json")
