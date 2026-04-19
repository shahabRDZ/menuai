import 'package:flutter/material.dart';

import 'app.dart';
import 'core/api/api_client.dart';
import 'core/auth/session_store.dart';
import 'core/config.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  final config = AppConfig.fromEnvironment();
  final apiClient = ApiClient(baseUrl: config.apiBaseUrl);
  final sessionStore = SessionStore();

  runApp(MenuAIApp(apiClient: apiClient, sessionStore: sessionStore));
}
