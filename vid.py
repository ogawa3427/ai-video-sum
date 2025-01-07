from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import json

# ImageMagickのパスを設定
change_settings({
    "IMAGEMAGICK_BINARY": r"ImageMagick\magick.exe"
})

def get_clip_segments():
    print("タイムスタンプの読み込みを開始します...")
    # gui.jsonからタイムスタンプを読み込む
    with open('fin.json', 'r', encoding='utf-8') as f:
        highlights = json.load(f)
    print(f"GUIから読み込んだハイライト数: {len(highlights)}")
    
    # timestamps.jsonから完全なタイムスタンプリストを読み込む
    with open('timestamps.json', 'r', encoding='utf-8') as f:
        full_timestamps = json.load(f)
    print(f"完全なタイムスタンプ数: {len(full_timestamps)}")
    
    segments = []
    for highlight in highlights:
        # GUI.jsonのタイムスタンプと一致するtimestamps.jsonのエントリを探す
        highlight_time = convert_timestamp_to_seconds(highlight['timestamp'])
        print(f"\n処理中のハイライト: {highlight['timestamp']} ({highlight_time}秒)")
        
        # 完全に一致するタイムスタンプを探す
        for ts in full_timestamps:
            if convert_timestamp_to_seconds(ts['timestamp']) == highlight_time:
                # 次のタイムスタンプまでを切り出す
                start_time = highlight_time
                end_time = find_next_timestamp(full_timestamps, start_time)
                segments.append((start_time, end_time))
                print(f"セグメント追加: {start_time}秒 → {end_time}秒")
                break
    
    print(f"\n合計 {len(segments)} 個のセグメントを抽出しました")
    return segments

def convert_timestamp_to_seconds(timestamp):
    """MM:SS形式のタイムスタンプを秒に変換"""
    minutes, seconds = map(int, timestamp.split(':'))
    return minutes * 60 + seconds

def find_previous_timestamp(full_timestamps, target_time):
    """target_timeの直前のタイムスタンプを見つける"""
    prev_time = 0
    for ts in full_timestamps:
        current_time = convert_timestamp_to_seconds(ts['timestamp'])
        if current_time >= target_time:
            return prev_time
        prev_time = current_time
    return prev_time

def find_next_timestamp(full_timestamps, target_time):
    """target_timeの直後のタイムスタンプを見つける"""
    for ts in full_timestamps:
        current_time = convert_timestamp_to_seconds(ts['timestamp'])
        if current_time > target_time:
            return current_time
    return min(target_time + 5, video.duration)  # 動画の長さを超えないようにする

def add_subtitles(video_clip, timestamps, segments):
    """動画に字幕を追加する"""
    print("字幕の追加を開始します...")
    
    # 字幕クリップのリストを作成
    subtitle_clips = []
    current_offset = 0  # 現在の時間オフセット
    
    for start, end in segments:
        for ts in timestamps:
            ts_time = convert_timestamp_to_seconds(ts['timestamp'])
            # このタイムスタンプがセグメントの範囲内かチェック
            if start <= ts_time < end:
                # 次のタイムスタンプまでを字幕の表示時間とする
                next_time = min(find_next_timestamp(timestamps, ts_time), end)
                duration = next_time - ts_time
                
                # TextClipを作成（フォントサイズ、色、位置を指定）
                text_clip = (TextClip(ts['text'], fontsize=24, color='yellow', font='Arial')
                           .set_position(('center', 'bottom'))
                           .set_duration(duration)
                           .set_start(ts_time - start + current_offset))
                
                subtitle_clips.append(text_clip)
                print(f"字幕クリップ追加: {duration}秒")
        
        current_offset += (end - start)
    
    # 字幕クリップを動画に合成
    final_clip = CompositeVideoClip([video_clip] + subtitle_clips)
    return final_clip

def cut_video(input_path, output_path):
    print(f"\n動画処理を開始します...")
    print(f"入力ファイル: {input_path}")
    print(f"出力ファイル: {output_path}")
    
    global video
    video = VideoFileClip(input_path)
    print(f"元の動画の長さ: {video.duration}秒")
    
    segments = get_clip_segments()
    print("\nクリップの切り出しを開始します...")
    
    # 各セグメントを切り出して連結
    clips = []
    for i, (start, end) in enumerate(segments, 1):
        print(f"クリップ {i}: {start}秒 → {end}秒 を切り出し中...")
        clip = video.subclip(start, end)
        clips.append(clip)
    
    # クリップを連結
    print("\nクリップの連結を開始します...")
    final_clip = concatenate_videoclips(clips)
    print(f"最終的な動画の長さ: {final_clip.duration}秒")
    
    # タイムスタンプを読み込む
    with open('timestamps.json', 'r', encoding='utf-8') as f:
        timestamps = json.load(f)
    
    # 字幕を追加（segmentsも渡す）
    # final_clip = add_subtitles(final_clip, timestamps, segments)
    
    # 出力
    print("\n動画の書き出しを開始します...")
    final_clip.write_videofile(output_path)
    print("動画の書き出しが完了しました")
    
    # クリーンアップ
    video.close()
    final_clip.close()
    print("処理が完了しました")

if __name__ == "__main__":
    input_video = "mini.mp4"  # 入力ビデオのパス
    output_video = "output4.mp4"  # 出力ビデオのパス
    cut_video(input_video, output_video)
