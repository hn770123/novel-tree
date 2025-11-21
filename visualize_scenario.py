#!/usr/bin/env python3
"""
シナリオの分岐構造を視覚化するスクリプト

このスクリプトは、シナリオの分岐構造をテキストベースのツリー図として表示します。
"""

import json
from typing import Dict, Set

def load_scenario(filename: str) -> Dict:
    """
    シナリオファイルを読み込む
    
    Args:
        filename: JSONファイルのパス
    
    Returns:
        シナリオデータの辞書
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def visualize_tree(scenario: Dict, max_depth: int = 3):
    """
    シナリオの分岐構造をツリー図として表示する
    
    Args:
        scenario: シナリオデータ
        max_depth: 最大表示深度
    """
    nodes = scenario.get('nodes', {})
    start_node = scenario.get('startNode')
    
    visited = set()
    
    def print_node(node_id: str, depth: int = 0, prefix: str = "", is_last: bool = True):
        """ノードを再帰的に表示"""
        if depth > max_depth or node_id in visited:
            if depth > max_depth:
                print(f"{prefix}{'└── ' if is_last else '├── '}... (省略)")
            return
        
        visited.add(node_id)
        
        if node_id not in nodes:
            print(f"{prefix}{'└── ' if is_last else '├── '}❌ [{node_id}] (存在しません)")
            return
        
        node = nodes[node_id]
        node_type = node.get('type', 'unknown')
        speaker = node.get('speaker', '')
        text = node.get('text', '')[:30].replace('\n', ' ')
        
        # ノードの種類に応じたアイコン
        icon = {
            'story': '📖',
            'dialogue': '💬',
            'choice': '🔀'
        }.get(node_type, '❓')
        
        # ノード情報を表示
        node_info = f"{icon} [{node_id}] {speaker}: {text}..."
        print(f"{prefix}{'└── ' if is_last else '├── '}{node_info}")
        
        # 次のノードを処理
        next_prefix = prefix + ("    " if is_last else "│   ")
        
        if node_type in ['story', 'dialogue']:
            next_node = node.get('next')
            if next_node:
                print_node(next_node, depth + 1, next_prefix, True)
        elif node_type == 'choice':
            choices = node.get('choices', [])
            for i, choice in enumerate(choices):
                choice_text = choice.get('text', '')[:20]
                next_node = choice.get('next')
                is_last_choice = (i == len(choices) - 1)
                
                print(f"{next_prefix}{'└── ' if is_last_choice else '├── '}➤ [{choice_text}]")
                if next_node:
                    choice_prefix = next_prefix + ("    " if is_last_choice else "│   ")
                    print_node(next_node, depth + 1, choice_prefix, True)
    
    print("\n🌳 シナリオツリー構造:")
    print("=" * 80)
    if start_node:
        print_node(start_node, 0, "", True)
    else:
        print("❌ 開始ノードが見つかりません")
    
    print("\n" + "=" * 80)

def show_choice_points(scenario: Dict):
    """
    選択ポイントの一覧を表示する
    
    Args:
        scenario: シナリオデータ
    """
    nodes = scenario.get('nodes', {})
    choice_nodes = [(node_id, node) for node_id, node in nodes.items() 
                    if node.get('type') == 'choice']
    
    print("\n🔀 選択ポイント一覧:")
    print("=" * 80)
    
    for i, (node_id, node) in enumerate(choice_nodes, 1):
        speaker = node.get('speaker', '')
        text = node.get('text', '')[:50].replace('\n', ' ')
        choices = node.get('choices', [])
        
        print(f"\n【選択 {i}】{node_id}")
        print(f"   {speaker}: {text}...")
        print(f"   選択肢数: {len(choices)}")
        
        for j, choice in enumerate(choices, 1):
            choice_text = choice.get('text', '')
            next_node = choice.get('next', '')
            flag = choice.get('flag', '')
            print(f"      {j}. {choice_text}")
            print(f"         → {next_node} (フラグ: {flag})")
    
    print("\n" + "=" * 80)

def show_endings(scenario: Dict):
    """
    エンディング一覧を表示する
    
    Args:
        scenario: シナリオデータ
    """
    nodes = scenario.get('nodes', {})
    
    # エンディングノードを検索（nextがNoneのノード）
    ending_nodes = [(node_id, node) for node_id, node in nodes.items() 
                    if node.get('next') is None and node.get('type') != 'choice']
    
    print("\n🎬 エンディング一覧:")
    print("=" * 80)
    
    for i, (node_id, node) in enumerate(ending_nodes, 1):
        speaker = node.get('speaker', '')
        text = node.get('text', '')[:100].replace('\n', ' ')
        
        print(f"\n【エンディング {i}】{node_id}")
        print(f"   {speaker}: {text}...")
    
    print("\n" + "=" * 80)

def show_statistics(scenario: Dict):
    """
    詳細な統計情報を表示する
    
    Args:
        scenario: シナリオデータ
    """
    nodes = scenario.get('nodes', {})
    
    # 各種カウント
    story_count = sum(1 for node in nodes.values() if node.get('type') == 'story')
    dialogue_count = sum(1 for node in nodes.values() if node.get('type') == 'dialogue')
    choice_count = sum(1 for node in nodes.values() if node.get('type') == 'choice')
    
    total_text_length = sum(len(node.get('text', '')) for node in nodes.values())
    total_choices = sum(len(node.get('choices', [])) 
                       for node in nodes.values() if node.get('type') == 'choice')
    
    # 話者の統計
    speakers = {}
    for node in nodes.values():
        speaker = node.get('speaker', 'Unknown')
        speakers[speaker] = speakers.get(speaker, 0) + 1
    
    print("\n📊 詳細統計:")
    print("=" * 80)
    print(f"総ノード数: {len(nodes)}")
    print(f"  ├─ ストーリーノード: {story_count}")
    print(f"  ├─ 会話ノード: {dialogue_count}")
    print(f"  └─ 選択ノード: {choice_count}")
    print(f"\n総テキスト文字数: {total_text_length:,}文字")
    print(f"総選択肢数: {total_choices}")
    print(f"平均選択肢数: {total_choices / choice_count if choice_count > 0 else 0:.1f}")
    
    print("\n話者別ノード数:")
    for speaker, count in sorted(speakers.items(), key=lambda x: x[1], reverse=True):
        print(f"  {speaker}: {count}ノード")
    
    print("\n" + "=" * 80)

def main():
    """メイン処理"""
    filename = 'scenario.json'
    
    print("🎮 シナリオ構造の視覚化")
    print("=" * 80)
    
    try:
        scenario = load_scenario(filename)
        
        # 統計情報
        show_statistics(scenario)
        
        # 選択ポイント
        show_choice_points(scenario)
        
        # エンディング
        show_endings(scenario)
        
        # ツリー構造（最初の3階層のみ）
        print("\n⚠️  ツリー構造は最初の3階層のみ表示します")
        visualize_tree(scenario, max_depth=3)
        
    except FileNotFoundError:
        print(f"\n❌ ファイルが見つかりません: {filename}")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSONパースエラー: {e}")
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")

if __name__ == '__main__':
    main()
