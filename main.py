from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.all import *
from .API.fish import simulate_fishing

@register("saris_fish", "城城", "赛博钓鱼-参考泰拉瑞亚", "1.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # self._init_env()
        logger.info("------ saris_fish ------")
        logger.info("欢迎使用赛博钓鱼插件！")
        self.database_plugin = self.context.get_registered_star("saris_db")
        if not self.database_plugin or not self.database_plugin.activated:
            logger.error("赛博钓鱼插件缺少数据库插件。请先加载 astrbot_plugin_saris_db.\n插件仓库地址：https://github.com/Astron/Astron-packages/tree/main/astrbot_plugin_saris_db")
            self.database_plugin_config = None  # 为了避免后续使用未初始化的属性
            self.database_plugin_activated = False
            logger.info("------ saris_fish ------")
        else:
            self.database_plugin_config = self.database_plugin.config
            self.database_plugin_activated = True
            from data.plugins.astrbot_plugin_saris_db.main import open_databases, DATABASE_FILE
            self.open_databases = open_databases
            self.DATABASE_FILE = DATABASE_FILE
            logger.info("------ saris_fish ------")

    
    @filter.command("钓鱼")
    async def fish(self, event: AstrMessageEvent):
        """
        钓鱼功能：
        """
        if not self.database_plugin_activated:

            # yield event.plain_result("数据库插件未加载，签到功能无法使用。\n请先安装并启用 astrbot_plugin_saris_db。\n插件仓库地址：https://github.com/Astron/Astron-packages/tree/main/astrbot_plugin_saris_db")
            return

        user_id = event.get_sender_id()
        try:
            with self.open_databases(self.database_plugin_config, self.DATABASE_FILE, user_id) as (db_user, db_economy, db_fish, db_backpack, db_store):
                fish = simulate_fishing(db_fish,db_economy,db_user, db_backpack)
                yield event.plain_result(fish)
        except Exception as e:
            logger.exception(f"用户 {user_id} 钓鱼失败: {e}")
            # yield event.plain_result("签到时发生错误，请稍后再试。")
    
    
    
    
    
    
    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
