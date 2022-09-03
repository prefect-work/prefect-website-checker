# prefect-website-checker
- Use `json_block.py` to generate a Prefect JSON Block with URLs and a strings to check in the website's source code (in the form of `List[dict]`)
- Using an environment with `prefect>=2.3.1` installed, run `flow.py`
- Create a "Notification" in Prefect Cloud 2.0 looking for "Failed" flow runs connected to a tag named "uptime-check"
