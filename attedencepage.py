from flet import *
from fletschema import TextFields
def take_attedence_view(reference,appbar,isdelete,checkbox_handler):
        return View(
            controls=[
                Row(
                    controls=[
                            Checkbox(
                                    label='Delete All',
                                    label_style=TextStyle(weight=FontWeight.W_700,color='black'),
                                    active_color='green',
                                    check_color='white',
                                    border_side=BorderSide(1,'grey'),
                                    key='delete_all',
                                    on_change=checkbox_handler
                            )
                        ],
                    alignment=MainAxisAlignment.END,
                    visible=isdelete
                ),    

                ListView(
                    ref=reference,
                )          
            ],
            appbar=appbar,
            scroll=ScrollMode.ADAPTIVE,
            bgcolor='white'
            
        )

def student_card_view(back,width,data):
    return View(
            controls=[
                Container(
                    expand=True,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=Column(
                        controls=[
                            SafeArea(
                                content=Column(
                                    controls=[
                                        Row(controls=[IconButton(icon=icons.ARROW_BACK,icon_size=30,icon_color='black',on_click=back)],alignment=MainAxisAlignment.START),
                                        Row(
                                            controls=[
                                                
                                                Image(
                                                    src='icon.png',
                                                    width=60,
                                                    height=60,
                                                    border_radius=60
                                                ),
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        )
                                    ]
                                )
                            ),
                            Row(
                                controls=[
                                    Text('L M E C',color='black',size=20,weight=FontWeight.W_700,text_align=TextAlign.CENTER)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Column(
                                controls=[
                                    Container(
                                        width=300,
                                        expand=True,
                                        #blur=Blur(100,100,tile_mode=BlurTileMode.MIRROR),
                                        border=border.all(1,'white'),
                                        shadow=BoxShadow(0,5,'black',blur_style=ShadowBlurStyle.OUTER),
                                        margin=margin.all(10),
                                        border_radius=20,
                                        padding=padding.all(10),
                                        content=Column(
                                            controls=[
                                                Row(
                                                    alignment=MainAxisAlignment.CENTER,
                                                    controls=[
                                                        Icon(name=icons.ACCOUNT_CIRCLE_OUTLINED,size=50,color='black')
                                                    ]
                                                ),
                                                Column(
                                                    spacing=15,
                                                    controls=[
                                                        ResponsiveRow(
                                                            controls=[
                                                                Text(list(i.keys())[0],col=6,weight=FontWeight.W_700,size=18,color='black'),
                                                                Text(list(i.values())[0],col=6,weight=FontWeight.W_700,size=18,color='black'),
                                                            ],
                                                            spacing=10
                                                        )
                                                        
                                                        for i in data
                                                    ]
                                                )
                                            ],
                                            
                                        )
                                    ),
                                    
                                ],
                                expand=True,
                                width=width,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            )
                            
                        ]
                    )
                )
            ],
            scroll=ScrollMode.ADAPTIVE
        )

def add_student_detail_view(back,width,btn_fun,btn_txt):
    return View(
         controls=[
              Container(
                   expand=True,
                   gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                   content=Column(
                        controls=[
                            SafeArea(
                                content=Column(
                                    controls=[
                                        Row(controls=[IconButton(icon=icons.ARROW_BACK,icon_size=30,icon_color='black',on_click=back)],alignment=MainAxisAlignment.START),
                                        Row(
                                            controls=[
                                                
                                                Image(
                                                    #icon.png
                                                    src='icon.png',
                                                    width=60,
                                                    height=60,
                                                    border_radius=60
                                                ),
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        )
                                    ]
                                )
                            ),
                            Row(
                                controls=[
                                    Text('L M E C',color='black',size=20,weight=FontWeight.W_700,text_align=TextAlign.CENTER)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Column(
                                 controls=[
                                      Container(
                                        width=300,
                                        expand=True,
                                        border=border.all(1,'white'),
                                        shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                                        margin=margin.all(10),
                                        border_radius=20,
                                        padding=padding.all(30),
                                        alignment=Alignment(0,0),
                                        content=Column(
                                             controls=[
                                                  TextFields(label='Enter Student Reg no',colour='black',keybordtype=KeyboardType.NUMBER),
                                                  TextFields(label='Enter Student Name',colour='black'),
                                                  TextFields(label='Enter Student Mobile No',colour='black',keybordtype=KeyboardType.NUMBER),
                                                  TextFields(label='Enter Parent Mobile No',colour='black',keybordtype=KeyboardType.NUMBER),
                                                Row(controls=[ElevatedButton(text=btn_txt,style=ButtonStyle(color='white'),on_click=btn_fun,key=btn_txt)],alignment=MainAxisAlignment.CENTER)
                                             ],
                                             width=width,
                                             spacing=35,
                                             expand=True,
                                             horizontal_alignment=CrossAxisAlignment.CENTER,
                                             alignment=MainAxisAlignment.CENTER,
                                             
                                        )
                                    )
                                 ],
                                 width=width,
                                 expand=True,
                                 horizontal_alignment=CrossAxisAlignment.CENTER,
                                 alignment=MainAxisAlignment.CENTER,
                                 scroll=ScrollMode.ADAPTIVE
                                 
                            )
                        ]
                   )
              )
         ],
    )

def successfull_message_view(back,width,message,icon_name,color):
     return View(
            controls=[
                Container(
                    expand=True,
                    gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                    content=Column(
                        controls=[
                            SafeArea(
                                content=Row(controls=[IconButton(icon=icons.ARROW_BACK,icon_size=30,icon_color='black',on_click=back)],alignment=MainAxisAlignment.START),
                                    
                            ),
                            Column(
                                controls=[
                                    Icon(icon_name,size=200,color=color),
                                    ResponsiveRow(controls=[Text(message.title(),text_align=TextAlign.CENTER,weight=FontWeight.W_700,color=color,size=30)],alignment=MainAxisAlignment.CENTER),
                                    ResponsiveRow(controls=[Text('Thank You !',text_align=TextAlign.CENTER,weight=FontWeight.W_700,color='green',size=30)],alignment=MainAxisAlignment.CENTER),
                                ],
                                expand=True,
                                width=width,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                alignment=MainAxisAlignment.CENTER,
                                scroll=ScrollMode.ADAPTIVE
                            )
                            
                        ]
                    )
                )
            ]
        )

def forgot_password_view(back,width,btn_fun,key):
     return View(
         controls=[
              Container(
                   expand=True,
                   gradient=LinearGradient(['white','cyan'],begin=alignment.top_center,end=alignment.bottom_center),
                   content=Column(
                        controls=[
                            SafeArea(
                                content=Column(
                                    controls=[
                                        Row(controls=[IconButton(icon=icons.ARROW_BACK,icon_size=30,icon_color='black',on_click=back)],alignment=MainAxisAlignment.START),
                                        Row(
                                            controls=[
                                                
                                                Image(
                                                    src='icon.png',
                                                    width=60,
                                                    height=60,
                                                    border_radius=60
                                                ),
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        )
                                    ]
                                )
                            ),
                            Row(
                                controls=[
                                    Text('L M E C',color='black',size=20,weight=FontWeight.W_700,text_align=TextAlign.CENTER)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Column(
                                 controls=[
                                      Container(
                                        width=300,
                                        expand=True,
                                        border=border.all(1,'white'),
                                        shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                                        margin=margin.all(10),
                                        border_radius=20,
                                        padding=padding.all(30),
                                        alignment=Alignment(0,0),
                                        content=Column(
                                             controls=[
                                                TextFields(label='Enter The Email',colour='black'),
                                                TextFields(label='Enter The Password',colour='black'),
                                                Row(controls=[ElevatedButton(text='Submit',style=ButtonStyle(color='white'),on_click=btn_fun,key=key)],alignment=MainAxisAlignment.CENTER)
                    
                                             ],
                                             width=width,
                                             spacing=35,
                                             expand=True,
                                             horizontal_alignment=CrossAxisAlignment.CENTER,
                                             alignment=MainAxisAlignment.CENTER,
                                             scroll=ScrollMode.ADAPTIVE
                                        )
                                    )
                                 ],
                                 width=width,
                                 expand=True,
                                 horizontal_alignment=CrossAxisAlignment.CENTER,
                                 alignment=MainAxisAlignment.CENTER,
                                 scroll=ScrollMode.ADAPTIVE
                            )
                        ]
                   )
              )
         ],
    )