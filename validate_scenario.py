#!/usr/bin/env python3
"""
シナリオファイルの整合性を検証するスクリプト

このスクリプトは以下をチェックします：
1. すべてのノードが存在するか
2. 参照されているノードが実際に存在するか
3. 開始ノードが存在するか
4. 到達不可能なノード（デッドノード）がないか
5. エンディングノードが正しく設定されているか
"""

import json
import sys
from typing import Set, Dict, List

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

def validate_scenario(scenario: Dict) -> tuple[bool, List[str]]:
    """
    シナリオの整合性を検証する
    
    Args:
        scenario: シナリオデータ
    
    Returns:
        (成功フラグ, エラーメッセージのリスト)
    """
    errors = []
    nodes = scenario.get('nodes', {})
    start_node = scenario.get('startNode')
    
    # 1. 開始ノードの存在確認
    if not start_node:
        errors.append("❌ 開始ノード（startNode）が定義されていません")
    elif start_node not in nodes:
        errors.append(f"❌ 開始ノード '{start_node}' が存在しません")
    
    # 2. 各ノードの検証
    all_referenced_nodes = set()
    
    for node_id, node in nodes.items():
        # ノードIDの一致確認
        if node.get('id') != node_id:
            errors.append(f"❌ ノード '{node_id}' のIDが一致しません: {node.get('id')}")
        
        # ノードタイプの確認
        node_type = node.get('type')
        if node_type not in ['story', 'dialogue', 'choice']:
            errors.append(f"❌ ノード '{node_id}' のタイプが不正です: {node_type}")
        
        # 次のノードの確認
        if node_type in ['story', 'dialogue']:
            next_node = node.get('next')
            if next_node:
                all_referenced_nodes.add(next_node)
                if next_node not in nodes:
                    errors.append(f"❌ ノード '{node_id}' が存在しないノード '{next_node}' を参照しています")
        elif node_type == 'choice':
            # 選択肢の確認
            choices = node.get('choices', [])
            if not choices:
                errors.append(f"❌ 選択ノード '{node_id}' に選択肢がありません")
            
            for i, choice in enumerate(choices):
                next_node = choice.get('next')
                if not next_node:
                    errors.append(f"❌ ノード '{node_id}' の選択肢 {i+1} に次のノードが指定されていません")
                else:
                    all_referenced_nodes.add(next_node)
                    if next_node not in nodes:
                        errors.append(f"❌ ノード '{node_id}' の選択肢 {i+1} が存在しないノード '{next_node}' を参照しています")
                
                if not choice.get('text'):
                    errors.append(f"❌ ノード '{node_id}' の選択肢 {i+1} にテキストがありません")
    
    # 3. 到達可能性の確認
    reachable_nodes = set()
    
    def mark_reachable(node_id: str):
        """ノードを到達可能としてマークし、その先も再帰的にマーク"""
        if node_id in reachable_nodes or node_id not in nodes:
            return
        
        reachable_nodes.add(node_id)
        node = nodes[node_id]
        
        if node.get('type') in ['story', 'dialogue']:
            next_node = node.get('next')
            if next_node:
                mark_reachable(next_node)
        elif node.get('type') == 'choice':
            for choice in node.get('choices', []):
                next_node = choice.get('next')
                if next_node:
                    mark_reachable(next_node)
    
    if start_node and start_node in nodes:
        mark_reachable(start_node)
    
    # 到達不可能なノードを検出
    unreachable_nodes = set(nodes.keys()) - reachable_nodes
    if unreachable_nodes:
        errors.append(f"⚠️  到達不可能なノードがあります: {', '.join(sorted(unreachable_nodes))}")
    
    # 4. エンディングノードの確認
    ending_nodes = [node_id for node_id, node in nodes.items() 
                    if node.get('next') is None and node.get('type') != 'choice']
    
    if not ending_nodes:
        errors.append("❌ エンディングノード（nextがnullのノード）が見つかりません")
    
    return len(errors) == 0, errors

def print_statistics(scenario: Dict):
    """
    シナリオの統計情報を表示する
    
    Args:
        scenario: シナリオデータ
    """
    nodes = scenario.get('nodes', {})
    
    story_nodes = sum(1 for node in nodes.values() if node.get('type') == 'story')
    dialogue_nodes = sum(1 for node in nodes.values() if node.get('type') == 'dialogue')
    choice_nodes = sum(1 for node in nodes.values() if node.get('type') == 'choice')
    
    ending_nodes = [node_id for node_id, node in nodes.items() 
                    if node.get('next') is None and node.get('type') != 'choice']
    
    total_choices = sum(len(node.get('choices', [])) 
                       for node in nodes.values() if node.get('type') == 'choice')
    
    print("\n📊 シナリオ統計:")
    print(f"   総ノード数: {len(nodes)}")
    print(f"   ├─ ストーリーノード: {story_nodes}")
    print(f"   ├─ 会話ノード: {dialogue_nodes}")
    print(f"   └─ 選択ノード: {choice_nodes}")
    print(f"   総選択肢数: {total_choices}")
    print(f"   エンディング数: {len(ending_nodes)}")
    
    metadata = scenario.get('metadata', {})
    if metadata:
        print("\n📝 メタデータ:")
        for key, value in metadata.items():
            print(f"   {key}: {value}")

def main():
    """メイン処理"""
    filename = 'scenario.json'
    
    print(f"🔍 シナリオファイルを検証中: {filename}")
    print("=" * 60)
    
    try:
        scenario = load_scenario(filename)
        is_valid, errors = validate_scenario(scenario)
        
        if is_valid:
            print("\n✅ シナリオファイルは正常です！")
            print_statistics(scenario)
            return 0
        else:
            print("\n❌ シナリオファイルにエラーが見つかりました:\n")
            for error in errors:
                print(f"   {error}")
            print_statistics(scenario)
            return 1
            
    except FileNotFoundError:
        print(f"\n❌ ファイルが見つかりません: {filename}")
        return 1
    except json.JSONDecodeError as e:
        print(f"\n❌ JSONパースエラー: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
