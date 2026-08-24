"use client";

import { useState } from "react";
import {
  ArrowDown,
  Sparkles,
} from "lucide-react";

import Navbar from "../components/Navbar";
import ImageUploader from "../components/ImageUploader";
import AnalysisPanel from "../components/AnalysisPanel";
import ProductGrid from "../components/ProductGrid";
import ChatBox from "../components/ChatBox";

import {
  analyzeClothing,
  AnalyzeResponse,
} from "../lib/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] =
    useState<AnalyzeResponse | null>(null);

  const [error, setError] = useState("");

  async function handleFile(file: File) {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeClothing(file);
      setResult(data);

      setTimeout(() => {
        document
          .getElementById("results")
          ?.scrollIntoView({
            behavior: "smooth",
          });
      }, 100);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#080808]">

      <Navbar />

      {/* HERO */}

      <section className="mx-auto max-w-7xl px-4 pb-16 pt-16 sm:px-6 sm:pb-24 sm:pt-24">

        <div className="mx-auto max-w-3xl text-center">

          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs text-white/60">
            <Sparkles size={13} />
            AI-powered fashion discovery
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
            Find the drip.
            <br />

            <span className="text-white/35">
              We find the match.
            </span>
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-sm leading-6 text-white/45 sm:text-base">
            Upload a clothing piece you love and
            DripSearch AI will find similar products
            available in India.
          </p>
        </div>

        {/* UPLOADER */}

        <div className="mx-auto mt-12 max-w-2xl">
          <ImageUploader
            onFileSelect={handleFile}
            loading={loading}
          />

          {error && (
            <div className="mt-4 rounded-2xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">
              {error}
            </div>
          )}
        </div>

        {!result && !loading && (
          <div className="mt-8 flex justify-center">
            <div className="flex items-center gap-2 text-xs text-white/25">
              <ArrowDown size={14} />
              Upload an image to get started
            </div>
          </div>
        )}
      </section>

      {/* RESULTS */}

      {result && (
        <section
          id="results"
          className="border-t border-white/10"
        >
          <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 sm:py-16">

            <AnalysisPanel
              analysis={result.analysis}
            />

            <div className="mt-12">

              <div className="mb-6 flex items-end justify-between">

                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-white/30">
                    AI Matches
                  </p>

                  <h2 className="mt-1 text-2xl font-bold sm:text-3xl">
                    Pieces you might love
                  </h2>
                </div>

                <span className="text-xs text-white/30">
                  {result.products.length} results
                </span>
              </div>

              <ProductGrid
                products={result.products}
              />
            </div>

            {/* CHAT */}

            <div className="mx-auto mt-16 max-w-2xl">
              <ChatBox />
            </div>

          </div>
        </section>
      )}

      {/* FOOTER */}

      <footer className="border-t border-white/10 px-4 py-8 text-center text-xs text-white/25">
        DripSearch AI · Find your style
      </footer>
    </main>
  );
}