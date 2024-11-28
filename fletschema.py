from flet import *

class BottomSheetCntCreator(Container):
    def __init__(self,text,key,click):
        super().__init__()
        self.col=6
        self.content=Text(text,weight=FontWeight.W_700,text_align=TextAlign.CENTER,color='black')
        self.width=130
        self.height=50
        self.shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER)
        self.border_radius=30
        self.alignment=Alignment(0,0)
        self.margin=margin.all(10)
        self.border=border.all(1.5,'white')
        self.key=key
        self.on_click=click

class AttedenceContainerCreator(Container):
    def __init__(self,reg_no,name,checkbox_handler=None,checkbox_value=False,checkbox_key='attedence',ischeckboxdisabeld=False,checkboxfillcolor=None,cnt_data=None,ischeckboxvisibel=True,cnt_onclick=None):
        super().__init__()
        self.height=100
        self.margin=margin.all(5)
        self.padding=padding.all(20)
        self.shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER)
        self.border_radius=10
        self.data=cnt_data
        self.on_click=cnt_onclick
        self.content=Row(
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Text(reg_no,size=20,weight=FontWeight.W_700,color='black'),
                        Text(name,size=20,weight=FontWeight.W_700,color='black')
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
                
                Row(
                    controls=[
                        Checkbox(
                            check_color='white',
                            active_color='green',
                            border_side=BorderSide(1,'black'),
                            on_change=checkbox_handler,
                            data=reg_no,
                            key=checkbox_key,
                            value=checkbox_value,
                            disabled=ischeckboxdisabeld,
                            fill_color=checkboxfillcolor,
                            visible=ischeckboxvisibel
                        )
                    ]
                )   
            ]
        )

class InformationContainer(Container):
    def __init__(self,bgcolor='green',icon=icons.VERIFIED_USER_OUTLINED,msg=None):
        super().__init__()
        self.content=Row(controls=[Icon(icon,color='white'),Text(msg,size=15,color='white',weight=FontWeight.W_700,text_align=TextAlign.CENTER)],alignment=MainAxisAlignment.CENTER)
        self.shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER)
        self.padding=padding.all(10)
        self.bgcolor=bgcolor
        self.width=300
        self.border_radius=10


                
class YearChoosingDropDown(Dropdown):
    def __init__(self,onchange=None,year_intial_value=None,year_final_value=None,key=None,width=None,height=None,value=None):
        super().__init__()
        self.options=[
            dropdown.Option(i,i)
            for i in range(year_intial_value,year_final_value+1)
        ]
        self.text_style=TextStyle(weight=FontWeight.W_700,color='black')
        self.label_style=TextStyle(weight=FontWeight.W_700,color='black')
        self.bgcolor='white'
        self.focused_border_color='black'
        self.icon_enabled_color='black'
        self.border_radius=20
        self.item_height=80
        self.key=key
        self.on_change=onchange
        self.width=width
        self.height=height
        self.alignment=Alignment(0,0)
        self.value=value
        self.padding=padding.all(-5)
        self.label='Choose Year...'
     
         

class TextFields(TextField):
    def __init__(self,label=None,hinttext=None,colour='white',autofocus=False,ispassword=False):
        super().__init__()
        self.width=200
        self.border=InputBorder.UNDERLINE
        self.label=label
        self.hint_text=hinttext
        self.label_style=TextStyle(weight=FontWeight.W_700,size=13,color=colour)
        self.hint_style=TextStyle(weight=FontWeight.W_600,size=13,color=colour)
        self.text_style=TextStyle(weight=FontWeight.W_700,size=15,color=colour)
        self.border_color=colour
        self.border_width=2
        self.text_align=TextAlign.CENTER
        self.cursor_color=colour
        self.autofocus=autofocus
        self.password=ispassword
        self.can_reveal_password=ispassword
        self.error_style=TextStyle(color='red',weight=FontWeight.W_600)