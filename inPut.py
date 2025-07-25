import json

def generate_mysql_insert(json_data: str) -> str:
    """
    将JSON数据转换为MySQL INSERT语句
    
    Args:
        json_data (str): JSON格式的字符串数据
        
    Returns:
        str: 成功时返回SQL插入语句，失败时返回错误信息字符串
    """
    try:
        # 解析JSON数据
        data = json.loads(json_data)
        
        # 定义表结构
        table_name = "image_info"
        required_fields = ['object', 'count', 'behavior', 'status', 'percentage', 'confidence', 'caption']
        optional_fields = ['animal']
        
        # 检查必填字段
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return f"错误：缺少必填字段 - {', '.join(missing_fields)}"
        
        # 收集字段和值
        fields = []
        values = []
        
        # 处理所有字段（必填+可选）
        all_fields = required_fields + optional_fields
        for field in all_fields:
            if field in data:
                fields.append(field)
                value = data[field]
                
                # 处理NULL值
                if value is None:
                    values.append("NULL")
                # 处理字符串类型
                elif isinstance(value, str):
                    # values.append(f"'{value.replace("'", "''")}'")
                    values.append(value)

                # 处理数字类型
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                else:
                    return f"错误：字段 '{field}' 类型不支持 - {type(value)}"
        
        # 构建SQL语句
        sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(values)});"
        return sql
    
    except json.JSONDecodeError:
        return "错误：无效的JSON格式"
    except Exception as e:
        return f"错误：{str(e)}"


# 示例用法
if __name__ == "__main__":
    # 测试用例1：正常数据
    test1 = '''{
        "object": "动物",
        "animal": "驼鹿",
        "count": 1,
        "behavior": "正在吃草",
        "status": "健康，自然状态",
        "percentage": 25,
        "confidence": 95,
        "caption": "图中展示了一只驼鹿在吃草"
    }'''
    print(generate_mysql_insert(test1))
    
    # # 测试用例2：缺少必填字段
    # test2 = '''{"object": "货物"}'''
    # print(generate_mysql_insert(test2))
    
    # # 测试用例3：无效JSON
    # test3 = "这不是JSON"
    # print(generate_mysql_insert(test3))