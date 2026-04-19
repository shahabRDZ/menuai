import 'package:flutter/foundation.dart';

import '../../core/api/api_client.dart';
import '../../core/api/api_exception.dart';
import '../../core/api/models.dart';
import '../../core/auth/session_store.dart';

enum AuthStatus { unknown, signedOut, signedIn }

class AuthController extends ChangeNotifier {
  AuthController({required this.api, required this.sessionStore});

  final ApiClient api;
  final SessionStore sessionStore;

  AuthStatus _status = AuthStatus.unknown;
  User? _user;

  AuthStatus get status => _status;
  User? get user => _user;

  Future<void> bootstrap() async {
    String? token;
    try {
      token = await sessionStore
          .readToken()
          .timeout(const Duration(seconds: 3), onTimeout: () => null);
    } catch (_) {
      token = null;
    }
    if (token == null || token.isEmpty) {
      _setSignedOut();
      notifyListeners();
      return;
    }
    api.setToken(token);
    try {
      _user = await api.me();
      _status = AuthStatus.signedIn;
    } catch (_) {
      try {
        await sessionStore.clear();
      } catch (_) {}
      _setSignedOut();
    }
    notifyListeners();
  }

  Future<void> login(String email, String password) async {
    final token = await api.login(email, password);
    await _completeSignIn(token);
  }

  Future<void> register({
    required String email,
    required String password,
    String? name,
    String targetLanguage = 'en',
  }) async {
    final token = await api.register(
      email: email,
      password: password,
      name: name,
      targetLanguage: targetLanguage,
    );
    await _completeSignIn(token);
  }

  Future<void> signOut() async {
    await sessionStore.clear();
    api.setToken(null);
    _setSignedOut();
    notifyListeners();
  }

  Future<void> _completeSignIn(String token) async {
    await sessionStore.writeToken(token);
    api.setToken(token);
    try {
      _user = await api.me();
    } on ApiException {
      await sessionStore.clear();
      api.setToken(null);
      rethrow;
    }
    _status = AuthStatus.signedIn;
    notifyListeners();
  }

  void _setSignedOut() {
    _status = AuthStatus.signedOut;
    _user = null;
    api.setToken(null);
  }
}
