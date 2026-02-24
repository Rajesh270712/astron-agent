# 機能と使用方法 FAQ

## 一文でエージェントを作成できないのはなぜですか？

プロンプトでエージェントを作成する際、「今すぐ作成」をクリックすると、iFlytek オープンプラットフォームのモデル機能を呼び出す必要があります。まず、Astron Agent を iFlytek オープンプラットフォームのアプリケーションにバインドし（デプロイドキュメントを参照）、対応するモデルのクォータを取得してください。または、「スキップ」をクリックして、サードパーティモデルを使用して会話を行います。

![](assets/p10_img1_b347613c90.png)
![](assets/p10_img2_4449fb26ec.png)

## ワークフローの作成に失敗したり、異常（Unknown column）が表示される場合

1. 原因: データベーステーブル構造のバージョンが古いことです。
2. 解決: バックエンドログを確認し、`Unknown column 'module_id'` や `type` などのエラーが表示される場合、データベースで対応する `ALTER TABLE` ステートメントを実行してフィールドを補完する必要があります（例: `alter table c_param add column module_id varchar(50) DEFAULT NULL`）。

## ナレッジベース（Knowledge Base）のよくある質問

1. ファイルのアップロード失敗:
- MinIO サービスが正常か、ポート（18998/18999 など）が開放されているか確認してください。
- Agent と RAGFlow、MinIO 間のネットワーク接続および環境変数設定を確認してください。
2. RAGFlow 同期: 現在、Agent から RAGFlow へのアップロードと同期をサポートしています。RAGFlow で直接アップロードされたファイルは、Agent 側で関連付け操作を行う必要があります。
3. Rerank モデル: 星火ナレッジベースではデフォルトで Rerank が有効になっています。

## 仮想アバターを使用するには？

Astron Agent で仮想アバター機能を使用するには、iFlytek 仮想アバター公式サイトで対応するサービスを申請し、環境変数に設定する必要があります：
1. iFlytek 仮想アバター公式サイト https://virtual-man.xfyun.cn/ を開き、アプリケーションコンソールに移動します
![](assets/p11_img1_fe633d4d47.png)
2. 左側のサイドバーの「接口服务」をクリックします
![](assets/p12_img1_57d9a2a545.png)
3. 右側の「详情」の「免费开通」をクリックします
![](assets/p12_img2_356897dc11.png)
4. 自分の情報に従ってフォームに入力し、送信します
![](assets/p12_img3_5f979ae479.png)
5. 送信成功後、自動的にページが遷移します。後から入る場合は、左側の「我的订阅」を直接クリックできます
![](assets/p13_img1_449f233261.png)
6. 「创建接口服务」をクリックします
![](assets/p13_img2_52c87bf72f.png)
7. 右上角の「创建接口服务」をクリックし、フォームに入力します
![](assets/p13_img3_330327572f.png)
8. アプリの三元情報を取得し、「发布」ボタンをクリックします
![](assets/p13_img4_c38d6df852.png)
9. アプリの三元情報を対応する .env の設定項目に入力し、docker compose サービスを起動/再起動して使用できます
![](assets/p13_img5_19834fc925.png)

⚠️特に、仮想アバターはブラウザのメディアキャプチャ API `navigator.mediaDevices` を使用するため、https または localhost などのセキュアな環境が必要です。そのような環境がない場合、Chrome ブラウザでチェックをバイパスする設定が可能です：
1. `chrome://flags/#unsafely-treat-insecure-origin-as-secure` を開きます
2. 「Insecure origins treated as secure」を検索し、この項目を見つけ、「有効にする」に設定します（設定しないと無効です）
3. 入力ボックスにアドレス（例: `http://172.29.192.11`）を入力します。複数ある場合は、英語のカンマで区切ります
4. 保存してブラウザを再起動すると、有効になります

## 変数はどのように使用しますか？

1. 参照方法: ノードの入力ボックスで `{{変数名}}` を使用して、上流ノードの出力またはグローバル変数を参照します。
2. 反復ノード: 反復ノード内で、現在の反復項目の変数（`item` など）を使用して処理します。

## 原子コンポーネントをカスタマイズするには？

現在、コードを変更し、データベースの原子ツリー情報を手動で更新する必要があります。今後のバージョンでは、より便利なカスタムコンポーネント開発方法が提供される予定です。

## カスタム MCP（Model Context Protocol）ツールをサポートしていますか？

はい、サポートしています。Web 端のワークフローノード（Agent インテリジェント決定ノードなど）で MCP ツールを追加・設定できます。

## ナレッジベース（RAG）の参照に問題があり、検索や回答ができない場合

1. 以前のバージョンの会話型 Agent はナレッジベースを参照する際にバグがある可能性があるため、最新バージョンのイメージへの更新をお勧めします。
2. ワークフローモードではナレッジベースの参照がより安定しています。

