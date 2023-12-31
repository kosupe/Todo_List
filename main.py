from class_file.Task_class import Task
from class_file.DB_class import DBClass

import flet as ft

class TodoApp(ft.UserControl):
    
    def build(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True, bgcolor=ft.colors.WHITE, 
                                     border_color=ft.colors.BLUE_900, border_width=1.5, focused_border_color=ft.colors.RED_400, max_length=34)
        self.tasks = ft.Column()
        tasks = DBClass.select_all()
        for task in tasks:
            self.tasks.controls.append(Task(task[1], self.task_delete, task[2], task[0]))
        
        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
            ],
        )
        
    def add_clicked(self, e):
        next_db_id = DBClass.select_next_id()
        task = Task(self.new_task.value, self.task_delete, 0, next_db_id)
        DBClass.insert(id=next_db_id, task_value=self.new_task.value, flg=0)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()
    
    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


def main(page: ft.Page):
    page.title   = "ToDo App"
    page.bgcolor = ft.colors.CYAN_100
    page.scroll  = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    todo = TodoApp()

    # add application's root control to the page
    page.add(todo)

ft.app(target=main)