import random
import math
from fractions import Fraction
from datetime import datetime, timedelta

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


# 定义渔获品质
FISHING_QUALITIES = ["丰富", "常见", "不常见", "罕见", "十分罕见", "非常罕见"]

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
        print(f"常见_chance: {常见_chance}")
        if random.random() < 常见_chance:
            successful_qualities.append("常见")

        # 不常见 (不常见)
        不常见_chance = min(1/3, fishing_power / 300)
        print(f"不常见_chance: {不常见_chance}")
        if random.random() < 不常见_chance:
            successful_qualities.append("不常见")

        # 罕见 (Rare)
        罕见_chance = min(1/4, fishing_power / 1050)
        print(f"罕见_chance: {罕见_chance}")
        if random.random() < 罕见_chance:
            successful_qualities.append("罕见")

        # 十分罕见 (Very Rare)
        十分罕见_chance = min(1/5, fishing_power / 2250)
        print(f"十分罕见_chance: {十分罕见_chance}")
        if random.random() < 十分罕见_chance:
            successful_qualities.append("十分罕见")

        # 非常罕见 (Extremely Rare)
        非常罕见_chance = min(1/6, fishing_power / 4500)
        print(f"非常罕见_chance: {非常罕见_chance}")
        if random.random() < 非常罕见_chance:
            successful_qualities.append("非常罕见")

    return successful_qualities

# 模拟钓鱼逻辑
def simulate_fishing(fish_db,db_economy,db_user, fishing_pole = "木钓竿", bait = "学徒诱饵", biome = "丛林", height = "地表"):
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

    time = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    fish_cooling = datetime.strptime(db_user.query_fish_cooling()[0], "%Y-%m-%d %H:%M:%S")
    
    print(f"鱼冷却时间: {fish_cooling}")
    if fish_cooling > time:
        test = f"""\
----- 赛博钓鱼 -----
你还在冷却时间内，请等待 {fish_cooling - time} 
{random.choice(fishing_quotes2)}
"""
        return test  # 冷却中，什么都没钓到
    else:
        db_user.update_fish_cooling() # 冷却时间更新



    # fish_db = Database_user()
    fishing_pole_power = fish_db.get_fishing_pole_by_kind(fishing_pole)[2]
    bait_power = fish_db.get_bait_by_kind(bait)[2]



    total_fishing_power = fishing_pole_power + bait_power
    # total_fishing_power = 300
    print(f"总渔力: {total_fishing_power}")
    # 基础成功率 (可以调整)
    base_success_rate = 0.1 + (total_fishing_power / 200)  # 将渔力转化为成功率的加成

    # 应用水域大小的影响
    # water_size_factor = min(1.0, water_size / WATER_HEIGHT)  # 水域越大，成功率越高，最大为1
    # base_success_rate *= (1 + water_size_factor* SIZE_MULTIPLIER) # 水域大小对成功率的调整

    # 应用诱饵的影响
    # base_success_rate *= (1 + bait_power * BAIT_MULTIPLIER/100) # 饵料对成功率的调整

    # 应用玩家运气
    # base_success_rate *= (1 + player.luck * LUCK_MULTIPLIER) # 运气对成功率的调整

    # 应用钓竿品质
    # base_success_rate *= (1 + fishing_pole_power / FishingPower.EXCELLENT * QUALITY_MULTIPLIER) # 钓竿品质对成功率的调整

    # 随机调整
    success_rate = random.uniform(max(0, base_success_rate - 0.05), min(1, base_success_rate + 0.05))
    print(f"成功率: {success_rate}")
    # 决定是否钓到东西
    if random.random() < success_rate:
        # 钓到了东西
        successful_qualities = determine_catch_quality(total_fishing_power) # 判定渔获品质
        successful_qualities.sort(key=lambda x: FISHING_QUALITIES.index(x), reverse=True) # 从最高品质开始判断
        print(f"通过判定的品质: {successful_qualities}")

        # 如果通过了非常罕见品质的判定，优先检查特殊渔获
        # if "十分罕见" in successful_qualities and biome == Biome.OCEAN:
        #     special_catches = [advanced_combat_techniques, red_herring, frog_leg, balloon_pufferfish, zephyr_fish]
        #     for catch in special_catches:
        #         if random.random() < 0.2:  # 假设每个特殊渔获有 20% 的概率钓到
        #             return catch

        # 检查生物群系特产鱼
        for quality in successful_qualities: # 从最高品质开始遍历
            print(f"{quality}")
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
            print(possible_catches)
            if possible_catches:
                chosen_fish = random.choice(possible_catches)
                db_economy.add_economy(chosen_fish[2]) # 获得钓到的鱼的价值
                if chosen_fish[7] == 1:
                    任务鱼 = True
                else:
                    任务鱼 = False
                test = f"""\
----- 赛博钓鱼 -----
你钓到了: {chosen_fish[1]}
价值: {chosen_fish[2]}
品质: {chosen_fish[3]}
任务鱼: {任务鱼}
当前金币: {db_economy.get_economy()[0]}
"""
                return test

    else:
        test = f"""\
----- 赛博钓鱼 -----
{random.choice(fishing_quotes)}
"""
        return test  # 什么都没钓到


# 使用示例
if __name__ == '__main__':
    caught_item = simulate_fishing()

    if caught_item:
        print(f"{caught_item}")
    else:
        print("什么都没钓到...")

# simplify_fraction(1, 2)

# print(simplify_fraction(100, 2250))
# print(determine_catch_quality(1000))