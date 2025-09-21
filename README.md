# 甘藍價格與產量預測模擬 / Cabbage Price & Production Forecast Simulation

A Streamlit application for forecasting cabbage prices and production with multi-language support.

## Features

- **價格預測 / Price Forecasting**: Predict cabbage prices based on variety, location, and environmental factors
- **產量模擬 / Production Simulation**: Simulate production volumes using IoT sensor data
- **颱風影響分析 / Typhoon Impact Analysis**: Analyze the impact of typhoons on supply chain resilience  
- **多語言支援 / Multi-language Support**: Support for Traditional Chinese (繁體中文) and English

## Multi-language Support (國際化支援)

This application supports multiple languages through a JSON-based internationalization system.

### Available Languages (可用語言)

- **繁體中文 (zh_TW)**: Traditional Chinese (default)
- **English (en)**: English

### Language Selection (語言選擇)

Users can switch languages using the language selector in the sidebar. The application will automatically update all text content to the selected language.

### Adding New Languages (新增其他語言支援)

To add support for a new language:

1. **Create a new translation file** in the `translations/` directory:
   ```
   translations/
   ├── zh_TW.json (繁體中文)
   ├── en.json (English)
   └── [language_code].json (your new language)
   ```

2. **Copy the structure** from an existing translation file (e.g., `en.json`) and translate all text values to your target language.

3. **Update the language display names** in `i18n.py`:
   ```python
   language_names = {
       'zh_TW': '繁體中文',
       'en': 'English',
       'your_code': 'Your Language Name'
   }
   ```

4. **Translation file structure**:
   ```json
   {
     "app_title": "Your translated title",
     "variety_label": "Your translated variety label",
     "variety_options": {
       "early_autumn": "Early autumn cabbage in your language",
       "imported": "Imported cabbage in your language",
       "brussels_sprouts": "Brussels sprouts in your language"
     },
     // ... continue with all other keys
   }
   ```

### Translation Key Structure (翻譯鍵結構)

The translation system uses nested JSON keys:

- **Simple keys**: `"app_title"`, `"variety_label"`
- **Nested keys**: `"variety_options.early_autumn"`, `"county_options.taitung"`

### Maintaining Translations (維護翻譯內容)

When adding new features to the application:

1. **Add new text keys** to all translation files
2. **Use descriptive key names** that indicate the purpose of the text
3. **Test language switching** to ensure all new text appears correctly
4. **Keep translations consistent** across all supported languages

### System Language Detection (系統語言偵測)

The application automatically detects the system language on startup:
- Traditional Chinese systems default to `zh_TW`
- English systems default to `en`
- Other systems default to `zh_TW`

## Running the Application (執行應用程式)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   streamlit run app.py
   ```

3. **Access the application**:
   Open your browser to `http://localhost:8501`

## Project Structure (專案結構)

```
cabbage-streamlit/
├── app.py                 # Main Streamlit application
├── i18n.py               # Internationalization utility module
├── translations/         # Translation files directory
│   ├── zh_TW.json        # Traditional Chinese translations
│   └── en.json           # English translations
├── requirements.txt      # Python dependencies
└── README.md            # This documentation file
```

## Dependencies (相依套件)

- `streamlit`: Web application framework
- `numpy`: Numerical computing
- `pandas`: Data manipulation and analysis

## Contributing (貢獻)

When contributing to this project:

1. **Maintain language support**: Ensure all new text is properly internationalized
2. **Update translations**: Add new translation keys to all supported language files
3. **Test language switching**: Verify that language switching works correctly for all new features
4. **Document changes**: Update this README if you add new languages or change the i18n system

## License (授權)

This project is open source. Please refer to the repository license for more information.