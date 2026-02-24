# モデルとAI機能 FAQ

## モールドロップダウンが空で、モデルを追加できない場合

1. プラットフォーム設定: Astron Console の「モデル管理」でモデルを追加します。
2. ネットワーク接続: コンテナが外部モデル API（星火、DeepSeek、OpenAI など）にアクセスできるか確認してください。

## DeepSeek またはその他の OpenAI 互換モデルを設定するには？

1. 「モデル管理」で新規モデルを選択します。
2. インターフェースアドレス: 対応する API アドレスを入力します。
3. API キー: 対応するキーを入力します。

## ローカルモデルを追加すると IP がブラックリストに登録されているエラーが表示される場合

デフォルト設定では、プライベートネットワークセグメントへの接続が禁止されている可能性があります。
- 解決方法: データベースにアクセスし、`config_info` テーブルの `category = 'NETWORK_SEGMENT_BLACK_LIST'` のレコードを削除またはクリアします。

## デバッグに成功しているのに「消費 0 トークン」と表示される場合

OpenAI SDK 経由で呼び出す場合、一部のモデルは実際にトークン消費を返さないことがあります。以下の例では、`usage` が `null` になっています。

![](assets/p5_img1_e97eef93a5.png)
![](assets/p5_img2_58f50e49c3.png)

## ローカルサービス（ローカルデプロイの大規模モデルなど）を設定して Agent に呼び出させるには？

1. ネットワーク接続: Docker コンテナ内のサービスがホストマシンまたはローカルネットワーク内のサービスにアクセスできるようにします。
- `localhost` または `127.0.0.1` は使用しないでください。これらはコンテナ自体を指すためです。
- ホストマシンのローカル IP（`192.168.x.x` など）または Docker の特殊 DNS `host.docker.internal`（Docker バージョンとシステムによります）を使用してください。

2. ブラックリスト制限: デフォルト設定では、プライベートネットワークセグメント（`192.168.x.x` など）への接続が禁止されている可能性があります。ブロックされる場合は、データベーステーブル `config_info`（または `config_info_en`）のブラックリスト設定を変更する必要があります。

## 画像理解/OCR プラグインでエラーが表示される場合

1. `.env` で iFlytek オープンプラットフォームの `PLATFORM_APP_ID`、`PLATFORM_API_KEY`、`PLATFORM_API_SECRET` を設定します。
2. その APP ID が iFlytek オープンプラットフォームで画像認識/OCR 能力の権限を有効にしているか確認してください。

## 星火ナレッジベースリソースを取得して使用するには？

星火ナレッジベースを使用する場合、公式が星火ナレッジベースを作成し、ナレッジベースデータセットを取得するツールを提供しています：
1. iFlytek オープンプラットフォームでナレッジベースの能力を有効にします: https://console.xfyun.cn/services/aidoc
2. 星火ナレッジベースを作成し、`XINGHUO_DATASET_ID` を取得します
3. データセット ID を取得したら、データセット ID を環境変数 `XINGHUO_DATASET_ID` に更新します
4. `xinghuo_rag_tool` を使用して `XINGHUO_DATASET_ID` を取得します（ブラウザで html を開く必要があります）
```
# プロジェクトから開く
cd astron-agent/docs/
open xinghuo_rag_tool.html
# xinghuo_rag_tool をダウンロード - 方法 1
wget https://raw.githubusercontent.com/iflytek/astron-agent/refs/heads/main/docs/xinghuo_rag_tool.html
# GitHub から直接ダウンロード - 方法 2
https://github.com/iflytek/astron-agent/blob/main/docs/xinghuo_rag_tool.html
```
