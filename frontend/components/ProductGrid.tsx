import { Product } from "../lib/api";
import ProductCard from "./ProductCard";

interface Props {
  products: Product[];
}

export default function ProductGrid({
  products,
}: Props) {
  if (!products.length) {
    return (
      <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-12 text-center">
        <p className="text-lg font-medium">
          No matching products found.
        </p>

        <p className="mt-2 text-sm text-white/40">
          Try another clothing image.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-2 sm:gap-5 lg:grid-cols-4">
      {products.map((product, index) => (
        <ProductCard
          key={`${product.title}-${index}`}
          product={product}
        />
      ))}
    </div>
  );
}