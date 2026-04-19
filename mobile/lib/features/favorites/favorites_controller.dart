import 'package:flutter/foundation.dart';

import '../../core/api/api_client.dart';
import '../../core/api/models.dart';

class FavoritesController extends ChangeNotifier {
  FavoritesController({required this.api});

  final ApiClient api;

  List<Dish> _dishes = const [];
  bool _loading = false;
  String? _error;
  final Set<String> _pending = <String>{};

  List<Dish> get dishes => _dishes;
  bool get loading => _loading;
  String? get error => _error;

  bool isPending(String dishId) => _pending.contains(dishId);

  Future<void> refresh() async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      _dishes = await api.listFavorites();
    } catch (e) {
      _error = e.toString();
    } finally {
      _loading = false;
      notifyListeners();
    }
  }

  Future<void> unfavorite(Dish dish) async {
    _pending.add(dish.id);
    notifyListeners();
    try {
      await api.removeFavorite(dish.id);
      _dishes = _dishes.where((d) => d.id != dish.id).toList();
    } catch (_) {
      // keep list as-is on failure
    } finally {
      _pending.remove(dish.id);
      notifyListeners();
    }
  }
}
