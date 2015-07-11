import json
from boto.s3.connection import Location
from pys3website import pys3website

def run():
    f = open("s3authkey.json", "r")
    auth = json.loads(f.read())
    f.close()

    mywebpage = pys3website.s3webpage(
        bucket_name = "richreview.edx",
        location = Location.DEFAULT,
        index_page = "index.html",
        err_page = "error.html",
        key_id = auth["access_key_id"],
        secret_key = auth["secret_access_key"]
    )

    mywebpage.update(
        local_path = "mywebsite"
    )

    print mywebpage.get_url()


if __name__ == "__main__":
    run()