/**
 * ノベルゲームエンジン
 * シナリオデータを読み込み、ブラウザでインタラクティブなノベルゲームを実行する
 */

// ゲーム状態管理
class GameState {
    constructor() {
        // 現在のノードID
        this.currentNodeId = null;
        // プレイヤーが設定したフラグ（選択の記録）
        this.flags = [];
        // 訪問済みノード（履歴）
        this.visitedNodes = [];
        // オートモード
        this.autoMode = false;
        // スキップモード
        this.skipMode = false;
        // シナリオデータ
        this.scenario = null;
    }

    /**
     * フラグを追加
     */
    addFlag(flag) {
        if (flag && !this.flags.includes(flag)) {
            this.flags.push(flag);
        }
    }

    /**
     * ノードを訪問済みとしてマーク
     */
    visitNode(nodeId) {
        if (!this.visitedNodes.includes(nodeId)) {
            this.visitedNodes.push(nodeId);
        }
    }

    /**
     * ゲーム状態をJSON形式で取得
     */
    toJSON() {
        return {
            currentNodeId: this.currentNodeId,
            flags: this.flags,
            visitedNodes: this.visitedNodes,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * JSON形式からゲーム状態を復元
     */
    fromJSON(data) {
        this.currentNodeId = data.currentNodeId;
        this.flags = data.flags || [];
        this.visitedNodes = data.visitedNodes || [];
    }
}

// ゲームエンジン本体
class NovelGameEngine {
    constructor() {
        this.state = new GameState();
        this.isReady = false;
        // 画像フォーマットの設定（拡張子）
        this.imageFormat = 'JPG';
        this.initElements();
        this.loadScenario();
    }

    /**
     * DOM要素の初期化
     */
    initElements() {
        // 主要な要素
        this.elements = {
            background: document.getElementById('background'),
            character: document.getElementById('character'),
            textBox: document.getElementById('text-box'),
            speakerName: document.getElementById('speaker-name'),
            textContent: document.getElementById('text-content'),
            continueIndicator: document.getElementById('continue-indicator'),
            choiceBox: document.getElementById('choice-box'),
            titleScreen: document.getElementById('title-screen'),
            startButton: document.getElementById('start-button'),
            menuButtons: document.getElementById('menu-buttons'),
            autoButton: document.getElementById('auto-button'),
            skipButton: document.getElementById('skip-button'),
            saveButton: document.getElementById('save-button'),
            loadButton: document.getElementById('load-button'),
            titleButton: document.getElementById('title-button'),
            saveLoadScreen: document.getElementById('save-load-screen'),
            saveLoadTitle: document.getElementById('save-load-title'),
            saveSlots: document.getElementById('save-slots'),
            closeSaveLoad: document.getElementById('close-save-load')
        };

        // イベントリスナーの設定
        this.setupEventListeners();
    }

    /**
     * イベントリスナーの設定
     */
    setupEventListeners() {
        // スタートボタン
        this.elements.startButton.addEventListener('click', () => this.startGame());

        // テキストボックスクリックで次へ
        this.elements.textBox.addEventListener('click', () => this.onTextBoxClick());

        // メニューボタン
        this.elements.autoButton.addEventListener('click', () => this.toggleAuto());
        this.elements.skipButton.addEventListener('click', () => this.toggleSkip());
        this.elements.saveButton.addEventListener('click', () => this.openSaveScreen());
        this.elements.loadButton.addEventListener('click', () => this.openLoadScreen());
        this.elements.titleButton.addEventListener('click', () => this.returnToTitle());

        // セーブ/ロード画面
        this.elements.closeSaveLoad.addEventListener('click', () => this.closeSaveLoadScreen());
    }

    /**
     * シナリオデータの読み込み
     */
    async loadScenario() {
        try {
            const response = await fetch('scenario.json');
            this.state.scenario = await response.json();
            this.isReady = true;
            console.log('シナリオを読み込みました:', this.state.scenario.title);
        } catch (error) {
            console.error('シナリオの読み込みに失敗しました:', error);
            alert('シナリオファイルの読み込みに失敗しました。');
        }
    }

    /**
     * ゲーム開始
     */
    startGame() {
        if (!this.isReady) {
            alert('シナリオの読み込み中です。しばらくお待ちください。');
            return;
        }

        // タイトル画面を非表示
        this.elements.titleScreen.style.display = 'none';

        // 最初のノードから開始
        this.state.currentNodeId = this.state.scenario.startNode;
        this.displayCurrentNode();
    }

    /**
     * 現在のノードを表示
     */
    displayCurrentNode() {
        const node = this.state.scenario.nodes[this.state.currentNodeId];
        if (!node) {
            console.error('ノードが見つかりません:', this.state.currentNodeId);
            return;
        }

        // ノードを訪問済みとしてマーク
        this.state.visitNode(this.state.currentNodeId);

        // 背景を設定
        if (node.background) {
            this.setBackground(node.background);
        }

        // キャラクターを設定
        if (node.character) {
            this.setCharacter(node.character);
        } else {
            this.hideCharacter();
        }

        // ノードタイプに応じて表示
        if (node.type === 'choice') {
            this.displayChoice(node);
        } else {
            this.displayText(node);
        }
    }

    /**
     * 背景画像を設定
     */
    setBackground(backgroundId) {
        const imagePath = `${backgroundId}.${this.imageFormat}`;
        this.elements.background.style.backgroundImage = `url('${imagePath}')`;
    }

    /**
     * キャラクター画像を設定
     */
    setCharacter(characterId) {
        const imagePath = `${characterId}.${this.imageFormat}`;
        this.elements.character.style.backgroundImage = `url('${imagePath}')`;
        this.elements.character.style.opacity = '1';
    }

    /**
     * キャラクターを非表示
     */
    hideCharacter() {
        this.elements.character.style.opacity = '0';
    }

    /**
     * テキストを表示（story/dialogueタイプ）
     */
    displayText(node) {
        // 選択肢ボックスを非表示
        this.elements.choiceBox.style.display = 'none';

        // テキストボックスを表示
        this.elements.textBox.style.display = 'block';
        this.elements.speakerName.textContent = node.speaker || '';
        this.elements.textContent.textContent = node.text || '';
        this.elements.continueIndicator.style.display = 'block';

        // オートモードまたはスキップモードの場合、自動的に次へ
        if (this.state.autoMode || this.state.skipMode) {
            const delay = this.state.skipMode ? 500 : 2500;
            setTimeout(() => {
                if (node.next) {
                    this.moveToNode(node.next);
                }
            }, delay);
        }
    }

    /**
     * 選択肢を表示（choiceタイプ）
     */
    displayChoice(node) {
        // オートモードとスキップモードを解除
        this.state.autoMode = false;
        this.state.skipMode = false;
        this.updateMenuButtons();

        // テキストボックスを表示（質問文）
        this.elements.textBox.style.display = 'block';
        this.elements.speakerName.textContent = node.speaker || '';
        this.elements.textContent.textContent = node.text || '';
        this.elements.continueIndicator.style.display = 'none';

        // 選択肢ボックスを表示
        this.elements.choiceBox.style.display = 'flex';
        this.elements.choiceBox.innerHTML = '';

        // 選択肢ボタンを生成
        node.choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-button';
            button.textContent = choice.text;
            button.addEventListener('click', () => this.onChoiceSelected(choice));
            this.elements.choiceBox.appendChild(button);
        });
    }

