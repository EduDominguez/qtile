# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Modified by E.D.G

import os
import subprocess
import requests 

from libqtile import hook
from typing import List  
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "terminator" 

###Keys###      
keys = [
    # Important: remind existing of a list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "control"], "m", lazy.layout.maximize(), desc='toggle window between minimum and maximum sizes' ),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn('rofi -combi-modi window,drun,ssh -show combi -location 0 '), desc="Spawn rofi"),

    # User programs
    Key([mod], "c", lazy.spawn("chromium"), desc="Spawn chromium"),
    Key([mod], "f", lazy.spawn("firefox"), desc="Spawn firefox"),
    Key([mod], "d", lazy.spawn("code"), desc="Spawn code"),
    Key([mod], "n", lazy.spawn("nitrogen"), desc="Spawn nitrogen"),
    Key([mod], "u", lazy.spawn('terminator -e "unimatrix -s 93 -a -f -o"'), desc="Spawn unimatrix"),
    Key([mod], "p", lazy.spawn('terminator -e "cd /opt/pycharm-community-2021.3/bin;./pycharm.sh"'), desc="Spawn pycharm"),
    Key([mod], "t", lazy.spawn('thunar'), desc="Spawn thunar"),
    Key([mod], "o", lazy.spawn('libreoffice'), desc="Spawn libreoffice"),
    Key([mod], "b", lazy.spawn('thunderbird'), desc="Spawn thunderbird"),
    Key([mod], "v", lazy.spawn('copyq'), desc="Spawn copyq"),    



    
    # Special Keys (atajos de teclado)
    Key([], "XF86AudioRaiseVolume", lazy.spawn('sh -c "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 +5%"'), desc="Raise volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn('sh -c "pactl set-sink-mute 0 false ; pactl set-sink-volume 0 -5%"'), desc="Lower volume"),
    Key([], "XF86AudioMute", lazy.spawn('pactl set-sink-mute 0 toggle'), desc="Mute volume"),
    Key([], "XF86AudioMicMute", lazy.spawn('pactl set-source-mute 1 toggle'), desc="Mute mic"),

        #ThinkPad T470 haven't play/pause and previous/next keys, so I use this:
    Key([mod], "Up", lazy.spawn('playerctl play-pause'), desc="Play-Pause"),
    Key([mod], "Down", lazy.spawn('playerctl play-pause'), desc="Play-Pause"),
    Key([mod], "Right", lazy.spawn('playerctl next'), desc="Next"),
    Key([mod], "Left", lazy.spawn('playerctl previous'), desc="Previous"),

    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause'), desc="Play-Pause"),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next'), desc="Play-Pause"),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous'), desc="Play-Pause"),
 
    Key([], "XF86MonBrightnessDown", lazy.spawn('xbacklight -dec 10'), desc="Bright down"),
    Key([], "XF86MonBrightnessUp", lazy.spawn('xbacklight -inc 10'), desc="Bright up"),

    Key([], "XF86Display", lazy.spawn('arandr'), desc="Display"),


    Key([], "XF86Bluetooth", lazy.spawn('blueman-applet'), desc="Bluetooth"), 

    Key([], "Print", lazy.spawn('sh -c "import -window root ~/Screenshots/$(date "+%Y%m%d-%H%M%S").jpg"'), desc="Screenshot"),
    Key(["control"], "Print", lazy.spawn('spectacle'), desc="Spectacle"), #Also a like use spectacle for my screenshots
]





###Groups###
groups = [Group(i) for i in [
    "", "", "", "", "懶", "", "", "", "",  
]]

for i, group in enumerate(groups):  
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])




###Layouts###
layout_theme = {"border_width": 3,
                "margin": 16,
                "border_focus": "#268bd2",
                "border_normal": "#000000"
                }


layouts = [
    layout.Columns(**layout_theme, single_border_width=0),
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Max(**layout_theme),
]

     

