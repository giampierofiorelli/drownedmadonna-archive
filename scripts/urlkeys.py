"""Shared URL normalisation for the downloader and the site builder."""

import re
import urllib.parse

SESSION_PARAMS = {"phpsessid", "oscsid", "sessionid", "jsessionid"}


def site_host(host):
    """Return the bare host if it belongs to the archived site, else None."""
    host = (host or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host if host == "drownedmadonna.com" or host.endswith(".drownedmadonna.com") else None


def normalize(url):
    """Collapse trivial URL variants (scheme, www, port, &amp;, session ids, param order)."""
    url = url.replace("&amp;", "&").replace("&amp", "&")
    parts = urllib.parse.urlsplit(url)
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = urllib.parse.unquote(parts.path) or "/"
    path = re.sub(r"/{2,}", "/", path)
    params = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
              if k and k.lower() not in SESSION_PARAMS]
    query = urllib.parse.urlencode(sorted(params))
    return host + path + ("?" + query if query else "")
