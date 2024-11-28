import pandas as pd

def download_student_details(data,file_name):
    try:
        df=pd.DataFrame(data)
        df.to_excel(file_name)
        return True
    except Exception as e:
        print(e)
        return False