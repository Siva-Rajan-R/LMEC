from flet import *
from main_home_page import main_home_view
from attedencepage import take_attedence_view,student_card_view,add_student_detail_view,successfull_message_view,forgot_password_view
from fletschema import BottomSheetCntCreator,AttedenceContainerCreator,InformationContainer,YearChoosingDropDown,TextFields
from requesthandler import requests_manager,requests
from download import download_student_details
from datetime import date,datetime
import time
import os

attedence_dict=dict()
delete_list=list()
download_dict={'Register No':[],'Student Name':[],'Department':[],'Semester':[],'Student Mobile No':[],'Parent Mobile No':[],'No Of Days Present':[],'Attedence Percentage':[]}
def main(page:Page):
    page.theme_mode=ThemeMode.DARK
    attedence_list_lv=Ref[ListView]()
    department=Ref[Dropdown]()
    semester=Ref[Dropdown]()

    def fp_handler(e:FilePickerResultEvent):
        if e.path:
            download_path=f'{e.path}/Latha Mathavan student Details.xlsx'
            if os.path.exists(download_path):
                i=0
                while os.path.exists(download_path):
                    download_path=f'{e.path}/Latha Mathavan student Details ({i}).xlsx'
                    i+=1

            response=download_student_details(download_dict,download_path)
            if response:
                dad.content=ResponsiveRow([Text('Successfully Downloded !',weight=FontWeight.W_700,size=18,color='green',text_align='center'),Text(f'{download_path}\n In {e.path}',weight=FontWeight.W_700,size=18,color=colors.BLUE_ACCENT,text_align='center')])
                dad.title=Image("1103-confetti.gif",width=75,height=75,scale=1.2)
            else:
                dad.content=ResponsiveRow([Text('Failed To Download !',weight=FontWeight.W_700,size=18,color='red',text_align='center'),Text('Try To Choose Different Folder',weight=FontWeight.W_700,size=18,color=colors.BLUE_ACCENT,text_align='center')])
                dad.title=Image('comp_3.webp',width=75,height=75,scale=1.2)
        else:
            dad.content=Text('Please Select a Folder To Download',weight=FontWeight.W_700,size=18,color='red',text_align='center')
            dad.title=Image('120-folder.gif',width=75,height=75)
        dad.open=True
        page.update()

    
    def old_view_and_delete_fun(ischeckboxvisible,cnt_onclick,key,checkbox_handler_fun,year,isinitialview):
        global download_dict
        download_dict={'Register No':[],'Student Name':[],'Department':[],'Semester':[],'Student Mobile No':[],'Parent Mobile No':[],'No Of Days Present':[],'Attedence Percentage':[]}
        attedence_list_lv.current.controls.clear()
        attedence_list_lv.current.controls.insert(0,ProgressBar(height=8,color="cyan", bgcolor="white"))
        page.update()
        attedence_dict=requests_manager('/show-old-student-details',requests.get,{'dep':department.current.value,'year':year},False,False)
        attedence_list_lv.current.controls.pop(0)
        page.update()

        if isinitialview:
            page.views[-1].controls.insert(
                0,
                Row(
                    controls=[
                        YearChoosingDropDown(year_intial_value=2020,year_final_value=int(date.today().strftime('%Y')),key='viewold',onchange=ad_action_btns,width=150,height=40,value=ad.title.value)
                    ],
                )
            )
            page.update()

        if isinstance(attedence_dict,dict):
            for i in list(attedence_dict.keys()):
                print(attedence_dict,i)
                reg_no=i
                name=attedence_dict.get(i).get('student_name')
                attedence_list_lv.current.controls.append(AttedenceContainerCreator(str(reg_no),name.title(),ischeckboxvisibel=ischeckboxvisible,cnt_data=attedence_dict.get(i),cnt_onclick=cnt_onclick,checkbox_key=key,checkbox_handler=checkbox_handler_fun))
                page.update()
                nod_student_present=len(attedence_dict.get(reg_no).get('presents'))-1
                download_dict['Register No'].append(int(reg_no))
                download_dict['Student Name'].append(name.title())
                download_dict['Department'].append(department.current.value)
                download_dict['Semester'].append(semester.current.value)
                if not download_dict.get('Year'):
                    download_dict['Year']=[f"{int(year)}-{int(year)+4}"]
                else:
                    download_dict['Year'].append(f"{int(year)}-{int(year)+4}")
                download_dict['Student Mobile No'].append(attedence_dict.get(reg_no).get('student_ph_no'))
                download_dict['Parent Mobile No'].append(attedence_dict.get(reg_no).get('parent_ph_no'))
                download_dict['No Of Days Present'].append(nod_student_present)
                download_dict['Attedence Percentage']=f"{requests_manager('/calculate-student-attedence',requests.get,{'dep':department.current.value,'sem':semester.current.value,'nod_student_present':nod_student_present},False,False)} %"
                
        else:
            icon=icons.FILE_DOWNLOAD_OFF_OUTLINED
            color='red'
            if attedence_dict=='Please Check Your Connection !':
                icon=icons.WIFI_OFF_OUTLINED
                color='red'
            
            if attedence_dict !=None:
                page.views.append(successfull_message_view(view_pop_handler,page.width,attedence_dict,icon,color))
        page.update()


    def current_view_fun(date_of_sd):
        global download_dict
        download_dict={'Register No':[],'Student Name':[],'Department':[],'Semester':[],'Student Mobile No':[],'Parent Mobile No':[],'No Of Days Present':[],'Attedence Percentage':[]}
        attedence_list_lv.current.controls.clear()
        attedence_list_lv.current.controls.insert(0,ProgressBar(height=8,color="cyan", bgcolor="white"))
        page.update()
        edit_attedence=requests_manager('/show-particular-date-student-details',requests.get,{'dep':department.current.value,'sem':semester.current.value,'date_of_student_details':date_of_sd,'isforeditattedence':False},False,False)
        attedence_list_lv.current.controls.pop(0)
        page.update()
        ispresent={'bool':False,'words':'Absent'}
        if isinstance(edit_attedence,dict):
            for i in list(edit_attedence.keys()):
                if i=='presents':
                    ispresent['bool']=True
                    ispresent['words']='Present'
                else:
                    ispresent['bool']=False
                    ispresent['words']='Absent'
                for j in edit_attedence.get(i):
                    key=list(j.keys())[0]
                    reg_no=key
                    name=j.get(key).get('student_name')
                    attedence_dict[reg_no]=str(ispresent)
                    attedence_list_lv.current.controls.append(AttedenceContainerCreator(str(reg_no),name.title(),checkbox_handler,ispresent['bool'],ischeckboxdisabeld=True,checkboxfillcolor='green',cnt_data=j.get(key),cnt_onclick=show_student_details))
                    page.update()
                    nod_student_present=len(j.get(key).get('presents'))-1
                    download_dict['Register No'].append(int(key))
                    download_dict['Student Name'].append(name.title())
                    download_dict['Department'].append(department.current.value)
                    download_dict['Semester'].append(semester.current.value)
                    download_dict['Student Mobile No'].append(j.get(key).get('student_ph_no'))
                    download_dict['Parent Mobile No'].append(j.get(key).get('parent_ph_no'))
                    if not download_dict.get(date_of_sd):
                        download_dict[date_of_sd]=[ispresent['words']]
                    else:
                        download_dict[date_of_sd].append(ispresent['words'])
                    download_dict['No Of Days Present'].append(nod_student_present)
                    download_dict['Attedence Percentage']=f"{requests_manager('/calculate-student-attedence',requests.get,{'dep':department.current.value,'sem':semester.current.value,'nod_student_present':nod_student_present},False,False)} %"

                    
        else:
            icon=icons.DRIVE_FILE_RENAME_OUTLINE
            color='red'
            if edit_attedence=='Please Check Your Connection !':
                icon=icons.WIFI_OFF_OUTLINED
                color='red'
            if edit_attedence !=None:
                page.views.append(successfull_message_view(view_pop_handler,page.width,edit_attedence,icon,color))
        page.update()


    def dp_handler(e):
        selected_date=e.control.value.strftime('%d-%m-%Y')
        page.views[-1].controls[0].controls[0].content.value=selected_date
        page.update()

        current_view_fun(selected_date)

    dp=DatePicker(value=datetime(int(date.today().year),int(date.today().month),int(date.today().day)),first_date=datetime(2020,1,1),last_date=datetime(int(date.today().year),int(date.today().month)+1,1),on_change=dp_handler)
    bs=BottomSheet(content=Text(),enable_drag=True,show_drag_handle=True,bgcolor='white')
    fp=FilePicker(on_result=fp_handler)
    dad=AlertDialog(bgcolor='white',title=Text())
    page.overlay.extend([bs,fp,dad])

    def view_pop_handler(e):
        page.views.pop()
        page.update()

    def checkbox_handler(e):
        global attedence_dict,delete_list
    
        if e.control.key=='attedence':
            attedence_dict[e.control.data]=str(e.control.value)

        elif e.control.key=='delete':
            if page.views[-1].controls[0].controls[0].value:
                page.views[-1].controls[0].controls[0].value=False
                page.update()
            if e.control.value:
                if int(e.control.data) not in delete_list:
                    delete_list.append(int(e.control.data))
            else:
                if int(e.control.data) in delete_list:
                    delete_list.remove(int(e.control.data))
            print(len(delete_list),len(attedence_list_lv.current.controls))
            if len(delete_list)==len(attedence_list_lv.current.controls):
                page.views[-1].controls[0].controls[0].value=True
                page.update()

        elif e.control.key=='delete_all':
            temp=len(attedence_list_lv.current.controls)
            for i in range(temp):
                if e.control.value==True:
                    attedence_list_lv.current.controls[i].content.controls[1].controls[0].value=True
                page.update()



    def send_attedence(e):
        global attedence_dict
        if e.control.key not in ['View Current SD','View Old SD','verify_user','send_password']:
            attedence_list_lv.current.controls.insert(0,ProgressBar(height=8,color="cyan", bgcolor="white"))
            attedence_list_lv.current.controls[0].key='top'
            page.views[-1].scroll_to(key='top')
            page.update()
        if e.control.key in ['Take Attedence','Edit Attedence']:
            if e.control.key=='Take Attedence':
                response=requests_manager("/add-attedence",requests.post,{'dep':department.current.value,'sem':semester.current.value,'presents':attedence_dict},True,False)
            elif e.control.key=='Edit Attedence':
                response=requests_manager("/edit-attedence",requests.put,{'dep':department.current.value,'sem':semester.current.value,'presents':attedence_dict},True,False)
            attedence_list_lv.current.controls.pop(0)
            page.views.pop()
            page.views.append(successfull_message_view(view_pop_handler,page.width,response,icons.VERIFIED_OUTLINED,'green'))
        
        elif e.control.key in ['Delete Current SD','Delete Old SD']:
            isdelete_all=page.views[-1].controls[0].controls[0].value
            if e.control.key=='Delete Current SD':
                response=requests_manager('/delete-current-student-details',requests.delete,{'dep':department.current.value,'sem':semester.current.value,'delete_all':isdelete_all,'reg_no':delete_list},False,True)
            elif e.control.key=='Delete Old SD':
                response=requests_manager('/delete-old-student-details',requests.delete,{'dep':department.current.value,'year':'2020','delete_all':isdelete_all,'reg_no':delete_list},False,True)
            attedence_list_lv.current.controls.pop(0)
            page.update()
            if response:
                if isdelete_all:
                    attedence_list_lv.current.controls.clear()
                else:
                    for i in range(len(attedence_list_lv.current.controls)-1,-1,-1):
                        if int(attedence_list_lv.current.controls[i].content.controls[1].controls[0].data) in delete_list:
                            attedence_list_lv.current.controls.pop(i)
                            page.update()

        elif e.control.key in ['View Current SD','View Old SD']:
            fp.get_directory_path()
        
        elif e.control.key=='verify_user':
            e.control.text='Verifying...'
            e.control.disabled=True
            page.update()
            res=requests_manager('/verify-password',requests.get,{'password':bs.content.controls[0].value},False,True)
            
            if isinstance(res,bool) and res:
                bs.open=False
                page.update()
                time.sleep(0.2)
                page.views.append(main_home_view(view_pop_handler,page.width,bottom_sheet_handler))
            else:
                bs.content.controls[0].error_text=res
            e.control.text='Verify'
            e.control.disabled=False

        elif e.control.key=='send_password':
            email=page.views[-1].controls[0].content.controls[2].controls[0].content.controls[0].value
            password=page.views[-1].controls[0].content.controls[2].controls[0].content.controls[1].value
            page.views[-1].controls[0].content.controls[2].controls[0].content.controls[2].controls[0].text='Submiting...'
            page.views[-1].controls[0].content.controls[2].controls[0].content.controls[2].controls[0].disabled=True
            page.update()
            res=requests_manager('/create-password',requests.post,{'admin_mail':email,'new_password':password},False,True)
            email=page.views[-1].controls[0].content.controls[2].controls[0].content.controls[0].value=""
            password=page.views[-1].controls[0].content.controls[2].controls[0].content.controls[1].value=""
            page.views[-1].controls[0].content.controls[2].controls[0].content.controls[2].controls[0].text='Submit'
            page.views[-1].controls[0].content.controls[2].controls[0].content.controls[2].controls[0].disabled=False
            if isinstance(res,bool):
                page.views[-1].controls[0].content.controls[2].controls.insert(
                    0,
                    InformationContainer(msg='Password Created Successfully')
                )
                page.update()
                time.sleep(1)
                page.views[-1].controls[0].content.controls[2].controls.pop(0)
                page.views.pop()
            else:
                page.views[-1].controls[0].content.controls[2].controls.insert(
                    0,
                    InformationContainer(msg=res,icon=icons.REPORT_GMAILERRORRED_OUTLINED,bgcolor='red')
                )
                page.update()
                time.sleep(1)
                page.views[-1].controls[0].content.controls[2].controls.pop(0)


        page.update()
        delete_list.clear()
        attedence_dict=dict()
    
    def search_students(e):
        for i in range(len(attedence_list_lv.current.controls)):
            if e.control.value in attedence_list_lv.current.controls[i].content.controls[1].controls[0].data:
                t=attedence_list_lv.current.controls.pop(i)
                attedence_list_lv.current.controls.insert(0,t)
                page.update()

    def show_student_details(e):
        reg_no=e.control.content.controls[0].controls[0].value
        sem_or_year={'Sem :':semester.current.value}
        if attedence_list_lv.current.controls[0].content.controls[1].controls[0].visible==False:
            sem_or_year={'Year :':f"{int(page.views[-1].controls[0].controls[0].value)}-{int(page.views[-1].controls[0].controls[0].value)+4}"}
        data=[{'Reg No :':reg_no},{'Student Name :':e.control.data['student_name'].title()},{'Dep :':department.current.value},sem_or_year,{'Mobile Number :':e.control.data['student_ph_no']},{'Parent Mobile Number':e.control.data['parent_ph_no']}]
        adp=len(e.control.data['presents'])-1
        page.views.append(student_card_view(view_pop_handler,page.width,data,adp))
        page.update()
        adp=requests_manager('/calculate-student-attedence',requests.get,{'nod_student_present':len(e.control.data['presents'])-1,'dep':department.current.value,'sem':semester.current.value},False,False)

    
    appbar=AppBar(
        automatically_imply_leading=False,
        title=Column(
            controls=[
                Row(
                    controls=[
                        Image(
                            src='https://www.lathamathavan.edu.in/wp-content/uploads/2021/11/cropped-LOGO-150x150.png',
                            width=50,
                            height=50,
                            border_radius=50
                        ),
                        Text('L M E C',color='black',size=20,weight=FontWeight.W_700,text_align=TextAlign.CENTER)
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                ResponsiveRow(
                    controls=[
                        IconButton(col=2,icon=icons.ARROW_BACK,icon_size=30,icon_color='black',on_click=view_pop_handler),
                        SearchBar(
                            col=8,
                            height=40,
                            bar_bgcolor='white',
                            bar_hint_text='search students here...',
                            bar_text_style=TextStyle(weight=FontWeight.W_700,color='black'),
                            bar_hint_text_style=TextStyle(weight=FontWeight.W_700,color='grey'),
                            view_header_text_style=TextStyle(weight=FontWeight.W_700,color='black'),
                            view_hint_text_style=TextStyle(weight=FontWeight.W_700,color='black'),
                            bar_trailing=[
                                Icon(name=icons.SEARCH,color='black')
                            ],
                            on_change=search_students,
                            
                        ),
                        IconButton(col=2,icon=icons.UPLOAD_OUTLINED,icon_size=30,icon_color='black',on_click=send_attedence)
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY
                ),
                    
            ],
            
        ),
        center_title=False,
        bgcolor=colors.CYAN_200,
        toolbar_height=150

    )

    def view_handler(e):
        global attedence_dict,delete_list
        appbar.title.controls[1].controls[1].value=''
        attedence_dict=dict()
        delete_list.clear()

        if e.control.key=='next':
            if department.current.value and semester.current.value:
                department.current.error_text=""
                semester.current.error_text=""
                bs.content=Column(
                        width=400,
                        height=200,
                        controls=[
                            TextFields('Enter The Passsword',None,'black',ispassword=True),
                            Row([TextButton('Forgot Password ?',style=ButtonStyle(color='red'),on_click=view_handler,key='Forgot Page')],alignment=MainAxisAlignment.CENTER),
                            OutlinedButton('verify',on_click=send_attedence,key='verify_user',style=ButtonStyle(color='black'))
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    )
                bs.open=True
                
            else:
                if department.current.value==None:
                    semester.current.error_text=""
                    department.current.error_style=TextStyle(color='red',weight=FontWeight.W_600)
                    department.current.error_text="couldn't be empty"
                else:
                    department.current.error_text=""
                    semester.current.error_style=TextStyle(color='red',weight=FontWeight.W_600)
                    semester.current.error_text="couldn't be empty"

        elif e.control.key=='Forgot Page':
            bs.open=False
            page.update()
            time.sleep(0.2)
            page.views.append(forgot_password_view(view_pop_handler,page.width,send_attedence,'send_password'))

        elif e.control.key in ['Take Attedence','Edit Attedence']:
            appbar.title.controls[1].controls[2].icon=icons.UPLOAD_OUTLINED
            appbar.title.controls[1].controls[2].key=e.control.key
            page.views.append(take_attedence_view(attedence_list_lv,appbar,False,checkbox_handler))
            page.update()
            attedence_list_lv.current.controls.insert(0,ProgressBar(height=8,color="cyan", bgcolor="white"))
            page.update()
            if e.control.key=='Take Attedence':
                attedence_dict=requests_manager('/show-all-student-details',requests.get,{'dep':department.current.value,'sem':semester.current.value,'isforattedence':True},False,False)
                attedence_list_lv.current.controls.pop(0)
                page.update()
                
                if isinstance(attedence_dict,dict):
                    for i in list(attedence_dict.keys()):
                        reg_no=i
                        name=attedence_dict.get(i).get('student_name')
                        attedence_dict[reg_no]='False'
                        attedence_list_lv.current.controls.append(AttedenceContainerCreator(str(reg_no),name.title(),checkbox_handler))
                        page.update()
                else:
                    icon=icons.VERIFIED_OUTLINED
                    color='green'
                    if attedence_dict=='Please Check Your Connection !':
                        icon=icons.WIFI_OFF_OUTLINED
                        color='red'
                    if attedence_dict!=None:
                        page.views.pop()
                        page.views.append(successfull_message_view(view_pop_handler,page.width,attedence_dict,icon,color))
            else:
                edit_attedence=requests_manager('/show-particular-date-student-details',requests.get,{'dep':department.current.value,'sem':semester.current.value,'date_of_student_details':date.today().strftime("%d-%m-%Y"),'isforeditattedence':True},False,False)
                attedence_list_lv.current.controls.pop(0)
                page.update()
                ispresent=False
                
                if isinstance(edit_attedence,dict):
                    for i in list(edit_attedence.keys()):
                        if i=='presents':
                            ispresent=True
                        else:
                            ispresent=False
                        for j in edit_attedence.get(i):
                            key=list(j.keys())[0]
                            reg_no=key
                            name=j.get(key).get('student_name')
                            attedence_dict[reg_no]=str(ispresent)
                            attedence_list_lv.current.controls.append(AttedenceContainerCreator(str(reg_no),name.title(),checkbox_handler,ispresent))
                            page.update()
                else:
                    icon=icons.ERROR_OUTLINE
                    color='red'
                    if edit_attedence=='Please Check Your Connection !':
                        icon=icons.WIFI_OFF_OUTLINED
                    if edit_attedence!=None:
                        page.views.pop()
                        page.views.append(successfull_message_view(view_pop_handler,page.width,edit_attedence,icon,color))

        elif e.control.key in ['Delete Current SD','Delete Old SD']:
            appbar.title.controls[1].controls[2].icon=icons.DELETE_OUTLINE
            appbar.title.controls[1].controls[2].key=e.control.key
            page.views.append(take_attedence_view(attedence_list_lv,appbar,True,checkbox_handler))
            page.update()
            
            if e.control.key=='Delete Current SD':
                attedence_list_lv.current.controls.insert(0,ProgressBar(height=8,color="cyan", bgcolor="white"))
                page.update()
                attedence_dict=requests_manager('/show-all-student-details',requests.get,{'dep':department.current.value,'sem':semester.current.value,'isforattedence':False},False,False) 
                attedence_list_lv.current.controls.pop(0)
                page.update()
            else:  
                ad.title=YearChoosingDropDown(year_intial_value=2020,year_final_value=int(date.today().strftime('%Y')))
                ad.actions[0].text='Submit'
                ad.actions[0].key='old'
                ad.open=True
             
            if isinstance(attedence_dict,dict):
                for i in list(attedence_dict.keys()):
                    reg_no=i
                    name=attedence_dict.get(i).get('student_name')
                    attedence_list_lv.current.controls.append(AttedenceContainerCreator(reg_no,name.title(),checkbox_handler,checkbox_key='delete'))
            else:
                icon=None
                color=None
                if attedence_dict=='Please Check Your Connection !':
                    icon=icons.WIFI_OFF_OUTLINED
                    color='red'
                if attedence_dict !=None:
                    page.views.append(successfull_message_view(view_pop_handler,page.width,attedence_dict,icon,color))
           

        elif e.control.key in ['View Current SD','View Old SD']:
            appbar.title.controls[1].controls[2].icon=icons.DOWNLOAD_OUTLINED
            appbar.title.controls[1].controls[2].key=e.control.key
            page.views.append(take_attedence_view(attedence_list_lv,appbar,False,checkbox_handler))
            page.update()
            if e.control.key=='View Current SD':
                page.views[-1].controls.insert(
                    0,
                    Row(
                        controls=[
                            Container(
                                border=border.all(1,'black'),
                                width=150,
                                height=40,
                                content=Text(date.today().strftime('%d-%m-%Y'),weight=FontWeight.W_700,color='black',size=18,text_align=TextAlign.CENTER),
                                on_click=lambda e:page.open(dp),
                                border_radius=20,
                                shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                                alignment=Alignment(0,0),
                                margin=margin.all(10)
                            )
                        ]
                    )                         
                )
                page.update()
                
                current_view_fun(date.today().strftime("%d-%m-%Y"))
                
            else:
                ad.title=YearChoosingDropDown(year_intial_value=2020,year_final_value=int(date.today().strftime('%Y')))
                ad.actions[0].text='Submit'
                ad.actions[0].key='oldview'
                ad.open=True
                page.update()
        elif e.control.key in ['Add SD','Edit SD']:
            btn_txt='Add'
            if e.control.key=='Edit SD':
                btn_txt='Update'
            page.views.append(add_student_detail_view(view_pop_handler,page.width,add_or_edit_student_details,btn_txt))

        page.update()

    def ad_action_btns(e):
        ad.open=False
        if e.control.key=='old':
            old_view_and_delete_fun(True,None,'delete',checkbox_handler,ad.title.value,False)

        elif e.control.key=='viewold':
            print(page.views[-1].controls[0].controls[0].value)
            old_view_and_delete_fun(False,show_student_details,None,None,page.views[-1].controls[0].controls[0].value,False)

        elif e.control.key=='oldview':
            old_view_and_delete_fun(False,show_student_details,None,None,ad.title.value,True)
            page.update()

        elif e.control.key=='movetonextsem':
            ad.actions[0].text='Moving...'
            ad.actions[0].disabled=True
            ad.actions[0].update()
            res=requests_manager('/move-to-next-sem',requests.put,{'dep':department.current.value},False,True)
            icon=icons.VERIFIED_OUTLINED
            color='green'
            if res=='Please Check Your Connection !':
                icon=icons.WIFI_OFF_OUTLINED
                color='red'
            
            ad.actions[0].text='Move'
            ad.actions[0].disabled=False
            ad.open=False
            ad.update()
            time.sleep(0.2)
            page.views.append(successfull_message_view(view_pop_handler,page.width,res,icon,color))
            print(res)

        page.update()

    ad=AlertDialog(
        alignment=Alignment(0,0),
        bgcolor='white',
        actions=[
            OutlinedButton(text='Submit',on_click=ad_action_btns,style=ButtonStyle(color='black',bgcolor=colors.WHITE30),key='old')
        ],
        actions_alignment=MainAxisAlignment.CENTER

    )
    page.overlay.append(ad)

    def add_or_edit_student_details(e):
        btn_txt=e.control.key
        sending_btn_txt='Adding...'
        route='/add-student-details'
        method=requests.post
        if e.control.key=='Update':
            sending_btn_txt='Updating...'
            route='/update-student-student-details'
            method=requests.put

        page.views[-1].controls[0].content.controls[2].controls[0].content.controls[4].controls[0].text=sending_btn_txt
        page.views[-1].controls[0].content.controls[2].controls[0].content.controls[4].controls[0].disabled=True
        page.update()
        try:
            reg_no=int(page.views[-1].controls[0].content.controls[2].controls[0].content.controls[0].value)
            name=page.views[-1].controls[0].content.controls[2].controls[0].content.controls[1].value
            spn=int(page.views[-1].controls[0].content.controls[2].controls[0].content.controls[2].value)
            ppn=int(page.views[-1].controls[0].content.controls[2].controls[0].content.controls[3].value)
            if name!="":
                res=requests_manager(route,method,{'dep':department.current.value,'sem':semester.current.value,'reg_no':reg_no,'student_name':name,'student_ph_no':spn,'parent_ph_no':ppn},False,True)
                page.views[-1].controls[0].content.controls[2].controls[0].content.controls[1].value=""
                page.views[-1].controls[0].content.controls[2].controls[0].content.controls[2].value=""
                page.views[-1].controls[0].content.controls[2].controls[0].content.controls[3].value=""
                page.views[-1].controls[0].content.controls[2].controls.insert(
                    0,
                    InformationContainer(msg=res)
                )
                page.update()
                time.sleep(1)
                page.views[-1].controls[0].content.controls[2].controls.pop(0)
                
            else:
                page.views[-1].controls[0].content.controls[2].controls.insert(
                    0,
                    InformationContainer(msg="input field couldn't be empty".title(),bgcolor='red',icon=icons.REPORT_GMAILERRORRED_OUTLINED)
                )
                page.update()
                time.sleep(1)
                page.views[-1].controls[0].content.controls[2].controls.pop(0)
                print("input field couldn't be empty")
                page.update()
        except:
            page.views[-1].controls[0].content.controls[2].controls.insert(
                    0,
                    InformationContainer(msg="input field couldn't be empty".title(),bgcolor='red',icon=icons.REPORT_GMAILERRORRED_OUTLINED)
                )
            page.update()
            time.sleep(1)
            page.views[-1].controls[0].content.controls[2].controls.pop(0)
            print('input field couldnt br empty')
        finally:
            page.views[-1].controls[0].content.controls[2].controls[0].content.controls[4].controls[0].text=btn_txt
            page.views[-1].controls[0].content.controls[2].controls[0].content.controls[4].controls[0].disabled=False
        page.update()

    def bottom_sheet_handler(e):
        print(e.control.key)
        if e.control.key=='Add Or Edit SD':
            bs.content=Container(
                    height=200,
                    width=500,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=ResponsiveRow(
                    spacing=20,
                    controls=[
                        BottomSheetCntCreator(i,i,view_handler)
                        for i in ['Add SD','Edit SD']
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=CrossAxisAlignment.CENTER
                )
            )
            bs.open=True
            

        elif e.control.key=='Attedence':
            bs.content=Container(
                    height=200,
                    width=500,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=ResponsiveRow(
                    spacing=20,
                    controls=[
                        BottomSheetCntCreator(i,i,view_handler)
                        for i in ['Take Attedence','Edit Attedence']
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=CrossAxisAlignment.CENTER
                )
            )
            bs.open=True
            
        elif e.control.key=='Move to Next Sem':
            ad.title=Column(
                controls=[
                    Text('Are You Sure You Want To Move To Next Sem ?',weight=FontWeight.W_700,size=18,color='black',text_align=TextAlign.CENTER),
                    Text("Note : This Couldn't Be Undone",weight=FontWeight.W_700,size=18,color='red',text_align=TextAlign.CENTER)
                ]
            )
            ad.actions[0].text='Move'
            ad.actions[0].key='movetonextsem'
            ad.open=True
            

        elif e.control.key=='Delete':
            bs.content=Container(
                    height=200,
                    width=500,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=ResponsiveRow(
                    spacing=20,
                    controls=[
                        BottomSheetCntCreator(i,i,view_handler)
                        for i in ['Delete Current SD','Delete Old SD']
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=CrossAxisAlignment.CENTER
                )
            )
            bs.open=True
        elif e.control.key=='Download And View':
            bs.content=Container(
                    height=200,
                    width=500,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=ResponsiveRow(
                    spacing=20,
                    controls=[
                        BottomSheetCntCreator(i,i,view_handler)
                        for i in ['View Current SD','View Old SD']
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=CrossAxisAlignment.CENTER
                )
            )
            bs.open=True
        page.update()
    

    def home_view():
        return View(
            controls=[
                Container(
                    expand=True,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=Column(
                        controls=[
                            SafeArea(
                                content=Row(
                                    controls=[
                                        Image(
                                            src='https://www.lathamathavan.edu.in/wp-content/uploads/2021/11/cropped-LOGO-150x150.png',
                                            width=100,
                                            height=100,
                                            border_radius=100
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.CENTER
                                )
                            ),
                            Row(
                                controls=[
                                    Text('L M E C',color='black',size=20,weight=FontWeight.W_700,text_align=TextAlign.CENTER)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Column(
                                width=page.width,
                                controls=[
                                    Container(
                                        width=300,
                                        height=400,
                                        #blur=Blur(40,40,tile_mode=BlurTileMode.MIRROR),
                                        shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                                        border=border.all(2,'white'),
                                        alignment=Alignment(0,0),
                                        border_radius=30,
                                        padding=padding.all(10),
                                        margin=margin.all(20),
                                        content=Column(
                                            controls=[
                                                Dropdown(
                                                    ref=department,
                                                    options=[dropdown.Option(key=i,text=i) for i in ['CSE','ECE','EEE','MECH','CIVIL']],
                                                    label='Choose Department',
                                                    text_style=TextStyle(weight=FontWeight.W_700,color=colors.WHITE),
                                                    label_style=TextStyle(color='black',weight=FontWeight.W_600),
                                                    focused_border_color='black',
                                                    icon_enabled_color='black',
                                                    border_radius=20,
                                                    
                                                ),
                                                Dropdown(
                                                    ref=semester,
                                                    options=[dropdown.Option(key=f"SEM-{i}",text=f"SEM-{i}") for i in range(1,9)],
                                                    label='Choose Semester',
                                                    text_style=TextStyle(weight=FontWeight.W_700,color='white'),
                                                    label_style=TextStyle(color='black',weight=FontWeight.W_600),
                                                    focused_border_color='black',
                                                    icon_enabled_color='black',
                                                    border_radius=20,
                                                    item_height=80,
                                                    enable_feedback=True
                                                    

                                                ),
                                                ElevatedButton(
                                                    text='Next',
                                                    icon=icons.ARROW_FORWARD_IOS,
                                                    width=130,
                                                    height=40,
                                                    style=ButtonStyle(color='white'),
                                                    key='next',
                                                    on_click=view_handler
                                                    
                                                )
                                            ],
                                            alignment=MainAxisAlignment.CENTER,
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            spacing=40
                                        )
                                        
                                    )
                                ],
                                expand=True,
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER
                            )
                           
                        ]
                    )
                )
            ]
        )
    
    page.views.append(home_view())
    page.on_view_pop=view_pop_handler
    page.update()
    
app(main)