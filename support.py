from pydantic import BaseModel


class Website(BaseModel):
    name: str
    url: str
    check_str: str
    server_url: str
    email_to: str


def clean_flow_name(name: str):
    return f"website-checker-{name.replace('https://', '').replace('/', '-')}"


def email_str(site: Website):
    return f"""
    The following website is unreachable: {site.url}
    <br><br>
    Server may need to be restarted.<br>
    Load Service Page: <a href="{site.server_url}">{site.name}</a>
    """