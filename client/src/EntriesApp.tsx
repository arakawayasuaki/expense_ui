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
        const response = await fetch(`${ENTRIES_ENDPOINT}/entries`);
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
  }, [processor]);

  return (
    <div className="app">
      <header className="header">
        <h1>経費エントリー一覧</h1>
        <p>JSONファイルのテストデータを表示します。</p>
      </header>

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
