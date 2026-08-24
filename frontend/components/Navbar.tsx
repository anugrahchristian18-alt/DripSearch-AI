"use client";

import Link from "next/link";
import { Heart, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { getWishlist } from "../lib/wishlist";

export default function Navbar() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const update = () => {
      setCount(getWishlist().length);
    };

    update();

    window.addEventListener("wishlist-updated", update);

    return () =>
      window.removeEventListener("wishlist-updated", update);
  }, []);

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-black/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">

        <Link
          href="/"
          className="flex items-center gap-2"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-black">
            <Sparkles size={17} />
          </div>

          <span className="text-lg font-bold tracking-tight">
            DripSearch
            <span className="text-white/40"> AI</span>
          </span>
        </Link>

        <Link
          href="/wishlist"
          className="relative flex items-center gap-2 rounded-full border border-white/10 px-3 py-2 text-sm text-white/80 transition hover:bg-white/10"
        >
          <Heart size={17} />

          <span className="hidden sm:block">
            Wishlist
          </span>

          {count > 0 && (
            <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-white px-1 text-[11px] font-bold text-black">
              {count}
            </span>
          )}
        </Link>
      </div>
    </nav>
  );
}