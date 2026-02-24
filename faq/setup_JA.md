# インストールと起動 FAQ

## イメージのプル失敗（Download failed）または速度が遅い場合

これは通常、国内ネットワークから Docker Hub への接続が不安定なことが原因です。
1. ミラーソースを設定: `/etc/docker/daemon.json` で国内アクセラレーションミラー（Aliyun、NetEase、南京大学など）を設定します。
- 例: `ghcr.nju.edu.cn` は `ghcr.io` の代替として使用できます。
2. 設定を変更: `docker-compose.yaml` を編集し、イメージアドレス内の `ghcr.io/` を国内ミラーソース（`ghcr.nju.edu.cn/` など）に置き換えます。
3. ネットワークプロキシ: サーバーが外部ネットワークにアクセスできるか確認するか、Docker プロキシを設定します。

## 起動時にポートが使用中（Port occupied）と表示される場合

1. ポートを確認: デフォルトでは 8000（Casdoor）、80（Nginx）、18998（MINIO）などのポートが使用されます。
2. 設定を変更: `.env` ファイルで競合しているサービスのポートマッピングを変更します。
3. Docker の競合: 古いコンテナが実行されていないことを確認します。`docker compose down` でクリーンアップしてから再起動してください。

## デプロイ後にアクセスすると 404 または 502 Bad Gateway が表示される場合

1. ログを確認: `docker compose logs -f` を実行して `astron-agent-console-hub` または `nginx` のエラーを確認します。
2. 起動待機: サービスの起動には時間がかかります。特に初めてイメージをプルしてデータベースを初期化する際は、しばらくお待ちください。
3. 設定を確認: `.env` の `HOST_BASE_ADDRESS` が正しく設定されているか確認します（リモートデプロイの場合はパブリック IP/ドメインを使用し、localhost は避けてください）。

## Docker のインストールは必須ですか？

はい、Astron Agent プラットフォームはコンテナ化デプロイのために Docker に依存しています。

## 最新バージョンに更新する方法は？

1. コードをプル: `git pull origin main`
2. イメージを更新: `docker compose pull`
3. サービスを再起動:
```
docker compose down
docker compose up -d
```
注意: データベースフィールドの変更が含まれる場合、データベース移行を実行する必要があります。テスト環境で許可される場合、`docker compose down -v` ですべてのデータをクリアして再初期化することもできます（データがすべて削除されるため注意してください）。

## 起動時に "request returned 500 Internal Server Error" エラーが表示される場合

これは通常、環境の状態が不一致であることが原因です。以下の手順を試してください：
1. 重要なデータをバックアップします。
2. `docker compose -f docker-compose-with-auth.yaml down -v` を実行してコンテナとデータボリュームをクリーンアップします（注意: この手順でデータが削除されます）。
3. `git restore docker` を実行して docker ディレクトリ内のファイル変更を復元します。
4. 環境変数 `ASTRON_AGENT_VERSION` が安定版（`v1.0.0-rc.x` など）に設定されているか確認します。
5. `docker compose -f docker-compose-with-auth.yaml up -d` を実行してサービスを再起動します。
6. ブラウザのキャッシュをクリアするか、シークレットモードでアクセスしてください。
