"use client";

import Link from "next/link";
import { Heart, Sparkles, LogIn, LogOut, User } from "lucide-react";
import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";
import { getWishlist } from "../lib/wishlist";

export default function Navbar() {
  const [count, setCount] = useState(0);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
  const updateWishlist = async () => {
    const wishlist = await getWishlist();
    setCount(wishlist.length);
  };

  updateWishlist();

  window.addEventListener("wishlist-updated", updateWishlist);

  async function getUser() {
    const {
      data: { user },
    } = await supabase.auth.getUser();

    setUser(user);
  }

  getUser();

  const {
    data: { subscription },
  } = supabase.auth.onAuthStateChange(
    (_event, session) => {
      setUser(session?.user ?? null);
      updateWishlist();
    }
  );

  return () => {
    window.removeEventListener(
      "wishlist-updated",
      updateWishlist
    );

    subscription.unsubscribe();
  };
}, []);

  async function handleLogout() {
    await supabase.auth.signOut();
    window.location.href = "/";
  }

  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-black/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">

        {/* LOGO */}

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

        {/* RIGHT SIDE */}

        <div className="flex items-center gap-2">

          {/* WISHLIST */}

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

          {/* AUTH */}

          {user ? (
            <>
              <div className="hidden items-center gap-2 rounded-full border border-white/10 px-3 py-2 text-sm text-white/60 sm:flex">
                <User size={15} />

                <span className="max-w-32 truncate">
                  {user.email}
                </span>
              </div>

              <button
                onClick={handleLogout}
                className="flex items-center gap-2 rounded-full border border-white/10 px-3 py-2 text-sm text-white/80 transition hover:bg-white/10"
              >
                <LogOut size={16} />

                <span className="hidden sm:block">
                  Logout
                </span>
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="flex items-center gap-2 rounded-full border border-white/10 px-3 py-2 text-sm text-white/80 transition hover:bg-white/10"
              >
                <LogIn size={16} />

                <span className="hidden sm:block">
                  Login
                </span>
              </Link>

              <Link
                href="/signup"
                className="hidden rounded-full bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-white/90 sm:block"
              >
                Sign up
              </Link>
            </>
          )}

        </div>
      </div>
    </nav>
  );
}