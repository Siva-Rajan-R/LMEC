from flet import *

def main_home_view(view_pop,width,bottom_sheet):

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
                                    Row(controls=[IconButton(icon=icons.ARROW_BACK,icon_size=30,icon_color='black',on_click=view_pop)],alignment=MainAxisAlignment.START),
                                    Image(
                                        src='https://www.lathamathavan.edu.in/wp-content/uploads/2021/11/cropped-LOGO-150x150.png',
                                        width=100,
                                        height=100,
                                        border_radius=100
                                    ),
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER
                            )
                        ),
                        Row(
                            controls=[
                                Text('L M E C',color='black',size=20,weight=FontWeight.W_700,text_align=TextAlign.CENTER)
                            ],
                            alignment=MainAxisAlignment.CENTER
                        ),
                        Column(
                            width=width,
                            expand=True,
                            spacing=25,
                            controls=[
                                Container(
                                    height=50,
                                    width=200,
                                    border_radius=20,
                                    content=Text(i,weight=FontWeight.W_700,color='black'),
                                    border=border.all(1.5,'white'),
                                    shadow=BoxShadow(0,5,'grey',blur_style=ShadowBlurStyle.OUTER),
                                    alignment=Alignment(0,0),
                                    on_click=bottom_sheet,
                                    key=i
                                )
                                for i in ['Add Or Edit SD','Attedence','Delete','Move to Next Sem','Download And View']
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        )
                    ]
                )
            )
        ]
    )

