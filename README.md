# dart-portal

ダーツプロ・イベント・店舗・ギアを横断して探せる FastAPI ベースの MVP です。
イベント収集スクリプト、一覧・詳細 API、推しプロに合わせたおすすめ生成をまとめています。

## 主な機能

- プロ一覧・詳細
- イベント一覧・詳細
- 店舗一覧・詳細
- ギア一覧・詳細
- 推しプロ × イベント × ギアのおすすめ生成
- 予算ベースのオファー生成
- 神戸六甲ボウルのイベントスクレイピング

## セットアップ

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

## イベント情報の更新

```powershell
.\.venv\Scripts\python.exe scrape_events.py
```

神戸六甲ボウルの来店イベントを取得し、`events.json` に保存します。

## API 起動

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8765
```

- Swagger UI: http://127.0.0.1:8765/docs
- ヘルスチェック: `GET /health`
- おすすめ生成: `POST /recommendations`
- オファー生成: `POST /offers`

### リクエスト例

```json
{
  "area": "Hyogo",
  "favorite_pro_ids": [101],
  "budget": 20000
}
```

## 検証

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

## 設計書

全体設計・API・CMS・ロードマップは [docs/DESIGN.md](docs/DESIGN.md) を参照してください。
