"""
API Data Fetcher - Fetch, parse, search, and display API data
Uses: requests module, JSON parsing, search/filter functionality
"""

import requests
import json
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime


# ── ANSI Color Codes ──────────────────────────────────────────────────────────

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# ── API Configuration ─────────────────────────────────────────────────────────

APIS = {
    "1": {
        "name": "GitHub Trending",
        "url": "https://api.github.com/search/repositories",
        "params": {"q": "stars:>1000", "sort": "stars", "order": "desc", "per_page": 30},
        "description": "Fetch trending GitHub repositories"
    },
    "2": {
        "name": "RandomUser API",
        "url": "https://randomuser.me/api/",
        "params": {"results": 20},
        "description": "Generate random user profiles"
    },
    "3": {
        "name": "REST Countries",
        "url": "https://restcountries.com/v3.1/all",
        "params": {},
        "description": "Get information about all countries"
    },
    "4": {
        "name": "Open Trivia DB",
        "url": "https://opentdb.com/api.php",
        "params": {"amount": 20, "type": "multiple"},
        "description": "Fetch trivia questions"
    },
    "5": {
        "name": "JSONPlaceholder Posts",
        "url": "https://jsonplaceholder.typicode.com/posts",
        "params": {},
        "description": "Sample blog posts (testing API)"
    }
}


# ── Utility Functions ─────────────────────────────────────────────────────────

def print_header(text: str) -> None:
    """Print a styled header."""
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{text.center(70)}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}\n")


def print_success(text: str) -> None:
    print(f"{Color.GREEN}✓ {text}{Color.END}")


def print_error(text: str) -> None:
    print(f"{Color.RED}✗ {text}{Color.END}")


def print_info(text: str) -> None:
    print(f"{Color.CYAN}ℹ {text}{Color.END}")


def print_warning(text: str) -> None:
    print(f"{Color.YELLOW}⚠ {text}{Color.END}")


# ── API Fetcher ───────────────────────────────────────────────────────────────

