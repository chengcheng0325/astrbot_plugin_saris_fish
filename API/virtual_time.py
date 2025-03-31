import time
from datetime import datetime, timedelta
import calendar

class VirtualClock:
    def __init__(self, start_real_time=None, start_virtual_time=None, time_ratio=12):
        """
        初始化虚拟时钟
        
        参数:
            start_real_time: 真实世界的参考时间(datetime对象)，默认为程序启动时间
            start_virtual_time: 虚拟时间的起始时间(datetime对象)，默认为程序启动时间
            time_ratio: 虚拟时间相对于真实时间的流逝比例，默认为12 (2小时=1虚拟天)
        """
        self.real_start = start_real_time if start_real_time else datetime.now()
        self.virtual_start = start_virtual_time if start_virtual_time else self.real_start
        
        # 时间流逝比例: 真实时间2小时 = 虚拟时间1天
        self.time_ratio = time_ratio  # 虚拟时间速度是真实时间的12倍 (24h/2h=12)

        self.moon_phases = {
            0: ("Moon-full.png", "满月"),
            1: ("Moon-2.png", "亏凸月"),
            2: ("Moon-3.png", "下弦月"),
            3: ("Moon-4.png", "残月"),
            4: ("Moon-new.png", "新月"),
            5: ("Moon-6.png", "娥眉月"),
            6: ("Moon-7.png", "上弦月"),
            7: ("Moon-8.png", "盈凸月")
        }

    def get_virtual_time(self):
        """获取当前的虚拟时间"""
        real_elapsed = datetime.now() - self.real_start
        virtual_elapsed = real_elapsed * self.time_ratio
        return self.virtual_start + virtual_elapsed

    def get_moon_phase(self, date):
        """
        计算给定日期的月相。使用简单的基于日期的估算方法。
        (更精确的月相计算需要更复杂的算法，这里使用简单的近似。)

        参数：
            date: datetime对象

        返回:
            (图像文件名, 月相名称) 
        """
        days_into_cycle = (date - datetime(2024,1,1)).days % 29.53  # 近似朔望月周期
        phase_index = int(days_into_cycle / (29.53 / 8)) % 8
        return self.moon_phases[phase_index]

    def get_virtual_clock_data(self):
        """
        获取当前的虚拟时钟数据，包括时间、日期、月相信息。

        返回：
            一个字典，包含以下键：
            - real_time (str): 真实时间，格式为 '%Y-%m-%d %H:%M:%S'
            - virtual_time (datetime): 虚拟时间，datetime对象
            - day_number (int): 虚拟日期是第几天
            - year (int): 虚拟年份
            - month (int): 虚拟月份
            - day (int): 虚拟日
            - weekday (str): 虚拟星期几（中文）
            - moon_phase_image (str): 月相图像文件名
            - moon_phase_name (str): 月相名称
        """
        virtual_now = self.get_virtual_time()
        real_now = datetime.now()

        # 使用中文星期几
        weekday_chinese = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][virtual_now.weekday()]

        moon_phase_image, moon_phase_name = self.get_moon_phase(virtual_now)

        return {
            "real_time": real_now.strftime('%Y-%m-%d %H:%M:%S'),
            "virtual_time": virtual_now,  # 返回datetime对象，而不是字符串
            "day_number": (virtual_now - self.virtual_start).days + 1,
            "year": virtual_now.year,
            "month": virtual_now.month,
            "day": virtual_now.day,
            "weekday": weekday_chinese,
            "moon_phase_image": moon_phase_image,
            "moon_phase_name": moon_phase_name
        }


    def run_clock(self, duration=10, interval=1):
        """运行虚拟时钟一段时间，并返回数据列表。

        参数：
            duration (int): 运行的秒数
            interval (int): 获取数据的间隔秒数

        返回:
            包含字典的列表，每个字典包含由`get_virtual_clock_data`函数提供的数据
        """
        data = []
        start_time = time.time()
        while time.time() - start_time < duration:
            data.append(self.get_virtual_clock_data())
            time.sleep(interval)
        return data



if __name__ == "__main__":
    # 可以自定义起始时间，例如:
    start_real = datetime(2025, 3, 31, 23, 0, 0)
    start_virtual = datetime(2025, 1, 1, 0, 0, 0)
    clock = VirtualClock(start_real,start_virtual,time_ratio=12)
    # clock = VirtualClock(start_real)


    # 获取一次虚拟时钟数据
    clock_data = clock.get_virtual_clock_data()
    print(clock_data)
    # 与 4:30 比较
    virtual_time = datetime.strptime("21:30:00", "%H:%M:%S").time()
    four_thirty = datetime.strptime("04:30:00", "%H:%M:%S").time()
    six_clock = datetime.strptime("06:00:00", "%H:%M:%S").time()
    nine_clock = datetime.strptime("09:00:00", "%H:%M:%S").time()
    fifteen_clock = datetime.strptime("15:00:00", "%H:%M:%S").time()
    eighteen_clock = datetime.strptime("18:00:00", "%H:%M:%S").time()
    nineteen_thirty = datetime.strptime("19:30:00", "%H:%M:%S").time()
    twenty_one_eighteen = datetime.strptime("21:18:00", "%H:%M:%S").time()
    two_forty_two = datetime.strptime("02:42:00", "%H:%M:%S").time()
    Time_multiplier = 1
    if four_thirty <= virtual_time < six_clock:
        Time_multiplier = 1.3
    elif nine_clock <= virtual_time < fifteen_clock: 
        Time_multiplier = 0.8
    elif eighteen_clock <= virtual_time < nineteen_thirty: 
        Time_multiplier = 1.3
    elif twenty_one_eighteen <= virtual_time and virtual_time > two_forty_two: 
        Time_multiplier = 0.8
    print(Time_multiplier)
    print(clock_data["virtual_time"].time())
    if clock_data["virtual_time"].time() < four_thirty:
        print("虚拟时间早于 4:30")
    else:
        print("虚拟时间晚于或等于 4:30")


    # 运行虚拟时钟一段时间并获取数据
    # clock_data_list = clock.run_clock(duration=5, interval=0.5) #运行5秒，每隔0.5秒返回一次数据
    # print(clock_data_list)
