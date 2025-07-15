import json
from googletrans import Translator
import time

def translate_json_file(input_file, output_file):
    """批量翻译JSON文件中的text字段"""
    # 初始化翻译器（添加重试机制）
    translator = Translator(service_urls=['translate.google.com', 'translate.google.cn'])
    
    # 读取原始JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 自定义翻译函数（带错误处理和术语词典）
    def translate_text(text):
        """翻译单条文本，包含运动术语处理"""
        # 运动术语预翻译词典
        sports_terms = {
            "quarterback": "四分卫",
            "NFL": "国家橄榄球联盟",
            "residential address": "住宅地址"
        }
        
        try:
            # 替换已知术语
            for term, trans in sports_terms.items():
                text = text.replace(term, trans)
                
            # 执行翻译（添加延迟避免被封IP）
            time.sleep(0.5)  # 降低请求频率
            result = translator.translate(text, src='en', dest='zh-cn').text
            
            # 后处理：修复人名翻译
            return result.replace("泰迪·布里奇沃特", "泰迪·布里奇沃特(Teddy Bridgewater)")
        except Exception as e:
            print(f"翻译失败: {text} | 错误: {str(e)}")
            return text  # 返回原文保底
    
    # 递归处理所有text字段
    def process_item(item):
        if isinstance(item, dict):
            for key in list(item.keys()):
                if key == "text":
                    item[key] = translate_text(item[key])
                else:
                    process_item(item[key])
        elif isinstance(item, list):
            for element in item:
                process_item(element)
    
    # 执行批量翻译
    process_item(data)
    
    # 保存翻译结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"翻译完成! 已保存至: {output_file}")

if __name__ == "__main__":
    translate_json_file(
        input_file='your_input.json', 
        output_file='translated_output.json'
    )
