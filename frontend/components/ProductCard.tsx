"use client";

import { ExternalLink, Heart, Star } from "lucide-react";
import { useEffect, useState } from "react";
import { Product } from "../lib/api";
import {
  isWishlisted,
  toggleWishlist,
} from "../lib/wishlist";

interface Props {
  product: Product;
}

export default function ProductCard({
  product,
}: Props) {
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function checkWishlist() {
      const result = await isWishlisted(product.title);
      setSaved(result);
    }

    checkWishlist();
  }, [product.title]);

  async function handleWishlist() {
    if (loading) return;

    setLoading(true);

    try {
      const result = await toggleWishlist(product);
      setSaved(result);
    } catch (error) {
      console.error("Wishlist error:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <article className="group overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] transition duration-300 hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.05]">

      <div className="relative aspect-[4/5] overflow-hidden bg-white">

        {product.image ? (
          <img
            src={product.image}
            alt={product.title}
            className="h-full w-full object-contain transition duration-500 group-hover:scale-105"
          />
        ) : (
          <div className="flex h-full items-center justify-center bg-neutral-900 text-sm text-white/30">
            No image
          </div>
        )}

        <button
          onClick={handleWishlist}
          disabled={loading}
          aria-label="Add to wishlist"
          className={`absolute right-3 top-3 flex h-10 w-10 items-center justify-center rounded-full backdrop-blur-xl transition ${
            saved
              ? "bg-white text-black"
              : "bg-black/60 text-white hover:bg-white hover:text-black"
          } ${loading ? "cursor-wait opacity-60" : ""}`}
        >
          <Heart
            size={18}
            fill={saved ? "currentColor" : "none"}
          />
        </button>

        {product.score !== undefined && (
          <div className="absolute bottom-3 left-3 rounded-full bg-black/75 px-3 py-1.5 text-xs font-medium backdrop-blur">
            {product.score} match
          </div>
        )}
      </div>

      <div className="p-4">

        <p className="text-xs text-white/40">
          {product.source}
        </p>

        <h3 className="mt-1 line-clamp-2 min-h-[40px] text-sm font-medium">
          {product.title}
        </h3>

        <div className="mt-4 flex items-center justify-between gap-3">

          <div>
            <p className="font-semibold">
              {product.price}
            </p>

            {product.rating &&
              product.rating !== "N/A" && (
                <div className="mt-1 flex items-center gap-1 text-xs text-white/50">
                  <Star
                    size={12}
                    fill="currentColor"
                  />
                  {product.rating}
                </div>
              )}
          </div>

          {product.link && (
            <a
              href={product.link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex h-9 w-9 items-center justify-center rounded-full bg-white text-black transition hover:scale-105"
            >
              <ExternalLink size={16} />
            </a>
          )}
        </div>
      </div>
    </article>
  );
}