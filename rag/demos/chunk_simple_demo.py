#!/usr/bin/env python3
"""
簡化版分塊邏輯演示
清楚展示核心概念
"""

def simple_chunk_demo():
    """
    用簡單的例子演示分塊邏輯
    """
    print("=" * 80)
    print("📚 文本分塊邏輯演示")
    print("=" * 80)

    # 準備文本
    text = "Python is great. Machine learning is powerful. AI is the future. Data science rocks."
    #       0              17                           48                 67                  84

    print(f"\n原始文本 (長度 {len(text)}):")
    print(f"  '{text}'\n")
    print("位置標記:")
    print("  0        10        20        30        40        50        60        70        80")
    print("  |---------|---------|---------|---------|---------|---------|---------|---------|")
    print(f"  {text}")
    print()

    # 參數
    chunk_size = 50
    chunk_overlap = 10

    print(f"參數設置:")
    print(f"  chunk_size = {chunk_size}")
    print(f"  chunk_overlap = {chunk_overlap}\n")

    # 手動演示三次迭代
    chunks = []

    # ===== 迭代 1 =====
    print("─" * 80)
    print("🔄 迭代 1")
    print("─" * 80)

    start = 0
    end = start + chunk_size  # 0 + 50 = 50

    print(f"1. start = {start}")
    print(f"2. end = start + chunk_size = {start} + {chunk_size} = {end}")
    print(f"3. 檢查是否在文本內: end ({end}) < len(text) ({len(text)})? {'是' if end < len(text) else '否'}")

    if end < len(text):
        # 尋找句子邊界
        print(f"4. 尋找句子邊界...")
        sentence_end = text.rfind('. ', start, end)
        print(f"   text.rfind('. ', {start}, {end}) = {sentence_end}")

        if sentence_end > start:
            print(f"   找到句號在位置 {sentence_end}: '{text[sentence_end:sentence_end+2]}'")
            end = sentence_end + 1
            print(f"   調整 end = {sentence_end} + 1 = {end}")

    chunk_text = text[start:end]
    print(f"5. 提取分塊: text[{start}:{end}]")
    print(f"   內容: '{chunk_text}'")
    print(f"   長度: {len(chunk_text)} 字元")

    chunks.append({'start': start, 'end': end, 'text': chunk_text})

    new_start = end - chunk_overlap
    print(f"6. 移動窗口: new_start = end - chunk_overlap = {end} - {chunk_overlap} = {new_start}")
    print(f"7. 重疊區域: [{new_start}:{end}] = '{text[new_start:end]}'")
    print(f"   重疊長度: {end - new_start} 字元\n")

    # ===== 迭代 2 =====
    print("─" * 80)
    print("🔄 迭代 2")
    print("─" * 80)

    start = new_start  # 40
    end = start + chunk_size  # 40 + 50 = 90

    print(f"1. start = {start}")
    print(f"2. end = start + chunk_size = {start} + {chunk_size} = {end}")
    print(f"3. 檢查是否在文本內: end ({end}) < len(text) ({len(text)})? {'是' if end < len(text) else '否'}")

    if end >= len(text):
        print(f"4. 已經超出文本末尾，這是最後一塊")
        end = len(text)
        print(f"   調整 end = len(text) = {end}")

    chunk_text = text[start:end]
    print(f"5. 提取分塊: text[{start}:{end}]")
    print(f"   內容: '{chunk_text}'")
    print(f"   長度: {len(chunk_text)} 字元")

    chunks.append({'start': start, 'end': end, 'text': chunk_text})

    new_start = end - chunk_overlap
    print(f"6. 移動窗口: new_start = end - chunk_overlap = {end} - {chunk_overlap} = {new_start}")

    if new_start < len(text):
        print(f"7. new_start ({new_start}) < len(text) ({len(text)})，繼續循環")
    else:
        print(f"7. new_start ({new_start}) >= len(text) ({len(text)})，結束循環")

    print("\n" + "=" * 80)
    print("📊 分塊結果總結")
    print("=" * 80)

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i}:")
        print(f"  位置: [{chunk['start']:2d}:{chunk['end']:2d}]")
        print(f"  長度: {len(chunk['text'])} 字元")
        print(f"  文本: '{chunk['text']}'")

        if i > 0:
            prev_chunk = chunks[i-1]
            overlap_start = chunk['start']
            overlap_end = prev_chunk['end']
            overlap_text = text[overlap_start:overlap_end]
            print(f"  🔗 與 Chunk {i-1} 重疊: '{overlap_text}'")

    # 視覺化
    print("\n" + "=" * 80)
    print("🎨 視覺化")
    print("=" * 80)
    print()
    print("位置標記:")
    print("  0        10        20        30        40        50        60        70        80")
    print("  |---------|---------|---------|---------|---------|---------|---------|---------|")
    print(f"  {text}")
    print()
    print(f"Chunk 0: [{chunks[0]['start']:2d}:{chunks[0]['end']:2d}]")
    print("  " + " " * chunks[0]['start'] + "├" + "─" * (chunks[0]['end'] - chunks[0]['start'] - 1) + "┤")
    print()
    print(f"Chunk 1: [{chunks[1]['start']:2d}:{chunks[1]['end']:2d}]")
    print("  " + " " * chunks[1]['start'] + "├" + "─" * (chunks[1]['end'] - chunks[1]['start'] - 1) + "┤")
    print()
    print("重疊區域:")
    overlap_start = chunks[1]['start']
    overlap_end = chunks[0]['end']
    print("  " + " " * overlap_start + "└" + "─" * (overlap_end - overlap_start - 1) + "┘")
    print("  " + " " * overlap_start + f"'{text[overlap_start:overlap_end]}'")


