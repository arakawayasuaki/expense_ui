import { LitElement, html } from "lit";
import { customElement, property } from "lit/decorators.js";
import { provide } from "@lit/context";
import { v0_8 } from "@a2ui/lit";
import * as UI from "@a2ui/lit/ui";
import { theme as defaultTheme } from "./theme/defaultTheme";

@customElement("a2ui-theme-provider")
export class A2UIThemeProvider extends LitElement {
  @provide({ context: UI.Context.themeContext })
  @property({ attribute: false })
  declare theme: v0_8.Types.Theme;

  constructor() {
    super();
    this.theme = defaultTheme;
  }

  protected createRenderRoot() {
    return this;
  }

  render() {
    return html`<slot></slot>`;
  }
}