def fetch_api_data(api_choice: str) -> Optional[Dict[str, Any]]:
    """
    Fetch data from the selected API.
    Returns the JSON response or None on failure.
    """
    if api_choice not in APIS:
        print_error("Invalid API choice.")
        return None

    api = APIS[api_choice]
    print_info(f"Fetching data from: {api['name']}")
    print_info(f"URL: {api['url']}")

    try:
        response = requests.get(
            api['url'],
            params=api['params'],
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 InterSpark API Fetcher"}
        )
        response.raise_for_status()
        
        data = response.json()
        print_success(f"Data fetched successfully! Status: {response.status_code}")
        return {"api_name": api['name'], "data": data}

    except requests.exceptions.Timeout:
        print_error("Request timed out. The API is taking too long to respond.")
    except requests.exceptions.ConnectionError:
        print_error("Connection error. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print_error(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
    except json.JSONDecodeError:
        print_error("Failed to parse JSON response.")
    
    return None


# ── Display Functions ─────────────────────────────────────────────────────────

def display_github_repos(data: List[Dict]) -> None:
    """Display GitHub repository data."""
    repos = data.get("items", [])
    
    print(f"\n{Color.BOLD}Found {len(repos)} repositories:{Color.END}\n")
    
    for i, repo in enumerate(repos, 1):
        print(f"{Color.BOLD}{Color.YELLOW}[{i}] {repo['name']}{Color.END}")
        print(f"    {Color.CYAN}Owner:{Color.END} {repo['owner']['login']}")
        print(f"    {Color.GREEN}⭐ Stars:{Color.END} {repo['stargazers_count']:,}")
        print(f"    {Color.BLUE}🍴 Forks:{Color.END} {repo['forks_count']:,}")
        print(f"    {Color.CYAN}Language:{Color.END} {repo.get('language', 'N/A')}")
        print(f"    {Color.UNDERLINE}URL:{Color.END} {repo['html_url']}")
        print(f"    {Color.YELLOW}Description:{Color.END} {repo.get('description', 'No description')[:80]}...")
        print()


def display_users(data: Dict) -> None:
    """Display random user data."""
    users = data.get("results", [])
    
    print(f"\n{Color.BOLD}Generated {len(users)} users:{Color.END}\n")
    
    for i, user in enumerate(users, 1):
        name = f"{user['name']['first']} {user['name']['last']}"
        print(f"{Color.BOLD}{Color.YELLOW}[{i}] {name}{Color.END}")
        print(f"    {Color.CYAN}Email:{Color.END} {user['email']}")
        print(f"    {Color.GREEN}Gender:{Color.END} {user['gender'].title()}")
        print(f"    {Color.BLUE}Location:{Color.END} {user['location']['city']}, {user['location']['country']}")
        print(f"    {Color.YELLOW}Phone:{Color.END} {user['phone']}")
        print(f"    {Color.CYAN}Age:{Color.END} {user['dob']['age']}")
        print()


def display_countries(data: List[Dict]) -> None:
    """Display country data."""
    print(f"\n{Color.BOLD}Found {len(data)} countries:{Color.END}\n")
    
    for i, country in enumerate(data[:20], 1):  # Show first 20
        name = country['name']['common']
        print(f"{Color.BOLD}{Color.YELLOW}[{i}] {name}{Color.END}")
        print(f"    {Color.CYAN}Capital:{Color.END} {', '.join(country.get('capital', ['N/A']))}")
        print(f"    {Color.GREEN}Region:{Color.END} {country.get('region', 'N/A')}")
        print(f"    {Color.BLUE}Population:{Color.END} {country.get('population', 0):,}")
        print(f"    {Color.YELLOW}Area:{Color.END} {country.get('area', 0):,} km²")
        print(f"    {Color.CYAN}Languages:{Color.END} {', '.join(country.get('languages', {}).values())[:50]}")
        print()


def display_trivia(data: Dict) -> None:
    """Display trivia questions."""
    questions = data.get("results", [])
    
    print(f"\n{Color.BOLD}Fetched {len(questions)} trivia questions:{Color.END}\n")
    
    for i, q in enumerate(questions, 1):
        print(f"{Color.BOLD}{Color.YELLOW}[{i}] Category: {q['category']}{Color.END}")
        print(f"    {Color.CYAN}Difficulty:{Color.END} {q['difficulty'].title()}")
        print(f"    {Color.GREEN}Question:{Color.END} {q['question']}")
        print(f"    {Color.BLUE}Correct Answer:{Color.END} {q['correct_answer']}")
        print()


def display_posts(data: List[Dict]) -> None:
    """Display blog posts."""
    print(f"\n{Color.BOLD}Found {len(data)} posts:{Color.END}\n")
    
    for i, post in enumerate(data[:15], 1):  # Show first 15
        print(f"{Color.BOLD}{Color.YELLOW}[{i}] {post['title'].title()}{Color.END}")
        print(f"    {Color.CYAN}User ID:{Color.END} {post['userId']}")
        print(f"    {Color.GREEN}Post ID:{Color.END} {post['id']}")
        print(f"    {Color.YELLOW}Body:{Color.END} {post['body'][:100]}...")
        print()


def display_data(api_name: str, data: Any) -> None:
    """Route data to the appropriate display function."""
    if "GitHub" in api_name:
        display_github_repos(data)
    elif "RandomUser" in api_name:
        display_users(data)
    elif "Countries" in api_name:
        display_countries(data)
    elif "Trivia" in api_name:
        display_trivia(data)
    elif "JSONPlaceholder" in api_name:
        display_posts(data)
    else:
        print(json.dumps(data, indent=2))


# ── Search & Filter ───────────────────────────────────────────────────────────

def search_github_repos(data: List[Dict], query: str) -> List[Dict]:
    """Search GitHub repos by name, language, or description."""
    repos = data.get("items", [])
    query_lower = query.lower()
    
    return [
        r for r in repos
        if query_lower in r['name'].lower()
        or query_lower in (r.get('language') or '').lower()
        or query_lower in (r.get('description') or '').lower()
    ]


def search_users(data: Dict, query: str) -> List[Dict]:
    """Search users by name, email, or location."""
    users = data.get("results", [])
    query_lower = query.lower()
    
    return [
        u for u in users
        if query_lower in f"{u['name']['first']} {u['name']['last']}".lower()
        or query_lower in u['email'].lower()
        or query_lower in u['location']['city'].lower()
        or query_lower in u['location']['country'].lower()
    ]


def search_countries(data: List[Dict], query: str) -> List[Dict]:
    """Search countries by name, region, or capital."""
    query_lower = query.lower()
    
    return [
        c for c in data
        if query_lower in c['name']['common'].lower()
        or query_lower in c.get('region', '').lower()
        or any(query_lower in cap.lower() for cap in c.get('capital', []))
    ]


def filter_data(api_name: str, data: Any, query: str) -> Any:
    """Filter data based on search query."""
    if not query.strip():
        return data
    
    print_info(f"Searching for: '{query}'")
    
    if "GitHub" in api_name:
        filtered = {"items": search_github_repos(data, query)}
        print_success(f"Found {len(filtered['items'])} matching repositories")
        return filtered
    elif "RandomUser" in api_name:
        filtered = {"results": search_users(data, query)}
        print_success(f"Found {len(filtered['results'])} matching users")
        return filtered
    elif "Countries" in api_name:
        filtered = search_countries(data, query)
        print_success(f"Found {len(filtered)} matching countries")
        return filtered
    else:
        print_warning("Search not implemented for this API.")
        return data


# ── Menu ──────────────────────────────────────────────────────────────────────

def print_menu() -> None:
    """Display the main menu."""
    print_header("API DATA FETCHER")
    print(f"{Color.BOLD}Select an API to fetch data from:{Color.END}\n")
    
    for key, api in APIS.items():
        print(f"  {Color.YELLOW}{key}.{Color.END} {Color.BOLD}{api['name']}{Color.END}")
        print(f"     {Color.CYAN}{api['description']}{Color.END}\n")
    
    print(f"  {Color.RED}0. Exit{Color.END}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point."""
    print(f"\n{Color.BOLD}{Color.GREEN}Welcome to API Data Fetcher!{Color.END}")
    print(f"{Color.CYAN}Fetch, parse, search, and display API data with ease.{Color.END}\n")
    
    while True:
        print_menu()
        
        choice = input(f"{Color.BOLD}Enter your choice (0-5): {Color.END}").strip()
        
        if choice == "0":
            print_success("Goodbye!")
            sys.exit(0)
        
        if choice not in APIS:
            print_error("Invalid choice. Please try again.")
            continue
        
        # Fetch data
        result = fetch_api_data(choice)
        if not result:
            continue
        
        api_name = result['api_name']
        data = result['data']
        
        # Ask if user wants to search/filter
        search_query = input(
            f"\n{Color.BOLD}Enter search term (or press Enter to show all): {Color.END}"
        ).strip()
        
        if search_query:
            data = filter_data(api_name, data, search_query)
        
        # Display results
        print_header(f"Results from {api_name}")
        display_data(api_name, data)
        
        # Ask to continue
        continue_choice = input(
            f"\n{Color.BOLD}Fetch another API? (y/n): {Color.END}"
        ).strip().lower()
        
        if continue_choice != 'y':
            print_success("Thanks for using API Data Fetcher!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Interrupted by user.{Color.END}")
        sys.exit(0)
