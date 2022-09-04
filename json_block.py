from prefect.blocks.system import JSON

websites = [
    {"url": "https://google.com", "check_str": "<div class=\"gb_Id\">Google apps</div>"},
]

json_block = JSON(value=websites)
json_block.save('website-checker-test', overwrite=True)
