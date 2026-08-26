import { Product } from "./api";
import { supabase } from "./supabase";

export async function getWishlist(): Promise<Product[]> {
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) return [];

  const { data, error } = await supabase
    .from("wishlist")
    .select("*")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false });

  if (error) {
    console.error("Error fetching wishlist:", error);
    return [];
  }

  return data ?? [];
}

export async function isWishlisted(
  title: string
): Promise<boolean> {
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) return false;

  const { data, error } = await supabase
    .from("wishlist")
    .select("id")
    .eq("user_id", user.id)
    .eq("title", title)
    .maybeSingle();

  if (error) {
    console.error("Error checking wishlist:", error);
    return false;
  }

  return !!data;
}

export async function toggleWishlist(
  product: Product
): Promise<boolean> {
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    throw new Error("You must be logged in to use the wishlist.");
  }

  const { data: existing, error: checkError } = await supabase
    .from("wishlist")
    .select("id")
    .eq("user_id", user.id)
    .eq("title", product.title)
    .maybeSingle();

  if (checkError) {
    throw checkError;
  }

  if (existing) {
    const { error } = await supabase
      .from("wishlist")
      .delete()
      .eq("id", existing.id)
      .eq("user_id", user.id);

    if (error) throw error;

    window.dispatchEvent(new Event("wishlist-updated"));

    return false;
  }

  const { error } = await supabase
    .from("wishlist")
    .insert({
      user_id: user.id,
      title: product.title,
      price: product.price,
      source: product.source,
      link: product.link,
      image: product.image,
      rating: product.rating,
      score: product.score,
    });

  if (error) throw error;

  window.dispatchEvent(new Event("wishlist-updated"));

  return true;
}