###Widgets###
widget_defaults = dict(
    font='Cantarell Bold',
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar( 
            [
                widget.TextBox( 
                    foreground = "#268bd2",
                    text = "",
                    fontsize = 35,
                    padding = 5,
                    mouse_callbacks = {"Button1": lazy.spawn('terminator -e bpytop')},
                ),
                 
                widget.GroupBox(
                    fontsize=30,
                    highlight_method='text',
                    rounded=True,
                    this_current_screen_border="#30D5AA",     
                    this_screen_border="#366E9D",
                    other_current_screen_border="#1ED495",
                    other_screen_border="#1ED495",
                ),
                
                widget.CurrentLayoutIcon(
                    foreground = "#FFFFFF",
                    scale = 0.5,
                ), 
                
                widget.Prompt(), 
                
                widget.WindowName(
                    foreground = "#FFFFFF",
                ),
                            
                widget.WidgetBox( 
                    text_closed = "", 
                    text_open = "",
                    fontsize = 30,
                    padding = 10,
                    widgets=[
                        widget.Image( #Microsft Teams
                            filename = "~/Iconos/teams.png",
                            margin = 6,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('teams')}
                            ),

                        widget.Image( #Zoom
                            filename = "~/Iconos/zoom.png",
                            margin = 3,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('zoom')}
                            ),

                        widget.Image( #Pycharm
                            filename = "~/Iconos/pycharm.png",
                            margin = 3,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('terminator -e "cd /opt/pycharm-community-2021.3/bin;./pycharm.sh"')}
                            ),

                        widget.Image( #Visual Code
                            filename = "~/Iconos/code.png",
                            margin = 3,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('code')}
                            ),

                        widget.Image( #Oracle VBox
                            filename = "~/Iconos/vbox.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('virtualbox')}
                            ),

                        widget.Image( #LibreOffice
                            filename = "~/Iconos/office.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('libreoffice')}
                            ),

                        widget.Image( #TexStudio
                            filename = "~/Iconos/texstudio.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('texstudio')}
                            ),

                        widget.Image( #Joplin
                            filename = "~/Iconos/joplin.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('joplin-desktop')}
                            ),
                        
                        widget.Image( #Chromium
                            filename = "~/Iconos/chromium.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('chromium')}
                            ),

                        widget.Image( #Midori
                            filename = "~/Iconos/midori.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('midori')}
                            ),

                        widget.Image( #Opera
                            filename = "~/Iconos/opera.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('opera')}
                            ),

                        widget.Image( #Firefox
                            filename = "~/Iconos/firefox.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('firefox')}
                            ),

                        widget.Image( #ThunderBird
                            filename = "~/Iconos/thunderbird.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('thunderbird')}
                            ),

                        widget.Image( #VLC
                            filename = "~/Iconos/vlc.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('vlc')}
                            ),

                        widget.Image( #PulseEffects
                            filename = "~/Iconos/pulse.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('pulseeffects')}
                            ),
                            
                        widget.Image( #whatsapp web
                            filename = "~/Iconos/whatsapp.png",
                            margin = 3,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('chromium -new-window https://web.whatsapp.com/')}
                            ), 
                            
                        widget.Image( #Telegram Web
                            filename = "~/Iconos/telegram.png",
                            margin = 3,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('chromium --new-window https://web.telegram.org/k/')}
                            ), 
                            
                        widget.Image( #Gimp
                            filename = "~/Iconos/gimp.png",
                            margin = 4,
                            #margin_x = 0 ,
                            #margin_y = 0,
                            mouse_callbacks = {"Button1": lazy.spawn('gimp')}
                            ),
                            
                        widget.TextBox(  #Button that open a directory (external drive when is plug)
                            font = "UbuntuMono",
                            text = "",    
                            fontsize = 30,
                            padding = 5,
                            mouse_callbacks = {"Button1": lazy.spawn('terminator -e "cd /run/media/edu/Samsung_T5/ && setsid thunar "')}  ##thunar --new-window run/media/edu/Samsung_T5/
                            ),
                            
                        widget.TextBox(  #button that open my Desktop
                            font = "UbuntuMono",
                            text = "",    
                            fontsize = 26,
                            padding = 5,
                            mouse_callbacks = {"Button1": lazy.spawn('terminator -e "cd /home/edu/Desktop && setsid thunar "')}  
                            ),
                            
                        widget.TextBox(
                            font = "UbuntuMono",
                            text = "",
                            fontsize = 25,
                            padding = 5,
                            mouse_callbacks = {"Button1": lazy.spawn('terminator -e "cd /home/edu/Desktop/Medicina && setsid thunar "')}
                            ),
                            
                        widget.TextBox(
                            font = "UbuntuMono",
                            text = "",
                            fontsize = 25,
                            padding = 5,
                            mouse_callbacks = {"Button1": lazy.spawn('terminator -e "cd /home/edu/Desktop/Medicina/Calendario && setsid thunar "')}
                        ),
                    ]
                ), 
                                       
                widget.Systray(
                        padding = 5,
                ),      
                widget.Clock( 
                    format ='%A, %d/%m/%Y',
                    padding = 5,
                    mouse_callbacks = {"Button1": lazy.spawn('terminator -e "calcurse"')}
                ),                            
                widget.Clock( 
                    format='%H:%M:%S ',
                    padding = 5,
                ),
                widget.TextBox( #Button to open sistem config menu bash script
                    font = "UbuntuMono",
                    text = "", 
                    foreground = "#F1AE1B",
                    fontsize = 27,
                    padding = 2,
                    mouse_callbacks = {"Button1": lazy.spawn('terminator -e ./menu.sh')}
                ),
                widget.TextBox( #Button to reboot
                    font = "UbuntuMono",
                    text = "",   #"ﰇ",
                    foreground = "#59C837",
                    fontsize = 27,
                    padding = 2,
                    mouse_callbacks = {"Button1": lazy.spawn('terminator -e "sudo reboot now"')}
                ),
                widget.QuickExit( #Button to Shutdown
                    padding = 2,
                    foreground = "#E9524A",
                    default_text = "", #'⏻',
                    countdown_format = '鈴',
                    fontsize = 32,
                ),                
            ], 
            28, background= "#171D2A", margin=[10, 16, 0, 16]  # N E S W
           ),
    ),
]

###Drag floating layouts###
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"





