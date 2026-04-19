import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../core/api/models.dart';

class DishCard extends StatelessWidget {
  const DishCard({
    required this.dish,
    required this.onToggleFavorite,
    super.key,
    this.pending = false,
  });

  final Dish dish;
  final VoidCallback onToggleFavorite;
  final bool pending;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: _Titles(
                    original: dish.nameOriginal,
                    translated: dish.nameTranslated,
                    textTheme: theme.textTheme,
                  ),
                ),
                const SizedBox(width: 12),
                _PriceLabel(price: dish.price, currency: dish.currency),
                const SizedBox(width: 4),
                IconButton(
                  onPressed: pending ? null : onToggleFavorite,
                  icon: Icon(
                    dish.isFavorite ? Icons.star_rounded : Icons.star_outline_rounded,
                    color: dish.isFavorite ? Colors.amber.shade600 : null,
                  ),
                  tooltip:
                      dish.isFavorite ? 'Remove from favorites' : 'Save as favorite',
                ),
              ],
            ),
            if (dish.description != null && dish.description!.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(
                dish.description!,
                style: theme.textTheme.bodyMedium?.copyWith(height: 1.4),
              ),
            ],
            const SizedBox(height: 12),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: _tags(theme).toList(growable: false),
            ),
            if (dish.ingredients != null && dish.ingredients!.isNotEmpty) ...[
              const SizedBox(height: 10),
              Text(
                dish.ingredients!.join(' · '),
                style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey.shade600),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Iterable<Widget> _tags(ThemeData theme) sync* {
    final category = dish.category;
    if (category != null && category.isNotEmpty) {
      yield _Tag(label: category);
    }
    if (dish.isVegetarian == true) yield const _Tag(label: 'Vegetarian', tone: _Tone.good);
    if (dish.isVegan == true) yield const _Tag(label: 'Vegan', tone: _Tone.good);
    final spice = dish.spiceLevel;
    if (spice != null && spice > 0) {
      yield _Tag(label: '🌶️' * spice.clamp(1, 3), tone: _Tone.warn);
    }
    for (final allergen in dish.allergens ?? const <String>[]) {
      yield _Tag(label: allergen, tone: _Tone.caution);
    }
  }
}

enum _Tone { neutral, good, warn, caution }

class _Tag extends StatelessWidget {
  const _Tag({required this.label, this.tone = _Tone.neutral});

  final String label;
  final _Tone tone;

  @override
  Widget build(BuildContext context) {
    final (bg, fg) = switch (tone) {
      _Tone.good => (const Color(0xFFD1FAE5), const Color(0xFF065F46)),
      _Tone.warn => (const Color(0xFFFEE2E2), const Color(0xFF991B1B)),
      _Tone.caution => (const Color(0xFFFEF3C7), const Color(0xFF92400E)),
      _Tone.neutral => (const Color(0xFFEAE7DF), const Color(0xFF3A3427)),
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        label,
        style: TextStyle(fontSize: 12, color: fg, fontWeight: FontWeight.w500),
      ),
    );
  }
}

class _Titles extends StatelessWidget {
  const _Titles({
    required this.original,
    required this.translated,
    required this.textTheme,
  });

  final String original;
  final String? translated;
  final TextTheme textTheme;

  @override
  Widget build(BuildContext context) {
    if (translated != null && translated!.isNotEmpty && translated != original) {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            translated!,
            style: textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
          ),
          Text(
            original,
            style: textTheme.bodySmall?.copyWith(color: Colors.grey.shade600),
          ),
        ],
      );
    }
    return Text(
      original,
      style: textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
    );
  }
}

class _PriceLabel extends StatelessWidget {
  const _PriceLabel({required this.price, required this.currency});

  final double? price;
  final String? currency;

  @override
  Widget build(BuildContext context) {
    if (price == null) return const SizedBox.shrink();
    final formatted = currency != null
        ? NumberFormat.currency(name: currency, symbol: '').format(price)
        : price!.toStringAsFixed(2);
    return Text(
      '${currency ?? ''} ${formatted.trim()}'.trim(),
      style: Theme.of(context).textTheme.titleSmall,
    );
  }
}
