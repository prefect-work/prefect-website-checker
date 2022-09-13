from time import sleep
from prefect import flow, get_run_logger
from prefect.blocks.system import JSON
from prefect_email import EmailServerCredentials, email_send_message
import requests
from requests.exceptions import RequestException
from support import Website, clean_flow_name, email_str


@flow()
def url_checker(url: str, check_str: str, timeout: float):
    logger = get_run_logger()

    headers={'content-type': 'text/html', "User-Agent": "Mozilla 5.0 (Windows NT 10.0)"}
    attempt = True
    try_n = 0
    while attempt == True:
        try:
            results = requests.get(url, headers=headers, timeout=timeout)
            logger.info(f"{url} response: {results.status_code}")
            if results.status_code == 200 or try_n >= 3:
                if check_str not in str(results.text):
                    message = f"{url} can't be reached"
                    logger.warning(message)
                    return False
                else:
                    logger.info(f"{url} is OK")
                    return True
            try_n += 1
            sleep(2)
        except RequestException as e:
            logger.info(f"TIMEOUT: {url} unreachable after trying for {timeout} seconds.")
            logger.error(f'Error String: {e}')
            if try_n <= 3:
                try_n += 1
            else:
                return False
            
    if check_str not in str(results.text):
        message = f"{url} can't be reached"
        logger.warning(message)
        return False
    else:
        logger.info(f"{url} is OK")
        return True


@flow(name="Website Checker")
def website_checker(timeout: float = 15):
    logger = get_run_logger()
    
    sites_json = JSON.load('website-checker')
    sites = [Website(**x) for x in sites_json.value]
    email_credentials = EmailServerCredentials.load('gmail-darridapy')
    
    for site in sites:
        flow_name = clean_flow_name(site.url)
        up = url_checker.with_options(name=flow_name)(site.url, site.check_str, timeout)
        if not up:
            message = email_str(site)
            email_send_message(
                email_server_credentials=email_credentials,
                subject=f"Website Checker: {site.url} is unreachable",
                msg=message,
                email_to=site.email_to,
            )
            logger.info(f"Sent 'unreachable' email to {site.email_to} for {site.url}")


if __name__ == "__main__":
    website_checker(timeout=15)
