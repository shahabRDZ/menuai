# MenuAI — Mobile

Flutter app for MenuAI. Snap a menu, save favorite dishes, come back to translated
scans anytime. Talks to the FastAPI backend.

## Stack

- Flutter 3.22+ / Dart 3.4+
- `provider` for DI and controller state
- `http` for the typed API client
- `flutter_secure_storage` for the JWT session
- `image_picker` for camera + gallery
- `intl` for currency and date formatting

## Layout

```
lib/
├── main.dart
├── app.dart                         root MaterialApp + route table
├── core/
│   ├── api/
│   │   ├── api_client.dart          ApiClient class, typed endpoints
│   │   ├── api_exception.dart
│   │   └── models.dart              User, Dish, MenuScan, MenuScanSummary
│   ├── auth/
│   │   └── session_store.dart       SecureStorage-backed token store
│   ├── config.dart                  AppConfig.fromEnvironment()
│   ├── languages.dart
│   └── theme.dart
├── features/
│   ├── auth/           AuthController + login/register pages
│   ├── scans/          ScansController, ScanDetailController + pages
│   ├── scan/           ScanController + capture/upload page
│   └── favorites/      FavoritesController + page
└── widgets/            DishCard, LoadingView, ErrorView, EmptyState
```

Controllers extend `ChangeNotifier` and are injected with providers. The app
navigates through a small `onGenerateRoute` table — no extra routing dependency
needed.

## Run

Requires Flutter 3.22+. If the backend is running at something other than
`http://localhost:8000`, pass it in as a compile-time constant:

```bash
cd mobile
flutter pub get

# default points at http://localhost:8000
flutter run

# or override
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

### Platform notes

- **iOS simulator**: `http://localhost:8000` works as-is.
- **Android emulator**: use `http://10.0.2.2:8000` (loopback from the emulator).
- **Physical device**: use your dev machine's LAN IP (and make sure the backend
  binds to `0.0.0.0`).

### Permissions

`image_picker` needs a few platform permissions before release:

- **iOS** — add to `ios/Runner/Info.plist`:
  - `NSCameraUsageDescription`
  - `NSPhotoLibraryUsageDescription`
- **Android** — handled by the plugin on API 33+; on older devices add
  `<uses-permission android:name="android.permission.CAMERA"/>` to
  `android/app/src/main/AndroidManifest.xml`.
