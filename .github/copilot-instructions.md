# Cabbage Price and Yield Forecasting Simulation

This is a Streamlit web application that provides cabbage price and yield forecasting with supply chain resilience simulation. The application is written in Python using Streamlit, NumPy, and Pandas to simulate cabbage pricing based on variety, location, IoT sensor data, and typhoon impact.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the information here.**

## Working Effectively

### Bootstrap and Setup
- Install Python dependencies:
  - `pip install -r requirements.txt` -- takes ~20 seconds. NEVER CANCEL. Set timeout to 120+ seconds.
  - **Network issues**: If pip install fails due to network timeouts, retry with `pip install --timeout 120 -r requirements.txt`
  - **Alternative**: Install packages individually: `pip install streamlit numpy pandas`
- The application has only 3 core dependencies: streamlit, numpy, pandas
- No additional system packages or complex build steps required

### Running the Application
- Start the Streamlit application:
  - `streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false --server.headless true`
  - Application starts in ~3-5 seconds on http://localhost:8501
  - NEVER CANCEL the streamlit server - it runs continuously until stopped
- Access the application at http://localhost:8501 in your browser

### Linting and Code Quality
- Install linting tools: `pip install flake8` -- takes ~5 seconds
- Run critical syntax checks: `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics` -- takes <1 second
- Run full style checks: `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics` -- takes <1 second
- **ALWAYS run both flake8 commands before committing** or the CI (.github/workflows/python-package-conda.yml) will fail
- **Known style issues in current code**: E302, E305, W292 (missing blank lines and newline at end of file)

### Testing
- Install testing tools: `pip install pytest` -- takes ~5 seconds
- Run tests: `pytest` -- takes <1 second (currently no tests exist, exits with code 5)
- The workflow expects pytest to run successfully, even with 0 tests
- **No tests currently exist** - this is normal for this simple application

## Validation Scenarios

**ALWAYS manually validate any changes by running through these complete scenarios:**

### End-to-End User Workflow
1. Start the application: `streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false --server.headless true`
2. Navigate to http://localhost:8501
3. Verify the page loads with title "甘藍價格與產量預測模擬" (Cabbage Price and Yield Forecasting Simulation)
4. Test all interactive elements:
   - Change cabbage variety dropdown (初秋甘藍, 進口甘藍, 芽甘藍, 高麗菜, 紫甘藍, 娃娃菜, 包心白菜, 結球白菜, 冬季甘藍, 春季甘藍)
   - Change county dropdown (台北市, 新北市, 桃園市, 台中市, 台南市, 高雄市, and 16 other counties/cities)
   - Adjust forecast days slider (1-30 days)
   - Modify IoT volume input (kg)
   - Adjust typhoon impact slider (0.0-1.0)
5. Verify the chart updates dynamically when parameters change
6. Verify profit calculation updates (預估總利潤) - example: 初秋甘藍 should show different profit than 進口甘藍
7. Verify supply chain resilience values update (農場, 運輸, 市場 韌性狀態)
8. Verify market analysis section updates (全台灣甘藍行情, 各縣市甘藍行情, 市場趨勢分析)

### Development Workflow
- Always test functionality after making code changes to app.py
- Always run `flake8` before committing
- Always verify the Streamlit app starts and loads correctly
- Take screenshots of UI changes to verify visual correctness

## CI/CD Pipeline

### GitHub Actions Workflow
- File: `.github/workflows/python-package-conda.yml`
- **WARNING**: The workflow references `environment.yml` (conda) but the project uses `requirements.txt` (pip)
- Workflow steps:
  1. Sets up Python 3.10
  2. Attempts to run `conda env update --file environment.yml --name base` (will fail - file doesn't exist)
  3. Installs and runs flake8 linting
  4. Installs and runs pytest

### Known Issues with CI
- **environment.yml vs requirements.txt mismatch**: The workflow expects conda but project primarily uses pip
- **Network timeouts**: Conda environment setup works but can fail during pip install phase due to network timeouts
- To make CI pass, either:
  - Create environment.yml with conda equivalents of requirements.txt (already exists but has additional packages)
  - OR modify workflow to use `pip install -r requirements.txt`
- **Conda command validation**: `conda env update --file environment.yml --name base` installs Python 3.10 and conda packages successfully, but may timeout during pip phase

## Project Structure

### Key Files
- `app.py` - Main Streamlit application (194 lines)
- `requirements.txt` - Python dependencies (streamlit, numpy, pandas)
- `environment.yml` - Conda environment configuration (includes matplotlib, plotly)
- `.devcontainer/devcontainer.json` - VS Code dev container configuration
- `.github/workflows/python-package-conda.yml` - CI/CD pipeline
- `render.yaml` - Deployment configuration (currently empty)

### Core Functionality in app.py
- `forecast_model()` function - Calculates price predictions based on variety, impact factors
- Streamlit UI with dropdowns, sliders, and number inputs
- Interactive line chart showing price predictions over time
- Profit calculation and supply chain resilience simulation

## Common Development Tasks

### Testing Application Changes
1. Make code changes to app.py
2. Save the file (Streamlit auto-reloads)
3. Refresh browser or check if changes appear automatically
4. Test all interactive elements work correctly
5. Verify data flows through the forecast model correctly

### Debugging Issues
- Check browser console for JavaScript errors
- Streamlit server logs appear in terminal
- Common issue: Chart warnings about "Infinite extent" are normal and non-blocking
- Expected warnings: "WARN Infinite extent for field" and "The input spec uses Vega-Lite v5.20.1, but the current version of Vega-Lite is v6.2.0"

### Performance Notes
- Application is lightweight - no heavy computations
- All operations complete in milliseconds
- No database or external API dependencies
- Random number generation creates slight variation in forecasts

## Environment Requirements
- Python 3.10+ (tested with 3.12.3)
- No special system dependencies
- Runs on Linux, Windows, Mac
- Dev container support available for consistent environment

**CRITICAL TIMING NOTES:**
- Dependency installation: ~15 seconds (may take longer with network issues) - NEVER CANCEL, set timeout to 120+ seconds
- Application startup: ~3-5 seconds
- Linting: <1 second each command (0.13s for critical checks, 0.14s for full style checks)  
- Testing: <1 second (currently no tests, 0.18s with 0 tests found, exits with code 5)
- All operations are fast - no long-running builds or tests in this project

**NETWORK ISSUES:**
- If experiencing pip install timeouts, retry with longer timeout: `pip install --timeout 120 -r requirements.txt`
- Alternative: Install packages individually if bulk install fails