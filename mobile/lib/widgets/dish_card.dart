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

    final borderColor = switch (dish.allergenRisk) {
      'high' => Colors.red.shade200,
      'medium' => Colors.amber.shade200,
      _ => const Color(0xFFEAE7DF),
    };

    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: borderColor),
      ),
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
                const SizedBox(width: 8),
                if (dish.recommendationScore != null)
                  _ScoreBadge(score: dish.recommendationScore!),
                const SizedBox(width: 8),
                _PriceLabel(price: dish.price, currency: dish.currency),
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
            if (dish.hiddenRisks != null && dish.hiddenRisks!.isNotEmpty) ...[
              const SizedBox(height: 12),
              _HiddenRisks(risks: dish.hiddenRisks!),
            ],
            if (dish.culturalContext != null) ...[
              const SizedBox(height: 10),
              _CulturalContext(context: dish.culturalContext!),
            ],
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
    if (dish.isHalalPossible == true) {
      yield const _Tag(label: 'Halal-possible', tone: _Tone.good);
    }
    final spice = dish.spiceLevel;
    if (spice != null && spice > 0) {
      yield _Tag(label: '🌶️' * spice.clamp(1, 3), tone: _Tone.warn);
    }
    if (dish.allergenRisk != null && dish.allergenRisk != 'low') {
      yield _Tag(label: '${dish.allergenRisk} allergen risk', tone: _Tone.warn);
    }
    if (dish.touristTrapRisk == 'high') {
      yield const _Tag(label: 'tourist trap risk', tone: _Tone.caution);
    }
    if (dish.localPopularity == 'high') {
      yield const _Tag(label: 'local favorite', tone: _Tone.good);
    }
    if (dish.valueAssessment == 'expensive') {
      yield const _Tag(label: 'pricey', tone: _Tone.caution);
    }
    if (dish.valueAssessment == 'cheap') {
      yield const _Tag(label: 'great value', tone: _Tone.good);
    }
    for (final allergen in dish.allergens ?? const <String>[]) {
      yield _Tag(label: allergen, tone: _Tone.caution);
    }
  }
}

class _ScoreBadge extends StatelessWidget {
  const _ScoreBadge({required this.score});

  final int score;

  @override
  Widget build(BuildContext context) {
    final (bg, fg) = score >= 85
        ? (const Color(0xFFD1FAE5), const Color(0xFF065F46))
        : score >= 70
            ? (const Color(0xFFFEF3C7), const Color(0xFF92400E))
            : (const Color(0xFFFEE2E2), const Color(0xFF991B1B));
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(999)),
      child: Text('$score', style: TextStyle(color: fg, fontWeight: FontWeight.w600)),
    );
  }
}

class _HiddenRisks extends StatelessWidget {
  const _HiddenRisks({required this.risks});

  final List<String> risks;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFBEB),
        border: Border.all(color: const Color(0xFFFDE68A)),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Hidden risks',
              style: TextStyle(color: Color(0xFF92400E), fontWeight: FontWeight.w600)),
          const SizedBox(height: 4),
          ...risks.map((r) => Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text('• $r',
                    style: const TextStyle(color: Color(0xFF92400E), fontSize: 12)),
              )),
        ],
      ),
    );
  }
}

class _CulturalContext extends StatelessWidget {
  const _CulturalContext({required this.context});

  final Map<String, dynamic> context;

  @override
  Widget build(BuildContext buildContext) {
    final origin = context['origin']?.toString();
    final tradition = context['tradition']?.toString();
    if ((origin == null || origin.isEmpty) && (tradition == null || tradition.isEmpty)) {
      return const SizedBox.shrink();
    }
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: const Color(0xFFEAE7DF),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (origin != null && origin.isNotEmpty)
            Text('Origin: $origin',
                style: const TextStyle(fontSize: 12, color: Color(0xFF3A3427))),
          if (tradition != null && tradition.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(tradition,
                style: const TextStyle(fontSize: 12, color: Color(0xFF3A3427))),
          ],
        ],
      ),
    );
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