def edge_case_demo():
    """
    演示邊界情況
    """
    print("\n\n" + "=" * 80)
    print("⚠️ 邊界情況演示")
    print("=" * 80)

    # Case 1: 文本比 chunk_size 短
    print("\nCase 1: 文本太短")
    print("─" * 40)
    text = "Short."
    chunk_size = 50
    print(f"文本: '{text}' (長度 {len(text)})")
    print(f"chunk_size: {chunk_size}")

    start = 0
    end = start + chunk_size  # 0 + 50 = 50
    print(f"\nend = {end}, len(text) = {len(text)}")
    print(f"end >= len(text)? {end >= len(text)}")
    print(f"結果: 取整個文本，只產生 1 個 chunk")
    print(f"chunk = text[0:{len(text)}] = '{text}'")

    # Case 2: 沒有句子邊界
    print("\n\nCase 2: 沒有句子邊界")
    print("─" * 40)
    text = "PythonJavaC++RustGo" * 5  # 沒有空格或標點
    chunk_size = 20
    print(f"文本: '{text[:30]}...' (長度 {len(text)})")
    print(f"chunk_size: {chunk_size}")

    start = 0
    end = 20
    sentence_end = text.rfind('. ', start, end)
    print(f"\ntext.rfind('. ', {start}, {end}) = {sentence_end}")
    print(f"結果: 沒找到，保持 end = {end}")
    print(f"chunk = text[0:{end}] = '{text[0:end]}'")
    print(f"結論: 精確按 {chunk_size} 字元切割")

    # Case 3: overlap 太大
    print("\n\nCase 3: overlap 太大的問題")
    print("─" * 40)
    text = "A" * 100
    chunk_size = 20
    chunk_overlap = 25  # 比 chunk_size 還大！
    print(f"文本: '{text[:30]}...' (長度 {len(text)})")
    print(f"chunk_size: {chunk_size}")
    print(f"chunk_overlap: {chunk_overlap}")

    start = 0
    end = 20
    new_start = end - chunk_overlap  # 20 - 25 = -5
    print(f"\n第一次迭代: start=0, end=20")
    print(f"new_start = {end} - {chunk_overlap} = {new_start}")
    print(f"⚠️ 問題: new_start < 0！")
    print(f"解決: 在實際代碼中，下次迭代 start 最小為 0")
    print(f"但這會導致重複切分相同區域！")


def rfind_explanation():
    """
    詳細解釋 rfind() 函數
    """
    print("\n\n" + "=" * 80)
    print("🔍 rfind() 函數詳解")
    print("=" * 80)

    text = "Python is great. Java is fast. C++ is powerful."
    #       0              17            30              47

    print(f"\n文本: '{text}'")
    print("位置:  0        10        20        30        40        ")
    print("       |---------|---------|---------|---------|--------")
    print(f"       {text}")
    print()

    # 示例 1
    print("示例 1: text.rfind('. ', 0, 50)")
    result = text.rfind('. ', 0, 50)
    print(f"  搜索範圍: [0:50]")
    print(f"  從右向左找 '. '")
    print(f"  結果: {result}")
    print(f"  找到: '{text[result:result+2]}'")
    print()

    # 示例 2
    print("示例 2: text.rfind('. ', 0, 25)")
    result = text.rfind('. ', 0, 25)
    print(f"  搜索範圍: [0:25]")
    print(f"  從右向左找 '. '")
    print(f"  結果: {result}")
    print(f"  找到: '{text[result:result+2]}' (第一個句號)")
    print(f"  注意: 第二個句號在位置 30，超出搜索範圍")
    print()

    # 示例 3
    print("示例 3: text.rfind('. ', 20, 40)")
    result = text.rfind('. ', 20, 40)
    print(f"  搜索範圍: [20:40]")
    print(f"  從右向左找 '. '")
    print(f"  結果: {result}")
    print(f"  找到: '{text[result:result+2]}' (第二個句號)")
    print()

    # 示例 4
    print("示例 4: text.rfind('! ', 0, 50)")
    result = text.rfind('! ', 0, 50)
    print(f"  搜索範圍: [0:50]")
    print(f"  從右向左找 '! '")
    print(f"  結果: {result}")
    print(f"  說明: 沒找到，返回 -1")


def main():
    simple_chunk_demo()
    edge_case_demo()
    rfind_explanation()

    print("\n\n" + "🎉" * 40)
    print("演示完成！")
    print("🎉" * 40)
    print("\n關鍵要點:")
    print("  1. chunk_size 決定每個分塊的目標大小")
    print("  2. 優先在句子邊界切割（用 rfind 找最後一個句號）")
    print("  3. chunk_overlap 讓分塊之間有重疊，避免切斷關鍵信息")
    print("  4. 滑動窗口: new_start = end - overlap")
    print("  5. 最後一塊直接取到文本末尾")
    print()


if __name__ == "__main__":
    main()
