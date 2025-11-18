import json
import os
from typing import List, Dict
from mitmproxy import http
from mitmproxy import ctx
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NETWORKS_FILE = os.path.join(BASE_DIR, "networks.json")

class NetworkMatcher:
    def __init__(self, file_path):
        self.file_path = file_path
        self.mtime = 0
        self.rules = []
        self.load()

    def load(self):
        try:
            m = os.path.getmtime(self.file_path)
            if m == self.mtime:
                return
            self.mtime = m
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            ctx.log.info(f"networks file not found: {self.file_path}")
            data = []
        except Exception as e:
            ctx.log.error(f"failed reading networks file: {e}")
            data = []

        # convert to normalized internal structures
        rules = []
        for it in data:
            rules.append({
                "host": it.get("host", "").lower(),
                "path_prefix": it.get("path_prefix", ""),
                "response_code": int(it.get("response_code", 500)),
                "response_body": it.get("response_body", ""),
                "content_type": it.get("content_type", "application/json"),
                "name": it.get("name", ""),
            })
        self.rules = rules
        ctx.log.info(f"Loaded {len(rules)} rules from {self.file_path}")

    def match(self, host: str, path: str):
        self.load()  # reload if file changed
        host = (host or "").lower()
        for r in self.rules:
            if r["host"] and r["host"] != host:
                continue
            # if path_prefix empty => match any path on host
            if r["path_prefix"]:
                if path.startswith(r["path_prefix"]):
                    return r
            else:
                return r
        return None

matcher = NetworkMatcher(NETWORKS_FILE)

def request(flow: http.HTTPFlow):
    # mitmproxy passes requests to this function
    host = flow.request.pretty_host
    path = flow.request.path  # includes query
    rule = matcher.match(host, path)
    if rule:
        # build response
        body = rule["response_body"]
        if isinstance(body, str):
            body_bytes = body.encode("utf-8")
        else:
            body_bytes = json.dumps(body).encode("utf-8")
        headers = {"Content-Type": rule.get("content_type", "application/json")}
        flow.response = http.Response.make(rule["response_code"], body_bytes, headers)
        ctx.log.info(f"Applied rule {rule.get('name')} -> {host}{path} -> {rule['response_code']}")
