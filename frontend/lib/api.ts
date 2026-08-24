const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ClothAnalysis {
  clothing_type: string;
  color: string;
  pattern: string;
  style: string;
  gender: string;
  search_query: string;
}

export interface Product {
  title: string;
  price: string;
  source: string;
  image?: string;
  link?: string;
  rating?: string | number;
  reviews?: string | number;
  score?: number;
}

export interface AnalyzeResponse {
  analysis: ClothAnalysis;
  products: Product[];
}

export async function analyzeClothing(
  file: File
): Promise<AnalyzeResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Something went wrong.");
  }

  return response.json();
}