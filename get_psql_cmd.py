import subprocess

CMD = "heroku config:get DATABASE_URL -a benzak"

RESULT = subprocess.run(CMD.split(" "), capture_output=True)

DATABASE_URL = RESULT.stdout.decode().strip()

import dj_database_url

P = dj_database_url.parse(DATABASE_URL)

print(f"\n\n<><><><><><><><>\n{P['PASSWORD']}\n<><><><><><><><>\n\n")

print(f"psql -h {P['HOST']} -p {P['PORT']} -d {P['NAME']} -U {P['USER']} -W")
