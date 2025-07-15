import json
import argparse
from collections import OrderedDict

def convert_rlhf_dataset(input_file, output_file):
    """
    将JSONL格式的RLHF数据集转换为目标格式
    
    参数:
    input_file: 输入的JSONL文件路径
    output_file: 输出的JSON文件路径
    """
    # 存储转换后的数据列表
    transformed_data = []
    
    # 读取原始JSONL文件
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line_num, line in enumerate(infile, 1):
            try:
                # 解析JSONL中的每一行
                original = json.loads(line.strip())
                
                # 转换对话历史
                conversations = []
                for turn in original.get("context", []):
                    role = "human" if turn["role"] == "human" else "gpt"
                    conversations.append({
                        "from": role,
                        "value": turn["text"]
                    })
                
                # 创建新格式的条目
                new_item = OrderedDict()
                if conversations:
                    new_item["conversations"] = conversations
                
                # 添加chosen和rejected
                if "chosen" in original:
                    new_item["chosen"] = {
                        "from": "gpt",
                        "value": original["chosen"]["text"]
                    }
                
                if "rejected" in original:
                    new_item["rejected"] = {
                        "from": "gpt",
                        "value": original["rejected"]["text"]
                    }
                
                transformed_data.append(new_item)
            
            except json.JSONDecodeError:
                print(f"警告: 跳过无效的JSON行 (行号 {line_num})")
            except KeyError as e:
                print(f"警告: 缺少必要字段 {e} (行号 {line_num})")
            except Exception as e:
                print(f"错误: 处理行 {line_num} 时发生意外错误: {str(e)}")

    # 写入转换后的JSON文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(transformed_data, outfile, ensure_ascii=False, indent=2)
    
    print(f"转换完成! 共处理 {len(transformed_data)} 条数据")
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    # 设置命令行参数
    # parser = argparse.ArgumentParser(description='RLHF数据集格式转换工具')
    # parser.add_argument('-i', '--input', required=True, help='输入JSONL文件路径')
    # parser.add_argument('-o', '--output', required=True, help='输出JSON文件路径')
    
    # args = parser.parse_args()
    
    # 执行转换
    convert_rlhf_dataset('hh_rlhf_train.jsonl', 'hh_rlhf_train_new.json')
