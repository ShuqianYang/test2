import json
import re
from bs4 import BeautifulSoup  # 使用BeautifulSoup解析HTML标签结构

def extract_answer_content(original_output):
    """从原始输出中提取并清理<answer>标签内容"""
    # 方法1：使用BeautifulSoup解析HTML标签
    try:
        soup = BeautifulSoup(original_output, 'html.parser')
        answer_tag = soup.find('answer')
        if answer_tag:
            # 提取标签内的文本内容
            answer_content = answer_tag.get_text(strip=False)
            
            # 清理可能的多余空格和换行
            answer_content = re.sub(r'\s+', ' ', answer_content).strip()
            
            # 修复boxed格式问题：将\boxed(64)改为\boxed{64}
            answer_content = re.sub(r'\\boxed\((\d+)\)', r'\\boxed{\1}', answer_content)
            
            return answer_content
    except:
        pass  # 如果BeautifulSoup失败，尝试备用方法
    
    # 方法2：使用正则表达式作为备选方案
    match = re.search(r'<answer>(.*?)</answer>', original_output, re.DOTALL)
    if match:
        answer_content = match.group(1)
        # 清理内容并修复boxed格式
        answer_content = re.sub(r'\s+', ' ', answer_content).strip()
        answer_content = re.sub(r'\\boxed\((\d+)\)', r'\\boxed{\1}', answer_content)
        return answer_content
    
    # 如果以上方法都失败，返回原始内容（但应该不会发生）
    return original_output

def convert_format(source_path, target_path):
    converted_data = []
    
    # 读取源文件
    with open(source_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                original = json.loads(line)
                
                # 构建新格式
                new_item = {
                    "instruction": original["input"],
                    "input": "",  # 无附加输入
                    "output": extract_answer_content(original["output"])
                }
                
                converted_data.append(new_item)
            except json.JSONDecodeError:
                print(f"JSON解析错误，跳过行: {line}")
                continue
    
    # 保存为JSON文件
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == "__main__":
    input_file = "train.jsonl"
    output_file = "math_sft_40k_answers.json"
    convert_format(input_file, output_file)
    print(f"转换完成! 结果已保存到 {output_file}")
