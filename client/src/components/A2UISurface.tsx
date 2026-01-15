import { useEffect, useRef } from "react";
import { v0_8 } from "@a2ui/lit";

type A2UISurfaceProps = {
  surfaceId: string;
  surface: v0_8.Types.Surface;
  processor: unknown;
  onAction: (event: CustomEvent) => void;
};

export function A2UISurface({
  surfaceId,
  surface,
  processor,
  onAction,
}: A2UISurfaceProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const elementRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!containerRef.current || elementRef.current) return;
    const element = document.createElement("a2ui-surface");
    (element as any).surfaceId = surfaceId;
    (element as any).surface = surface;
    (element as any).processor = processor;
    elementRef.current = element;
    containerRef.current.appendChild(element);
    const handler = (event: Event) => {
      onAction(event as CustomEvent);
    };
    element.addEventListener("a2uiaction", handler);
    return () => {
      element.removeEventListener("a2uiaction", handler);
      element.remove();
      elementRef.current = null;
    };
  }, [onAction, surfaceId, surface, processor]);

  useEffect(() => {
    if (!elementRef.current) return;
    (elementRef.current as any).surfaceId = surfaceId;
    (elementRef.current as any).surface = surface;
    (elementRef.current as any).processor = processor;
  }, [surfaceId, surface, processor]);

  return <div ref={containerRef} />;
}
