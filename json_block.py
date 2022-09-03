from prefect.blocks.system import JSON

websites = [
    {"url": "https://google.com", "check_str": "<div class=\"gb_Id\">Google apps</div>"},
]

json_block = JSON(value={"the_answer": 42})
json_block.save('website-checker')