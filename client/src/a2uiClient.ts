import { Part, SendMessageSuccessResponse, Task } from "@a2a-js/sdk";
import { A2AClient } from "@a2a-js/sdk/client";
import { v0_8 } from "@a2ui/lit";

const A2UI_MIME_TYPE = "application/json+a2ui";

export class A2UIClient {
  #client: A2AClient | null = null;
  #serverUrl: string;

  constructor(serverUrl: string) {
    this.#serverUrl = serverUrl;
  }

  async #getClient() {
    if (!this.#client) {
      this.#client = await A2AClient.fromCardUrl(
        `${this.#serverUrl}/.well-known/agent-card.json`,
        {
          fetchImpl: async (url, init) => {
            const headers = new Headers(init?.headers);
            headers.set(
              "X-A2A-Extensions",
              "https://a2ui.org/a2a-extension/a2ui/v0.8"
            );
            return fetch(url, { ...init, headers });
          },
        }
      );
    }
    return this.#client;
  }

  async send(
    message: v0_8.Types.A2UIClientEventMessage | Record<string, unknown>
  ): Promise<v0_8.Types.ServerToClientMessage[]> {
    const client = await this.#getClient();
    const parts: Part[] = [
      {
        kind: "data",
        data: message as Record<string, unknown>,
        mimeType: A2UI_MIME_TYPE,
      } as Part,
    ];

    const response = await client.sendMessage({
      message: {
        messageId: crypto.randomUUID(),
        role: "user",
        parts,
        kind: "message",
      },
    });

    if ("error" in response) {
      throw new Error(response.error.message);
    }

    const result = (response as SendMessageSuccessResponse).result as Task;
    if (result.kind === "task" && result.status.message?.parts) {
      const messages: v0_8.Types.ServerToClientMessage[] = [];
      for (const part of result.status.message.parts) {
        if (part.kind === "data") {
          messages.push(part.data as v0_8.Types.ServerToClientMessage);
        }
      }
      return messages;
    }

    return [];
  }
}
