def build_qa_prompt(query: str, chunks: list[dict]) -> str:
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[资料片段{i}] (document_id={chunk['document_id']}, chunk_index={chunk['chunk_index']})\n"
            f"{chunk['content']}"
        )

    context_text = "\n\n".join(context_parts)

    prompt = f"""
请基于下面提供的资料片段回答问题。

要求：
1. 优先依据资料内容作答。
2. 如果资料不足以回答，请明确说“资料不足，无法确定”。
3. 尽量不要编造资料中没有的信息。
4. 回答后可简要总结。

用户问题：
{query}

资料片段：
{context_text}
"""
    return prompt.strip()