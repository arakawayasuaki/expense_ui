import { v0_8 } from "@a2ui/lit";

/** Elements */

const a = {
  "typography-f-sf": true,
  "typography-fs-n": true,
  "typography-w-500": true,
  "layout-as-n": true,
  "layout-dis-iflx": true,
  "layout-al-c": true,
  "typography-td-none": true,
  "color-c-p40": true,
};

const audio = {
  "layout-w-100": true,
};

const body = {
  "typography-f-s": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "layout-mt-0": true,
  "layout-mb-2": true,
  "typography-sz-bm": true,
  "color-c-n10": true,
};

const button = {
  "typography-f-sf": true,
  "typography-fs-n": true,
  "typography-w-500": true,
  "layout-pt-3": true,
  "layout-pb-3": true,
  "layout-pl-5": true,
  "layout-pr-5": true,
  "layout-mb-1": true,
  "border-br-16": true,
  "border-bw-0": true,
  "border-c-n70": true,
  "border-bs-s": true,
  "color-bgc-s30": true,
  "behavior-ho-80": true,
};

const heading = {
  "typography-f-sf": true,
  "typography-fs-n": true,
  "typography-w-500": true,
  "layout-mt-0": true,
  "layout-mb-2": true,
};

const iframe = {
  "behavior-sw-n": true,
};

const input = {
  "typography-f-sf": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "layout-pl-4": true,
  "layout-pr-4": true,
  "layout-pt-2": true,
  "layout-pb-2": true,
  "border-br-6": true,
  "border-bw-1": true,
  "color-bc-s70": true,
  "border-bs-s": true,
  "layout-as-n": true,
  "color-c-n10": true,
};

const p = {
  "typography-f-s": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "layout-m-0": true,
  "typography-sz-bm": true,
  "layout-as-n": true,
  "color-c-n10": true,
};

const orderedList = {
  "typography-f-s": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "layout-m-0": true,
  "typography-sz-bm": true,
  "layout-as-n": true,
  "color-c-n10": true,
};

const unorderedList = {
  "typography-f-s": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "layout-m-0": true,
  "typography-sz-bm": true,
  "layout-as-n": true,
  "color-c-n10": true,
};

const listItem = {
  "typography-f-s": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "layout-m-0": true,
  "typography-sz-bm": true,
  "layout-as-n": true,
  "color-c-n10": true,
};

const pre = {
  "typography-f-c": true,
  "typography-fs-n": true,
  "typography-w-400": true,
  "typography-sz-bm": true,
  "typography-ws-p": true,
  "layout-as-n": true,
};

const textarea = {
  ...input,
  "layout-r-none": true,
  "layout-fs-c": true,
};

const video = {
  "layout-el-cv": true,
};

const aLight = v0_8.Styles.merge(a, {});
const inputLight = v0_8.Styles.merge(input, {});
const textareaLight = v0_8.Styles.merge(textarea, {});
const buttonLight = v0_8.Styles.merge(button, {});
const bodyLight = v0_8.Styles.merge(body, {});
const pLight = v0_8.Styles.merge(p, {});
const preLight = v0_8.Styles.merge(pre, {});
const orderedListLight = v0_8.Styles.merge(orderedList, {});
const unorderedListLight = v0_8.Styles.merge(unorderedList, {});
const listItemLight = v0_8.Styles.merge(listItem, {});

