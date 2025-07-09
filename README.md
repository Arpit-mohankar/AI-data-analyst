# 🧠 AI Data Analyst

A Streamlit web application that leverages Google Gemini (Generative AI) and OpenAI APIs to provide automated data analysis, visualization, and interactive chat-based insights for your datasets. Upload your CSV or Excel files and let the AI help you understand, visualize, and explore your data.

## Features
- **Upload CSV or Excel datasets** via the sidebar
- **Automated dataset summary** using Gemini AI
- **Full data profiling** with ydata-profiling
- **Interactive data exploration** (preview, dtypes, memory usage)
- **Customizable visualizations** (scatter, bar, line charts with Plotly)
- **Chat with an AI data analyst** for insights, explanations, and code
- **Downloadable profiling reports**

## Demo
![Demo Screenshot](#) <!-- Add a screenshot if available -->

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Arpit-mohankar/AI-data-analyst.git
cd AI-data-analyst
```

### 2. Install dependencies
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
The app requires API keys for Google Gemini and OpenAI. You can provide them via Streamlit secrets or a `.env` file.

#### Option 1: Using `.streamlit/secrets.toml`
Create or edit `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-gemini-api-key"
OPENAI_API_KEY = "your-openai-api-key"
```

#### Option 2: Using `.env` file
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

- Upload your dataset (CSV or Excel) from the sidebar
- Explore, visualize, and chat with the AI about your data

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

## Notes
- Your API keys are sensitive. **Do not share or commit them.**
- The app uses [ydata-profiling](https://github.com/ydataai/ydata-profiling) for data profiling.
- The AI chat uses Google Gemini (default) and OpenAI APIs.

## Live Demo
[https://ai-data-analysst.streamlit.app/](https://ai-data-analysst.streamlit.app/)

## License
[MIT](LICENSE) <!-- Add a LICENSE file if available -->

## Author
Made by [Arpit Mohankar](mailto:arpitmohankar24@gmail.com) 
