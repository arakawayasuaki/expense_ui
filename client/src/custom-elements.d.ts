import React from "react";

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      "a2ui-surface": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement>,
        HTMLElement
      >;
      "a2ui-theme-provider": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement>,
        HTMLElement
      >;
    }
  }
}

export {};
