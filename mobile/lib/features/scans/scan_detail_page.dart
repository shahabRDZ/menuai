import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/api/api_client.dart';
import '../../widgets/dish_card.dart';
import '../../widgets/state_views.dart';
import 'scans_controller.dart';

class ScanDetailPage extends StatelessWidget {
  const ScanDetailPage({required this.scanId, super.key});

  final String scanId;

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ScanDetailController(api: context.read<ApiClient>(), scanId: scanId)..load(),
      child: const _ScanDetailView(),
    );
  }
}

class _ScanDetailView extends StatelessWidget {
  const _ScanDetailView();

  @override
  Widget build(BuildContext context) {
    final ctrl = context.watch<ScanDetailController>();
    final scan = ctrl.scan;

    return Scaffold(
      appBar: AppBar(
        title: Text(scan?.restaurantName ?? 'Menu'),
        actions: [
          if (scan != null)
            IconButton(
              tooltip: 'Delete scan',
              onPressed: () => _confirmDelete(context),
              icon: const Icon(Icons.delete_outline),
            ),
        ],
      ),
      body: _body(context, ctrl),
    );
  }

  Widget _body(BuildContext context, ScanDetailController ctrl) {
    if (ctrl.loading) return const LoadingView();
    if (ctrl.error != null) {
      return ErrorView(message: ctrl.error!, onRetry: ctrl.load);
    }
    final scan = ctrl.scan;
    if (scan == null || scan.dishes.isEmpty) {
      return const EmptyState(
        title: 'Nothing to show',
        message: 'We couldn\'t find any dishes in this scan. Try a clearer photo.',
      );
    }

    return ListView.separated(
      padding: const EdgeInsets.all(16),
      itemCount: scan.dishes.length,
      separatorBuilder: (_, __) => const SizedBox(height: 12),
      itemBuilder: (context, i) {
        final dish = scan.dishes[i];
        return DishCard(
          dish: dish,
          pending: ctrl.isTogglePending(dish.id),
          onToggleFavorite: () => ctrl.toggleFavorite(dish),
        );
      },
    );
  }

  Future<void> _confirmDelete(BuildContext context) async {
    final ctrl = context.read<ScanDetailController>();
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete this scan?'),
        content: const Text('This cannot be undone.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancel'),
          ),
          FilledButton.tonal(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    final api = ctrl.api;
    try {
      await api.deleteScan(ctrl.scanId);
      if (context.mounted) Navigator.of(context).pop();
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Could not delete: $e')),
        );
      }
    }
  }
}
