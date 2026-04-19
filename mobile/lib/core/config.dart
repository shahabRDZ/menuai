class AppConfig {
  const AppConfig({required this.apiBaseUrl});

  factory AppConfig.fromEnvironment() {
    const fromEnv = String.fromEnvironment('API_BASE_URL');
    return const AppConfig(
      apiBaseUrl: fromEnv.isNotEmpty ? fromEnv : 'http://localhost:8000',
    );
  }

  final String apiBaseUrl;
}
