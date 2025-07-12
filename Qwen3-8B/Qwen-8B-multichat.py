'''
多轮对话：不断地把新的 `{"role":"user",...}` 和 `{"role":"assistant",...}` 加入同一个 `messages` 列表，
每次都用它来生成下一个回答。
'''
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

# 1.初始化消息列表，可选加入一条 system 消息做全局指令
messages = [
    {"role": "system",    "content": "You are a helpful assistant."},
    {"role": "user",      "content": "你好，模型！"}
]

def chat_once(messages):
    # 用 tokenizer.apply_chat_template 拼接会话
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )
    # 分词并转 tensor
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    # 生成
    gen_ids = model.generate(**inputs, max_new_tokens=1024)
    output_ids = gen_ids[0][len(inputs.input_ids[0]) : ].tolist() 
    # 解码
    full = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
    # 如果你也想截取 thinking/content，可参照前面那段逻辑
    return full

# 2.第一轮对话
assistant_reply = chat_once(messages)
# 把模型回复 append 到消息里
messages.append({"role": "assistant", "content": assistant_reply})

# 3.第二轮用户提问
messages.append({"role": "user", "content": "能给我讲讲大语言模型的应用场景吗？"})
assistant_reply = chat_once(messages)
messages.append({"role": "assistant", "content": assistant_reply})

# 如此循环，messages 中会越来越长，包含全部上下文
