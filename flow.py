import asyncio
from typing import List
from prefect import flow, task, get_run_logger
from prefect.orion.schemas.states import Failed
from prefect.task_runners import ConcurrentTaskRunner
from prefect.blocks.system import JSON
# from prefect_email import
from pydantic import BaseModel
import requests


class WebsiteDown(Exception):
    def __init__(self, message):
        super().__init__(message)


def clean_flow_name(name: str):
    return f"website-checker-{name.replace('https://', '').replace('/', '-')}"


@flow()
async def url_checker(url: str, check_str: str):
    logger = get_run_logger()
    
    headers={'content-type': 'text/html', "User-Agent": "Mozilla 5.0 (Windows NT 10.0)"}
    results = requests.get(url, headers=headers)
    logger.info(f"{url} response: {results.status_code}")

    if check_str not in str(results.text):
        message = f"{url} can't be reached"
        logger.warning(message)
        raise WebsiteDown(message)
    else:
        logger.info(f"{url} is OK")


class Websites(BaseModel):
    url: str
    check_str: str


sites_json = JSON.load('website-checker')
sites = [Websites(**x) for x in sites_json.value]


@flow(name="Website Checker", task_runner=ConcurrentTaskRunner)
async def website_checker(sites: List[Websites] = sites):
    for site in sites:
        name = clean_flow_name(site.url)
        await url_checker.with_options(name=name)(site.url, site.check_str, return_state=True)


if __name__ == "__main__":
    state = asyncio.run(website_checker())


# prefect deployment build flow_website_checker.py:website_checker -sb s3/noaa-data -ib docker-container/prefect-shared-2-3-1 --path website_checker -n website_checker