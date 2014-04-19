import mugui
import mumusic
import mudb

# Start interface
interface = mugui.Interface("Mesh-Up", "900x600")
music_data = mudb.loadDB()
interface.startMenu(music_data)
interface.startScrollBox()
interface.startTargetButton()
interface.startMatchButton()







interface.startLoop()