export const theme: v0_8.Types.Theme = {
  additionalStyles: {
    Button: {
      "--n-35": "var(--n-100)",
      "--n-10": "var(--n-0)",
      background:
        "linear-gradient(135deg, light-dark(#818cf8, #06b6d4) 0%, light-dark(#a78bfa, #3b82f6) 100%)",
      boxShadow: "0 4px 15px rgba(102, 126, 234, 0.4)",
      padding: "12px 28px",
      textTransform: "uppercase",
    },
    Text: {
      h1: {
        color: "transparent",
        background:
          "linear-gradient(135deg, light-dark(#818cf8, #06b6d4) 0%, light-dark(#a78bfa, #3b82f6) 100%)",
        "-webkit-background-clip": "text",
        "background-clip": "text",
        "-webkit-text-fill-color": "transparent",
      },
      h2: {
        color: "transparent",
        background:
          "linear-gradient(135deg, light-dark(#818cf8, #06b6d4) 0%, light-dark(#a78bfa, #3b82f6) 100%)",
        "-webkit-background-clip": "text",
        "background-clip": "text",
        "-webkit-text-fill-color": "transparent",
      },
      h3: {
        color: "transparent",
        background:
          "linear-gradient(135deg, light-dark(#818cf8, #06b6d4) 0%, light-dark(#a78bfa, #3b82f6) 100%)",
        "-webkit-background-clip": "text",
        "background-clip": "text",
        "-webkit-text-fill-color": "transparent",
      },
      h4: {},
      h5: {},
      body: {},
      caption: {},
    },
  },
  components: {
    AudioPlayer: audio,
    Button: buttonLight,
    Card: {
      "layout-mb-2": true,
      "layout-pt-4": true,
      "layout-pb-4": true,
      "layout-pl-4": true,
      "layout-pr-4": true,
      "border-br-8": true,
      "border-bw-1": true,
      "border-bs-s": true,
      "border-c-n80": true,
      "color-bgc-n100": true,
      "layout-dis-iflx": true,
      "layout-fd-c": true,
      "layout-g-4": true,
    },
    Column: {
      "layout-dis-iflx": true,
      "layout-fd-c": true,
      "layout-g-4": true,
    },
    Row: {
      "layout-dis-iflx": true,
      "layout-g-4": true,
      "layout-al-c": true,
    },
    Divider: {
      "layout-w-100": true,
      "border-bw-1": true,
      "border-bc-n80": true,
      "border-bs-s": true,
    },
    Image: {
      all: {
        "layout-w-100": true,
        "border-br-8": true,
      },
      icon: {
        "layout-w-8": true,
        "layout-h-8": true,
      },
      avatar: {
        "layout-w-12": true,
        "layout-h-12": true,
        "border-br-100": true,
      },
      smallFeature: {
        "layout-w-20": true,
      },
      mediumFeature: {
        "layout-w-40": true,
      },
      largeFeature: {
        "layout-w-60": true,
      },
      header: {
        "layout-w-100": true,
      },
    },
    Icon: {
      "layout-w-6": true,
      "layout-h-6": true,
    },
    List: {
      "layout-w-100": true,
      "layout-g-4": true,
    },
    Modal: {
      backdrop: {
        "color-bgc-n20": true,
        "opacity-50": true,
      },
      element: {
        "layout-p-4": true,
        "border-br-8": true,
        "color-bgc-n100": true,
      },
    },
    MultipleChoice: {
      container: {
        "layout-dis-iflx": true,
        "layout-fd-c": true,
        "layout-g-3": true,
      },
      element: {
        "layout-dis-iflx": true,
        "layout-al-c": true,
        "layout-g-2": true,
      },
      label: {
        "typography-f-s": true,
        "color-c-n10": true,
      },
    },
    Slider: {
      container: {
        "layout-dis-iflx": true,
        "layout-fd-c": true,
        "layout-g-2": true,
      },
      element: {
        "layout-w-100": true,
      },
      label: {
        "typography-f-s": true,
        "color-c-n10": true,
      },
    },
    Tabs: {
      container: {
        "layout-dis-iflx": true,
        "layout-fd-c": true,
        "layout-g-3": true,
      },
      element: {
        "layout-dis-iflx": true,
        "layout-g-2": true,
      },
      controls: {
        all: {
          "layout-dis-iflx": true,
          "layout-g-2": true,
        },
        selected: {
          "color-c-p40": true,
        },
      },
    },
    Text: {
      all: pLight,
      h1: v0_8.Styles.merge(heading, { "typography-sz-2xl": true }),
      h2: v0_8.Styles.merge(heading, { "typography-sz-xl": true }),
      h3: v0_8.Styles.merge(heading, { "typography-sz-l": true }),
      h4: v0_8.Styles.merge(heading, { "typography-sz-m": true }),
      h5: v0_8.Styles.merge(heading, { "typography-sz-s": true }),
      caption: v0_8.Styles.merge(bodyLight, { "typography-sz-xs": true }),
      body: bodyLight,
    },
    TextField: {
      container: {
        "layout-dis-iflx": true,
        "layout-fd-c": true,
        "layout-g-2": true,
      },
      element: inputLight,
      label: {
        "typography-f-s": true,
        "color-c-n10": true,
      },
    },
    CheckBox: {
      container: {
        "layout-dis-iflx": true,
        "layout-al-c": true,
        "layout-g-2": true,
      },
      element: {
        "layout-w-4": true,
        "layout-h-4": true,
      },
      label: {
        "typography-f-s": true,
        "color-c-n10": true,
      },
    },
    DateTimeInput: {
      container: {
        "layout-dis-iflx": true,
        "layout-fd-c": true,
        "layout-g-2": true,
      },
      element: inputLight,
      label: {
        "typography-f-s": true,
        "color-c-n10": true,
      },
    },
    Video: video,
  },
  elements: {
    a: aLight,
    audio,
    body: bodyLight,
    button: buttonLight,
    h1: v0_8.Styles.merge(heading, { "typography-sz-2xl": true }),
    h2: v0_8.Styles.merge(heading, { "typography-sz-xl": true }),
    h3: v0_8.Styles.merge(heading, { "typography-sz-l": true }),
    h4: v0_8.Styles.merge(heading, { "typography-sz-m": true }),
    h5: v0_8.Styles.merge(heading, { "typography-sz-s": true }),
    iframe,
    input: inputLight,
    p: pLight,
    pre: preLight,
    textarea: textareaLight,
    video,
  },
  markdown: {
    p: [],
    h1: [],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    ul: [],
    ol: [],
    li: [],
    a: [],
    strong: [],
    em: [],
  },
};
