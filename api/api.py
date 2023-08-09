from http.cookiejar import CookieJar
from typing import Dict

import locust as loc


def get(locust: loc.user.users, endpoint: str, params: Dict[str, any] = None,
        headers: Dict[str, any] = None, cookies: CookieJar = None,
        name: str = None, redirect: bool = False):

    response = locust.client.get(
        endpoint,
        params=params,
        headers=headers,
        cookies=cookies,
        name="get_" + name,
        allow_redirects=redirect
    )

    return response


def post(locust: loc.user.users, endpoint: str, params: Dict[str, any] = None,
         headers: Dict[str, any] = None, cookies: CookieJar = None,
         body: Dict[str, any] = None, name: str = None, redirect: bool = False,
         files: Dict[str, any] = None, auth: tuple[str, str] = None,
         json: any = None):

    response = locust.client.post(
        endpoint,
        params=params,
        headers=headers,
        cookies=cookies,
        data=body,
        name="post_" + name,
        allow_redirects=redirect,
        files=files,
        auth=auth,
        json=json
    )

    return response


def put(locust: loc.user.users, endpoint: str, params: Dict[str, any] = None,
        headers: Dict[str, any] = None, cookies: CookieJar = None,
        body: Dict[str, any] = None, name: str = None, redirect: bool = False,
        files: Dict[str, any] = None, auth: tuple[str, str] = None,
        json: any = None):

    response = locust.client.put(
        endpoint,
        params=params,
        headers=headers,
        cookies=cookies,
        data=body,
        name="put_" + name,
        allow_redirects=redirect,
        files=files,
        auth=auth,
        json=json
    )

    return response


def patch(locust: loc.user.users, endpoint: str, params: Dict[str, any] = None,
          headers: Dict[str, any] = None, cookies: CookieJar = None,
          body: Dict[str, any] = None, name: str = None, redirect: bool = False,
          files: Dict[str, any] = None, auth: tuple[str, str] = None,
          json: any = None):

    response = locust.client.patch(
        endpoint,
        params=params,
        headers=headers,
        cookies=cookies,
        data=body,
        name="patch_" + name,
        allow_redirects=redirect,
        files=files,
        auth=auth,
        json=json
    )

    return response


def delete(locust: loc.user.users, endpoint: str, params: Dict[str, any] = None,
           headers: Dict[str, any] = None, cookies: CookieJar = None,
           body: Dict[str, any] = None, name: str = None, redirect: bool = False,
           files: Dict[str, any] = None, auth: tuple[str, str] = None,
           json: any = None):

    response = locust.client.delete(
        endpoint,
        params=params,
        headers=headers,
        cookies=cookies,
        data=body,
        name="delete_" + name,
        allow_redirects=redirect,
        files=files,
        auth=auth,
        json=json
    )

    return response
