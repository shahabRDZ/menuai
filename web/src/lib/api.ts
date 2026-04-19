const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? process.env.API_BASE_URL ?? "http://localhost:8000";

export type CulturalContext = {
  origin?: string | null;
  tradition?: string | null;
  when_eaten?: string | null;
};

export type AiRecommendations = {
  best_for_user?: { dish_name: string; reason: string }[];
  avoid_if?: { condition: string; reason: string }[];
};

export type OrderSuggestions = {
  light_option?: string | null;
  protein_rich_option?: string | null;
  budget_option?: string | null;
  local_experience_option?: string | null;
};

export type Dish = {
  id: string;
  scan_id: string;
  position: number;
  name_original: string;
  name_translated: string | null;
  description: string | null;
  category: string | null;
  price: number | null;
  currency: string | null;
  ingredients: string[] | null;
  allergens: string[] | null;
  allergen_risk: "low" | "medium" | "high" | null;
  hidden_risks: string[] | null;
  is_vegetarian: boolean | null;
  is_vegan: boolean | null;
  is_halal_possible: boolean | null;
  spice_level: number | null;
  local_popularity: "low" | "medium" | "high" | null;
  tourist_trap_risk: "low" | "medium" | "high" | null;
  value_assessment: "cheap" | "fair" | "expensive" | null;
  recommendation_score: number | null;
  cultural_context: CulturalContext | null;
  is_favorite: boolean;
  created_at: string;
};

export type MenuScan = {
  id: string;
  restaurant_name: string | null;
  location: string | null;
  cuisine_type: string | null;
  source_language: string;
  target_language: string;
  created_at: string;
  ai_recommendations: AiRecommendations | null;
  order_suggestions: OrderSuggestions | null;
  dishes: Dish[];
};

export type MenuScanSummary = {
  id: string;
  restaurant_name: string | null;
  target_language: string;
  created_at: string;
  dish_count: number;
};

export type User = {
  id: string;
  email: string;
  name: string | null;
  native_language: string;
  target_language: string;
  created_at: string;
};

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

class ApiClient {
  constructor(private readonly baseUrl: string) {}

  async register(input: {
    email: string;
    password: string;
    name?: string;
    native_language?: string;
    target_language?: string;
  }): Promise<{ access_token: string }> {
    return this.request("/auth/register", { method: "POST", json: input });
  }

  async login(email: string, password: string): Promise<{ access_token: string }> {
    const body = new URLSearchParams({ username: email, password });
    return this.request("/auth/login", {
      method: "POST",
      body,
      headers: { "content-type": "application/x-www-form-urlencoded" },
    });
  }

  async me(token: string): Promise<User> {
    return this.request("/auth/me", { token });
  }

  async listScans(token: string): Promise<MenuScanSummary[]> {
    return this.request("/menus", { token });
  }

  async getScan(token: string, scanId: string): Promise<MenuScan> {
    return this.request(`/menus/${scanId}`, { token });
  }

  async deleteScan(token: string, scanId: string): Promise<void> {
    await this.request(`/menus/${scanId}`, { method: "DELETE", token, raw: true });
  }

  async scanMenu(
    token: string,
    input: {
      image: Blob;
      imageName?: string;
      targetLanguage?: string;
      sourceLanguage?: string;
      restaurantName?: string;
    },
  ): Promise<MenuScan> {
    const form = new FormData();
    form.append("image", input.image, input.imageName ?? "menu.jpg");
    if (input.targetLanguage) form.append("target_language", input.targetLanguage);
    if (input.sourceLanguage) form.append("source_language", input.sourceLanguage);
    if (input.restaurantName) form.append("restaurant_name", input.restaurantName);

    return this.request("/menus/scan", { method: "POST", body: form, token });
  }

  async importMenu(
    token: string,
    input: { url: string; targetLanguage?: string; restaurantName?: string },
  ): Promise<MenuScan> {
    return this.request("/menus/import", {
      method: "POST",
      token,
      json: {
        url: input.url,
        target_language: input.targetLanguage ?? "",
        restaurant_name: input.restaurantName ?? null,
      },
    });
  }

  async listFavorites(token: string): Promise<Dish[]> {
    return this.request("/favorites", { token });
  }

  async addFavorite(token: string, dishId: string): Promise<void> {
    await this.request(`/favorites/${dishId}`, { method: "POST", token, raw: true });
  }

  async removeFavorite(token: string, dishId: string): Promise<void> {
    await this.request(`/favorites/${dishId}`, { method: "DELETE", token, raw: true });
  }

  private async request<T>(
    path: string,
    options: {
      method?: string;
      body?: BodyInit;
      json?: unknown;
      headers?: Record<string, string>;
      token?: string;
      raw?: boolean;
    } = {},
  ): Promise<T> {
    const headers: Record<string, string> = { ...(options.headers ?? {}) };
    let body = options.body;

    if (options.json !== undefined) {
      headers["content-type"] = "application/json";
      body = JSON.stringify(options.json);
    }
    if (options.token) {
      headers.authorization = `Bearer ${options.token}`;
    }

    const response = await fetch(`${this.baseUrl}${path}`, {
      method: options.method ?? "GET",
      body,
      headers,
      cache: "no-store",
    });

    if (!response.ok) {
      const text = await response.text().catch(() => "");
      let message = response.statusText;
      try {
        const parsed = JSON.parse(text);
        message = parsed.detail ?? message;
      } catch {
        if (text) message = text;
      }
      throw new ApiError(response.status, message);
    }
    if (options.raw) return undefined as T;
    return response.json();
  }
}

export const api = new ApiClient(API_BASE);
