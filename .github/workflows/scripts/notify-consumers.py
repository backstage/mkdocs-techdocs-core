import argparse
import tomllib
import json
from urllib.request import Request, urlopen

data = tomllib.load(open("pyproject.toml", "rb"))

parser = argparse.ArgumentParser()
parser.add_argument(
    "--event-type",
    dest="event_type",
    type=str,
    default="MKDOCS_TECHDOCS_CORE::PUBLISHED_NEW_VERSION",
    help="The consuming repository will use this to trigger workflows.",
)
parser.add_argument(
    "--repo-owner",
    dest="repo_owner",
    type=str,
    default="backstage",
    help="The repository owner will be joined with repo_name. e.g (backstage/techdocs-container)",
)
parser.add_argument("--repo-name", dest="repo_name", type=str, required=True, help="")
parser.add_argument(
    "--authorization-token",
    dest="authorization_token",
    type=str,
    required=True,
    help='The token must have the following permissions:\n "Contents" repository permissions (write)',
)
args = parser.parse_args()

# Extract whatever information we want to expose
name = data["project"]["name"]
version = data["project"]["version"]

event_type = f""
event_payload = {"name": name, "version": version}

headers = {
    "Accept": "application/vnd.github.everest-preview+json",
    "Authorization": args.authorization_token,
}

API_URL = f"https://api.github.com/repos/{args.repo_owner}/{args.repo_name}/dispatches"

post_data = json.dumps(
    {"event_type": args.event_type, "client_payload": event_payload}
).encode("utf-8")
req = Request(API_URL, post_data, headers)

res = urlopen(req)
if res.status > 400:
    print(f"❌ Failed to notify consumers: \n Response Body: {res.read()}")
else:
    print(f"✅ Notified Consumers")
