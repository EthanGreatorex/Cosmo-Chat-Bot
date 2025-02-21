import requests
import html2text

# Function to fetch the raw HTML content using requests
def fetch_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  # Return the raw HTML of the page
        else:
            return None
    except Exception as e:
        return None
    
# Function to convert the html to text to reduce size
def convert_to_text(html):
    h = html2text.HTML2Text()
    # h.ignore_links = True
    h.ignore_images = True
    h.ignore_mailto_links = True
    return h.handle(html).strip().replace('\n',',')

def crawl_website(urls, type):
    fetched_data = []
    for url in urls:
        data = fetch_page(url)
        if data:
            if type == 'markdown':
                # Convert the html to text
                data = convert_to_text(data)
            fetched_data.append([url,data])
        else:
            fetched_data.append([url,None])
    
    
    return fetched_data


