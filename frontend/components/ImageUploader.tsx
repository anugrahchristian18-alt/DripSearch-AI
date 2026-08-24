"use client";

import { ImagePlus, Upload, X } from "lucide-react";
import { useRef, useState } from "react";

interface Props {
  onFileSelect: (file: File) => void;
  loading: boolean;
}

export default function ImageUploader({
  onFileSelect,
  loading,
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);

  function handleFile(file?: File) {
    if (!file) return;

    if (!file.type.startsWith("image/")) return;

    setPreview(URL.createObjectURL(file));
    onFileSelect(file);
  }

  function removeImage() {
    setPreview(null);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  }

  return (
    <div className="w-full">

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={(e) =>
          handleFile(e.target.files?.[0])
        }
      />

      {!preview ? (
        <button
          type="button"
          disabled={loading}
          onClick={() => inputRef.current?.click()}
          className="group flex min-h-[300px] w-full flex-col items-center justify-center rounded-3xl border border-dashed border-white/20 bg-white/[0.03] px-6 transition hover:border-white/40 hover:bg-white/[0.05] sm:min-h-[360px]"
        >
          <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-white text-black transition group-hover:scale-105">
            <ImagePlus size={28} />
          </div>

          <h3 className="text-lg font-semibold">
            Upload your outfit
          </h3>

          <p className="mt-2 max-w-xs text-center text-sm text-white/40">
            Drop an image here or tap to choose from your device
          </p>

          <div className="mt-6 flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-xs text-white/50">
            <Upload size={14} />
            JPG, PNG, WEBP
          </div>
        </button>
      ) : (
        <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">
          <img
            src={preview}
            alt="Uploaded clothing"
            className="h-[360px] w-full object-contain sm:h-[460px]"
          />

          {!loading && (
            <button
              onClick={removeImage}
              className="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full bg-black/70 text-white backdrop-blur transition hover:bg-black"
            >
              <X size={18} />
            </button>
          )}

          {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm">
              <div className="text-center">
                <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-white/20 border-t-white" />

                <p className="mt-4 text-sm text-white/70">
                  AI is analyzing your drip...
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}