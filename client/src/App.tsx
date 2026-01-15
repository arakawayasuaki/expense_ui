import { useCallback, useMemo, useState } from "react";
import { v0_8 } from "@a2ui/lit";
import { A2UISurface } from "./components/A2UISurface";

type ExpenseFormData = {
  receiptName: string;
  merchant: string;
  date: string;
  amount: string;
  currency: string;
  category: string;
  paymentMethod: string;
  memo: string;
};

type ExpenseRecord = ExpenseFormData & {
  id: string;
  createdAt: string;
};

type OcrResponse = {
  text: string;
  merchant: string;
  date: string;
  amount: string;
  currency: string;
};

const STORAGE_KEY = "expenseClaims";
const OCR_ENDPOINT =
  import.meta.env.VITE_OCR_ENDPOINT ?? "http://localhost:10002";

const loadClaims = (): ExpenseRecord[] => {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw) as ExpenseRecord[];
  } catch {
    return [];
  }
};

const saveClaims = (claims: ExpenseRecord[]) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(claims));
};

const addClaim = (payload: ExpenseFormData) => {
  const claims = loadClaims();
  const record: ExpenseRecord = {
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
    ...payload,
  };
  claims.push(record);
  saveClaims(claims);
  return record;
};

const searchClaims = (query: string) => {
  const claims = loadClaims();
  if (!query) return claims;
  const lower = query.toLowerCase();
  return claims.filter((claim) =>
    [
      claim.receiptName,
      claim.merchant,
      claim.date,
      claim.amount,
      claim.currency,
      claim.category,
      claim.paymentMethod,
      claim.memo,
    ]
      .join(" ")
      .toLowerCase()
      .includes(lower)
  );
};

const fileToBase64 = (file: File) =>
  new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result !== "string") {
        reject(new Error("Failed to read receipt"));
        return;
      }
      resolve(reader.result);
    };
    reader.onerror = () => reject(new Error("Failed to read receipt"));
    reader.readAsDataURL(file);
  });

const runOcr = async (file: File): Promise<OcrResponse> => {
  const fileBase64 = await fileToBase64(file);
  const response = await fetch(`${OCR_ENDPOINT}/ocr`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      fileBase64,
      fileName: file.name,
      fileType: file.type || "application/octet-stream",
    }),
  });

  if (!response.ok) {
    const message = await response.text().catch(() => "");
    throw new Error(message || "OCR request failed");
  }

  return (await response.json()) as OcrResponse;
};

const buildExpenseForm = (data: ExpenseFormData) => [
  {
    beginRendering: {
      surfaceId: "expense-form",
      root: "expense-root",
      styles: { primaryColor: "#2F5AFF", font: "Roboto" },
    },
  },
  {
    surfaceUpdate: {
      surfaceId: "expense-form",
      components: [
        {
          id: "expense-root",
          component: {
            Column: {
              children: {
                explicitList: [
                  "form-title",
                  "receipt-name",
                  "merchant-field",
                  "date-field",
                  "amount-field",
                  "currency-field",
                  "category-field",
                  "payment-field",
                  "memo-field",
                  "submit-button",
                ],
              },
            },
          },
        },
        {
          id: "form-title",
          component: {
            Text: {
              usageHint: "h2",
              text: { literalString: "経費申請フォーム" },
            },
          },
        },
        {
          id: "receipt-name",
          component: { Text: { text: { path: "receiptName" } } },
        },
        {
          id: "merchant-field",
          component: {
            TextField: {
              label: { literalString: "支払先" },
              text: { path: "merchant" },
              textFieldType: "shortText",
            },
          },
        },
        {
          id: "date-field",
          component: {
            TextField: {
              label: { literalString: "日付" },
              text: { path: "date" },
              textFieldType: "date",
            },
          },
        },
        {
          id: "amount-field",
          component: {
            TextField: {
              label: { literalString: "金額" },
              text: { path: "amount" },
              textFieldType: "number",
            },
          },
        },
        {
          id: "currency-field",
          component: {
            TextField: {
              label: { literalString: "通貨" },
              text: { path: "currency" },
              textFieldType: "shortText",
            },
          },
        },
        {
          id: "category-field",
          component: {
            TextField: {
              label: { literalString: "カテゴリ" },
              text: { path: "category" },
              textFieldType: "shortText",
            },
          },
        },
        {
          id: "payment-field",
          component: {
            TextField: {
              label: { literalString: "支払方法" },
              text: { path: "paymentMethod" },
              textFieldType: "shortText",
            },
          },
        },
        {
          id: "memo-field",
          component: {
            TextField: {
              label: { literalString: "備考" },
              text: { path: "memo" },
              textFieldType: "longText",
            },
          },
        },
        {
          id: "submit-button",
          component: {
            Button: {
              child: "submit-button-text",
              primary: true,
              action: {
                name: "submit_expense",
                context: [
                  { key: "receiptName", value: { path: "receiptName" } },
                  { key: "merchant", value: { path: "merchant" } },
                  { key: "date", value: { path: "date" } },
                  { key: "amount", value: { path: "amount" } },
                  { key: "currency", value: { path: "currency" } },
                  { key: "category", value: { path: "category" } },
                  { key: "paymentMethod", value: { path: "paymentMethod" } },
                  { key: "memo", value: { path: "memo" } },
                ],
              },
            },
          },
        },
        {
          id: "submit-button-text",
          component: { Text: { text: { literalString: "申請する" } } },
        },
      ],
    },
  },
  {
    dataModelUpdate: {
      surfaceId: "expense-form",
      path: "/",
      contents: [
        { key: "receiptName", valueString: data.receiptName },
        { key: "merchant", valueString: data.merchant },
        { key: "date", valueString: data.date },
        { key: "amount", valueString: data.amount },
        { key: "currency", valueString: data.currency },
        { key: "category", valueString: data.category },
        { key: "paymentMethod", valueString: data.paymentMethod },
        { key: "memo", valueString: data.memo },
      ],
    },
  },
];

