import random
import math
from fractions import Fraction
from datetime import datetime, timedelta
from .virtual_time import VirtualClock
from .maintenance import Equipment

fishing_quotes = [
    "今天又是空军日，蓝天白云，不见鱼影。",
    "梦想很丰满，现实很骨感，鱼护很空旷。",
    "我与鱼之间，隔着一个太平洋的寂寞。",
    "今天鱼儿放假，全体罢工。",
    "别人钓鱼钓的是快乐，我钓鱼钓的是寂寞。",
    "水至清则无鱼，可能是我太清澈了，所以一条都没钓到。",
    "装备升级再快，也赶不上我空军的速度。",
    "鱼：今天风大浪急，不宜出门。",
    "鱼饵：我怀疑你馋我，但我没有证据。",
    "钓鱼的最高境界：人空军，心不空。",
    "我可能不是来钓鱼的，我是来喂鱼的。",
    "别人钓鱼，我钓了个“空”字。",
    "我的鱼竿可能自带“驱鱼”功能。",
    "可能我的魅力还不足以吸引鱼儿上钩。",
    "我可能更适合去当渔具推销员，毕竟自己用不好，推销别人更理直气壮。",
    "钓鱼？不存在的，我只是在和水谈恋爱。",
    "我的鱼护，已经空到可以跑马了。",
    "鱼对我说：兄弟，下次再来玩啊！（下次还空军）",
    "钓鱼不在于鱼，在于心情。",
    "起码享受了阳光和风景，钓不钓得到鱼不重要。",
    "今天空军，明天肯定爆护！ (安慰自己)",
    "没关系，就当是给鱼儿放生了。",
    "钓鱼嘛，重要的是过程，结果什么的都是浮云。"
]

fishing_quotes2 = [
    "今天的鱼可能去度假了，我也顺便休息一下吧！",
    "鱼竿也累了，让它也休息一下，顺便我也看看风景。",
    "鱼可能在开会，讨论怎么不上我的钩，我先休息一下，给它们一点时间。",
    "钓鱼的最高境界就是：钓不在鱼，在乎山水之间也。休息一下，感受一下！",
    "鱼：今天不上班！ 我：好吧，那我也摸鱼休息一下！"
]

quotes = [
    "没有鱼竿，寸步难行，何谈捕鱼？",
    "巧妇难为无米之炊，无竿难钓水中鱼。",
    "欲钓鱼，先备竿，方可临渊而羡鱼，不如退而结网。",
    "空有钓鱼之心，无钓鱼之器，只能望洋兴叹。",
    "钓鱼之道，始于竿，终于鱼，无竿则无始。",
    "梦想虽美，现实残酷，无竿在手，只剩空想。",
    "磨刀不误砍柴工，钓鱼先备好鱼竿。",
    "装备先行，事半功倍，没有鱼竿，事倍功半。",
    "英雄无用武之地，有钓技无鱼竿，也是徒劳。",
    "成功垂钓的秘诀：合适的鱼竿，耐心，还有一点运气。"
]

quotes2 = [
    "没有鱼饵，鱼儿不理睬，钓鱼成了空等待。",
    "姜太公钓鱼，愿者上钩，无饵之人，空手而归。",
    "鱼儿觅食为天性，无饵引诱，难见真容。",
    "巧妇难为无米之炊，钓鱼无饵寸步难行。",
    "欲钓大鱼，先备好饵料，投其所好，方可成功。",
    "空有钓鱼之心，无诱饵之实，难得鱼儿垂青。",
    "钓鱼之道，饵料先行，方能引鱼入瓮。",
    "梦想丰收，现实骨感，无饵诱惑，难见鱼影。",
    "磨刀不误砍柴工，钓鱼先备足鱼饵。",
    "纵有高超钓技，无饵诱鱼，终究是徒劳。"
]

