declare module "tesseract.js" {
  const Tesseract: {
    recognize: (
      image: HTMLCanvasElement,
      lang: string,
      options?: {
        logger?: (message: unknown) => void;
        tessedit_pageseg_mode?: string;
      }
    ) => Promise<{
      data: { text?: string };
    }>;
  };
  export default Tesseract;
}

declare module "pdfjs-dist/legacy/build/pdf" {
  export const getDocument: (options: { data: ArrayBuffer }) => {
    promise: Promise<{
      getPage: (pageNumber: number) => Promise<{
        getViewport: (options: { scale: number }) => {
          width: number;
          height: number;
        };
        render: (options: {
          canvasContext: CanvasRenderingContext2D;
          viewport: { width: number; height: number };
        }) => { promise: Promise<void> };
      }>;
    }>;
  };
  export const GlobalWorkerOptions: { workerSrc: string };
}
