import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/api/api_client.dart';
import '../../widgets/dish_card.dart';
import '../../widgets/state_views.dart';
import 'favorites_controller.dart';

class FavoritesTab extends StatelessWidget {
  const FavoritesTab({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => FavoritesController(api: context.read<ApiClient>())..refresh(),
      child: const _FavoritesView(),
    );
  }
}

class _FavoritesView extends StatelessWidget {
  const _FavoritesView();

  @override
  Widget build(BuildContext context) {
    final ctrl = context.watch<FavoritesController>();

    return Scaffold(
      appBar: AppBar(title: const Text('Favorites')),
      body: RefreshIndicator(
        onRefresh: ctrl.refresh,
        child: _body(ctrl),
      ),
    );
  }

  Widget _body(FavoritesController ctrl) {
    if (ctrl.loading && ctrl.dishes.isEmpty) return const LoadingView();
    if (ctrl.error != null && ctrl.dishes.isEmpty) {
      return ErrorView(message: ctrl.error!, onRetry: ctrl.refresh);
    }
    if (ctrl.dishes.isEmpty) {
      return ListView(
        children: const [
          SizedBox(height: 120),
          EmptyState(
            title: 'No favorites yet',
            message:
                'Tap the star next to a dish inside any scan to keep it here across your trips.',
          ),
        ],
      );
    }

    return ListView.separated(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 100),
      itemCount: ctrl.dishes.length,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, i) {
        final dish = ctrl.dishes[i];
        return DishCard(
          dish: dish,
          pending: ctrl.isPending(dish.id),
          onToggleFavorite: () => ctrl.unfavorite(dish),
        );
      },
    );
  }
}
