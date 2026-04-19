class User {
  User({
    required this.id,
    required this.email,
    required this.nativeLanguage,
    required this.targetLanguage,
    required this.createdAt,
    this.name,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String?,
      nativeLanguage: json['native_language'] as String? ?? 'en',
      targetLanguage: json['target_language'] as String? ?? 'en',
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  final String id;
  final String email;
  final String? name;
  final String nativeLanguage;
  final String targetLanguage;
  final DateTime createdAt;
}

class Dish {
  Dish({
    required this.id,
    required this.scanId,
    required this.position,
    required this.nameOriginal,
    required this.isFavorite,
    required this.createdAt,
    this.nameTranslated,
    this.description,
    this.category,
    this.price,
    this.currency,
    this.priceUsd,
    this.typicalPriceMin,
    this.typicalPriceMax,
    this.priceFairness,
    this.priceDeltaPercent,
    this.priceEstimateConfidence,
    this.ingredients,
    this.allergens,
    this.allergenRisk,
    this.hiddenRisks,
    this.isVegetarian,
    this.isVegan,
    this.isHalalPossible,
    this.spiceLevel,
    this.localPopularity,
    this.touristTrapRisk,
    this.valueAssessment,
    this.recommendationScore,
    this.culturalContext,
  });

  factory Dish.fromJson(Map<String, dynamic> json) {
    return Dish(
      id: json['id'] as String,
      scanId: json['scan_id'] as String,
      position: json['position'] as int? ?? 0,
      nameOriginal: json['name_original'] as String,
      nameTranslated: json['name_translated'] as String?,
      description: json['description'] as String?,
      category: json['category'] as String?,
      price: (json['price'] as num?)?.toDouble(),
      currency: json['currency'] as String?,
      priceUsd: (json['price_usd'] as num?)?.toDouble(),
      typicalPriceMin: (json['typical_price_min'] as num?)?.toDouble(),
      typicalPriceMax: (json['typical_price_max'] as num?)?.toDouble(),
      priceFairness: json['price_fairness'] as String?,
      priceDeltaPercent: json['price_delta_percent'] as int?,
      priceEstimateConfidence: json['price_estimate_confidence'] as String?,
      ingredients: _stringList(json['ingredients']),
      allergens: _stringList(json['allergens']),
      allergenRisk: json['allergen_risk'] as String?,
      hiddenRisks: _stringList(json['hidden_risks']),
      isVegetarian: json['is_vegetarian'] as bool?,
      isVegan: json['is_vegan'] as bool?,
      isHalalPossible: json['is_halal_possible'] as bool?,
      spiceLevel: json['spice_level'] as int?,
      localPopularity: json['local_popularity'] as String?,
      touristTrapRisk: json['tourist_trap_risk'] as String?,
      valueAssessment: json['value_assessment'] as String?,
      recommendationScore: json['recommendation_score'] as int?,
      culturalContext: json['cultural_context'] is Map<String, dynamic>
          ? Map<String, dynamic>.from(json['cultural_context'] as Map)
          : null,
      isFavorite: json['is_favorite'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  final String id;
  final String scanId;
  final int position;
  final String nameOriginal;
  final String? nameTranslated;
  final String? description;
  final String? category;
  final double? price;
  final String? currency;
  final double? priceUsd;
  final double? typicalPriceMin;
  final double? typicalPriceMax;
  final String? priceFairness;
  final int? priceDeltaPercent;
  final String? priceEstimateConfidence;
  final List<String>? ingredients;
  final List<String>? allergens;
  final String? allergenRisk;
  final List<String>? hiddenRisks;
  final bool? isVegetarian;
  final bool? isVegan;
  final bool? isHalalPossible;
  final int? spiceLevel;
  final String? localPopularity;
  final String? touristTrapRisk;
  final String? valueAssessment;
  final int? recommendationScore;
  final Map<String, dynamic>? culturalContext;
  final bool isFavorite;
  final DateTime createdAt;

  String get displayName => nameTranslated ?? nameOriginal;

  Dish copyWith({bool? isFavorite}) {
    return Dish(
      id: id,
      scanId: scanId,
      position: position,
      nameOriginal: nameOriginal,
      nameTranslated: nameTranslated,
      description: description,
      category: category,
      price: price,
      currency: currency,
      priceUsd: priceUsd,
      typicalPriceMin: typicalPriceMin,
      typicalPriceMax: typicalPriceMax,
      priceFairness: priceFairness,
      priceDeltaPercent: priceDeltaPercent,
      priceEstimateConfidence: priceEstimateConfidence,
      ingredients: ingredients,
      allergens: allergens,
      allergenRisk: allergenRisk,
      hiddenRisks: hiddenRisks,
      isVegetarian: isVegetarian,
      isVegan: isVegan,
      isHalalPossible: isHalalPossible,
      spiceLevel: spiceLevel,
      localPopularity: localPopularity,
      touristTrapRisk: touristTrapRisk,
      valueAssessment: valueAssessment,
      recommendationScore: recommendationScore,
      culturalContext: culturalContext,
      isFavorite: isFavorite ?? this.isFavorite,
      createdAt: createdAt,
    );
  }
}

class MenuScan {
  MenuScan({
    required this.id,
    required this.sourceLanguage,
    required this.targetLanguage,
    required this.createdAt,
    required this.dishes,
    this.restaurantName,
    this.location,
    this.cuisineType,
    this.aiRecommendations,
    this.orderSuggestions,
  });

  factory MenuScan.fromJson(Map<String, dynamic> json) {
    return MenuScan(
      id: json['id'] as String,
      restaurantName: json['restaurant_name'] as String?,
      location: json['location'] as String?,
      cuisineType: json['cuisine_type'] as String?,
      sourceLanguage: json['source_language'] as String? ?? 'auto',
      targetLanguage: json['target_language'] as String? ?? 'en',
      createdAt: DateTime.parse(json['created_at'] as String),
      aiRecommendations: json['ai_recommendations'] is Map<String, dynamic>
          ? Map<String, dynamic>.from(json['ai_recommendations'] as Map)
          : null,
      orderSuggestions: json['order_suggestions'] is Map<String, dynamic>
          ? Map<String, dynamic>.from(json['order_suggestions'] as Map)
          : null,
      dishes: (json['dishes'] as List<dynamic>?)
              ?.map((d) => Dish.fromJson(d as Map<String, dynamic>))
              .toList() ??
          <Dish>[],
    );
  }

  final String id;
  final String? restaurantName;
  final String? location;
  final String? cuisineType;
  final String sourceLanguage;
  final String targetLanguage;
  final DateTime createdAt;
  final Map<String, dynamic>? aiRecommendations;
  final Map<String, dynamic>? orderSuggestions;
  final List<Dish> dishes;
}

class MenuScanSummary {
  MenuScanSummary({
    required this.id,
    required this.targetLanguage,
    required this.createdAt,
    required this.dishCount,
    this.restaurantName,
  });

  factory MenuScanSummary.fromJson(Map<String, dynamic> json) {
    return MenuScanSummary(
      id: json['id'] as String,
      restaurantName: json['restaurant_name'] as String?,
      targetLanguage: json['target_language'] as String? ?? 'en',
      createdAt: DateTime.parse(json['created_at'] as String),
      dishCount: json['dish_count'] as int? ?? 0,
    );
  }

  final String id;
  final String? restaurantName;
  final String targetLanguage;
  final DateTime createdAt;
  final int dishCount;
}

List<String>? _stringList(dynamic value) {
  if (value is! List) return null;
  return value.whereType<String>().toList();
}
