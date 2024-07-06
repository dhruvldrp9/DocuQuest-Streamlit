import requests
from bs4 import BeautifulSoup


class LinkParser:
    def get_website_text(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-200 status codes

            soup = BeautifulSoup(response.content, 'html.parser')

            # Identify the element(s) containing the text you want to extract
            # This is where you'll need to customize based on the website structure
            # Here are some common examples:
            #  * Find all paragraphs: text_elements = soup.find_all('p')
            #  * Find elements with a specific class: text_elements = soup.find_all(class_='article-text')
            #  * Use CSS selectors: text_elements = soup.select('div.content p')  # Adjust the selector as needed

            extracted_text = ''
            for element in soup:
                # Extract text from the element, considering potential child elements
                extracted_text += element.get_text(separator='\n\n')  # Add a newline between paragraphs

            return extracted_text

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None






# # Example usage with two websites (replace with your actual URLs)
# website1_url = "https://en.wikipedia.org/wiki/Volunteering"

# text_from_website1 = LinkParser.extract_text(website1_url)

# if text_from_website1:
#     print(f"Text extracted from website 1:\n{text_from_website1}")

