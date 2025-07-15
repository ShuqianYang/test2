import json
import argparse

def convert_jsonl_to_list(input_file, output_file):
    """
    将JSONL格式的数据集转换为包含字典列表的JSON文件
    
    参数:
    input_file: 输入的JSONL文件路径
    output_file: 输出的JSON文件路径
    """
    # 存储转换后的数据列表
    transformed_data = []
    
    # 读取原始JSONL文件
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            try:
                # 解析JSONL中的每一行
                original = json.loads(line.strip())
                
                # 创建新格式的条目
                new_item = {
                    "instruction": original["question"],
                    "chosen": original["chosen"],
                    "rejected": original["rejected"]
                }
                
                # 如果system存在且非空，添加到input字段
                if "system" in original and original["system"].strip():
                    new_item["input"] = original["system"]
                
                transformed_data.append(new_item)
            
            except json.JSONDecodeError:
                print(f"警告: 跳过无效的JSON行: {line}")
            except KeyError as e:
                print(f"警告: 缺少必要字段 {e}，跳过此行: {line}")

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
    convert_jsonl_to_list('btfChinese_DPO.jsonl', 'btfChinese_DPO_new.jsonl')
