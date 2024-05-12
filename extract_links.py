import requests
from bs4 import BeautifulSoup

def extract_links_dawn():
    url = "https://www.dawn.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return links

def extract_links_bbc():
    url = "https://www.bbc.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return links


if __name__ == "__main__":
    dawn_links = extract_links_dawn()
    bbc_links = extract_links_bbc()

    print("Dawn.com Links:")
    for link in dawn_links:
        print(link)

    print("\nBBC.com Links:")
    for link in bbc_links:
        print(link)
