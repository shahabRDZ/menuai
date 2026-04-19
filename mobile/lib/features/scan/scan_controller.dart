import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:image_picker/image_picker.dart';

import '../../core/api/api_client.dart';
import '../../core/api/models.dart';

class ScanController extends ChangeNotifier {
  ScanController({required this.api, ImagePicker? picker})
      : _picker = picker ?? ImagePicker();

  final ApiClient api;
  final ImagePicker _picker;

  File? _pickedImage;
  bool _submitting = false;
  String? _error;

  File? get pickedImage => _pickedImage;
  bool get submitting => _submitting;
  String? get error => _error;
  bool get canSubmit => _pickedImage != null && !_submitting;

  Future<void> pickFromCamera() => _pick(ImageSource.camera);

  Future<void> pickFromGallery() => _pick(ImageSource.gallery);

  Future<void> _pick(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(
        source: source,
        imageQuality: 85,
        maxWidth: 2000,
      );
      if (picked != null) {
        _pickedImage = File(picked.path);
        _error = null;
        notifyListeners();
      }
    } catch (e) {
      _error = 'Could not open ${source.name}: ${e.toString()}';
      notifyListeners();
    }
  }

  void reset() {
    _pickedImage = null;
    _error = null;
    notifyListeners();
  }

  Future<MenuScan?> submit({
    required String targetLanguage,
    String? restaurantName,
  }) async {
    final image = _pickedImage;
    if (image == null) return null;

    _submitting = true;
    _error = null;
    notifyListeners();

    try {
      final scan = await api.scanMenu(
        imageFile: image,
        targetLanguage: targetLanguage,
        restaurantName: restaurantName,
      );
      _pickedImage = null;
      return scan;
    } catch (e) {
      _error = 'We couldn\'t read this menu. ${_humanizeError(e)}';
      return null;
    } finally {
      _submitting = false;
      notifyListeners();
    }
  }

  String _humanizeError(Object e) {
    final message = e.toString();
    return message.split(':').last.trim();
  }
}