quotes3 = [
    "鱼竿断裂，希望破灭，垂钓乐趣化为乌有。",
    "工欲善其事，必先利其器，竿已损毁，垂钓无望。",
    "巧妇难为无米之炊，竿已折断，如何捕鱼？",
    "欲钓大鱼，鱼竿先行，若竿已坏，一切皆休。",
    "空有钓鱼之心，无完好之竿，只能望水兴叹。",
    "钓鱼之道，始于竿，终于鱼，竿断则止。",
    "梦想丰收，现实无奈，鱼竿损坏，空留遗憾。",
    "磨刀不误砍柴工，维护鱼竿是关键。",
    "装备精良，方能驰骋，鱼竿损坏，寸步难行。",
    "英雄无用武之地，有钓技无好竿，也是徒劳。"
]




# 定义渔获品质
FISHING_QUALITIES = ["丰富", "常见", "不常见", "罕见", "十分罕见", "非常罕见"]

def calculate_fish(fishing_power, fish_type):
    """
    计算一次钓鱼获得的鱼数量。

    Args:
        fishing_power: 玩家的渔力。
        fish_type: 鱼的类型，可以是 "bomb_fish" 或 "frost_fish"。

    Returns:
        钓到的鱼数量。
    """

    if fish_type == "炸弹鱼":
        # 炸弹鱼的计算
        min_val = math.floor((fishing_power / 20 + 3) / 2)
        max_val = math.floor((fishing_power / 10 + 6) / 2)

        random_numbers = [
            random.randint(0, 49),
            random.randint(0, 99),
            random.randint(0, 149),
            random.randint(0, 199),
        ]

        for rand_num in random_numbers:
            if rand_num < fishing_power:
                max_val += 1

    elif fish_type == "寒霜飞鱼":
        # 寒霜飞鱼的计算
        min_val = math.floor((fishing_power / 4 + 15) / 2)
        max_val = math.floor((fishing_power / 2 + 40) / 2)

        random_numbers = [
            random.randint(0, 49),
            random.randint(0, 99),
            random.randint(0, 149),
            random.randint(0, 199),
        ]

        increase_amount = 0
        for rand_num in random_numbers:
            if rand_num < fishing_power:
                increase_amount += 6

        max_val += increase_amount

    else:
        print("无效的鱼类型")
        return 0  # 或者抛出一个异常

    fish_count = random.randint(int(min_val), int(max_val))

    return fish_count


def determine_catch_quality(fishing_power):
    """
    根据渔力判定渔获品质。

    Args:
        fishing_power: 总渔力。

    Returns:
        一个包含所有通过判定的渔获品质的列表。
    """
    successful_qualities = []
    successful_qualities.append("丰富")
    # 渔获品质判定
    if fishing_power > 0: # 渔力大于0才进行判定
        # 常见 (Common)
        常见_chance = min(1/2, fishing_power / 150)
        # print(f"常见_chance: {常见_chance}")
        if random.random() < 常见_chance:
            successful_qualities.append("常见")

        # 不常见 (不常见)
        不常见_chance = min(1/3, fishing_power / 300)
        # print(f"不常见_chance: {不常见_chance}")
        if random.random() < 不常见_chance:
            successful_qualities.append("不常见")

        # 罕见 (Rare)
        罕见_chance = min(1/4, fishing_power / 1050)
        # print(f"罕见_chance: {罕见_chance}")
        if random.random() < 罕见_chance:
            successful_qualities.append("罕见")

        # 十分罕见 (Very Rare)
        十分罕见_chance = min(1/5, fishing_power / 2250)
        # print(f"十分罕见_chance: {十分罕见_chance}")
        if random.random() < 十分罕见_chance:
            successful_qualities.append("十分罕见")

        # 非常罕见 (Extremely Rare)
        非常罕见_chance = min(1/6, fishing_power / 4500)
        # print(f"非常罕见_chance: {非常罕见_chance}")
        if random.random() < 非常罕见_chance:
            successful_qualities.append("非常罕见")

    return successful_qualities

