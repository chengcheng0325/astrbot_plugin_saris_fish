import copy

class Equipment:
    def __init__(self, original_max: int, current_max: int, current: int, original_value: float):
        """
        初始化装备
        :param original_max: 出厂最大耐久
        :param current_max: 当前最大耐久
        :param current: 当前耐久
        :param original_value: 原始价值(元)
        """
        self.original_max = original_max
        self.current_max = current_max
        self.current = current
        self.original_value = original_value
        self.current_value = self._calculate_value()
        self.repair_results = {}  # 初始化维修结果字典

    def _calculate_value(self) -> float:
        """计算当前价值"""
        return self.original_value * (self.current / self.original_max)

    def _calculate_wear_ratio(self) -> float:
        """计算损耗比例(0-1)"""
        if self.current_max <= 0 or self.current >= self.current_max:
            return 0.0
        return (self.current_max - self.current) / self.current_max

    def calculate_repair_cost(self, repair_type: str) -> float:
        """
        计算维修费用，但不执行维修
        :param repair_type: 维修类型 ('low', 'medium', 'high')
        :return: 维修费用 (元)
        """
        if self.current >= self.current_max:
            return 0.0

        wear_ratio = self._calculate_wear_ratio()

        # 维修参数配置
        repair_config = {
            'low': {
                'base_cost': 20.0,
                'wear_multiplier': 0.5
            },
            'medium': {
                'base_cost': 50.0,
                'wear_multiplier': 0.3
            },
            'high': {
                'base_cost': 100.0,
                'wear_multiplier': 0.1
            }
        }

        if repair_type not in repair_config:
            raise ValueError("无效维修类型，请选择: 'low', 'medium', 'high'")

        config = repair_config[repair_type]

        # 计算维修费用
        cost = (
            config['base_cost'] +
            config['base_cost'] * wear_ratio * config['wear_multiplier'] +
            self.original_value * 0.01
        )
        return round(cost, 2)

    def simulate_repair(self, repair_type: str) -> dict:
        """
        模拟维修，返回维修结果但不实际修改装备状态
        :param repair_type: 维修类型('low','medium','high')
        :return:  维修结果字典
        """
        original_current_max = self.current_max
        original_current = self.current

        if self.current >= self.current_max:
            cost = 0.0
            success = None  # None表示不需要维修
            new_current_max = self.current_max
            new_current = self.current

        else:

            wear_ratio = self._calculate_wear_ratio()

            # 维修参数配置
            repair_config = {
                'low': {
                    'base_cost': 20.0,
                    'durability_loss': 0.15 + wear_ratio * 0.3,
                    'original_penalty': 0.05,
                    'wear_multiplier': 0.5
                },
                'medium': {
                    'base_cost': 50.0,
                    'durability_loss': 0.08 + wear_ratio * 0.15,
                    'original_penalty': 0.02,
                    'wear_multiplier': 0.3
                },
                'high': {
                    'base_cost': 100.0,
                    'durability_loss': 0.03 + wear_ratio * 0.05,
                    'original_penalty': 0.01,
                    'wear_multiplier': 0.1
                }
            }

            if repair_type not in repair_config:
                raise ValueError("无效维修类型，请选择: 'low', 'medium', 'high'")

            config = repair_config[repair_type]

            # 计算维修费用
            cost = (
                config['base_cost'] +
                config['base_cost'] * wear_ratio * config['wear_multiplier'] +
                self.original_value * 0.01
            )

            # 计算新耐久(至少为1)
            new_current_max = max(1, int(
                original_current_max * (1 - config['durability_loss']) -
                self.original_max * config['original_penalty']
            ))

            new_current = new_current_max
            success = True

        result = {
            "cost": round(cost, 2),
            "success": success,
            "new_current_max": new_current_max,
            "new_current": new_current,
            "repair_cost": self.calculate_repair_cost(repair_type)
        }

        return result


    def repair(self, repair_type: str) -> tuple[float, bool]:
        """
        执行维修
        :param repair_type: 维修类型('low','medium','high')
        :return: (费用(元), 是否成功)
        """
        simulation_result = self.simulate_repair(repair_type)

        if simulation_result["success"] is not None:  # 只有当需要维修时才进行实际修改
            self.current_max = simulation_result["new_current_max"]
            self.current = simulation_result["new_current"]
            self.current_value = self._calculate_value()
            self.repair_results[repair_type] = simulation_result
            return simulation_result["cost"], True
        else:
            self.repair_results[repair_type] = simulation_result
            return simulation_result["cost"], False

    def simulate_all_repairs(self) -> dict:
        """模拟所有维修方案，返回结果，不修改装备状态"""
        repair_types = ['low', 'medium', 'high']
        all_results = {}
        for repair_type in repair_types:
            # 创建装备的深拷贝，确保每个维修方案都在原始状态下进行
            equipment_copy = copy.deepcopy(self)
            all_results[repair_type] = equipment_copy.simulate_repair(repair_type)  # 使用 simulate_repair
        return all_results

    def get_data(self):
        """返回 Equipment 对象的数据字典"""
        return {
            "original_max": self.original_max,
            "current_max": self.current_max,
            "current": self.current,
            "original_value": self.original_value,
            "current_value": self.current_value,
            "repair_results": self.repair_results
        }

    def __str__(self):
        return (
            f"【装备状态】\n"
            f"原始最大耐久: {self.original_max}\n"
            f"当前最大耐久: {self.current_max}\n"
            f"当前耐久值: {self.current}\n"
            f"原始价值: {self.original_value:.2f}元\n"
            f"当前价值: {self.current_value:.2f}元\n"
            f"维修结果: {self.repair_results}"
        )


if __name__ == "__main__":
    # 创建受损装备
    sword = Equipment(
        original_max=70,
        current_max=70,
        current=65,
        original_value=2000.0
    )

    # 应用所有维修方案并获取结果
    all_repair_results = sword.simulate_all_repairs()  # 调用 simulate_all_repairs
    print("所有维修方案的结果:")
    print(all_repair_results)
    print(sword.original_value)
    print(sword.current_value)
    # 打印装备状态
    # print("\n原始装备状态 (未修改):")
    # print(sword)
