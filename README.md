# AI Video Summarizer
このリポジトリは、GPTのみを使用して動画を要約するアプリケーションです。
したがってポッドキャストのように動画の動きが少ない=視覚情報の優先度が低い動画の要約しかできないと考えています。

english
this repository is an application that summarizes videos using only GPT.
Therefore, I think that only summaries of videos with low motion=low priority visual information, such as podcasts, can be made.

MIT License


# o1にこのプロンプトで投げたやつをvid.pyする

**タスク説明:**

以下に示すJSON形式のデータ配列があります。各要素はtimestamp（タイムスタンプ）とtext（テキスト）を含んでいます。この配列の要素を保持したまま、各textフィールドの重要な部分のみを抽出し、新しいJSON配列を作成してください。ただし、最終的な結論から逆算して要点に至る流れを伝えられるように考えて作業してください。元の構造を維持し、不要な部分は削除してください。それぞれのtextとtimestampは変更しないでください

**入力形式:**

json
[
    {
        "timestamp": "11:47",
        "text": "へえそれだごめん普通になんか誰かがこう"
    },
    {
        "timestamp": "11:51",
        "text": "いうのあったらいいなって言ってたやつ"
    },
    {
        "timestamp": "11:53",
        "text": "なんかと思ったわよかったよかったえ"
    },
    {
        "timestamp": "11:55",
        "text": "ゼルドあるんなるほど"
    }
    // 実際にはもっと多くの要素があります
]


**期待する出力形式:**

json
[
    {
        "timestamp": "11:53",
        "text": "なんかと思ったわよかったよかったえ"
    },
        {
        "timestamp": "11:47",
        "text": "へえそれだごめん普通になんか誰かがこう"
    },
]


**具体例:**

**入力:**

json
[
    {
        "timestamp": "11:47",
        "text": "へえそれだごめん普通になんか誰かがこう"
    },
    {
        "timestamp": "11:51",
        "text": "いうのあったらいいなって言ってたやつ"
    }
]


**出力:**

json
[
    {
        "timestamp": "11:51",
        "text": "いうのあったらいいなって言ってたやつ"
    }
]


**注意事項:**

- 配列の順序と各要素のtimestampはそのまま保持してください。
- 出力は有効なJSON形式である必要があります。


**データ:**


[ 
  {
    "timestamp": "00:00",
    "text": "上がった"
  },
  {
    "timestamp": "00:02",
    "text": "最初は切っちゃうかオッケー"
  },
  {
    "timestamp": "00:08",
    "text": "じゃあまずは"
  },
  {
    "timestamp": "00:14",
    "text": "動画見てどう?"
  },
  {
    "timestamp": "00:20",
    "text": "なんか うんうん"
  },
  {
    "timestamp": "00:24",
    "text": "思い浮かぶ"
  },
  {
    "timestamp": "00:27",
    "text": "今まで出てる習った内容"
  },