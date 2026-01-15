# Expense UI (A2UI + OCR)

経費申請UIの独立パッケージです。OCRはクライアント内で実行し、結果をフォームに反映します。

## 構成

- `client/`: React + A2UI(Lit) クライアント
- `a2ui-renderer/`: A2UI Lit renderer (ローカル依存)
- `a2ui-extension/`: A2UI Python拡張 (エージェント用)
- `agent/`: A2A エージェント (任意)

## 開発サーバ起動

```bash
cd client
npm install
npm run dev
```

## エージェント起動 (任意)

```bash
cd agent
uv run .
```

