import requests


def request(request_type, url, payload=None, params=None, allow_redirects=False, cookies=None, headers=None):
    """
    This is a wrapper around the python requests library
    which prints out request details for better debugging
    """

    if request_type == 'GET':
        print(f'GET: {url}\nparams: {params}\n')
        return requests.get(url,
                            params=params,
                            allow_redirects=allow_redirects,
                            cookies=cookies,
                            headers=headers,
                            timeout=30
                            )

    if request_type == 'POST':
        print(f'POST: {url}\nPayload: {payload}\n\n')
        return requests.post(url, json=payload, cookies=cookies, headers=headers, timeout=30)

    if request_type == 'PUT':
        print(f'PUT: {url}\nPayload: {payload}\n\n')
        return requests.put(url, json=payload, cookies=cookies, headers=headers, timeout=30)

    if request_type == 'DELETE':
        print(f'DELETE: {url}')
        return requests.delete(url, cookies=cookies, headers=headers, timeout=30)