import requests

def requests_manager(route,method,data,isjson,isdata):
    url='https://terrible-lotty-sivarajan-cbd2472b.koyeb.app'+route
    try:
        if isjson:
            response=method(url,json=data)
        elif isdata:
            response=method(url,data=data)
        else:
            response=method(url,params=data)

        return response.json()
    except requests.exceptions.ConnectionError:
        return 'Please Check Your Connection !'