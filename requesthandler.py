import requests

def requests_manager(route,method,data,isjson,isdata):
    url='https://lmec-backend.vercel.app'+route
    try:
        response=None
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
