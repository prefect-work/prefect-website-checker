from prefect.blocks.system import JSON

websites = [
    {
        "name": "Google",
        "url": "https://google.com", 
        "check_str": "<div class=\"gb_Id\">Google apps</div>",
        "server_url": "https://www.google.com/appsstatus/dashboard/",
        "email_to": "<email>@gmail.com,<email2>@gmail.com",
    },
    {
        "name": "Google2",
        "url": "https://google.com", 
        "check_str": "<div class=\"gb_Id\">Google apps</div>",
        "server_url": "https://www.google.com/appsstatus/dashboard/",
        "email_to": "<email3>@gmail.com",
    },
]

json_block = JSON(value=websites)
json_block.save('website-checker-test', overwrite=True)
