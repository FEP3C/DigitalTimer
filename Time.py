# digital_timer.py

import wx
import wx.adv
import time
import threading
import locale
import gettext

# Set up gettext
locale_dir = 'locales'
gettext.bindtextdomain('messages', locale_dir)
gettext.textdomain('messages')
_ = gettext.gettext

class DigitalTimer(wx.Frame):
    def __init__(self, parent, title):
        super(DigitalTimer, self).__init__(parent, title=title, size=(600, 400))
        
        self.locale = wx.Locale(wx.LANGUAGE_DEFAULT)
        self.init_ui()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)
        self.timer.Start(1000)
        
        self.stopwatch_timer = None
        self.stopwatch_running = False
        self.countdown_timer = None
        self.pomodoro_timer = None

    def init_ui(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.time_display = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.time_display.SetFont(font)
        hbox.Add(self.time_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.start_stop_btn = wx.Button(panel, label=_("Start Stopwatch"))
        self.start_stop_btn.Bind(wx.EVT_BUTTON, self.toggle_stopwatch)
        vbox.Add(self.start_stop_btn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.reset_btn = wx.Button(panel, label=_("Reset Stopwatch"))
        self.reset_btn.Bind(wx.EVT_BUTTON, self.reset_stopwatch)
        vbox.Add(self.reset_btn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.countdown_btn = wx.Button(panel, label=_("Start Countdown"))
        self.countdown_btn.Bind(wx.EVT_BUTTON, self.start_countdown_dialog)
        vbox.Add(self.countdown_btn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.pomodoro_btn = wx.Button(panel, label=_("Start Pomodoro"))
        self.pomodoro_btn.Bind(wx.EVT_BUTTON, self.start_pomodoro_dialog)
        vbox.Add(self.pomodoro_btn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        
        self.zen_mode_btn = wx.Button(panel, label=_("Enter Zen Mode"))
        self.zen_mode_btn.Bind(wx.EVT_BUTTON, self.toggle_zen_mode)
        vbox.Add(self.zen_mode_btn, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        
        hbox.Add(vbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        
        self.date_display = wx.StaticText(panel, label="", style=wx.ALIGN_LEFT)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.date_display.SetFont(font)
        
        vbox_bottom = wx.BoxSizer(wx.HORIZONTAL)
        vbox_bottom.Add(self.date_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        vbox_main = wx.BoxSizer(wx.VERTICAL)
        vbox_main.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vbox_main.Add(vbox_bottom, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        
        panel.SetSizer(vbox_main)
        
        self.create_menu_bar()
        
        self.Centre()
        self.Show(True)
        
    def create_menu_bar(self):
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        exit_item = file_menu.Append(wx.ID_EXIT, _("Exit"), _("Exit application"))
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        menubar.Append(file_menu, _("File"))
        
        lang_menu = wx.Menu()
        lang_menu.AppendRadioItem(1, "English")
        lang_menu.AppendRadioItem(2, "中文")
        lang_menu.AppendRadioItem(3, "Deutsch")
        lang_menu.AppendRadioItem(4, "Français")
        self.Bind(wx.EVT_MENU, self.switch_language, id=1)
        self.Bind(wx.EVT_MENU, self.switch_language, id=2)
        self.Bind(wx.EVT_MENU, self.switch_language, id=3)
        self.Bind(wx.EVT_MENU, self.switch_language, id=4)
        menubar.Append(lang_menu, _("Language"))
        
        settings_menu = wx.Menu()
        settings_item = settings_menu.Append(wx.ID_ANY, _("Settings..."), _("Application settings (Placeholder)"))
        self.Bind(wx.EVT_MENU, self.show_settings, settings_item)
        menubar.Append(settings_menu, _("Settings"))

        self.SetMenuBar(menubar)
        
    def update_time(self, event):
        current_time = time.strftime('%I:%M %p')
        self.time_display.SetLabel(current_time)
        
        current_date = time.strftime('Year: %Y       | Month: %m       | Day: %d')
        self.date_display.SetLabel(current_date)
        
    def toggle_stopwatch(self, event):
        if not self.stopwatch_running:
            self.start_stop_btn.SetLabel(_("Stop Stopwatch"))
            self.stopwatch_running = True
            self.start_stopwatch()
        else:
            self.start_stop_btn.SetLabel(_("Start Stopwatch"))
            self.stopwatch_running = False
            if self.stopwatch_timer:
                self.stopwatch_timer.Stop()
                
    def start_stopwatch(self):
        self.stopwatch_start_time = time.time()
        self.stopwatch_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_stopwatch, self.stopwatch_timer)
        self.stopwatch_timer.Start(100)
        
    def update_stopwatch(self, event):
        elapsed_time = time.time() - self.stopwatch_start_time
        self.time_display.SetLabel(time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
        
    def reset_stopwatch(self, event):
        self.stopwatch_running = False
        if self.stopwatch_timer:
            self.stopwatch_timer.Stop()
        self.start_stop_btn.SetLabel(_("Start Stopwatch"))
        self.time_display.SetLabel("00:00:00")
        
    def start_countdown_dialog(self, event):
        dlg = wx.TextEntryDialog(self, _("Enter countdown time in seconds:"), _("Countdown"))
        if dlg.ShowModal() == wx.ID_OK:
            countdown_time = int(dlg.GetValue())
            self.start_countdown(countdown_time)
        dlg.Destroy()
        
    def start_countdown(self, countdown_time):
        self.countdown_time = countdown_time
        self.countdown_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_countdown, self.countdown_timer)
        self.countdown_timer.Start(1000)
        
    def update_countdown(self, event):
        if self.countdown_time > 0:
            self.countdown_time -= 1
            self.time_display.SetLabel(time.strftime('%M:%S', time.gmtime(self.countdown_time)))
        else:
            self.countdown_timer.Stop()
            wx.MessageBox(_("Countdown finished!"), _("Info"), wx.OK | wx.ICON_INFORMATION)
        
    def start_pomodoro_dialog(self, event):
        dlg = wx.TextEntryDialog(self, _("Enter pomodoro time in minutes:"), _("Pomodoro"))
        if dlg.ShowModal() == wx.ID_OK:
            pomodoro_time = int(dlg.GetValue()) * 60
            self.start_pomodoro(pomodoro_time)
        dlg.Destroy()
        
    def start_pomodoro(self, pomodoro_time):
        self.pomodoro_time = pomodoro_time
        self.pomodoro_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_pomodoro, self.pomodoro_timer)
        self.pomodoro_timer.Start(1000)
        
    def update_pomodoro(self, event):
        if self.pomodoro_time > 0:
            self.pomodoro_time -= 1
            self.time_display.SetLabel(time.strftime('%M:%S', time.gmtime(self.pomodoro_time)))
        else:
            self.pomodoro_timer.Stop()
            wx.MessageBox(_("Pomodoro finished!"), _("Info"), wx.OK | wx.ICON_INFORMATION)
    
    def toggle_zen_mode(self, event):
        self.zen_mode = not hasattr(self, 'zen_mode') or not self.zen_mode
        if self.zen_mode:
            self.zen_mode_btn.SetLabel(_("Exit Zen Mode"))
            self.SetBackgroundColour(wx.BLACK)
            self.time_display.SetForegroundColour(wx.WHITE)
            self.date_display.SetForegroundColour(wx.WHITE)
        else:
            self.zen_mode_btn.SetLabel(_("Enter Zen Mode"))
            self.SetBackgroundColour(wx.NullColour)
            self.time_display.SetForegroundColour(wx.NullColour)
            self.date_display.SetForegroundColour(wx.NullColour)
        self.Refresh()
    
    def on_exit(self, event):
        self.Close(True)
        
    def show_settings(self, event):
        wx.MessageBox(_("Settings dialog placeholder"), _("Settings"), wx.OK | wx.ICON_INFORMATION)
        
    def switch_language(self, event):
        lang_id = event.GetId()
        if lang_id == 1:
            self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        elif lang_id == 2:
            self.locale = wx.Locale(wx.LANGUAGE_CHINESE)
        elif lang_id == 3:
            self.locale = wx.Locale(wx.LANGUAGE_GERMAN)
        elif lang_id == 4:
            self.locale = wx.Locale(wx.LANGUAGE_FRENCH)
        self.update_ui_language()
        
    def update_ui_language(self):
        self.start_stop_btn.SetLabel(_("Start Stopwatch"))
        self.reset_btn.SetLabel(_("Reset Stopwatch"))
        self.countdown_btn.SetLabel(_("Start Countdown"))
        self.pomodoro_btn.SetLabel(_("Start Pomodoro"))
        self.zen_mode_btn.SetLabel(_("Enter Zen Mode"))
        self.SetTitle(_("Digital Timer"))

if __name__ == "__main__":
    app = wx.App()
    locale.setlocale(locale.LC_ALL, '')
    _ = wx.GetTranslation
    DigitalTimer(None, title=_("Digital Timer"))
    app.MainLoop()
