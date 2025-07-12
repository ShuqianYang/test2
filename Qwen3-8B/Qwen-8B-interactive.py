#!/usr/bin/env python3
"""
Interactive Qwen Chat Script

This script enables a multi-turn interactive conversation with the Qwen3-8B model.
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def main():
    # 1. 模型与分词器初始化
    model_name = "Qwen/Qwen3-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    device = next(model.parameters()).device

    # 2. 会话消息列表，首条 system 消息定义助手角色
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("===== Starting interactive Qwen chat. Type 'exit' or 'quit' to end. =====")

    while True:
        # 3. 获取用户输入
        user_input = input("User: ")
        if user_input.strip().lower() in ("exit", "quit"):
            print("Exiting chat. Goodbye!")
            break

        # 4. 将用户消息追加到对话历史
        messages.append({"role": "user", "content": user_input})

        # 5. 应用聊天模板生成输入文本
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=True
        )

        # 6. 分词并转为张量，发送到模型所在设备
        inputs = tokenizer([text], return_tensors="pt").to(device)

        # 7. 模型生成
        generated = model.generate(
            **inputs,
            max_new_tokens=1024
        )
        output_ids = generated[0][len(inputs.input_ids[0]):].tolist()

        # 8. 分离 "思考" 与 "回答"
        think_end_id = tokenizer.convert_tokens_to_ids("</think>")
        try:
            # 找到最后一个 "</think>" 的位置
            rev = output_ids[::-1]
            split_idx = len(output_ids) - rev.index(think_end_id)
        except ValueError:
            split_idx = 0

        thinking = tokenizer.decode(output_ids[:split_idx], skip_special_tokens=True).strip()
        content = tokenizer.decode(output_ids[split_idx:], skip_special_tokens=True).strip()

        # 9. 打印模型的 "思考" 过程与正式回答
        if thinking:
            print(f"[Thinking]: {thinking}\n")
        print(f"Assistant: {content}\n")

        # 10. 将模型回答追加到消息历史
        messages.append({"role": "assistant", "content": content})

if __name__ == "__main__":
    main()
    
    
# ###### from huggingface
# from transformers import AutoModelForCausalLM, AutoTokenizer

# class QwenChatbot:
#     def __init__(self, model_name="Qwen/Qwen3-8B"):
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(model_name)
#         self.history = []

#     def generate_response(self, user_input):
#         messages = self.history + [{"role": "user", "content": user_input}]

#         text = self.tokenizer.apply_chat_template(
#             messages,
#             tokenize=False,
#             add_generation_prompt=True
#         )

#         inputs = self.tokenizer(text, return_tensors="pt")
#         response_ids = self.model.generate(**inputs, max_new_tokens=32768)[0][len(inputs.input_ids[0]):].tolist()
#         response = self.tokenizer.decode(response_ids, skip_special_tokens=True)

#         # Update history
#         self.history.append({"role": "user", "content": user_input})
#         self.history.append({"role": "assistant", "content": response})

#         return response

# # Example Usage
# if __name__ == "__main__":
#     chatbot = QwenChatbot()

#     # First input (without /think or /no_think tags, thinking mode is enabled by default)
#     user_input_1 = "How many r's in strawberries?"
#     print(f"User: {user_input_1}")
#     response_1 = chatbot.generate_response(user_input_1)
#     print(f"Bot: {response_1}")
#     print("----------------------")

#     # Second input with /no_think
#     user_input_2 = "Then, how many r's in blueberries? /no_think"
#     print(f"User: {user_input_2}")
#     response_2 = chatbot.generate_response(user_input_2)
#     print(f"Bot: {response_2}") 
#     print("----------------------")

#     # Third input with /think
#     user_input_3 = "Really? /think"
#     print(f"User: {user_input_3}")
#     response_3 = chatbot.generate_response(user_input_3)
#     print(f"Bot: {response_3}")
