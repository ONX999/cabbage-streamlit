import json
import locale
import os
from typing import Dict, Any

class I18n:
    """Internationalization utility class for multi-language support."""
    
    def __init__(self, default_language='zh_TW'):
        """Initialize the I18n class with default language."""
        self.default_language = default_language
        # Try to detect system language, fallback to default
        detected_language = self.detect_system_language()
        self.current_language = detected_language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all available translation files."""
        translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
        
        if not os.path.exists(translations_dir):
            return
            
        for filename in os.listdir(translations_dir):
            if filename.endswith('.json'):
                language_code = filename[:-5]  # Remove .json extension
                filepath = os.path.join(translations_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[language_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading translation file {filename}: {e}")
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages with their display names."""
        language_names = {
            'zh_TW': '繁體中文',
            'en': 'English'
        }
        
        available = {}
        for code in self.translations.keys():
            available[code] = language_names.get(code, code)
        
        return available
    
    def set_language(self, language_code: str):
        """Set the current language."""
        if language_code in self.translations:
            self.current_language = language_code
        else:
            print(f"Language '{language_code}' not available. Using default.")
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for a given key."""
        # Navigate nested keys (e.g., "variety_options.early_autumn")
        keys = key.split('.')
        translation_dict = self.translations.get(self.current_language, {})
        
        for k in keys:
            if isinstance(translation_dict, dict) and k in translation_dict:
                translation_dict = translation_dict[k]
            else:
                # Fallback to default language
                fallback_dict = self.translations.get(self.default_language, {})
                for fk in keys:
                    if isinstance(fallback_dict, dict) and fk in fallback_dict:
                        fallback_dict = fallback_dict[fk]
                    else:
                        return default or key
                return fallback_dict if isinstance(fallback_dict, str) else default or key
        
        return translation_dict if isinstance(translation_dict, str) else default or key
    
    def detect_system_language(self) -> str:
        """Detect system language and return appropriate language code."""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                if system_locale.startswith('zh_TW') or system_locale.startswith('zh_Hant'):
                    return 'zh_TW'
                elif system_locale.startswith('en'):
                    return 'en'
        except:
            pass
        
        return self.default_language

# Global instance
i18n = I18n()