# Ghibli API Project

## Overview
This Django project interfaces with the Ghibli API to serve movie and actor information. It's designed for efficiency and scalability, using Python, `Pydantic`, `httpx`, `asyncio`, and `Django/DRF`

## Key Features
- **Asynchronous Data Fetching**: Fetches actor details concurrently.
- **Two-Tier Caching**: Optimizes response times for overall data and individual actor details.
- **API Key Authentication**: Secures endpoints using `GhibliApiKeyAuthentication`.
- **Testing**: Comprehensive tests written with pytest.
- **Dependency Management**: Managed with `pip-compile` in a `venv`.

## Setup
1. **Clone and Navigate**: 
   ```bash
   git clone https://github.com/RahEnglishScore/Ghibli-Project
   cd Ghibli-Project
   ```
2. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Environment Variables**: Set `GHIBLI_API_KEY` in a `.env` file.

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Structure and Usage
- **`urls.py`**: Maps endpoints to views.
- **`views.py`**: Handles API logic, data fetching, and caching.
- **`models.py`**: Defines Pydantic models for data structure.
- **`authentication.py`**: Manages API key authentication.
- **`ghibli_api.py`**: Contains async functions for external API interactions.
- **`data_processing.py`**: Contains functions for data processing.
- **`tests`**: Directory for pytest-based tests.

## Running Tests
Execute `pytest` to run all tests.