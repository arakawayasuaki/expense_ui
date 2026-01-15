# A2UI Expense Reporter (OCR + Local JSON)

領収書(PDF/画像)を OCR で読み取り、A2UI で申請フォームを表示して保存するサンプルです。

## 依存関係

- Python 3.10+
- Tesseract OCR
- Poppler (PDF 読み取り用)

macOS:

```bash
brew install tesseract poppler
```

## 起動

```bash
cd samples/agent/adk/expense_reporter
uv run .
```

`http://localhost:10002` で A2A サーバが起動します。
