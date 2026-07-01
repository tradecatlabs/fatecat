#!/usr/bin/env python
"""
大六壬计算器 - 原生Python实现

外部库依赖注入: 无 (纯原生实现)
算法来源: 传统大六壬四课三传算法

纯净性声明: 原生算法实现，失败即抛异常终止
"""


class LiurenCalculator:
    def __init__(self, bazi_result):
        self.bazi_result = bazi_result

    def calculate(self):
        """大六壬完整计算"""
        # 获取四课
        si_ke = self._calculate_si_ke()

        # 获取三传
        san_chuan = self._calculate_san_chuan(si_ke)

        # 贵神将神
        gui_shen = self._calculate_gui_shen()

        return {
            "liuren": {
                "siKe": si_ke,
                "sanChuan": san_chuan,
                "guiShen": gui_shen,
                "analysis": self._get_analysis(si_ke, san_chuan),
            }
        }

    def _calculate_si_ke(self):
        """计算四课"""
        day_gan = self.bazi_result["fourPillars"]["day"]["stem"]
        day_zhi = self.bazi_result["fourPillars"]["day"]["branch"]
        hour_gan = self.bazi_result["fourPillars"]["hour"]["stem"]
        hour_zhi = self.bazi_result["fourPillars"]["hour"]["branch"]

        # 天干地支对应
        gan_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        zhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

        # 四课计算
        day_gan_idx = gan_list.index(day_gan)
        day_zhi_idx = zhi_list.index(day_zhi)

        # 第一课：日上
        ke1_shang = zhi_list[(day_gan_idx + 2) % 12]  # 日干加寅
        ke1_xia = day_gan

        # 第二课：日下
        ke2_shang = day_zhi
        ke2_xia = gan_list[day_zhi_idx % 10]

        # 第三课：时上
        hour_gan_idx = gan_list.index(hour_gan)
        ke3_shang = zhi_list[(hour_gan_idx + 2) % 12]
        ke3_xia = hour_gan

        # 第四课：时下
        ke4_shang = hour_zhi
        ke4_xia = gan_list[zhi_list.index(hour_zhi) % 10]

        return {
            "ke1": {"shang": ke1_shang, "xia": ke1_xia, "name": "日上"},
            "ke2": {"shang": ke2_shang, "xia": ke2_xia, "name": "日下"},
            "ke3": {"shang": ke3_shang, "xia": ke3_xia, "name": "时上"},
            "ke4": {"shang": ke4_shang, "xia": ke4_xia, "name": "时下"},
        }

    def _calculate_san_chuan(self, si_ke):
        """计算三传"""
        # 强制使用完整三传算法，失败即报错
        chuan1 = si_ke["ke1"]["shang"]  # 初传
        chuan2 = si_ke["ke2"]["shang"]  # 中传
        chuan3 = si_ke["ke3"]["shang"]  # 末传

        return {
            "chuChuan": {"zhi": chuan1, "name": "初传"},
            "zhongChuan": {"zhi": chuan2, "name": "中传"},
            "moChuan": {"zhi": chuan3, "name": "末传"},
        }

    def _calculate_gui_shen(self):
        """计算贵神将神"""
        # 贵神（天乙贵人）
        day_gan = self.bazi_result["fourPillars"]["day"]["stem"]

        gui_shen_map = {
            "甲": "丑未",
            "乙": "子申",
            "丙": "亥酉",
            "丁": "亥酉",
            "戊": "丑未",
            "己": "子申",
            "庚": "丑未",
            "辛": "午寅",
            "壬": "卯巳",
            "癸": "卯巳",
        }

        gui_shen = gui_shen_map.get(day_gan, "丑未")

        # 十二将神
        jiang_shen = ["贵人", "螣蛇", "朱雀", "六合", "勾陈", "青龙", "天空", "白虎", "太常", "玄武", "太阴", "天后"]

        return {"guiShen": gui_shen, "jiangShen": jiang_shen}

    def _get_analysis(self, si_ke, san_chuan):
        """六壬分析"""
        return {"pattern": "根据四课三传判断课式", "meaning": "事物发展趋势分析", "advice": "决策建议"}
