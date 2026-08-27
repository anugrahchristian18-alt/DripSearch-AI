import {
  Palette,
  Shirt,
  Sparkles,
  Tags,
  User,
} from "lucide-react";
import { ClothAnalysis } from "../lib/api";

interface Props {
  analysis: ClothAnalysis;
}

export default function AnalysisPanel({
  analysis,
}: Props) {
  const items = [
  {
    label: "Type",
    value: analysis?.clothing_type ?? "Unknown",
    icon: Shirt,
  },
  {
    label: "Color",
    value: analysis?.color ?? "Unknown",
    icon: Palette,
  },
  {
    label: "Pattern",
    value: analysis?.pattern ?? "Unknown",
    icon: Sparkles,
  },
  {
    label: "Style",
    value: analysis?.style ?? "Unknown",
    icon: Shirt,
  },
  {
    label: "Gender",
    value: analysis?.gender ?? "Unknown",
    icon: User,
  },
];
  return (
    <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-5 sm:p-6">

      <div className="mb-5">
        <p className="text-xs font-medium uppercase tracking-[0.2em] text-white/40">
          AI Analysis
        </p>

        <h2 className="mt-1 text-xl font-semibold">
          We found your style
        </h2>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.label}
              className="rounded-2xl border border-white/10 bg-black/30 p-4"
            >
              <Icon
                size={17}
                className="text-white/40"
              />

              <p className="mt-3 text-xs text-white/40">
                {item.label}
              </p>

              <p className="mt-1 truncate text-sm font-medium capitalize">
                {item.value}
              </p>
            </div>
          );
        })}
      </div>

      <div className="mt-4 rounded-2xl border border-white/10 bg-white/[0.03] p-4">
        <p className="text-xs text-white/40">
          AI Search Query
        </p>

        <p className="mt-1 text-sm text-white/80">
          {analysis?.search_query ?? "Unknown"}
        </p>
      </div>
    </section>
  );
}