# 模拟钓鱼逻辑
def simulate_fishing(fish_db,db_economy,db_user, db_backpack, db_store, config, biome = "任意", height = "地表"):
    """
    模拟钓鱼过程。

    Args:
        fishing_pole: 钓竿
        bait: 诱饵
        biome: 当前生物群系 (雪原, 神圣, 丛林, 沙漠, 海洋)
        height: 当前高度 (地下, 洞穴, 地狱, 天空, 地表)

    Returns:
        钓到的物品 (Fish 对象)，如果没有钓到则返回 None。
    """

    # 时间模拟
    start_real = datetime(2025, 3, 31, 0, 0, 0)
    start_virtual = datetime(2025, 1, 1, 0, 0, 0)
    clock = VirtualClock(start_real,start_virtual,time_ratio=12)
    clock_data = clock.get_virtual_clock_data()
    print(f"虚拟时间: {clock_data["virtual_time"].time()}")

    # 时间影响
    virtual_time = clock_data["virtual_time"].time()
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

    # 月相影响
    Moon_phase_magnification = 1
    if clock_data["moon_phase_name"] == "满月": Moon_phase_magnification = 1.1
    elif clock_data["moon_phase_name"] == "亏凸月" or clock_data["moon_phase_name"] == "盈凸月": Moon_phase_magnification = 1.05
    elif clock_data["moon_phase_name"] == "残月" or clock_data["moon_phase_name"] == "娥眉月": Moon_phase_magnification = 0.95
    elif clock_data["moon_phase_name"] == "新月": Moon_phase_magnification = 0.9





    fish_config = config.get("fish", {})
    Basic_fishing_power = fish_config.get("Basic_fishing_power", 50)
    if Basic_fishing_power == None: Basic_fishing_power = 50
    time = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    fish_cooling = datetime.strptime(db_user.query_fish_cooling()[0], "%Y-%m-%d %H:%M:%S")
    
    fishing_pole = db_backpack.query_backpack_item_type("鱼竿")
    # print(f"鱼竿: {fishing_pole}")
    bait = db_backpack.query_backpack_item_type("鱼饵")
    # print(f"鱼饵: {bait}")

    if fishing_pole is None: return f"----- 赛博钓鱼 -----\n你还没有钓竿\n{random.choice(quotes)}"
    if fishing_pole is None: return f"----- 赛博钓鱼 -----\n你还没有鱼饵\n{random.choice(quotes2)}"
    state = False
    for i in fishing_pole:
        if i[8] == 1:
            fishing_pole = i
            state = True
            break
    if state == False:
        return f"----- 赛博钓鱼 -----\n你还没有装备钓竿\n{random.choice(quotes)}"
    state = False
    for i in bait:
        if i[8] == 1:
            bait = i
            state = True
            break
    if state == False:
        return f"----- 赛博钓鱼 -----\n你还没有装备鱼饵\n{random.choice(quotes2)}"

    if fishing_pole[7] <= 0: return f"----- 赛博钓鱼 -----\n你的[{fishing_pole[0]}]{fishing_pole[2]}已经损坏了，请更换。\n{random.choice(quotes3)}"


    if fish_cooling > time:
        test = f"----- 赛博钓鱼 -----\n你还在冷却时间内，请等待 {fish_cooling - time}\n{random.choice(fishing_quotes2)}"
        return test  # 冷却中，什么都没钓到
    else:
        db_user.update_fish_cooling(10) # 冷却时间更新

    # 获取渔力
    fishing_pole_power = fish_db.get_fishing_pole_by_kind(fishing_pole[2])
    bait_power = fish_db.get_bait_by_kind(bait[2])[2]
    # 计算总渔力
    total_fishing_power = (Basic_fishing_power + fishing_pole_power[2] + bait_power) * Time_multiplier * Moon_phase_magnification
    print(f"基础渔力: {Basic_fishing_power}|钓竿: {fishing_pole_power[2]}|饵料: {bait_power}|时间: {Time_multiplier}|月相: {Moon_phase_magnification}|总渔力: {total_fishing_power}")
    # total_fishing_power = 500

    # 渔饵消耗
    buy_state = ""
    消耗几率 = 1/(1 + bait_power/6)
    if random.random() < 消耗几率:
        db_backpack.update_backpack_item_count(-1, bait[0]) # 数量-1
        if bait[3] - 1 <= 0:
            iteam = db_store.get_bait_store_item(bait[0])
            if iteam[4] > db_economy.get_economy():
                buy_state = "\n自动购买失败 余额不足"
                db_backpack.delete_backpack(bait[0]) # 数量为0，删除
            else:
                db_economy.reduce_economy(iteam[4])
                db_backpack.update_backpack_item_count(iteam[2], bait[0])
                buy_state = f"\n自动购买成功 {bait[2]}+{iteam[2]}"
        消耗 = True
    else:
        消耗 = False
    
    # 鱼竿消耗
    db_backpack.update_backpack_item_current_durability(1, fishing_pole[0]) # 耐久-1

    # 基础成功率 (可以调整)
    base_success_rate = 0.5 + (total_fishing_power / 200)  # 将渔力转化为成功率的加成


    # 随机调整
    success_rate = random.uniform(max(0, base_success_rate - 0.05), min(1, base_success_rate + 0.05))

    # 决定是否钓到东西
    if random.random() < success_rate:
        # 钓到了东西
        successful_qualities = determine_catch_quality(total_fishing_power) # 判定渔获品质
        successful_qualities.sort(key=lambda x: FISHING_QUALITIES.index(x), reverse=True) # 从最高品质开始判断
        # print(f"通过判定的品质: {successful_qualities}")

        # 检查生物群系特产鱼
        for quality in successful_qualities: # 从最高品质开始遍历
            # print(f"{quality}")
            fish = fish_db.get_all_fish()
            # print(fish)
            fish_list = []
            for f in fish:
                # print(f)
                if quality in f[6] and len(quality) == len(f[6]):
                    fish_list.append(f)
            possible_catches = [fish for fish in fish_list if "任意" in fish[5] or biome in fish[5]]  # 根据生物群系过滤
            # print(possible_catches)
            possible_catches = [fish for fish in possible_catches if "任意" in fish[4] or height in fish[4]] # 根据高度过滤
            # print(possible_catches)
            sword = Equipment(
                original_max=fishing_pole_power[5],
                current_max=fishing_pole[6],
                current=fishing_pole[7]-1,
                original_value=fishing_pole_power[3]
            )
            current_value = round(sword.current_value, 2)
            db_backpack.update_backpack_item_value(current_value, fishing_pole[0]) # 更新钓竿的价值

            if possible_catches:
                chosen_fish = random.choice(possible_catches)
                if chosen_fish[8] == 1:
                    任务鱼 = True
                else:
                    任务鱼 = False
                fish_count = 1
                if chosen_fish[1] == "炸弹鱼" or chosen_fish[1] == "寒霜飞鱼":
                    fish_count = calculate_fish(total_fishing_power, chosen_fish[1])

                
                test = f"\n----- 赛博钓鱼 -----\n你钓到了: {chosen_fish[1]}x{fish_count}\n价值: {chosen_fish[2]}\n品质: {chosen_fish[3]}\n类型: {chosen_fish[7]}\n鱼饵消耗: {消耗}\n耐久损失: {fishing_pole[7] - 1}[-1]\n任务鱼: {任务鱼}\n当前金币: {db_economy.get_economy()+chosen_fish[2]*fish_count}[+{chosen_fish[2]*fish_count}]"


                if chosen_fish[7] != "箱子" and chosen_fish[8] == 0:
                    db_economy.add_economy(chosen_fish[2]*fish_count) # 获得钓到的鱼的价值
                    return test
                else:
                    if db_backpack.query_backpack_ItemName(chosen_fish[1]) is None:
                        db_backpack.insert_backpack(chosen_fish[1], 1, chosen_fish[7], chosen_fish[2], 0, 0, 0) # 加入背包
                    else:
                        # print(chosen_fish[1]+"数量+1")
                        db_backpack.update_backpack_item_count(1, db_backpack.query_backpack_ItemName(chosen_fish[1])[0]) # 数量+1
                    return test


    else:
        test = f"----- 赛博钓鱼 -----\n鱼饵消耗: {消耗}{buy_state}\n耐久损失: {fishing_pole[7] - 1}[-1]\n{random.choice(fishing_quotes2)}"
        return test  # 什么都没钓到


# 使用示例
if __name__ == '__main__':
    caught_item = simulate_fishing()

    if caught_item:
        print(f"{caught_item}")
    else:
        print("什么都没钓到...")
