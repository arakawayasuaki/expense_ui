import React from "react";
import ReactDOM from "react-dom/client";
import EntriesApp from "./EntriesApp";
import "./styles.css";
import "@a2ui/lit/ui";
import "./a2uiThemeProvider";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <EntriesApp />
  </React.StrictMode>
);
