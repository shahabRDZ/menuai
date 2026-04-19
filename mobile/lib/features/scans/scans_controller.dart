import 'package:flutter/foundation.dart';

import '../../core/api/api_client.dart';
import '../../core/api/models.dart';

class ScansController extends ChangeNotifier {
  ScansController({required this.api});

  final ApiClient api;

  List<MenuScanSummary> _scans = const [];
  bool _loading = false;
  String? _error;

  List<MenuScanSummary> get scans => _scans;
  bool get loading => _loading;
  String? get error => _error;

  Future<void> refresh() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      _scans = await api.listScans();
    } catch (e) {
      _error = e.toString();
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  Future<void> remove(String id) async {
    await api.deleteScan(id);
    _scans = _scans.where((s) => s.id != id).toList();
    notifyListeners();
  }
}

class ScanDetailController extends ChangeNotifier {
  ScanDetailController({required this.api, required this.scanId});

  final ApiClient api;
  final String scanId;

  MenuScan? _scan;
  bool _loading = true;
  String? _error;
  final Set<String> _pendingFavorites = <String>{};

  MenuScan? get scan => _scan;
  bool get loading => _loading;
  String? get error => _error;

  bool isTogglePending(String dishId) => _pendingFavorites.contains(dishId);

  Future<void> load() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      _scan = await api.getScan(scanId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  Future<void> toggleFavorite(Dish dish) async {
    final current = _scan;
    if (current == null) return;

    _pendingFavorites.add(dish.id);
    _scan = _withDish(current, dish.copyWith(isFavorite: !dish.isFavorite));
    notifyListeners();

    try {
      if (dish.isFavorite) {
        await api.removeFavorite(dish.id);
      } else {
        await api.addFavorite(dish.id);
      }
    } catch (_) {
      _scan = _withDish(current, dish);
    } finally {
      _pendingFavorites.remove(dish.id);
      notifyListeners();
    }
  }

  MenuScan _withDish(MenuScan scan, Dish updated) {
    final dishes = scan.dishes
        .map((d) => d.id == updated.id ? updated : d)
        .toList(growable: false);
    return MenuScan(
      id: scan.id,
      restaurantName: scan.restaurantName,
      sourceLanguage: scan.sourceLanguage,
      targetLanguage: scan.targetLanguage,
      createdAt: scan.createdAt,
      dishes: dishes,
    );
  }
}
