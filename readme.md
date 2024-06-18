
# AI Chatbot for Weather and Stock Queries

This project is an AI chatbot built with Python using the LangChain and Streamlit libraries. The chatbot can answer questions about the weather and stock prices using the OpenWeather and Polygon APIs.

## Features

- Fetch current weather information for any city.
- Retrieve the previous closing price of a given stock ticker.
- Interactive chat interface built with Streamlit.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- An OpenWeather API key
- A Polygon API key

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/ai-chatbot.git
   cd ai-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of your project and add your API keys:
   ```env
   POLYGON_KEY=your_polygon_api_key
   OPENWEATHER_KEY=your_openweather_api_key
   OPENAPI_KEY=your_openai_api_key
   ```

### Running the App

1. **Start the Streamlit app:**
   ```sh
   streamlit run app.py
   ```

2. **Interact with the chatbot:**
   Open your web browser and go to `http://localhost:8501` to interact with the chatbot.

## Project Structure

- `app.py`: The main Streamlit app file.
- `requirements.txt`: List of Python dependencies.
- `.env`: Environment variables file (not included in the repository).

## Usage

- Ask the chatbot about the weather in any city by providing the city name and country code.
- Request the previous closing price of any stock by providing its ticker symbol.
- The chatbot will respond accordingly based on the provided inputs.

## Example Queries

- "What is the weather in New York, US?"
- "What was the closing price of AAPL?"

## License

This project is licensed under the MIT License.
