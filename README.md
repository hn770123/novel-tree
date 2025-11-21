# 目覚めの部屋 - セルフセラピーノベル

## 概要

「目覚めの部屋」は、プレイヤーが自分自身の深層心理と向き合うセルフセラピー型ノベルゲームのシナリオです。

### ストーリー

あなたは女性で、目が覚めると真っ白な空間にいました。
目の前には黒髪黒服の眼鏡の男性が、笑顔と呼ぶには感情を感じさせない顔でこちらを見ています。

彼はセラピスト。あなた自身を映す鏡のような存在です。

彼との対話を通じて、あなたは自分の心と向き合い、大切なことを思い出していきます。
そして最後には、気持ちの良い目覚めを迎えることができるでしょう。

## 特徴

### 🌟 セルフセラピー体験
- プレイヤーが自分自身と向き合う時間を提供
- すべての選択肢に正解・不正解はありません
- 受容的なセラピストがあなたの心を優しく導きます

### 🔀 豊富な分岐システム
- 4つの選択ポイント
- 256通りの体験パターン
- 4種類のエンディング（すべてポジティブ）

### 💭 間接的な記憶探索
- 「子供の頃の思い出は？」といった直接的な質問は避けます
- 「心に浮かぶ色」「行きたい場所」など抽象的な質問を通じて、自然に過去の記憶が蘇ります
- プレイヤー自身が気づきを得られる設計

### ✨ ポジティブな結末
- どの選択をしても、最終的には「気持ちの良い目覚め」に到達
- プレイヤーに希望と前向きな気持ちを残します

## ファイル構成

```
novel-tree/
├── README.md                  # このファイル
├── scenario.json              # メインシナリオファイル
├── SCENARIO_STRUCTURE.md      # シナリオ構造の詳細説明
├── SCENARIO_FLOWCHART.md      # シナリオフローチャート（視覚的な分岐図）
├── validate_scenario.py       # シナリオ検証スクリプト
└── visualize_scenario.py      # シナリオ視覚化スクリプト
```

## シナリオファイルの構造

### scenario.json

JSON形式でノベルゲームのシナリオを定義しています。

#### 主要な要素

- **title**: ゲームのタイトル
- **description**: ゲームの説明
- **startNode**: 開始ノードのID
- **nodes**: すべてのシーンノード
- **metadata**: メタデータ（バージョン、作者、推定プレイ時間など）

#### ノードの種類

1. **story**: ナレーションや状況説明（自動進行）
2. **dialogue**: キャラクターの会話（自動進行）
3. **choice**: プレイヤーの選択分岐

### ノード構造の例

```json
{
  "id": "opening",
  "type": "story",
  "speaker": "ナレーション",
  "text": "目が覚めると、そこは真っ白な空間だった。",
  "background": "white_room",
  "next": "meet_therapist"
}
```

```json
{
  "id": "question_color",
  "type": "choice",
  "speaker": "セラピスト",
  "text": "今、あなたの心に浮かぶ色は何色ですか？",
  "background": "white_room",
  "character": "therapist_neutral",
  "choices": [
    {
      "text": "暖かいオレンジ色",
      "next": "response_color_warm",
      "flag": "warm_color"
    },
    {
      "text": "冷たい青色",
      "next": "response_color_cool",
      "flag": "cool_color"
    }
  ]
}
```

## シナリオの分岐構造

### 選択ポイント

1. **心に浮かぶ色**（4択）
   - 暖かいオレンジ色
   - 冷たい青色
   - 優しい緑色
   - 何も思い浮かばない

2. **行きたい場所**（4択）
   - 静かな図書館
   - 賑やかなお祭り
   - 広い海辺
   - 小さな部屋

3. **記憶への感情**（4択）
   - 温かく、穏やかな気持ち
   - 少し切ない気持ち
   - 複雑な気持ち
   - よくわからない

4. **大切にしたいもの**（4択）
   - 自分自身の心
   - 大切な人との繋がり
   - 自由に生きること
   - 穏やかな日々

### エンディング

4つのエンディングがありますが、すべて「気持ちの良い目覚め」で終わります。

1. **自己愛エンディング**: 自分を大切にすることに気づく
2. **繋がりエンディング**: 人との絆の大切さに気づく
3. **自由エンディング**: 自分らしく生きる権利に気づく
4. **平和エンディング**: 穏やかな日々の尊さに気づく

詳細な分岐図は `SCENARIO_STRUCTURE.md` を参照してください。

## 必要なアセット

### 背景画像

- `white_room`: 真っ白な空間
- `memory_blur`: ぼやけた記憶のイメージ
- `white_light`: 光に包まれる空間
- `morning_room`: 朝の光が差し込む部屋

### キャラクター画像

- `therapist_neutral`: 無表情のセラピスト
- `therapist_smile`: 微笑むセラピスト
- `therapist_gentle`: 優しい表情のセラピスト

## 使用方法

### 1. ノベルゲームエンジンでの読み込み

このシナリオファイルは、以下のようなノベルゲームエンジンで使用できます：

- Ren'Py（変換が必要）
- TyranoScript（変換が必要）
- カスタムHTML5ノベルゲームエンジン
- 独自開発のゲームエンジン

### 2. シナリオの実装例

```javascript
// JavaScriptでの実装例
const scenario = require('./scenario.json');
let currentNode = scenario.nodes[scenario.startNode];

function displayNode(node) {
  // テキストを表示
  console.log(`${node.speaker}: ${node.text}`);
  
  // 背景を設定
  setBackground(node.background);
  
  // キャラクターを表示
  if (node.character) {
    showCharacter(node.character);
  }
  
  // ノードタイプに応じた処理
  if (node.type === 'choice') {
    // 選択肢を表示
    showChoices(node.choices);
  } else {
    // 自動進行
    setTimeout(() => {
      currentNode = scenario.nodes[node.next];
      displayNode(currentNode);
    }, 2000);
  }
}

function onChoiceSelected(choice) {
  // フラグを保存
  saveFlag(choice.flag);
  
  // 次のノードへ
  currentNode = scenario.nodes[choice.next];
  displayNode(currentNode);
}
```

### 3. Webブラウザでの簡易再生

HTMLとJavaScriptを使用して、簡易的なノベルゲームとして再生できます。

```html
<!DOCTYPE html>
<html>
<head>
  <title>目覚めの部屋</title>
  <style>
    body { font-family: sans-serif; max-width: 800px; margin: 50px auto; }
    #text-box { padding: 20px; border: 1px solid #ccc; min-height: 150px; }
    .choice-button { display: block; margin: 10px 0; padding: 10px; }
  </style>
</head>
<body>
  <div id="text-box"></div>
  <div id="choices"></div>
  <script src="novel-engine.js"></script>
</body>
</html>
```

## プレイ時間

推定プレイ時間：10〜15分

## テーマ

- セルフセラピー
- 自己理解
- 深層心理
- 記憶と感情
- ポジティブな気づき

## ライセンス

このシナリオは自由に使用・改変できます。
商用・非商用問わず、ご自由にお使いください。

## 作者

Novel Tree Project

## バージョン

1.0.0

## 更新履歴

- 2025-11-21: 初版リリース
  - 基本シナリオの作成
  - 4つの選択ポイント
  - 4種類のエンディング
  - 256通りの体験パターン

## お問い合わせ

バグ報告や改善提案は、GitHubのIssueでお願いします。

---

**注意**: このシナリオは娯楽目的で作成されています。実際の心理療法やカウンセリングの代替にはなりません。深刻な心理的問題を抱えている場合は、専門家にご相談ください。
