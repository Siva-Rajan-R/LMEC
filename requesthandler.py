import requests

def requests_manager(route,method,data,isjson,isdata):
    url='http://127.0.0.1:8000'+route
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
    except Exception as e:
        return 'Something Went Wrong'