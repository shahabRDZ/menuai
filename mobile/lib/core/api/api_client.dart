import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'api_exception.dart';
import 'models.dart';

class ApiClient {
  ApiClient({required this.baseUrl, http.Client? httpClient})
      : _http = httpClient ?? http.Client();

  final String baseUrl;
  final http.Client _http;

  String? _token;

  void setToken(String? token) => _token = token;

  Map<String, String> get _authHeaders {
    final headers = <String, String>{};
    final token = _token;
    if (token != null && token.isNotEmpty) {
      headers['authorization'] = 'Bearer $token';
    }
    return headers;
  }

  Future<String> register({
    required String email,
    required String password,
    String? name,
    String targetLanguage = 'en',
  }) async {
    final response = await _http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'content-type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
        if (name != null && name.isNotEmpty) 'name': name,
        'native_language': targetLanguage,
        'target_language': targetLanguage,
      }),
    );
    return _decodeToken(response);
  }

  Future<String> login(String email, String password) async {
    final response = await _http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'content-type': 'application/x-www-form-urlencoded'},
      body: 'username=${Uri.encodeQueryComponent(email)}'
          '&password=${Uri.encodeQueryComponent(password)}',
    );
    return _decodeToken(response);
  }

  Future<User> me() async {
    final response = await _http.get(
      Uri.parse('$baseUrl/auth/me'),
      headers: _authHeaders,
    );
    _ensureOk(response);
    return User.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<List<MenuScanSummary>> listScans() async {
    final response = await _http.get(
      Uri.parse('$baseUrl/menus'),
      headers: _authHeaders,
    );
    _ensureOk(response);
    final list = jsonDecode(response.body) as List<dynamic>;
    return list
        .map((e) => MenuScanSummary.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<MenuScan> getScan(String scanId) async {
    final response = await _http.get(
      Uri.parse('$baseUrl/menus/$scanId'),
      headers: _authHeaders,
    );
    _ensureOk(response);
    return MenuScan.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<void> deleteScan(String scanId) async {
    final response = await _http.delete(
      Uri.parse('$baseUrl/menus/$scanId'),
      headers: _authHeaders,
    );
    _ensureOk(response);
  }

  Future<MenuScan> scanMenu({
    required File imageFile,
    String? targetLanguage,
    String sourceLanguage = 'auto',
    String? restaurantName,
  }) async {
    final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/menus/scan'))
      ..headers.addAll(_authHeaders)
      ..fields['source_language'] = sourceLanguage;

    if (targetLanguage != null && targetLanguage.isNotEmpty) {
      request.fields['target_language'] = targetLanguage;
    }
    if (restaurantName != null && restaurantName.isNotEmpty) {
      request.fields['restaurant_name'] = restaurantName;
    }
    request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);
    _ensureOk(response);
    return MenuScan.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<MenuScan> importMenu({
    required String url,
    String? targetLanguage,
    String? restaurantName,
  }) async {
    final response = await _http.post(
      Uri.parse('$baseUrl/menus/import'),
      headers: {'content-type': 'application/json', ..._authHeaders},
      body: jsonEncode({
        'url': url,
        'target_language': targetLanguage ?? '',
        'restaurant_name': restaurantName,
      }),
    );
    _ensureOk(response);
    return MenuScan.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
  }

  Future<List<Dish>> listFavorites() async {
    final response = await _http.get(
      Uri.parse('$baseUrl/favorites'),
      headers: _authHeaders,
    );
    _ensureOk(response);
    final list = jsonDecode(response.body) as List<dynamic>;
    return list.map((e) => Dish.fromJson(e as Map<String, dynamic>)).toList();
  }

  Future<void> addFavorite(String dishId) async {
    final response = await _http.post(
      Uri.parse('$baseUrl/favorites/$dishId'),
      headers: _authHeaders,
    );
    _ensureOk(response);
  }

  Future<void> removeFavorite(String dishId) async {
    final response = await _http.delete(
      Uri.parse('$baseUrl/favorites/$dishId'),
      headers: _authHeaders,
    );
    _ensureOk(response);
  }

  String _decodeToken(http.Response response) {
    _ensureOk(response);
    final body = jsonDecode(response.body) as Map<String, dynamic>;
    final token = body['access_token'] as String?;
    if (token == null || token.isEmpty) {
      throw ApiException(500, 'Missing access_token in response');
    }
    return token;
  }

  void _ensureOk(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) return;
    String message = response.reasonPhrase ?? 'Request failed';
    try {
      final decoded = jsonDecode(response.body);
      if (decoded is Map && decoded['detail'] is String) {
        message = decoded['detail'] as String;
      }
    } catch (_) {
      if (response.body.isNotEmpty) message = response.body;
    }
    throw ApiException(response.statusCode, message);
  }
}
