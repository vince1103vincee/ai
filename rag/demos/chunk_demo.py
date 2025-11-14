#!/usr/bin/env python3
"""
文本分塊邏輯演示程序
展示 chunk_text 函數的執行過程
"""

def chunk_text_with_debug(text: str, chunk_size: int = 500, chunk_overlap: int = 50):
    """
    帶調試輸出的分塊函數
    """
    print("=" * 80)
    print(f"📝 開始分塊")
    print(f"   文本長度: {len(text)} 字元")
    print(f"   chunk_size: {chunk_size}")
    print(f"   chunk_overlap: {chunk_overlap}")
    print("=" * 80)

    chunks = []
    start = 0
    iteration = 1

    while start < len(text):
        print(f"\n{'─' * 80}")
        print(f"🔄 迭代 {iteration}")
        print(f"{'─' * 80}")
        print(f"當前 start 位置: {start}")

        # 計算初始結束位置
        end = start + chunk_size
        print(f"計算 end = start + chunk_size = {start} + {chunk_size} = {end}")

        # 檢查是否需要調整邊界
        if end < len(text):
            print(f"\n🔍 end ({end}) < len(text) ({len(text)})，嘗試尋找句子邊界...")

            # 尋找各種結束符
            period_pos = text.rfind('. ', start, end)
            exclamation_pos = text.rfind('! ', start, end)
            question_pos = text.rfind('? ', start, end)
            newline_pos = text.rfind('\n', start, end)

            print(f"   尋找 '. ': {period_pos if period_pos != -1 else '未找到'}")
            print(f"   尋找 '! ': {exclamation_pos if exclamation_pos != -1 else '未找到'}")
            print(f"   尋找 '? ': {question_pos if question_pos != -1 else '未找到'}")
            print(f"   尋找 '\\n': {newline_pos if newline_pos != -1 else '未找到'}")

            sentence_end = max(period_pos, exclamation_pos, question_pos, newline_pos)
            print(f"   max() = {sentence_end}")

            if sentence_end > start:
                old_end = end
                end = sentence_end + 1
                print(f"✅ 找到句子邊界！調整 end: {old_end} → {end}")
                print(f"   在位置 {sentence_end} 找到: '{text[sentence_end:sentence_end+2]}'")
            else:
                print(f"❌ 未找到有效句子邊界，保持原 end = {end}")
        else:
            print(f"\n📍 end ({end}) >= len(text) ({len(text)})，這是最後一塊")
            end = len(text)
            print(f"   調整 end 為文本長度: {end}")

        # 提取分塊
        chunk_text = text[start:end].strip()
        print(f"\n✂️ 提取分塊:")
        print(f"   範圍: [{start}:{end}]")
        print(f"   長度: {len(chunk_text)} 字元")
        print(f"   內容預覽: '{chunk_text[:50]}{'...' if len(chunk_text) > 50 else ''}'")

        if chunk_text:
            chunk_info = {
                'chunk_index': len(chunks),
                'start_char': start,
                'end_char': end,
                'length': len(chunk_text),
                'text': chunk_text
            }
            chunks.append(chunk_info)
            print(f"✅ 添加到 chunks[{chunk_info['chunk_index']}]")
        else:
            print(f"⚠️ 分塊為空，跳過")

        # 計算下一個起始位置
        old_start = start
        start = end - chunk_overlap
        print(f"\n➡️ 移動窗口:")
        print(f"   新 start = end - chunk_overlap = {end} - {chunk_overlap} = {start}")

        # 防止無限循環：如果 start 沒有前進，強制前進
        if start <= old_start:
            print(f"⚠️ 檢測到可能的無限循環！start ({start}) <= old_start ({old_start})")
            start = old_start + 1
            print(f"   強制前進: start = {start}")

        if start < len(text):
            overlap_start = max(old_start, start)
            overlap_end = min(end, len(text))
            overlap_text = text[overlap_start:overlap_end]
            print(f"   重疊區域: [{overlap_start}:{overlap_end}] (長度: {overlap_end - overlap_start})")
            print(f"   重疊內容: '{overlap_text[:30]}{'...' if len(overlap_text) > 30 else ''}'")

        iteration += 1

    print(f"\n{'=' * 80}")
    print(f"✅ 分塊完成！")
    print(f"   總共產生 {len(chunks)} 個分塊")
    print(f"   總字元數（含重疊）: {sum(c['length'] for c in chunks)}")
    print(f"   原始文本長度: {len(text)}")
    print(f"   重疊比例: {(sum(c['length'] for c in chunks) - len(text)) / len(text) * 100:.1f}%")
    print("=" * 80)

    return chunks


