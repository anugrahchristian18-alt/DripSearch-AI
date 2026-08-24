import { Product } from "./api";

const STORAGE_KEY = "dripsearch-wishlist";

export function getWishlist(): Product[] {
  if (typeof window === "undefined") return [];

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
}

export function isWishlisted(title: string): boolean {
  return getWishlist().some((item) => item.title === title);
}

export function toggleWishlist(product: Product): boolean {
  const wishlist = getWishlist();

  const exists = wishlist.some(
    (item) => item.title === product.title
  );

  let updated: Product[];

  if (exists) {
    updated = wishlist.filter(
      (item) => item.title !== product.title
    );
  } else {
    updated = [...wishlist, product];
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));

  window.dispatchEvent(new Event("wishlist-updated"));

  return !exists;
}