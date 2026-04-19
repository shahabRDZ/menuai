import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/api/api_client.dart';
import 'core/auth/session_store.dart';
import 'core/theme.dart';
import 'features/auth/auth_controller.dart';
import 'features/auth/login_page.dart';
import 'features/auth/register_page.dart';
import 'features/import/import_page.dart';
import 'features/scan/scan_page.dart';
import 'features/scans/scan_detail_page.dart';
import 'features/scans/scans_controller.dart';
import 'features/scans/scans_page.dart';
import 'widgets/state_views.dart';

class MenuAIApp extends StatelessWidget {
  const MenuAIApp({
    required this.apiClient,
    required this.sessionStore,
    super.key,
  });

  final ApiClient apiClient;
  final SessionStore sessionStore;

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        Provider<ApiClient>.value(value: apiClient),
        Provider<SessionStore>.value(value: sessionStore),
        ChangeNotifierProvider<AuthController>(
          create: (_) =>
              AuthController(api: apiClient, sessionStore: sessionStore)..bootstrap(),
        ),
        ChangeNotifierProvider<ScansController>(
          create: (_) => ScansController(api: apiClient),
        ),
      ],
      child: MaterialApp(
        title: 'MenuAI',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.light,
        onGenerateRoute: _onGenerateRoute,
        home: const _AuthGate(),
      ),
    );
  }

  Route<dynamic>? _onGenerateRoute(RouteSettings settings) {
    final name = settings.name ?? '/';

    if (name == '/login') return _page(const LoginPage());
    if (name == '/register') return _page(const RegisterPage());
    if (name == '/scan') return _page(const ScanPage());
    if (name == '/import') return _page(const ImportPage());

    const scanDetailPrefix = '/scan/';
    if (name.startsWith(scanDetailPrefix)) {
      final id = name.substring(scanDetailPrefix.length);
      if (id.isNotEmpty) return _page(ScanDetailPage(scanId: id));
    }

    return _page(const ScansPage());
  }

  MaterialPageRoute<dynamic> _page(Widget child) {
    return MaterialPageRoute(builder: (_) => child);
  }
}

class _AuthGate extends StatelessWidget {
  const _AuthGate();

  @override
  Widget build(BuildContext context) {
    final status = context.watch<AuthController>().status;

    switch (status) {
      case AuthStatus.unknown:
        return const Scaffold(body: LoadingView(message: 'Getting ready…'));
      case AuthStatus.signedOut:
        return const LoginPage();
      case AuthStatus.signedIn:
        return const ScansPage();
    }
  }
}