const buildConfirmation = (record: ExpenseRecord) => [
  {
    beginRendering: {
      surfaceId: "expense-confirm",
      root: "confirm-card",
      styles: { primaryColor: "#2F5AFF", font: "Roboto" },
    },
  },
  {
    surfaceUpdate: {
      surfaceId: "expense-confirm",
      components: [
        {
          id: "confirm-card",
          component: { Card: { child: "confirm-column" } },
        },
        {
          id: "confirm-column",
          component: {
            Column: {
              children: {
                explicitList: [
                  "confirm-title",
                  "confirm-receipt",
                  "confirm-merchant",
                  "confirm-date",
                  "confirm-amount",
                  "confirm-category",
                  "confirm-payment",
                  "confirm-memo",
                  "confirm-back",
                ],
              },
            },
          },
        },
        {
          id: "confirm-title",
          component: {
            Text: {
              usageHint: "h2",
              text: { literalString: "申請が完了しました" },
            },
          },
        },
        {
          id: "confirm-receipt",
          component: { Text: { text: { path: "receiptName" } } },
        },
        {
          id: "confirm-merchant",
          component: { Text: { text: { path: "merchant" } } },
        },
        { id: "confirm-date", component: { Text: { text: { path: "date" } } } },
        {
          id: "confirm-amount",
          component: { Text: { text: { path: "amountDisplay" } } },
        },
        {
          id: "confirm-category",
          component: { Text: { text: { path: "category" } } },
        },
        {
          id: "confirm-payment",
          component: { Text: { text: { path: "paymentMethod" } } },
        },
        { id: "confirm-memo", component: { Text: { text: { path: "memo" } } } },
        {
          id: "confirm-back",
          component: {
            Button: {
              child: "confirm-back-text",
              action: { name: "back_to_top" },
            },
          },
        },
        {
          id: "confirm-back-text",
          component: { Text: { text: { literalString: "TOPに戻る" } } },
        },
      ],
    },
  },
  {
    dataModelUpdate: {
      surfaceId: "expense-confirm",
      path: "/",
      contents: [
        { key: "receiptName", valueString: record.receiptName },
        { key: "merchant", valueString: record.merchant },
        { key: "date", valueString: record.date },
        {
          key: "amountDisplay",
          valueString: `${record.amount} ${record.currency}`,
        },
        { key: "category", valueString: record.category },
        { key: "paymentMethod", valueString: record.paymentMethod },
        { key: "memo", valueString: record.memo },
      ],
    },
  },
];

const buildSearchResults = (results: ExpenseRecord[]) => {
  const items = results.map((claim, idx) => ({
    key: `item${idx + 1}`,
    valueMap: [
      { key: "merchant", valueString: claim.merchant },
      { key: "date", valueString: claim.date },
      {
        key: "amountDisplay",
        valueString: `${claim.amount} ${claim.currency}`,
      },
      { key: "category", valueString: claim.category },
      { key: "memo", valueString: claim.memo },
      { key: "receiptName", valueString: claim.receiptName },
    ],
  }));

  return [
    {
      beginRendering: {
        surfaceId: "expense-search",
        root: "results-root",
        styles: { primaryColor: "#2F5AFF", font: "Roboto" },
      },
    },
    {
      surfaceUpdate: {
        surfaceId: "expense-search",
        components: [
          {
            id: "results-root",
            component: {
              Column: {
                children: { explicitList: ["results-title", "results-list"] },
              },
            },
          },
          {
            id: "results-title",
            component: {
              Text: { usageHint: "h2", text: { literalString: "検索結果" } },
            },
          },
          {
            id: "results-list",
            component: {
              List: {
                direction: "vertical",
                children: {
                  template: {
                    dataBinding: "/items",
                    componentId: "result-card-template",
                  },
                },
              },
            },
          },
          {
            id: "result-card-template",
            component: { Card: { child: "result-card-column" } },
          },
          {
            id: "result-card-column",
            component: {
              Column: {
                children: {
                  explicitList: [
                    "result-merchant",
                    "result-date",
                    "result-amount",
                    "result-category",
                    "result-memo",
                    "result-receipt",
                  ],
                },
              },
            },
          },
          {
            id: "result-merchant",
            component: { Text: { text: { path: "merchant" } } },
          },
          {
            id: "result-date",
            component: { Text: { text: { path: "date" } } },
          },
          {
            id: "result-amount",
            component: { Text: { text: { path: "amountDisplay" } } },
          },
          {
            id: "result-category",
            component: { Text: { text: { path: "category" } } },
          },
          {
            id: "result-memo",
            component: { Text: { text: { path: "memo" } } },
          },
          {
            id: "result-receipt",
            component: { Text: { text: { path: "receiptName" } } },
          },
        ],
      },
    },
    {
      dataModelUpdate: {
        surfaceId: "expense-search",
        path: "/",
        contents: [{ key: "items", valueMap: items }],
      },
    },
  ];
};