    /**
     * 選択肢が選ばれた時の処理
     */
    onChoiceSelected(choice) {
        // フラグを設定
        if (choice.flag) {
            this.state.addFlag(choice.flag);
        }

        // 次のノードへ移動
        this.moveToNode(choice.next);
    }

    /**
     * テキストボックスがクリックされた時の処理
     */
    onTextBoxClick() {
        const node = this.state.scenario.nodes[this.state.currentNodeId];
        
        // 選択肢表示中は無視
        if (node.type === 'choice') {
            return;
        }

        // 次のノードへ移動
        if (node.next) {
            this.moveToNode(node.next);
        }
    }

    /**
     * 指定されたノードへ移動
     */
    moveToNode(nodeId) {
        this.state.currentNodeId = nodeId;
        this.displayCurrentNode();
    }

    /**
     * オートモードの切り替え
     */
    toggleAuto() {
        this.state.autoMode = !this.state.autoMode;
        if (this.state.autoMode) {
            this.state.skipMode = false;
        }
        this.updateMenuButtons();
    }

    /**
     * スキップモードの切り替え
     */
    toggleSkip() {
        this.state.skipMode = !this.state.skipMode;
        if (this.state.skipMode) {
            this.state.autoMode = false;
        }
        this.updateMenuButtons();
    }

