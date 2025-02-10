import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
from tabulate import tabulate

def get_certificate_details(url):
    hostname = urlparse(url).hostname
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            return expiry_date

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

urls = read_urls_from_file('urls.txt')

results = []

for url in urls:
    try:
        expiry_date = get_certificate_details(url)
        results.append([url, expiry_date, ])
    except Exception as e:
        results.append([url, f"Failed to get the SSL certificate: {e}", "N/A"])

print(tabulate(results, headers=["URL", "Expiry Date"], tablefmt="grid"))
