"use client";

import { useEffect, useState } from "react";
import { Heart, ArrowLeft } from "lucide-react";
import Link from "next/link";

import Navbar from "../../components/Navbar";
import ProductCard from "../../components/ProductCard";
import { Product } from "../../lib/api";
import { getWishlist } from "../../lib/wishlist";

export default function WishlistPage() {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    setProducts(getWishlist());

    const update = () => {
      setProducts(getWishlist());
    };

    window.addEventListener("wishlist-updated", update);

    return () =>
      window.removeEventListener(
        "wishlist-updated",
        update
      );
  }, []);

  return (
    <main className="min-h-screen bg-[#080808]">

      <Navbar />

      <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 sm:py-16">

        <Link
          href="/"
          className="mb-8 inline-flex items-center gap-2 text-sm text-white/40 hover:text-white"
        >
          <ArrowLeft size={16} />
          Back to search
        </Link>

        <div className="mb-10">

          <div className="mb-3 flex items-center gap-3">
            <Heart
              size={22}
              fill="currentColor"
            />

            <p className="text-xs uppercase tracking-[0.2em] text-white/40">
              Saved pieces
            </p>
          </div>

          <h1 className="text-4xl font-bold">
            Your Wishlist
          </h1>

          <p className="mt-2 text-sm text-white/40">
            {products.length} saved{" "}
            {products.length === 1
              ? "item"
              : "items"}
          </p>
        </div>

        {products.length === 0 ? (
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] px-6 py-20 text-center">

            <Heart
              size={35}
              className="mx-auto text-white/20"
            />

            <h2 className="mt-5 text-xl font-semibold">
              Your wishlist is empty
            </h2>

            <p className="mt-2 text-sm text-white/35">
              Save pieces you love while exploring.
            </p>

            <Link
              href="/"
              className="mt-6 inline-flex rounded-full bg-white px-5 py-3 text-sm font-semibold text-black"
            >
              Find my drip
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-2 sm:gap-5 lg:grid-cols-4">
            {products.map((product, index) => (
              <ProductCard
                key={`${product.title}-${index}`}
                product={product}
              />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}