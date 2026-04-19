import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/api/api_client.dart';
import '../../core/languages.dart';
import '../auth/auth_controller.dart';
import 'scan_controller.dart';

class ScanPage extends StatelessWidget {
  const ScanPage({super.key});

  @override
  Widget build(BuildContext context) {
    final api = context.read<ApiClient>();
    return ChangeNotifierProvider(
      create: (_) => ScanController(api: api),
      child: const _ScanView(),
    );
  }
}

class _ScanView extends StatefulWidget {
  const _ScanView();

  @override
  State<_ScanView> createState() => _ScanViewState();
}

class _ScanViewState extends State<_ScanView> {
  final _restaurantController = TextEditingController();
  late String _targetLanguage =
      context.read<AuthController>().user?.targetLanguage ?? 'en';

  @override
  void dispose() {
    _restaurantController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final scan = await context.read<ScanController>().submit(
          targetLanguage: _targetLanguage,
          restaurantName: _restaurantController.text.trim(),
        );
    if (scan != null && mounted) {
      Navigator.of(context).pushReplacementNamed('/scan/${scan.id}');
    }
  }

  @override
  Widget build(BuildContext context) {
    final scan = context.watch<ScanController>();
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Scan a menu')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _ImagePreview(controller: scan),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: scan.submitting ? null : scan.pickFromCamera,
                      icon: const Icon(Icons.photo_camera_outlined),
                      label: const Text('Camera'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: scan.submitting ? null : scan.pickFromGallery,
                      icon: const Icon(Icons.photo_library_outlined),
                      label: const Text('Gallery'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              DropdownButtonFormField<String>(
                initialValue: _targetLanguage,
                decoration: const InputDecoration(labelText: 'Translate to'),
                items: supportedLanguages
                    .map(
                      (l) => DropdownMenuItem(value: l.code, child: Text(l.label)),
                    )
                    .toList(),
                onChanged: scan.submitting
                    ? null
                    : (v) => setState(() => _targetLanguage = v ?? 'en'),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _restaurantController,
                decoration: const InputDecoration(
                  labelText: 'Restaurant (optional)',
                  hintText: 'e.g. Çiya Sofrası',
                ),
                enabled: !scan.submitting,
              ),
              if (scan.error != null) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFEE2E2),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    scan.error!,
                    style: const TextStyle(color: Color(0xFF991B1B)),
                  ),
                ),
              ],
              const SizedBox(height: 20),
              FilledButton(
                onPressed: scan.canSubmit ? _submit : null,
                child: scan.submitting
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Scan this menu'),
              ),
              const SizedBox(height: 12),
              Text(
                'Tip: a flat page and good light give the best results. A slight angle is fine.',
                style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey.shade600),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ImagePreview extends StatelessWidget {
  const _ImagePreview({required this.controller});

  final ScanController controller;

  @override
  Widget build(BuildContext context) {
    final image = controller.pickedImage;

    return AspectRatio(
      aspectRatio: 4 / 3,
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          border: Border.all(color: const Color(0xFFEAE7DF)),
          borderRadius: BorderRadius.circular(12),
        ),
        clipBehavior: Clip.antiAlias,
        child: image == null
            ? const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.camera_alt_outlined, size: 48, color: Colors.grey),
                    SizedBox(height: 8),
                    Text('No photo yet', style: TextStyle(color: Colors.grey)),
                  ],
                ),
              )
            : Image.file(image, fit: BoxFit.cover),
      ),
    );
  }
}
