from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-8B"


# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",  # 让 Transformers 自动选择最合适的 PyTorch 数据类型（比如 float16 或 float32）
    device_map="auto"  # 自动将模型切分并放到可用 GPU/CPU 上，方便大模型分布式或多 GPU 运行
)


# prepare the model input
prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "user", "content": prompt}
]
## qwen系列自定义的扩展方法
text = tokenizer.apply_chat_template(
    messages,         # 把用户提问封装成 messages 列表（支持多轮对话）。
    tokenize=False,   # 先用模板拼接成完整字符串，不立即分词
    add_generation_prompt=True,   # 在末尾加入模型“生成”提示（如 <gen>）；
    enable_thinking=True # Switches between thinking and non-thinking modes. Default is True. 
)
# 在模板中启用“思考”阶段标记，模型会生成包裹在<think>...</think>块中的思考内容，然后是最终的响应。
model_inputs = tokenizer([text], return_tensors="pt").to(model.device) 
# 这里的 "pt" 代表 PyTorch, tokenizer 把分词结果封装成 PyTorch 的 torch.Tensor。


# conduct text completion
generated_ids = model.generate( # [batch_size, seq_len]
    **model_inputs,
    max_new_tokens=32768
)
# 因为 generated_ids 包含原始输入的 token，所以用 len(input_ids) 跳过输入部分，只保留模型新生成的那一段。
# 如果一次性给模型多条输入，模型也会生成对应的多个序列
# input_ids[0]是你传给模型的第 1 条输入本身对应的 token ID 列表。
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 


# parsing thinking content
# 在 “思考” 模板里，</think> 对应的 token ID 假设是 151668。
# 通过反向查找 151668 来确定“思考”结束的位置 index；若找不到结束标记，则把所有输出当成正式回答。
try:
    # rindex finding 151668 (</think>)
    index = len(output_ids) - output_ids[::-1].index(151668)
except ValueError:
    index = 0


# thinking_content：从头到 index 之前的部分，即模型“思考”过程；
# content：从 index 开始到末尾的正式回答。
thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

print("thinking content:", thinking_content)
print("content:", content)

'''
问题：
1. tokenizer.apply_chat_template 是什么模型才有？

这是 Qwen 系列（以及少数其他开源聊天模型）的自定义扩展方法，不是 Hugging Face transformers 中所有分词器都具备的。
它基于特定的「聊天模板」设计，把 messages（带 role／content）列表格式化成带系统提示、用户提示、助手回答以及可选的 <think>...</think> 标记的完整字符串。
只有模型／分词器作者在 tokenizer 类里自己实现了 apply_chat_template，你才能直接调用。普通的 GPT-2、BERT、Llama 等模型的 AutoTokenizer 并不包含这一方法。

'''