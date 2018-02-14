import PysideDockUI as pw
import Test_UI as test_ui
reload(test_ui)
# Not Docking
pw.create_window(test_ui.Test_UI)

#Docking
pw.dock_window(test_ui.Test_UI)