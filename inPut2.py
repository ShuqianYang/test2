import json

def main(json_data: str): #-> dict[str, Union[str, None]]:
    """
    将输入的JSON数据转换为MySQL INSERT语句
    
    Args:
        json_data (str): 输入的JSON字符串
        
    Returns:
        dict: 包含生成的SQL语句或错误信息的字典，结构为:
            {
                "sql": str,         # 生成的SQL语句（成功时）
                "error": str        # 错误信息（失败时）
            }
    """
    try:
        # 解析输入为字典
        data = json.loads(json_data)
        
        # 定义表结构约束
        table_name = "image_info"
        required_fields = {
            'object': str,
            'count': int,
            'behavior': str,
            'status': str,
            'percentage': int,
            'confidence': int,
            'caption': str
        }
        optional_fields = {'animal': str}
        
        # 验证必填字段
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"缺少必填字段: {', '.join(missing_fields)}"
        
        # 收集字段和值
        fields = []
        values = []
        
        # 处理必填字段
        for field in required_fields:
            fields.append(field)
            values.append(data[field])
        
        # 处理可选字段
        for field in optional_fields:
            if field in data:
                fields.append(field)
                values.append(data[field])
      
        
        # 构建SQL值部分
        formatted_values = []
        for value in values:
            if value is None:
                formatted_values.append("NULL")
            elif isinstance(value, str):
                formatted_values.append(f"'{value.replace("'", "''")}'")
            elif isinstance(value, (int, float)):
                formatted_values.append(str(value))
            else:
                return f"错误：字段 '{field}' 类型不支持 - {type(value)}"
        
        # 生成完整SQL
         sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(values)});"
         return sql
    
    except json.JSONDecodeError:
        return "错误：无效的JSON格式"
    except ValueError as e:
      #   return {"sql": None, "error": str(e)}
        return f"错误：{str(e)}"
    except Exception as e:
      #   return {"sql": None, "error": f"未知错误: {str(e)}"}
        return f"未知错误：{str(e)}"


# 示例使用
if __name__ == "__main__":
    # 测试用例1：正常输入
    test_input1 = '''{
        "object": "动物",
        "animal": "驼鹿",
        "count": 1,
        "behavior": "正在吃草",
        "status": "健康，自然状态",
        "percentage": 25,
        "confidence": 95,
        "caption": "图中展示了一只驼鹿在茂密的森林中吃草的场景。"
    }'''
    
    # 测试用例2：缺少必填字段
    test_input2 = '''{"object": "货物", "count": 2}'''
    
    for test_input in [test_input1, test_input2]:
        result = main(test_input)
        if result["sql"]:
            print("生成的SQL:")
            print(result["sql"])
        else:
            print("错误:", result["error"])
        print("-" * 50)