def visualize_chunks(text: str, chunks: list):
    """
    視覺化分塊結果
    """
    print("\n" + "=" * 80)
    print("📊 分塊視覺化")
    print("=" * 80)

    # 創建一個字元級別的標記數組
    char_markers = [' '] * len(text)

    for i, chunk in enumerate(chunks):
        marker = str(i)
        for pos in range(chunk['start_char'], chunk['end_char']):
            if pos < len(char_markers):
                if char_markers[pos] == ' ':
                    char_markers[pos] = marker
                else:
                    char_markers[pos] = '*'  # 重疊區域用 * 標記

    # 打印每個分塊的詳細信息
    for i, chunk in enumerate(chunks):
        print(f"\n📦 Chunk {i}:")
        print(f"   位置: [{chunk['start_char']:4d}:{chunk['end_char']:4d}]")
        print(f"   長度: {chunk['length']} 字元")
        print(f"   文本: {chunk['text'][:80]}{'...' if len(chunk['text']) > 80 else ''}")

        # 顯示重疊信息
        if i > 0:
            prev_chunk = chunks[i - 1]
            overlap_start = chunk['start_char']
            overlap_end = prev_chunk['end_char']
            if overlap_start < overlap_end:
                overlap_len = overlap_end - overlap_start
                overlap_text = text[overlap_start:overlap_end]
                print(f"   🔗 與 Chunk {i-1} 重疊: {overlap_len} 字元")
                print(f"      重疊內容: '{overlap_text[:50]}{'...' if len(overlap_text) > 50 else ''}'")

    # 打印字元級別的視覺化
    print(f"\n📏 字元級別視覺化（每行 100 字元）:")
    print(f"   0 = Chunk 0, 1 = Chunk 1, * = 重疊區域\n")

    for i in range(0, len(char_markers), 100):
        line_markers = ''.join(char_markers[i:i+100])
        print(f"   {i:4d}: {line_markers}")


def demo_simple_text():
    """
    演示 1：簡單文本
    """
    print("\n" + "🎯" * 40)
    print("演示 1：簡單文本（有明確句子邊界）")
    print("🎯" * 40)

    text = """Python is a high-level programming language. It was created by Guido van Rossum. Python emphasizes code readability. It supports multiple programming paradigms. Python is widely used in data science and machine learning."""

    chunks = chunk_text_with_debug(text, chunk_size=100, chunk_overlap=20)
    visualize_chunks(text, chunks)


def demo_no_punctuation():
    """
    演示 2：沒有標點符號的文本
    """
    print("\n" + "🎯" * 40)
    print("演示 2：沒有標點符號（只能按字元數切割）")
    print("🎯" * 40)

    text = "Python" * 50  # "PythonPythonPython..." 300 字元

    chunks = chunk_text_with_debug(text, chunk_size=100, chunk_overlap=20)
    visualize_chunks(text, chunks)


