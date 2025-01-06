import env

import json
from typing import List, Dict
from openai import OpenAI

def summarize_subtitles(subtitles: List[Dict[str, str]], api_key: str) -> List[Dict[str, str]]:
    """字幕を要約してJSONファイルを更新する"""
    
    # OpenAI APIの設定
    client = OpenAI(api_key=env.api_key)
    
    # 字幕テキストを結合
    full_text = " ".join([subtitle["text"] for subtitle in subtitles])
    
    try:
        # GPT-3.5-turboを使用して要約を生成
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "以下の字幕テキストを要約してください。元の意図を保ちながら、簡潔に表現してください。JSONの配列の要素を破壊しないで使ってください。"},
                {"role": "user", "content": full_text}
            ]
        )
        
        # 要約テキストを取得
        summary = response.choices[0].message.content
        
        # 要約テキストを元のJSON構造に合わせて分割
        # この例では単純に最初の字幕に要約を入れ、他は空にします
        summarized_subtitles = subtitles.copy()
        summarized_subtitles[0]["text"] = summary
        for i in range(1, len(summarized_subtitles)):
            summarized_subtitles[i]["text"] = ""
        
        return summarized_subtitles
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return subtitles

def extract_key_timestamps(subtitles: List[Dict[str, str]], api_key: str) -> List[Dict[str, str]]:
    """重要な字幕のみを抽出する"""
    
    client = OpenAI(api_key=api_key)
    
    try:
        # GPT-4に重要な部分を選択させる
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "以下の字幕から、動画の主要なポイントを含む重要なタイムスタンプのみを選択してください。選択は10個程度に抑えてください。"},
                {"role": "user", "content": json.dumps(subtitles, ensure_ascii=False)}
            ]
        )
        
        # GPTの応答から重要なタイムスタンプを抽出
        selected_timestamps = json.loads(response.choices[0].message.content)
        
        # 元の字幕から選択されたタイムスタンプのみを抽出
        key_subtitles = [
            subtitle for subtitle in subtitles 
            if subtitle["timestamp"] in [ts["timestamp"] for ts in selected_timestamps]
        ]
        
        return key_subtitles
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []

def main():
    # JSONファイルを読み込む
    with open("timestamps.json", "r", encoding="utf-8") as f:
        subtitles = json.load(f)
    
    # 字幕を要約
    # summarized_subtitles = summarize_subtitles(subtitles, env.api_key)
    summarized_subtitles = extract_key_timestamps(subtitles, env.api_key)
    
    # 要約した字幕をJSONファイルに保存
    with open("summarized_timestamps.json", "w", encoding="utf-8") as f:
        json.dump(summarized_subtitles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()