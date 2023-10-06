from pathlib import Path


# Hunter API Key
HUNTER_API_KEY = "841e74e10225a3376475d01ec1b4d491c04d861b"

# Hunter API base url (no ending /)
HUNTER_BASE_URL = "https://api.hunter.io/v2"

# Google Custom Search Engine ID (cx)
GOOGLE_CUSTOM_SEARCH_ENGINE_ID = "84dd05669349947ef"

# Google Custom Search API Key
GOOGLE_CUSTOM_SEARCH_API_KEY = "AIzaSyCsINkJv-Oi0XXXU49OCKETP99kdEc3Elc"

# SerpApi API Key
SERPAPI_API_KEY = "4e60395b07dad18b57251f3d42960028bd07b6b82abdfeb0eca270d0db15ac68"

# SerpApi Google Maps LL Parameter
# To find this, basically go to Google Maps, search anything
# Then copy everything including and after the @ in the URL.
SERPAPI_LL = "@51.5261639,-0.1998848,14z"

# SerpApi Number of Results per Page
SERPAPI_RESULTS_PER_PAGE = 20

# Semrush Account Credentials
SEMRUSH_EMAIL = "hhcoanpd@ezztt.com"
SEMRUSH_PASSWORD = "Nawedi22."

# Google Cloud Engine Bucket
GCS_S3_BUCKET_NAME = "dsada"

# Google Cloud Credentials.json Path
GCS_CREDENTIALS_PATH = Path.cwd() / "credentials.json"

# Screenshots folder path
SCREENSHOTS_PATH = Path.cwd() / "screenshots"

# Path to chrome executable, set to None if it's in the default location
CHROME_PATH = None # r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Path to Chromedriver executable
CHROMEDRIVER_PATH = Path.cwd() / "driver" / "chromedriver"

# Show browser window
SHOW_WINDOW = False

# False = Include Google Search Result if Operating Hours not listed
# True = Skip Google Search Result if Operating Hours not listed
SKIP_IF_NO_OPERATING_HOURS = True

# Cutoff to consider a website high traffic
HIGH_TRAFFIC_THRESHOLD = 1000

# Include result if semrush doesn't have traffic info
INCLUDE_IF_NO_TRAFFIC = True
