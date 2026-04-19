class Language {
  const Language(this.code, this.label);
  final String code;
  final String label;
}

const supportedLanguages = <Language>[
  Language('en', 'English'),
  Language('fa', 'Persian'),
  Language('ar', 'Arabic'),
  Language('tr', 'Turkish'),
  Language('de', 'German'),
  Language('fr', 'French'),
  Language('es', 'Spanish'),
  Language('ru', 'Russian'),
];

String languageLabel(String code) {
  for (final lang in supportedLanguages) {
    if (lang.code == code) return lang.label;
  }
  return code.toUpperCase();
}
