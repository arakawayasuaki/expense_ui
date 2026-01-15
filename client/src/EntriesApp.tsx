import { useEffect, useMemo, useState } from "react";
import { v0_8 } from "@a2ui/lit";
import { A2UISurface } from "./components/A2UISurface";

const ENTRIES_ENDPOINT =
  import.meta.env.VITE_OCR_ENDPOINT ?? "http://localhost:10002";

export default function EntriesApp() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [surfaces, setSurfaces] = useState<Array<[string, v0_8.Types.Surface]>>(
    []
  );
  const [layoutMode, setLayoutMode] = useState<"list" | "grid">("grid");
  const [visibleFields, setVisibleFields] = useState<string[]>([
    "title",
    "date",
    "amount",
    "currency",
    "memo",
  ]);
  const [theme, setTheme] = useState<"default" | "forest" | "sunset">(
    "default"
  );

  const processor = useMemo(
    () => v0_8.Data.createSignalA2uiMessageProcessor(),
    []
  );

  const processMessages = (messages: v0_8.Types.ServerToClientMessage[]) => {
    processor.clearSurfaces();
    processor.processMessages(messages);
    setSurfaces(Array.from(processor.getSurfaces()));
  };

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      setError(null);
      processor.clearSurfaces();
      setSurfaces([]);
      try {
        const params = new URLSearchParams();
        params.set("mode", layoutMode);
        params.set("theme", theme);
        params.set("fields", visibleFields.join(","));
        const response = await fetch(
          `${ENTRIES_ENDPOINT}/entries?${params.toString()}`
        );
        if (!response.ok) {
          throw new Error("Failed to load entries");
        }
        const messages =
          (await response.json()) as v0_8.Types.ServerToClientMessage[];
        processMessages(messages);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };
    void run();
  }, [processor, layoutMode, visibleFields, theme]);

  return (
    <div className="app">
      <header className="header">
        <h1>経費エントリー一覧</h1>
        <p>JSONファイルのテストデータを表示します。</p>
      </header>

      <section className="panel">
        <h2>表示設定</h2>
        <div className="row">
          <label>
            <input
              type="radio"
              name="layoutMode"
              value="list"
              checked={layoutMode === "list"}
              onChange={() => setLayoutMode("list")}
            />
            リスト
          </label>
          <label>
            <input
              type="radio"
              name="layoutMode"
              value="grid"
              checked={layoutMode === "grid"}
              onChange={() => setLayoutMode("grid")}
            />
            グリッド
          </label>
        </div>
        <div className="row">
          <label>
            テーマ
            <select
              value={theme}
              onChange={(event) =>
                setTheme(event.target.value as "default" | "forest" | "sunset")
              }
            >
              <option value="default">Default</option>
              <option value="forest">Forest</option>
              <option value="sunset">Sunset</option>
            </select>
          </label>
        </div>
        <div className="row">
          {[
            { id: "title", label: "タイトル" },
            { id: "date", label: "日付" },
            { id: "amount", label: "金額" },
            { id: "currency", label: "通貨" },
            { id: "memo", label: "備考" },
          ].map((field) => (
            <label key={field.id}>
              <input
                type="checkbox"
                checked={visibleFields.includes(field.id)}
                onChange={(event) => {
                  setVisibleFields((current) => {
                    if (event.target.checked) {
                      return [...current, field.id];
                    }
                    const next = current.filter((item) => item !== field.id);
                    return next.length === 0 ? ["title"] : next;
                  });
                }}
              />
              {field.label}
            </label>
          ))}
        </div>
      </section>

      {error && <div className="error">{error}</div>}
      {loading && <div className="loading">読み込み中...</div>}

      <section className="a2ui">
        <a2ui-theme-provider>
          {surfaces.map(([surfaceId, surface]) => (
            <A2UISurface
              key={surfaceId}
              surfaceId={surfaceId}
              surface={surface}
              processor={processor}
              onAction={() => {}}
            />
          ))}
        </a2ui-theme-provider>
      </section>
    </div>
  );
}
