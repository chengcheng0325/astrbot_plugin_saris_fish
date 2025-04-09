from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.all import *
from .API.fish import simulate_fishing

FISH = """\
----- 赛博游戏指南钓鱼 -----
钓鱼需要鱼竿和鱼饵
商店 渔具 鱼竿|鱼饵 [可以查看鱼竿和鱼饵的价格和ID]
购买 渔具  鱼竿|鱼饵 ID [购买鱼竿或鱼饵]
我的背包 [查看背包内的鱼饵和鱼竿的ID]
使用 渔具 ID [装备鱼竿或鱼饵]
维修 查询 ID [查看鱼竿或鱼饵的维修信息]
维修 低级|中级|高级 ID [修理鱼竿或鱼饵]
开箱 ID [打开宝箱]
钓鱼 [开始钓鱼]

鱼竿每次使用损失1点耐久
鱼饵按照鱼饵的渔力来决定消耗率
鱼饵的渔力越高，鱼饵的损耗率越低
捕获的成功率根据渔力决定,渔力越高，成功率越高
只有垃圾和鱼会自动出售,其他东西会留在背包
鱼竿如果没有耐久不会消失,只会损坏,后续会出维修\
"""
# 路径配置
PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_saris_fish')

@register("saris_fish", "城城", "赛博钓鱼-参考泰拉瑞亚", "1.1.1")
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config

    @filter.on_astrbot_loaded()
    async def on_astrbot_loaded(self):
        """
        插件初始化
        """
        logger.info("------ saris_fish ------")
        logger.info(f"如果有问题，请在 https://github.com/chengcheng0325/astrbot_plugin_saris_fish/issues 提出 issue")
        logger.info("或加作者QQ: 3079233608 进行反馈。")
        self.database_plugin = self.context.get_registered_star("saris_db")
        self.economic_plugin = self.context.get_registered_star("saris_Economic")
        # 数据库插件
        if not self.database_plugin or not self.database_plugin.activated:
            logger.error("赛博钓鱼插件缺少数据库插件。请先加载 astrbot_plugin_saris_db.\n插件仓库地址：https://github.com/chengcheng0325/astrbot_plugin_saris_db")
            self.database_plugin_config = None  # 为了避免后续使用未初始化的属性
            self.database_plugin_activated = False
        else:
            self.database_plugin_config = self.database_plugin.config
            self.database_plugin_activated = True
            from data.plugins.astrbot_plugin_saris_db.main import open_databases, DATABASE_FILE
            self.open_databases = open_databases
            self.DATABASE_FILE = DATABASE_FILE
        # 经济插件
        if not self.economic_plugin or not self.economic_plugin.activated:
            logger.error("赛博钓鱼插件缺少经济插件。请先加载 astrbot_plugin_saris_Economic.\n插件仓库地址：https://github.com/chengcheng0325/astrbot_plugin_saris_Economic")
            self.economic_plugin_activated = False
        else:
            self.economic_plugin_activated = True
        logger.info("------ saris_fish ------")


    @filter.command("钓鱼")
    async def fish(self, event: AstrMessageEvent):
        """
        钓鱼功能：
        """
        if not self.database_plugin_activated:
            yield event.plain_result("数据库插件未加载，钓鱼功能无法使用。\n请先安装并启用 astrbot_plugin_saris_db。\n插件仓库地址：https://github.com/chengcheng0325/astrbot_plugin_saris_db")
            return
        
        if not self.economic_plugin_activated:
            yield event.plain_result("经济插件未加载，钓鱼功能无法使用。\n请先安装并启用 astrbot_plugin_saris_Economic。\n插件仓库地址：https://github.com/chengcheng0325/astrbot_plugin_saris_Economic")
            return

        user_id = event.get_sender_id()
        try:
            with self.open_databases(self.database_plugin_config, self.DATABASE_FILE, user_id) as (db_user, db_economy, db_fish, db_backpack, db_store):
                fish = simulate_fishing(db_fish,db_economy,db_user, db_backpack, db_store, self.config)
                yield event.plain_result(fish)
        except Exception as e:
            logger.exception(f"用户 {user_id} 钓鱼失败: {e}")
    
    
    @filter.command("钓鱼游戏", alias={"赛博钓鱼"})
    async def fish_game(self, event: AstrMessageEvent):
        """
        赛博钓鱼游戏指南
        """
        try:
            yield event.image_result(os.path.join(PLUGIN_DIR, "help.png"))
            # yield event.plain_result(FISH)
        except Exception as e:
            logger.exception(f"钓鱼游戏指南发送失败: {e}")
    
    
    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
