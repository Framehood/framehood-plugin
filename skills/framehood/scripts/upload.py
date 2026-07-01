#!/usr/bin/env python3
"""Upload a local file to Framehood in original quality, of any size (up to the
server's cap), via a presigned upload URL + short-lived token.

Get the `upload_url` and `token` from the MCP tool `files(create_upload, filename,
content_type)` first, then run:

    python3 upload.py <local_file> --url <upload_url> --token <token>

On success it prints the hosted asset URL (use it as image_url/video_url/etc.).
Standard-library only (no pip installs).
"""
import argparse
import json
import mimetypes
import sys
from pathlib import Path
from urllib.parse import urlparse
import urllib.error
import urllib.request

# The file bytes + the token are only ever sent to Framehood's own host. This is a
# guard against being pointed at an attacker-controlled URL (e.g. if the calling
# agent were tricked): the token is scoped to your own storage key and useless
# elsewhere, but your file should never leave Framehood.
ALLOWED_HOST_SUFFIX = ".framehood.ai"


def die(msg: str, code: int) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def main() -> None:
    ap = argparse.ArgumentParser(description="Upload a local file to Framehood.")
    ap.add_argument("file", help="Path to the local file to upload")
    ap.add_argument("--url", required=True, help="upload_url from files(create_upload)")
    ap.add_argument("--token", required=True, help="token from files(create_upload)")
    ap.add_argument("--content-type", help="Override the content type (else inferred from the filename)")
    args = ap.parse_args()

    parsed = urlparse(args.url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not (host == "framehood.ai" or host.endswith(ALLOWED_HOST_SUFFIX)):
        die(f"refusing to upload to a non-Framehood URL: {args.url}", 1)

    fp = Path(args.file).expanduser()
    if not fp.is_file():
        die(f"file not found: {args.file}", 1)

    ctype = args.content_type or mimetypes.guess_type(str(fp))[0] or "application/octet-stream"
    data = fp.read_bytes()

    req = urllib.request.Request(
        args.url,
        data=data,
        method="PUT",
        headers={"Authorization": f"Bearer {args.token}", "Content-Type": ctype},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            url = resp.headers.get("X-Asset-Url")
            if not url:
                try:
                    url = json.loads(resp.read().decode()).get("url")
                except Exception:
                    url = None
            if not url:
                die("upload succeeded but the server returned no URL", 2)
            print(url)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        die(f"HTTP {e.code}: {body}", 2)
    except urllib.error.URLError as e:
        die(f"could not reach {host}: {e.reason}", 2)


if __name__ == "__main__":
    main()
