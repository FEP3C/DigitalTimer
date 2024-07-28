import datetime
import time
import wx
import math
class ClockApp(wx.App):
    def __init__(self, show_analog_clock=False):
        super().__init__()
        
        self.show_analog_clock = show_analog_clock
        
        # 创建主窗口
        self.frame = wx.Frame(None, title="Essentiel Clock", size=(1120, 630))
        self.panel = wx.Panel(self.frame)

        # 设置字体样式
        font = wx.Font(100, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.time_text = wx.StaticText(self.panel, label=self.get_current_time(), pos=(0, 0), font=font)
        self.date_text = wx.StaticText(self.panel, label=self.get_current_date(), pos=(0, 100), font=font)

        # 添加模拟指针式时钟
        if self.show_analog_clock:
            self.analog_clock = AnalogClock(self.panel, (560, 315))

        # 添加菜单和按钮
        self.menu_bar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.exit_item = self.file_menu.Append(wx.ID_EXIT, "E&xit")
        self.menu_bar.Append(self.file_menu, "&File")

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time_and_date, self.timer)
        self.timer.Start(1000)  # 更新时间间隔为1秒

        self.Bind(wx.EVT_MENU, self.on_exit, self.exit_item)

        self.SetTopWindow(self.frame)
        self.frame.Show()

    def update_time_and_date(self, event):
        self.time_text.SetLabel(self.get_current_time())
        self.date_text.SetLabel(self.get_current_date())

    def get_current_time(self):
        return str(datetime.datetime.now().strftime("%H:%M:%S"))

    def get_current_date(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d"))

    def on_exit(self, event):
        self.timer.Stop()
        self.Destroy()

class AnalogClock(wx.Window):
    def __init__(self, parent, pos):
        super().__init__(parent, pos=pos, size=(500, 500))

        self.hour_hand = None
        self.minute_hand = None
        self.second_hand = None

        self.draw_clock()

    def draw_clock(self):
        dc = wx.ClientDC(self)
        dc.Clear()

        center_x, center_y = self.GetClientSize().Get()[:2]
        radius = min(center_x, center_y) * 0.75

        current_time = time.localtime(time.time())
        hour_angle = (current_time.tm_hour % 12) * 30 + current_time.tm_min / 2 + current_time.tm_sec / 120
        minute_angle = current_time.tm_min * 6 + current_time.tm_sec / 10
        second_angle = current_time.tm_sec * 6

        dc.SetPen(wx.Pen("BLACK", 1))
        dc.DrawCircle(center_x, center_y, radius)

        self.hour_hand = dc.DrawLine(center_x, center_y, center_x + radius * 0.6 * math.cos(math.radians(hour_angle)), center_y - radius * 0.6 * math.sin(math.radians(hour_angle)))
        self.minute_hand = dc.DrawLine(center_x, center_y, center_x + radius * 0.8 * math.cos(math.radians(minute_angle)), center_y - radius * 0.8 * math.sin(math.radians(minute_angle)))
        self.second_hand = dc.DrawLine(center_x, center_y, center_x + radius * 0.9 * math.cos(math.radians(second_angle)), center_y - radius * 0.9 * math.sin(math.radians(second_angle)))

if __name__ == "__main__":
    app = ClockApp(show_analog_clock=True)
    app.MainLoop()