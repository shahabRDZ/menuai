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
    this.ingredients,
    this.allergens,
    this.isVegetarian,
    this.isVegan,
    this.spiceLevel,
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
      ingredients: _stringList(json['ingredients']),
      allergens: _stringList(json['allergens']),
      isVegetarian: json['is_vegetarian'] as bool?,
      isVegan: json['is_vegan'] as bool?,
      spiceLevel: json['spice_level'] as int?,
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
  final List<String>? ingredients;
  final List<String>? allergens;
  final bool? isVegetarian;
  final bool? isVegan;
  final int? spiceLevel;
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
      ingredients: ingredients,
      allergens: allergens,
      isVegetarian: isVegetarian,
      isVegan: isVegan,
      spiceLevel: spiceLevel,
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
  });

  factory MenuScan.fromJson(Map<String, dynamic> json) {
    return MenuScan(
      id: json['id'] as String,
      restaurantName: json['restaurant_name'] as String?,
      sourceLanguage: json['source_language'] as String? ?? 'auto',
      targetLanguage: json['target_language'] as String? ?? 'en',
      createdAt: DateTime.parse(json['created_at'] as String),
      dishes: (json['dishes'] as List<dynamic>?)
              ?.map((d) => Dish.fromJson(d as Map<String, dynamic>))
              .toList() ??
          <Dish>[],
    );
  }

  final String id;
  final String? restaurantName;
  final String sourceLanguage;
  final String targetLanguage;
  final DateTime createdAt;
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
