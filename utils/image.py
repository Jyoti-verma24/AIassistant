import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_image_from_url(url):
    """
    Scrapes a webpage to find the most relevant content image.
    It prioritizes social media tags and then looks for the first large,
    content-related image, trying to ignore small icons and banners.
    """
    print(f"Attempting to extract a smart image from: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Priority 1: Look for Open Graph (og:image) meta tag ---
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            image_url = urljoin(url, og_image['content'])
            print(f"Found high-priority image via og:image tag: {image_url}")
            return image_url

        # --- Priority 2: Find the first large, meaningful image ---
        # Find all images and filter out ones that are likely irrelevant
        all_images = soup.find_all('img')
        candidate_images = []

        for img in all_images:
            src = img.get('src')
            if not src or src.startswith('data:image'):
                continue # Skip empty or inline images

            # Check for minimum dimensions to avoid small icons/logos
            width = int(img.get('width', 0))
            height = int(img.get('height', 0))
            if width < 150 or height < 150:
                continue

            # Skip images with "logo" or "banner" in their path, if possible
            if 'logo' in src.lower() or 'banner' in src.lower() or 'header' in src.lower():
                continue

            # Add the full URL to our list of candidates
            full_url = urljoin(url, src)
            candidate_images.append(full_url)
        
        if candidate_images:
            # Return the first good candidate we found
            best_image = candidate_images[0]
            print(f"Found a suitable content image: {best_image}")
            return best_image

        # --- Fallback: If no large images are found, return nothing ---
        print("No suitable large content image found on the page.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"NETWORK ERROR while trying to scrape image: {e}")
        return None
    except Exception as e:
        print(f"An unknown error occurred during image scraping: {e}")
        return None

