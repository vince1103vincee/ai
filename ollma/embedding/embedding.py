from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 載入模型（用 GPT-2 示範，因為不需要權限，原理相同）
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# ===== 測試 =====

text = "Hello world"
tokens = tokenizer.encode(text, return_tensors="pt")

print(f"文字：{text}")
print(f"Token IDs：{tokens[0].tolist()}")
print(f"序列長度：{tokens.shape[1]}")

# ===== 步驟 1：Token Embeddings =====
token_embedding_layer = model.transformer.wte  # Word Token Embeddings
token_embeddings = token_embedding_layer(tokens)

print(f"\n步驟 1：Token Embeddings")
print(f"形狀：{token_embeddings.shape}")
print(f"第一個 token 的前 10 個數字：")
print(token_embeddings[0, 0, :10])

# ===== 步驟 2：Position Embeddings =====
position_embedding_layer = model.transformer.wpe  # Word Position Embeddings
seq_len = tokens.shape[1]
position_ids = torch.arange(seq_len).unsqueeze(0)  # [0, 1, 2, ...]

position_embeddings = position_embedding_layer(position_ids)

print(f"\n步驟 2：Position Embeddings")
print(f"位置 IDs：{position_ids[0].tolist()}")
print(f"形狀：{position_embeddings.shape}")
print(f"位置 0 的前 10 個數字：")
print(position_embeddings[0, 0, :10])

# ===== 步驟 3：相加 =====
final_embeddings = token_embeddings + position_embeddings

print(f"\n步驟 3：Token Embeddings + Position Embeddings")
print(f"形狀：{final_embeddings.shape}")
print(f"位置 0 的最終 embedding（前 10 個數字）：")
print(final_embeddings[0, 0, :10])

# ===== 驗證 =====
print(f"\n驗證：")
print(f"Token[0][0][0] = {token_embeddings[0, 0, 0].item():.6f}")
print(f"Position[0][0][0] = {position_embeddings[0, 0, 0].item():.6f}")
print(f"Final[0][0][0] = {final_embeddings[0, 0, 0].item():.6f}")
print(f"相加驗證：{token_embeddings[0, 0, 0].item():.6f} + {position_embeddings[0, 0, 0].item():.6f} = {final_embeddings[0, 0, 0].item():.6f}")