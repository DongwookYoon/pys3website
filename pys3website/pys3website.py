import os
import boto

policy = {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "PublicReadForGetBucketObjects",
			"Effect": "Allow",
			"Principal": "*",
			"Action": [
				"s3:GetObject"
			],
			"Resource": [
				"arn:aws:s3:::<bucket_name>/*"
			]
		}
	]
}

class s3webpage:
    bucket = ""
    bucket_name = ""
    def __init__(self, bucket_name, location, index_page, err_page,
                 key_id, secret_key):
        self.bucket_name = bucket_name
        conn = boto.connect_s3(key_id,secret_key)

        try:
            self.bucket = conn.get_bucket(bucket_name)
        except boto.exception.S3ResponseError as e:
            if(e.status == 404): #not found
                self.bucket = conn.create_bucket(
                    bucket_name, location=location, policy='public-read')

    def update(self, local_path):
        for path, dirs, files in os.walk(local_path):
            for file in files:
                key = self.bucket.new_key(os.path.join(path, file))
                fp = open(os.path.join(path, file))
                key.set_contents_from_file(fp)
                fp.close()
                print os.path.join(path, file)
        self.bucket.configure_website(suffix="index.html")
        import json
        a = json.dumps(policy)
        self.bucket.set_policy(a.replace("<bucket_name>",self.bucket_name))

    def get_url(self):
        return self.bucket.get_website_endpoint()