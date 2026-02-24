# トラブルシューティング FAQ

## データベースエラー "PostgreSQL node request error"、"SQLSyntaxErrorException" または SQL 構文エラーが表示される場合

1. SQL を確認: 生成された SQL ステートメントが有効か、フィールドが一致しているか確認します。
2. バージョン同期: コードは更新されたがデータベースでエラーが表示される場合、データベーススキーマが同期されていない可能性があります。`docker compose up -d atlas` を実行するか、手動で SQL を実行してフィールドを補完してください。
3. よくあるエラー: `SQLSyntaxErrorException` は通常、コードは更新されたがデータベースが自動的に移行されていないことを示します。ログの SQL エラーを確認し、不足しているフィールドを手動で追加してください。

## データベース移行が失敗し "Validate failed: Migrations have failed validation" と表示される場合

これは Flyway バージョン管理の競合です。
- テスト環境: `docker compose down -v` でデータをクリアしてリセットします。
- 本番環境: `flyway_schema_history` テーブルを手動で修復します。

## インターフェースエラー "auth name: Authorization, auth value: None" が表示される場合

1. トークンの欠落: リクエストヘッダーに有効な Authorization トークンが含まれていません。
2. 設定エラー: Casdoor Client ID/Secret が `.env` と一致しているか確認してください。

## サードパーティツールを呼び出す際に SSL エラーが表示される場合

これは通常、コンテナ内の SSL 証明書の問題またはネットワーク環境が原因です。コンテナがパブリック HTTPS アドレスに正常にアクセスできるか確認してください。

## サービスの起動に失敗する（例: `astron-core-link returned non-zero exit status 1`）場合、どのように調査すればよいですか？

1. ポートを確認: ポートの競合が使用中である可能性があるため、関連ポートの使用状況を確認してください。
2. ログを確認: `docker logs <container_name>` を使用して詳細なエラーログを確認し、問題を特定します。

## CORS（クロスオリジン）問題を解決するには？

フロントエンドからバックエンドインターフェースを呼び出す際に CORS エラーが表示される場合、Nginx プロキシ設定またはバックエンドサービスの CORS 許可ドメイン設定を確認してください。

## 起動後に `core-tenant` または `core-aitools` サービスが再起動を繰り返し、データベースに接続できないエラーが表示される場合

1. `.env` ファイルの MySQL 設定が正しいか確認します。
2. MySQL コンテナを手動で再起動してみてください: `docker restart astron-agent-mysql`（具体的なコンテナ名は `docker ps` で確認してください）。
3. 問題が解決しない場合、`docker compose down -v` を実行してクリーンアップしてから再起動してください。

## ページへのアクセス時にエラーが表示されたり、読み込まれない場合、どのように調査すればよいですか？

1. ブラウザコンソール: `Ctrl + Shift + I`（Windows）または `Cmd + Option + I`（Mac）を押して開発者ツールを開き、Network パネルでリクエストエラー（赤い 4xx/500 エラー）がないか確認します。
2. コンテナログを確認:
- すべてのログを確認: `docker compose logs -f`
- 特定サービスのログを確認: `docker compose logs -f <サービス名>`（例: `astron-agent-console-hub`、`astron-agent-core-tenant`）。
- 特に `core-tenant`（テナントサービス）と `console-hub`（コンソールバックエンド）のログに注意してください。

## データベースの更新またはフィールドの欠落によりエラーが表示される場合、どうすればよいですか？

最新のコード（`git pull`）をプルし、`docker compose up -d atlas` を実行してデータベース移行を実行し、フィールドを更新してください。

## API でワークフローを呼び出す際に "Failed to get application" エラーが表示される場合

1. 認証情報を確認: ヘッダーに `Authorization: Bearer {API_KEY}:{API_SECRET}` が正しく渡されているか確認してください。
2. ID の一致を確認:
- 使用する `flow_id` が公開された API ID と一致しているか確認してください。
- App ID と Flow ID を区別してください。
- リクエスト URL の Host と Port が正しいか（`console-hub` またはゲートウェイポートを指しているか）確認してください。
3. パラメータの置換: サンプルコードからコピーした場合、`xxx` などのプレースホルダーを実際の値に置き換えているか確認してください。
