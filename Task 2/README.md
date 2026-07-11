# API Data Fetcher

Fetch, parse, search, and display data from multiple public APIs with a beautiful command-line interface.

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-API Support** | 5 different public APIs to choose from |
| **JSON Parsing** | Automatic JSON response parsing and validation |
| **Search & Filter** | Search through fetched data with keyword matching |
| **Colored Output** | Beautiful ANSI-colored terminal display |
| **Error Handling** | Graceful handling of timeouts, connection errors, HTTP errors |
| **User-Friendly** | Interactive menu with clear instructions |

---

## Supported APIs

1. **GitHub Trending** — Fetch top-starred repositories
2. **RandomUser API** — Generate random user profiles
3. **REST Countries** — Get info about all world countries
4. **Open Trivia DB** — Fetch trivia questions
5. **JSONPlaceholder** — Sample blog posts (for testing)

---

## Requirements

- Python 3.7+
- `requests` library

---

## Installation

```bash
pip install requests
```

---

## Usage

```bash
cd "Task 2"
python api_fetcher.py
```

### Example Flow

```
1. Select an API from the menu (1-5)
2. Wait for data to be fetched
3. Optionally enter a search term to filter results
4. View the formatted output
5. Choose to fetch from another API or exit
```

---

## Search Examples

| API | Search Term | Matches |
|-----|-------------|---------|
| GitHub Trending | `python` | Repos with "python" in name, language, or description |
| RandomUser | `john` | Users with "john" in first/last name |
| REST Countries | `asia` | Countries in Asia region or with "asia" in name |

---

## Output Examples

### GitHub Repositories
```
[1] tensorflow
    Owner: tensorflow
    ⭐ Stars: 185,432
    🍴 Forks: 74,123
    Language: Python
    URL: https://github.com/tensorflow/tensorflow
    Description: An Open Source Machine Learning Framework...
```

### Random Users
```
[1] John Doe
    Email: john.doe@example.com
    Gender: Male
    Location: New York, United States
    Phone: (555) 123-4567
    Age: 34
```

### Countries
```
[1] India
    Capital: New Delhi
    Region: Asia
    Population: 1,380,004,385
    Area: 3,287,590 km²
    Languages: Hindi, English
```

---

## Error Handling

The script handles:
- **Timeouts** — API taking too long to respond
- **Connection Errors** — No internet or API down
- **HTTP Errors** — 404, 500, rate limiting, etc.
- **JSON Parsing Errors** — Invalid response format
- **Keyboard Interrupts** — Graceful exit on Ctrl+C

---

## Code Structure

```python
# Main Components
fetch_api_data()     # Makes HTTP request, handles errors
display_data()       # Routes data to appropriate formatter
filter_data()        # Implements search/filter logic
search_*()           # API-specific search functions

# Display Functions (per API)
display_github_repos()
display_users()
display_countries()
display_trivia()
display_posts()
```

---

## Technical Details

- **HTTP Library:** `requests`
- **Timeout:** 10 seconds per request
- **User-Agent:** Custom header to avoid rate limiting
- **JSON Validation:** Automatic with error handling
- **Color Support:** ANSI escape codes (works on Windows 10+, Linux, macOS)

---

## License

MIT — Free to use and modify.