## ナレッジベース（RAG）でモデルのハルシネーションを防ぐには？

1. 検索されたナレッジベースの内容は、コンテキストとしてプロンプトに埋め込まれてモデルに送信されます。

2. プロンプトを変更することでモデルを制約できます。例えば、「検索された内容のみに基づいて回答してください。検索内容に答えがない場合は、直接『わかりません』と返信し、でっち上げないでください」と追加します。

## 公開されたアプリケーションを削除または下書きに戻すにはどうすればよいですか？

- 現在のバージョン（オープンソース版）では、インターフェース上に「下書きに戻す」ボタンが提供されていない場合があります。
- 通常、「マイエージェント」カード内で削除オプションを探す必要があります。
- 下書き/削除の入り口が見つからない場合、現在のバージョンの既知の問題（Issue）である可能性があるため、GitHub リポジトリの修正進捗に注目してください。

## HTTPS プロトコルでプロジェクトにアクセスするには？

1. 設定ファイルを変更します。図のように https 公開インターフェースを追加し、CONSOLE_DOMAIN 環境変数を変更します。
![](assets/img1.png)
![](assets/img2.png)
2. docker-compose.yaml ファイルの nginx コンテナ設定を変更し、https と casdoor のポート番号を公開し、https 証明書ファイルをマッピングします。
![](assets/img3.png)
3. docker/astronAgent/nginx/nginx.conf 設定ファイルを変更して https プロトコルに適応させます
```
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    multi_accept on;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Log format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    # Access log
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Basic configuration
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Upload size limit
    client_max_body_size 20m;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/xml+rss
        application/javascript
        application/json;

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;

        # Health check
        location /nginx-health {
            access_log off;
            return 200 "nginx is healthy\n";
            add_header Content-Type text/plain;
        }

        # Redirect all other HTTP traffic to HTTPS
        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl http2;
        server_name localhost;

        ssl_certificate     /etc/nginx/certs/localhost.pem;
        ssl_certificate_key /etc/nginx/certs/localhost-key.pem;
        ssl_protocols       TLSv1.2 TLSv1.3;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;

        # Runtime config - no cache (dynamic config file)
        location = /runtime-config.js {
            proxy_pass http://console-frontend:1881;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;

            # Disable caching for runtime config
            expires -1;
            add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
            add_header Pragma "no-cache";
        }

        # Static resource caching
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            proxy_pass http://console-frontend:1881;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;

            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # SSE (Server-Sent Events) API proxy for workflow chat completions
        location /workflow/v1/chat/completions {
            proxy_pass http://core-workflow:7880/workflow/v1/chat/completions;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;

            # SSE specific settings
            proxy_buffering off;
            proxy_cache off;
            proxy_set_header Connection '';
            proxy_http_version 1.1;
            chunked_transfer_encoding on;

            # Prevent nginx from buffering responses
            proxy_set_header X-Accel-Buffering no;

            # Timeout settings - SSE requires long-lived connections
            proxy_connect_timeout 60s;
            proxy_send_timeout 1800s;
            proxy_read_timeout 1800s;

            # Set correct headers for SSE
            add_header Cache-Control 'no-cache';
            add_header X-Accel-Buffering 'no';
        }

        # SSE (Server-Sent Events) API proxy for chat messages
        location /console-api/chat-message/ {
            proxy_pass http://console-hub:8080/chat-message/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;

            # SSE specific settings
            proxy_buffering off;
            proxy_cache off;
            proxy_set_header Connection '';
            proxy_http_version 1.1;
            chunked_transfer_encoding on;

            # Prevent nginx from buffering responses
            proxy_set_header X-Accel-Buffering no;

            # Timeout settings - SSE requires long-lived connections
            proxy_connect_timeout 60s;
            proxy_send_timeout 1800s;
            proxy_read_timeout 1800s;

            # Set correct headers for SSE
            add_header Cache-Control 'no-cache';
            add_header X-Accel-Buffering 'no';
        }

        # Backend API proxy - proxy /console-api path to console-hub
        location /console-api/ {
            proxy_pass http://console-hub:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;

            # Timeout settings
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Frontend application proxy - default proxy to console-frontend
        location / {
            proxy_pass http://console-frontend:1881;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;

            # Timeout settings
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Health check
        location /nginx-health {
            access_log off;
            return 200 "nginx is healthy\n";
            add_header Content-Type text/plain;
        }
    }

    # Casdoor HTTPS endpoint (same cert, different port)
    server {
        listen 8000 ssl http2;
        server_name localhost;

        ssl_certificate     /etc/nginx/certs/localhost.pem;
        ssl_certificate_key /etc/nginx/certs/localhost-key.pem;
        ssl_protocols       TLSv1.2 TLSv1.3;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;

        location / {
            proxy_pass http://casdoor:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
        }
    }
}
```