def demo_real_document():
    """
    演示 3：真實文檔
    """
    print("\n" + "🎯" * 40)
    print("演示 3：真實文檔（來自 demo_docs）")
    print("🎯" * 40)

    text = """Python is a high-level, interpreted programming language known for its simplicity and readability.
It was created by Guido van Rossum and first released in 1991. Python emphasizes code readability
with its use of significant indentation.

Python supports multiple programming paradigms, including procedural, object-oriented, and functional
programming. It has a comprehensive standard library that supports many common programming tasks.

Common use cases for Python include web development, data analysis, artificial intelligence,
scientific computing, and automation. Popular frameworks include Django and Flask for web development,
NumPy and Pandas for data analysis, and TensorFlow and PyTorch for machine learning."""

    chunks = chunk_text_with_debug(text, chunk_size=200, chunk_overlap=30)
    visualize_chunks(text, chunks)


def demo_edge_cases():
    """
    演示 4：邊界情況
    """
    print("\n" + "🎯" * 40)
    print("演示 4：邊界情況")
    print("🎯" * 40)

    # Case 1: 文本比 chunk_size 短
    print("\n" + "─" * 40)
    print("Case 1: 文本太短")
    print("─" * 40)
    text1 = "Short text."
    chunks1 = chunk_text_with_debug(text1, chunk_size=100, chunk_overlap=20)

    # Case 2: 只有空白
    print("\n" + "─" * 40)
    print("Case 2: 空白文本")
    print("─" * 40)
    text2 = "     "
    chunks2 = chunk_text_with_debug(text2, chunk_size=100, chunk_overlap=20)

    # Case 3: 精確等於 chunk_size
    print("\n" + "─" * 40)
    print("Case 3: 文本長度正好等於 chunk_size")
    print("─" * 40)
    text3 = "A" * 100
    chunks3 = chunk_text_with_debug(text3, chunk_size=100, chunk_overlap=20)


def compare_parameters():
    """
    演示 5：比較不同參數的效果
    """
    print("\n" + "🎯" * 40)
    print("演示 5：比較不同參數組合")
    print("🎯" * 40)

    text = """Machine Learning is a subset of artificial intelligence. It enables systems to learn and improve.
Supervised learning uses labeled data. Unsupervised learning finds patterns. Reinforcement learning learns through trial and error."""

    configs = [
        (100, 10, "小塊、小重疊"),
        (100, 30, "小塊、大重疊"),
        (200, 20, "大塊、小重疊"),
        (50, 25, "超小塊、50% 重疊"),
    ]

    for chunk_size, chunk_overlap, desc in configs:
        print(f"\n{'═' * 80}")
        print(f"配置: {desc}")
        print(f"chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
        print(f"{'═' * 80}")

        chunks = chunk_text_with_debug(text, chunk_size, chunk_overlap)

        print(f"\n📊 統計:")
        print(f"   分塊數量: {len(chunks)}")
        print(f"   平均分塊長度: {sum(c['length'] for c in chunks) / len(chunks):.1f}")
        print(f"   最短分塊: {min(c['length'] for c in chunks)}")
        print(f"   最長分塊: {max(c['length'] for c in chunks)}")


def main():
    """
    主函數
    """
    import sys

    print("""
╔══════════════════════════════════════════════════════════════════════╗
║             文本分塊邏輯演示程序 (chunk_text)                        ║
╚══════════════════════════════════════════════════════════════════════╝

可用演示：
  1 - 簡單文本（有句子邊界）
  2 - 沒有標點符號
  3 - 真實文檔（來自 demo_docs）
  4 - 邊界情況測試
  5 - 參數比較
  all - 運行所有演示

""")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("選擇演示 (1-5 或 'all'): ").strip()

    if choice == '1':
        demo_simple_text()
    elif choice == '2':
        demo_no_punctuation()
    elif choice == '3':
        demo_real_document()
    elif choice == '4':
        demo_edge_cases()
    elif choice == '5':
        compare_parameters()
    elif choice.lower() == 'all':
        demo_simple_text()
        demo_no_punctuation()
        demo_real_document()
        demo_edge_cases()
        compare_parameters()
    else:
        print("無效選擇，使用 1, 2, 3, 4, 5 或 'all'")
        return

    print("\n" + "🎉" * 40)
    print("演示完成！")
    print("🎉" * 40)


if __name__ == "__main__":
    main()
