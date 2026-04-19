import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:provider/provider.dart';

import '../../core/api/api_client.dart';
import '../../core/languages.dart';
import '../auth/auth_controller.dart';
import 'import_controller.dart';

class ImportPage extends StatelessWidget {
  const ImportPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ImportController(api: context.read<ApiClient>()),
      child: const _ImportView(),
    );
  }
}

class _ImportView extends StatefulWidget {
  const _ImportView();

  @override
  State<_ImportView> createState() => _ImportViewState();
}

class _ImportViewState extends State<_ImportView> {
  final _urlController = TextEditingController();
  final _restaurantController = TextEditingController();
  late String _targetLanguage =
      context.read<AuthController>().user?.targetLanguage ?? 'en';

  @override
  void dispose() {
    _urlController.dispose();
    _restaurantController.dispose();
    super.dispose();
  }

  Future<void> _openScanner() async {
    final detected = await Navigator.of(context).push<String>(
      MaterialPageRoute(builder: (_) => const _QrScanView()),
    );
    if (detected != null && detected.isNotEmpty) {
      setState(() => _urlController.text = detected);
    }
  }

  Future<void> _submit() async {
    final scan = await context.read<ImportController>().submit(
          url: _urlController.text,
          targetLanguage: _targetLanguage,
          restaurantName: _restaurantController.text.trim(),
        );
    if (scan != null && mounted) {
      Navigator.of(context).pushReplacementNamed('/scan/${scan.id}');
    }
  }

  @override
  Widget build(BuildContext context) {
    final ctrl = context.watch<ImportController>();
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Import QR-code menu')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              OutlinedButton.icon(
                onPressed: ctrl.submitting ? null : _openScanner,
                icon: const Icon(Icons.qr_code_scanner_rounded),
                label: const Text('Scan restaurant QR code'),
              ),
              const SizedBox(height: 16),
              Text(
                'or paste the link manually',
                textAlign: TextAlign.center,
                style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey.shade600),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _urlController,
                decoration: const InputDecoration(
                  labelText: 'Menu URL',
                  hintText: 'https://restaurant.com/menu',
                ),
                keyboardType: TextInputType.url,
                enabled: !ctrl.submitting,
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                initialValue: _targetLanguage,
                decoration: const InputDecoration(labelText: 'Translate to'),
                items: supportedLanguages
                    .map((l) => DropdownMenuItem(value: l.code, child: Text(l.label)))
                    .toList(),
                onChanged: ctrl.submitting
                    ? null
                    : (v) => setState(() => _targetLanguage = v ?? 'en'),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _restaurantController,
                decoration: const InputDecoration(
                  labelText: 'Restaurant (optional)',
                ),
                enabled: !ctrl.submitting,
              ),
              if (ctrl.error != null) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFEE2E2),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    ctrl.error!,
                    style: const TextStyle(color: Color(0xFF991B1B)),
                  ),
                ),
              ],
              const SizedBox(height: 20),
              FilledButton(
                onPressed: ctrl.submitting ? null : _submit,
                child: ctrl.submitting
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Import this menu'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _QrScanView extends StatefulWidget {
  const _QrScanView();

  @override
  State<_QrScanView> createState() => _QrScanViewState();
}

class _QrScanViewState extends State<_QrScanView> {
  final MobileScannerController _controller = MobileScannerController(
    formats: const [BarcodeFormat.qrCode],
  );
  bool _handled = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onDetect(BarcodeCapture capture) {
    if (_handled) return;
    for (final code in capture.barcodes) {
      final value = code.rawValue;
      if (value != null && value.isNotEmpty) {
        _handled = true;
        Navigator.of(context).pop(value);
        return;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan QR code'),
        actions: [
          IconButton(
            onPressed: () => _controller.toggleTorch(),
            icon: const Icon(Icons.flash_on_rounded),
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(controller: _controller, onDetect: _onDetect),
          Positioned.fill(
            child: IgnorePointer(
              child: Center(
                child: Container(
                  width: 240,
                  height: 240,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.white, width: 2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
          ),
          const Positioned(
            bottom: 32,
            left: 24,
            right: 24,
            child: Text(
              'Hold the camera steady on the restaurant\'s QR code',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white, fontWeight: FontWeight.w500),
            ),
          ),
        ],
      ),
    );
  }
}