    /**
     * メニューボタンの表示を更新
     */
    updateMenuButtons() {
        this.elements.autoButton.classList.toggle('active', this.state.autoMode);
        this.elements.skipButton.classList.toggle('active', this.state.skipMode);
    }

    /**
     * セーブ画面を開く
     */
    openSaveScreen() {
        this.elements.saveLoadTitle.textContent = 'セーブ';
        this.renderSaveSlots('save');
        this.elements.saveLoadScreen.style.display = 'flex';
    }

    /**
     * ロード画面を開く
     */
    openLoadScreen() {
        this.elements.saveLoadTitle.textContent = 'ロード';
        this.renderSaveSlots('load');
        this.elements.saveLoadScreen.style.display = 'flex';
    }

    /**
     * セーブ/ロード画面を閉じる
     */
    closeSaveLoadScreen() {
        this.elements.saveLoadScreen.style.display = 'none';
    }

    /**
     * セーブスロットを描画
     */
    renderSaveSlots(mode) {
        this.elements.saveSlots.innerHTML = '';

        for (let i = 1; i <= 5; i++) {
            const slotKey = `save_slot_${i}`;
            const saveData = localStorage.getItem(slotKey);
            
            const slot = document.createElement('div');
            slot.className = 'save-slot';
            
            if (saveData) {
                const data = JSON.parse(saveData);
                const date = new Date(data.timestamp);
                slot.innerHTML = `
                    <div class="save-slot-title">スロット ${i}</div>
                    <div class="save-slot-info">
                        ${date.toLocaleString('ja-JP')}<br>
                        進行度: ${data.visitedNodes.length}ノード
                    </div>
                `;
            } else {
                slot.classList.add('empty');
                slot.innerHTML = `
                    <div class="save-slot-title">スロット ${i}</div>
                    <div class="save-slot-info">空きスロット</div>
                `;
            }

            slot.addEventListener('click', () => {
                if (mode === 'save') {
                    this.saveGame(slotKey);
                } else {
                    this.loadGame(slotKey);
                }
            });

            this.elements.saveSlots.appendChild(slot);
        }
    }

    /**
     * ゲームをセーブ
     */
    saveGame(slotKey) {
        const saveData = this.state.toJSON();
        localStorage.setItem(slotKey, JSON.stringify(saveData));
        alert('セーブしました。');
        this.closeSaveLoadScreen();
    }

    /**
     * ゲームをロード
     */
    loadGame(slotKey) {
        const saveData = localStorage.getItem(slotKey);
        if (!saveData) {
            alert('セーブデータがありません。');
            return;
        }

        const data = JSON.parse(saveData);
        this.state.fromJSON(data);
        this.closeSaveLoadScreen();
        
        // タイトル画面を非表示
        this.elements.titleScreen.style.display = 'none';
        
        // ロードしたノードを表示
        this.displayCurrentNode();
    }

    /**
     * タイトルに戻る
     */
    returnToTitle() {
        if (confirm('タイトルに戻りますか？\n（進行状況は失われます）')) {
            // シナリオデータを保持
            const scenario = this.state.scenario;
            // ゲーム状態をリセット
            this.state = new GameState();
            this.state.scenario = scenario;
            
            // タイトル画面を表示
            this.elements.titleScreen.style.display = 'flex';
            
            // 画面をクリア
            this.elements.textBox.style.display = 'none';
            this.elements.choiceBox.style.display = 'none';
            this.hideCharacter();
        }
    }
}

// ゲームエンジンの初期化
let game;
window.addEventListener('DOMContentLoaded', () => {
    game = new NovelGameEngine();
});
