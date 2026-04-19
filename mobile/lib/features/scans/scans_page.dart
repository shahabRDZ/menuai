import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../../core/languages.dart';
import '../../widgets/state_views.dart';
import '../auth/auth_controller.dart';
import '../favorites/favorites_page.dart';
import 'scans_controller.dart';

class ScansPage extends StatefulWidget {
  const ScansPage({super.key});

  @override
  State<ScansPage> createState() => _ScansPageState();
}

class _ScansPageState extends State<ScansPage> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    const pages = [_HistoryTab(), FavoritesTab(), _ProfileTab()];

    return Scaffold(
      body: pages[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.history_outlined),
            selectedIcon: Icon(Icons.history),
            label: 'History',
          ),
          NavigationDestination(
            icon: Icon(Icons.star_outline_rounded),
            selectedIcon: Icon(Icons.star_rounded),
            label: 'Favorites',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline_rounded),
            selectedIcon: Icon(Icons.person_rounded),
            label: 'Profile',
          ),
        ],
      ),
      floatingActionButton: _index == 0
          ? Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                FloatingActionButton.small(
                  heroTag: 'fab-import',
                  onPressed: () async {
                    final controller = context.read<ScansController>();
                    await Navigator.of(context).pushNamed('/import');
                    await controller.refresh();
                  },
                  child: const Icon(Icons.qr_code_scanner_rounded),
                ),
                const SizedBox(height: 10),
                FloatingActionButton.extended(
                  heroTag: 'fab-scan',
                  onPressed: () async {
                    final controller = context.read<ScansController>();
                    await Navigator.of(context).pushNamed('/scan');
                    await controller.refresh();
                  },
                  icon: const Icon(Icons.camera_alt_rounded),
                  label: const Text('Scan'),
                ),
              ],
            )
          : null,
    );
  }
}

class _HistoryTab extends StatefulWidget {
  const _HistoryTab();

  @override
  State<_HistoryTab> createState() => _HistoryTabState();
}

class _HistoryTabState extends State<_HistoryTab> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ScansController>().refresh();
    });
  }

  @override
  Widget build(BuildContext context) {
    final ctrl = context.watch<ScansController>();

    return Scaffold(
      appBar: AppBar(title: const Text('Your scans')),
      body: RefreshIndicator(
        onRefresh: ctrl.refresh,
        child: _body(ctrl),
      ),
    );
  }

  Widget _body(ScansController ctrl) {
    if (ctrl.loading && ctrl.scans.isEmpty) {
      return const LoadingView();
    }
    if (ctrl.error != null && ctrl.scans.isEmpty) {
      return ErrorView(message: ctrl.error!, onRetry: ctrl.refresh);
    }
    if (ctrl.scans.isEmpty) {
      return ListView(
        children: [
          const SizedBox(height: 120),
          EmptyState(
            title: 'Nothing here yet',
            message:
                'Snap a photo of any menu and we\'ll turn it into a translated, tagged list.',
            action: FilledButton(
              onPressed: () =>
                  Navigator.of(context).pushNamed('/scan').then((_) => ctrl.refresh()),
              child: const Text('Scan your first menu'),
            ),
          ),
        ],
      );
    }

    return ListView.separated(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 100),
      itemCount: ctrl.scans.length,
      separatorBuilder: (_, __) => const SizedBox(height: 10),
      itemBuilder: (context, i) {
        final scan = ctrl.scans[i];
        return Card(
          child: ListTile(
            contentPadding:
                const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            title: Text(scan.restaurantName ?? 'Untitled menu'),
            subtitle: Text(
              '${scan.dishCount} ${scan.dishCount == 1 ? 'dish' : 'dishes'} · '
              '${languageLabel(scan.targetLanguage)} · '
              '${DateFormat.MMMd().add_jm().format(scan.createdAt)}',
            ),
            trailing: const Icon(Icons.chevron_right_rounded),
            onTap: () =>
                Navigator.of(context).pushNamed('/scan/${scan.id}').then((_) => ctrl.refresh()),
          ),
        );
      },
    );
  }
}

class _ProfileTab extends StatelessWidget {
  const _ProfileTab();

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthController>();
    final user = auth.user;

    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (user != null) ...[
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(user.name ?? user.email,
                        style: Theme.of(context).textTheme.titleMedium),
                    const SizedBox(height: 4),
                    Text(user.email,
                        style: Theme.of(context).textTheme.bodySmall),
                    const SizedBox(height: 12),
                    Text(
                      'Translates menus to ${languageLabel(user.targetLanguage)}',
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
          ],
          OutlinedButton.icon(
            onPressed: () async {
              await context.read<AuthController>().signOut();
              if (context.mounted) {
                Navigator.of(context).pushNamedAndRemoveUntil('/login', (_) => false);
              }
            },
            icon: const Icon(Icons.logout_rounded),
            label: const Text('Log out'),
          ),
        ],
      ),
    );
  }
}
