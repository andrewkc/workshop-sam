import { useEffect, useRef, useState } from "react";
import { Product, TryOn, createTryOn } from "../api";

type Point = { x: number; y: number };
export default function TryOnCamera({
  product,
  onClose,
}: {
  product: Product;
  onClose(): void;
}) {
  const video = useRef<HTMLVideoElement>(null),
    pointers = useRef(new Map<number, Point>()),
    start = useRef<{
      distance: number;
      scale: number;
      angle: number;
      rotation: number;
    } | null>(null);
  const [data, setData] = useState<TryOn | null>(null),
    [error, setError] = useState(""),
    [position, setPosition] = useState({ x: 50, y: 55 }),
    [scale, setScale] = useState(1),
    [rotation, setRotation] = useState(0),
    [shadow, setShadow] = useState(true);
  useEffect(() => {
    let stream: MediaStream | undefined;
    createTryOn(product.id)
      .then(setData)
      .catch((e: Error) => setError(e.message));
    navigator.mediaDevices
      ?.getUserMedia({
        video: { facingMode: { ideal: "environment" } },
        audio: false,
      })
      .then((s) => {
        stream = s;
        if (video.current) video.current.srcObject = s;
      })
      .catch(() =>
        setError(
          "No pudimos acceder a la cámara. Revisa los permisos e inténtalo de nuevo.",
        ),
      );
    return () => stream?.getTracks().forEach((track) => track.stop());
  }, [product.id]);
  const points = () => [...pointers.current.values()];
  const dist = ([a, b]: Point[]) => Math.hypot(a.x - b.x, a.y - b.y);
  const angle = ([a, b]: Point[]) =>
    (Math.atan2(b.y - a.y, b.x - a.x) * 180) / Math.PI;
  function pointerDown(event: React.PointerEvent) {
    (event.currentTarget as HTMLElement).setPointerCapture(event.pointerId);
    pointers.current.set(event.pointerId, {
      x: event.clientX,
      y: event.clientY,
    });
    if (pointers.current.size === 2)
      start.current = {
        distance: dist(points()),
        scale,
        angle: angle(points()),
        rotation,
      };
  }
  function pointerMove(event: React.PointerEvent) {
    const previous = pointers.current.get(event.pointerId);
    if (!previous) return;
    const next = { x: event.clientX, y: event.clientY };
    pointers.current.set(event.pointerId, next);
    if (pointers.current.size === 1)
      setPosition((p) => ({
        x: Math.max(
          8,
          Math.min(92, p.x + ((next.x - previous.x) / window.innerWidth) * 100),
        ),
        y: Math.max(
          10,
          Math.min(
            90,
            p.y + ((next.y - previous.y) / window.innerHeight) * 100,
          ),
        ),
      }));
    else if (start.current) {
      const current = points();
      setScale(
        Math.max(
          0.35,
          Math.min(
            2.8,
            (start.current.scale * dist(current)) / start.current.distance,
          ),
        ),
      );
      setRotation(
        start.current.rotation + angle(current) - start.current.angle,
      );
    }
  }
  function pointerUp(event: React.PointerEvent) {
    pointers.current.delete(event.pointerId);
    start.current = null;
  }
  const reset = () => {
    setPosition({ x: 50, y: 55 });
    setScale(1);
    setRotation(0);
  };
  return (
    <main className="camera-page">
      <video ref={video} autoPlay playsInline muted />
      <div className="camera-head">
        <button onClick={onClose}>×</button>
        <div>
          <b>{product.name}</b>
          <span>
            {data ? "Arrastra, escala o rota" : "Preparando recorte…"}
          </span>
        </div>
        <label>
          <input
            type="checkbox"
            checked={shadow}
            onChange={(e) => setShadow(e.target.checked)}
          />{" "}
          sombra
        </label>
      </div>
      {data && (
        <div
          className="object-layer"
          style={{
            left: `${position.x}%`,
            top: `${position.y}%`,
            transform: `translate(-50%,-50%) scale(${scale}) rotate(${rotation}deg)`,
          }}
          onPointerDown={pointerDown}
          onPointerMove={pointerMove}
          onPointerUp={pointerUp}
          onPointerCancel={pointerUp}
        >
          {shadow && <i className="shadow" />}
          <img
            src={`data:image/png;base64,${data.imageBase64}`}
            alt={`Vista previa de ${product.name}`}
          />
        </div>
      )}
      <div className="controls">
        <button
          onClick={() => setScale((s) => Math.min(2.8, s + 0.15))}
          aria-label="Aumentar tamaño"
        >
          ＋
        </button>
        <button
          onClick={() => setScale((s) => Math.max(0.35, s - 0.15))}
          aria-label="Reducir tamaño"
        >
          −
        </button>
        <button onClick={reset}>Centrar</button>
      </div>
      {error && <p className="camera-error">{error}</p>}
    </main>
  );
}
