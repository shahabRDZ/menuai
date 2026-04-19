import 'package:flutter/foundation.dart';

import '../../core/api/api_client.dart';
import '../../core/api/models.dart';

class ImportController extends ChangeNotifier {
  ImportController({required this.api});

  final ApiClient api;

  bool _submitting = false;
  String? _error;

  bool get submitting => _submitting;
  String? get error => _error;

  void reset() {
    _error = null;
    notifyListeners();
  }

  Future<MenuScan?> submit({
    required String url,
    required String targetLanguage,
    String? restaurantName,
  }) async {
    final trimmed = url.trim();
    if (trimmed.isEmpty) {
      _error = 'Paste a menu URL first.';
      notifyListeners();
      return null;
    }
    if (!trimmed.startsWith('http://') && !trimmed.startsWith('https://')) {
      _error = 'URL must start with http:// or https://';
      notifyListeners();
      return null;
    }

    _submitting = true;
    _error = null;
    notifyListeners();

    try {
      return await api.importMenu(
        url: trimmed,
        targetLanguage: targetLanguage,
        restaurantName: restaurantName,
      );
    } catch (e) {
      _error = e.toString().split(':').last.trim();
      return null;
    } finally {
      _submitting = false;
      notifyListeners();
    }
  }
}
