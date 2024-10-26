import os
import requests
import platform

def local():
    # Check the OS type
    os_type = platform.system()

    # Check for cloud-specific metadata services
    cloud_services = {
        "AWS": "http://169.254.169.254/latest/meta-data/",
        "GCP": "http://metadata.google.internal/computeMetadata/v1/instance/",
        "Azure": "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
        "DigitalOcean": "http://169.254.169.254/metadata/v1/"
    }

    for cloud, url in cloud_services.items():
        try:
            response = requests.get(url, headers={"Metadata": "true"}, timeout=1)
            if response.status_code == 200:
                return f"Running in {cloud} cloud environment."
        except requests.RequestException:
            continue

    return f"Running in a local environment. OS: {os_type}"

# Example usage
if __name__ == "__main__":
    environment = local()
    print(environment)