export default function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [surfaces, setSurfaces] = useState<Array<[string, v0_8.Types.Surface]>>(
    []
  );
  const [searchQuery, setSearchQuery] = useState("");

  const processor = useMemo(
    () => v0_8.Data.createSignalA2uiMessageProcessor(),
    []
  );

  const processMessages = useCallback(
    (messages: v0_8.Types.ServerToClientMessage[]) => {
      processor.clearSurfaces();
      processor.processMessages(messages);
      setSurfaces(Array.from(processor.getSurfaces()));
    },
    [processor]
  );

  const handleUpload = useCallback(
    async (file: File) => {
      setLoading(true);
      setError(null);
      processor.clearSurfaces();
      setSurfaces([]);
      try {
        const ocr = await runOcr(file);
        const formData: ExpenseFormData = {
          receiptName: file.name,
          merchant: ocr.merchant,
          date: ocr.date,
          amount: ocr.amount,
          currency: ocr.currency,
          category: "",
          paymentMethod: "",
          memo: "",
        };
        processMessages(buildExpenseForm(formData));
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    },
    [processMessages]
  );

  const handleSearch = useCallback(
    async (query: string) => {
      const results = searchClaims(query);
      processMessages(buildSearchResults(results));
    },
    [processMessages]
  );

  const handleA2uiAction = useCallback(
    async (surfaceId: string, event: CustomEvent) => {
      const detail = event.detail;
      if (!detail?.action) return;

      if (detail.action.name === "back_to_top") {
        processor.clearSurfaces();
        setSurfaces([]);
        return;
      }

      const context: Record<string, unknown> = {};
      if (detail.action.context) {
        for (const item of detail.action.context) {
          if (item.value?.literalBoolean !== undefined) {
            context[item.key] = item.value.literalBoolean;
          } else if (item.value?.literalNumber !== undefined) {
            context[item.key] = item.value.literalNumber;
          } else if (item.value?.literalString !== undefined) {
            context[item.key] = item.value.literalString;
          } else if (item.value?.path) {
            const path = processor.resolvePath(
              item.value.path,
              detail.dataContextPath
            );
            const value = processor.getData(
              detail.sourceComponent,
              path,
              surfaceId
            );
            context[item.key] = value;
          }
        }
      }

      if (detail.action.name === "submit_expense") {
        const payload: ExpenseFormData = {
          receiptName: String(context.receiptName ?? ""),
          merchant: String(context.merchant ?? ""),
          date: String(context.date ?? ""),
          amount: String(context.amount ?? ""),
          currency: String(context.currency ?? "JPY"),
          category: String(context.category ?? ""),
          paymentMethod: String(context.paymentMethod ?? ""),
          memo: String(context.memo ?? ""),
        };
        const record = addClaim(payload);
        processMessages(buildConfirmation(record));
      }
    },
    [processor, processMessages]
  );

  return (
    <div className="app">
      <header className="header">
        <h1>経費申請（A2UI + OCR）</h1>
        <p>領収書をアップロードするとOCRで自動入力します。</p>
      </header>

      <section className="panel">
        <h2>領収書アップロード</h2>
        <input
          type="file"
          accept="image/*,application/pdf"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) {
              void handleUpload(file);
            }
          }}
          disabled={loading}
        />
      </section>

      <section className="panel">
        <h2>過去申請の検索</h2>
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void handleSearch(searchQuery);
          }}
        >
          <input
            type="text"
            placeholder="支払先・日付・金額など"
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            検索
          </button>
        </form>
      </section>

      {error && <div className="error">{error}</div>}
      {loading && <div className="loading">処理中...</div>}

      <section className="a2ui">
        <a2ui-theme-provider>
          {surfaces.map(([surfaceId, surface]) => (
            <A2UISurface
              key={surfaceId}
              surfaceId={surfaceId}
              surface={surface}
              processor={processor}
              onAction={(event) => handleA2uiAction(surfaceId, event)}
            />
          ))}
        </a2ui-theme-provider>
      </section>
    </div>
  );
}
