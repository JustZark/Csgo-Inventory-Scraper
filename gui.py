from row_manager import RowManager
from user import User
import dearpygui.dearpygui as dpg

class ScraperGui:
   def __init__(self):
        self.actual_user = None
        self.row_manager = RowManager()

        dpg.create_context()
        dpg.create_viewport(title='CS:GO Inventory', height = 661, width = 735, resizable=False, decorated=False, x_pos=200, y_pos=20)

        with dpg.window(label="Inventory", width=735, height=661, pos=(0,0), no_close=True, no_collapse=True, no_resize=True, no_scrollbar=True, no_move=True):
           with dpg.group(horizontal=True):
              dpg.add_text("Steam ID:")
              dpg.add_input_text(width=140, tag='user_input')
              dpg.add_button(label="Scrape", callback=self._log)

              dpg.add_spacer(height=1)

           with dpg.child_window(autosize_x=True, height=603, no_scrollbar=True):
              with dpg.child_window(autosize_x=True, height=200, tag='user_window'):
                with dpg.group(horizontal=True, tag='user_details'):
                  self.load_image('media/default_user.jpg', 'user_details', 'user_avatar')
                  with dpg.group():
                      dpg.add_text("Name", tag='user_name')
                      dpg.add_separator()
                      dpg.add_spacer(height=5)
                      with dpg.group(horizontal=True):
                         dpg.add_text("Nickname:")
                         dpg.add_text("", tag='user_nick')
                      with dpg.group(horizontal=True):
                         dpg.add_text("ID: ")
                         dpg.add_text("", tag='user_id')

              dpg.add_child_window(autosize_x=True, autosize_y=True, height=300, tag='inventory_window', no_scrollbar=True)
              dpg.add_group(tag='row_0', parent='inventory_window', horizontal=True)
                        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

   def _log (self, sender, data):
       #print(f"Sender: {sender}, Data: {data}")

       if sender == 25:
           self.load_user(dpg.get_value('user_input'))

   def load_user(self, user_nickname):
       self.actual_user = User(user_nickname)

       self.uptdate_avatar()

       dpg.set_value(item='user_name', value=self.actual_user.steam_name)
       dpg.set_value('user_nick', value=self.actual_user.vanityurl)
       dpg.set_value('user_id', value= self.actual_user.steam_id)

       for item in self.actual_user.inventory.items:
           self.create_placeholder(item)

   def uptdate_avatar(self):
       width, height, channels, data = dpg.load_image('media/user_avatar.jpg')
       dpg.set_value("user_avatar", data)

   def load_image(self, image_path, parent, texture_id):
       width, height, channels, data = dpg.load_image(image_path)

       with dpg.texture_registry() as reg_id:
           texture_id = dpg.add_dynamic_texture(width, height, data, parent=reg_id, tag=texture_id)

       return dpg.add_image(texture_id, parent=parent)

   def create_placeholder(self, item_processed):
       if self.row_manager.increment_index() == True:
           dpg.add_group(horizontal=True, tag=f"row_{self.row_manager.row_number}", parent='inventory_window')

       dpg.add_child_window(tag=f"{item_processed.item_id}_placeholder", parent=f"row_{self.row_manager.row_number}", height=200, width=166, no_scrollbar=True)
       self.load_image(f'media/weapon_skins/{item_processed.item_id}.png', f"{item_processed.item_id}_placeholder", item_processed.item_id)
       dpg.add_text(item_processed.name, parent=f"{item_processed.item_id}_placeholder")
       dpg.add_text("$" + item_processed.price, parent=f"{item_processed.item_id}_placeholder")



