import streamlit as st
import random
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional

try:
    from zhdate import ZhDate
    ZHDATE_AVAILABLE = True
except ImportError:
    ZHDATE_AVAILABLE = False


class YijingCore:
    """易经核心算法类"""
    
    def __init__(self):
        # 农历月份
        self.lunar_months = ['正月', '二月', '三月', '四月', '五月', '六月',
                             '七月', '八月', '九月', '十月', '十一月', '十二月']
        
        # 农历日期
        self.lunar_days = ['', '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
                           '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
                           '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十']
        
        # 天干
        self.tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        
        # 地支
        self.dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 地支映射
        self.dizhi_map = {
            '子': 1, '丑': 2, '寅': 3, '卯': 4, '辰': 5, '巳': 6,
            '午': 7, '未': 8, '申': 9, '酉': 10, '戌': 11, '亥': 12
        }
        
        # 八卦映射
        self.bagua_map = {
            1: '乾', 2: '兑', 3: '离', 4: '震',
            5: '巽', 6: '坎', 7: '艮', 8: '坤'
        }
        
        # 八卦符号
        self.bagua_symbols = {
            '乾': ['━━━', '━━━', '━━━'],
            '兑': ['━ ━', '━━━', '━━━'],
            '离': ['━━━', '━ ━', '━━━'],
            '震': ['━ ━', '━ ━', '━━━'],
            '巽': ['━━━', '━━━', '━ ━'],
            '坎': ['━ ━', '━━━', '━ ━'],
            '艮': ['━━━', '━ ━', '━ ━'],
            '坤': ['━ ━', '━ ━', '━ ━']
        }
        
        # 完整的卦名映射
        self.gua_names = {
            ('乾', '乾'): '乾为天', ('乾', '兑'): '天泽履', ('乾', '离'): '天火同人', ('乾', '震'): '天雷无妄',
            ('乾', '巽'): '天风姤', ('乾', '坎'): '天水讼', ('乾', '艮'): '天山遁', ('乾', '坤'): '天地否',
            ('兑', '乾'): '泽天夬', ('兑', '兑'): '兑为泽', ('兑', '离'): '泽火革', ('兑', '震'): '泽雷随',
            ('兑', '巽'): '泽风大过', ('兑', '坎'): '泽水困', ('兑', '艮'): '泽山咸', ('兑', '坤'): '泽地萃',
            ('离', '乾'): '火天大有', ('离', '兑'): '火泽睽', ('离', '离'): '离为火', ('离', '震'): '火雷噬嗑',
            ('离', '巽'): '火风鼎', ('离', '坎'): '火水未济', ('离', '艮'): '火山旅', ('离', '坤'): '火地晋',
            ('震', '乾'): '雷天大壮', ('震', '兑'): '雷泽归妹', ('震', '离'): '雷火丰', ('震', '震'): '震为雷',
            ('震', '巽'): '雷风恒', ('震', '坎'): '雷水解', ('震', '艮'): '雷山小过', ('震', '坤'): '雷地豫',
            ('巽', '乾'): '风天小畜', ('巽', '兑'): '风泽中孚', ('巽', '离'): '风火家人', ('巽', '震'): '风雷益',
            ('巽', '巽'): '巽为风', ('巽', '坎'): '风水涣', ('巽', '艮'): '风山渐', ('巽', '坤'): '风地观',
            ('坎', '乾'): '水天需', ('坎', '兑'): '水泽节', ('坎', '离'): '水火既济', ('坎', '震'): '水雷屯',
            ('坎', '巽'): '水风井', ('坎', '坎'): '坎为水', ('坎', '艮'): '水山蹇', ('坎', '坤'): '水地比',
            ('艮', '乾'): '山天大畜', ('艮', '兑'): '山泽损', ('艮', '离'): '山火贲', ('艮', '震'): '山雷颐',
            ('艮', '巽'): '山风蛊', ('艮', '坎'): '山水蒙', ('艮', '艮'): '艮为山', ('艮', '坤'): '山地剥',
            ('坤', '乾'): '地天泰', ('坤', '兑'): '地泽临', ('坤', '离'): '地火明夷', ('坤', '震'): '地雷复',
            ('坤', '巽'): '地风升', ('坤', '坎'): '地水师', ('坤', '艮'): '地山谦', ('坤', '坤'): '坤为地'
        }
        
        # 六亲
        self.liuqin = ['父母', '官鬼', '兄弟', '妻财', '子孙']
        
        # 五行属性
        self.wuxing = {
            '金': ['庚', '辛', '申', '酉'],
            '木': ['甲', '乙', '寅', '卯'],
            '水': ['壬', '癸', '子', '亥'],
            '火': ['丙', '丁', '巳', '午'],
            '土': ['戊', '己', '辰', '戌', '丑', '未']
        }
        
        # 天干五行属性
        self.tiangan_wuxing = {
            '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
            '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
        }
        
        # 地支五行属性
        self.dizhi_wuxing = {
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        }
        
        # 八卦五行属性（本宫卦的五行）
        self.bagua_wuxing = {
            '乾': '金', '兑': '金', '离': '火', '震': '木',
            '巽': '木', '坎': '水', '艮': '土', '坤': '土'
        }
        
        # 五行生克关系
        self.wuxing_shengke = {
            '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
            '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
            '水': {'生': '木', '克': '火', '被生': '金', '被克': '土'},
            '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
            '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'}
        }
        
        # 八卦纳甲表（简化为只包含地支，因为天干可以通过规则推导）
        # 注意：这里的顺序对应爻位，索引0=第1爻，索引1=第2爻，...，索引5=第6爻
        self.bagua_najia = {
            '乾': ['子', '寅', '辰', '午', '申', '戌'],     # 乾卦纳甲子
            '坤': ['未', '巳', '卯', '丑', '亥', '酉'],     # 坤卦纳乙未
            '震': ['子', '寅', '辰', '午', '申', '戌'],     # 震卦纳庚子
            '巽': ['丑', '亥', '酉', '未', '巳', '卯'],     # 巽卦纳辛丑
            '坎': ['寅', '辰', '午', '申', '戌', '子'],     # 坎卦纳戊寅
            '离': ['卯', '丑', '亥', '酉', '未', '巳'],     # 离卦纳己卯
            '艮': ['辰', '午', '申', '戌', '子', '寅'],     # 艮卦纳丙辰
            '兑': ['巳', '卯', '丑', '亥', '酉', '未']      # 兑卦纳丁巳
        }
        
        # 完整的六十四卦世应位置表
        # 世应位置：世爻和应爻的位置（1-6爻）
        self.complete_shi_ying_positions = {
            # 乾宫八卦
            '乾为天': {'世': 6, '应': 3},      # 本宫卦
            '天风姤': {'世': 1, '应': 4},      # 一世卦
            '天山遁': {'世': 2, '应': 5},      # 二世卦
            '天地否': {'世': 3, '应': 6},      # 三世卦
            '风地观': {'世': 4, '应': 1},      # 四世卦
            '山地剥': {'世': 5, '应': 2},      # 五世卦
            '火地晋': {'世': 4, '应': 1},      # 游魂卦
            '火天大有': {'世': 3, '应': 6},    # 归魂卦
            
            # 坤宫八卦
            '坤为地': {'世': 6, '应': 3},      # 本宫卦
            '地雷复': {'世': 1, '应': 4},      # 一世卦
            '地泽临': {'世': 2, '应': 5},      # 二世卦
            '地天泰': {'世': 3, '应': 6},      # 三世卦
            '雷天大壮': {'世': 4, '应': 1},    # 四世卦
            '泽天夬': {'世': 5, '应': 2},      # 五世卦
            '水天需': {'世': 4, '应': 1},      # 游魂卦
            '水地比': {'世': 3, '应': 6},      # 归魂卦
            
            # 震宫八卦
            '震为雷': {'世': 6, '应': 3},      # 本宫卦
            '雷地豫': {'世': 1, '应': 4},      # 一世卦
            '雷水解': {'世': 2, '应': 5},      # 二世卦
            '雷风恒': {'世': 3, '应': 6},      # 三世卦
            '地风升': {'世': 4, '应': 1},      # 四世卦
            '水风井': {'世': 5, '应': 2},      # 五世卦
            '泽风大过': {'世': 4, '应': 1},    # 游魂卦
            '泽雷随': {'世': 3, '应': 6},      # 归魂卦
            
            # 巽宫八卦
            '巽为风': {'世': 6, '应': 3},      # 本宫卦
            '风天小畜': {'世': 1, '应': 4},    # 一世卦
            '风火家人': {'世': 2, '应': 5},    # 二世卦
            '风雷益': {'世': 3, '应': 6},      # 三世卦
            '天雷无妄': {'世': 4, '应': 1},    # 四世卦
            '火雷噬嗑': {'世': 5, '应': 2},    # 五世卦
            '山雷颐': {'世': 4, '应': 1},      # 游魂卦
            '山风蛊': {'世': 3, '应': 6},      # 归魂卦
            
            # 坎宫八卦
            '坎为水': {'世': 6, '应': 3},      # 本宫卦
            '水泽节': {'世': 1, '应': 4},      # 一世卦
            '水雷屯': {'世': 2, '应': 5},      # 二世卦
            '水火既济': {'世': 3, '应': 6},    # 三世卦
            '泽火革': {'世': 4, '应': 1},      # 四世卦
            '雷火丰': {'世': 5, '应': 2},      # 五世卦
            '地火明夷': {'世': 4, '应': 1},    # 游魂卦
            '地水师': {'世': 3, '应': 6},      # 归魂卦
            
            # 离宫八卦
            '离为火': {'世': 6, '应': 3},      # 本宫卦
            '火山旅': {'世': 1, '应': 4},      # 一世卦
            '火风鼎': {'世': 2, '应': 5},      # 二世卦
            '火水未济': {'世': 3, '应': 6},    # 三世卦
            '山水蒙': {'世': 4, '应': 1},      # 四世卦
            '风水涣': {'世': 5, '应': 2},      # 五世卦
            '天水讼': {'世': 4, '应': 1},      # 游魂卦
            '天火同人': {'世': 3, '应': 6},    # 归魂卦
            
            # 艮宫八卦
            '艮为山': {'世': 6, '应': 3},      # 本宫卦
            '山火贲': {'世': 1, '应': 4},      # 一世卦
            '山天大畜': {'世': 2, '应': 5},    # 二世卦
            '山泽损': {'世': 3, '应': 6},      # 三世卦
            '火泽睽': {'世': 4, '应': 1},      # 四世卦
            '天泽履': {'世': 5, '应': 2},      # 五世卦
            '风泽中孚': {'世': 4, '应': 1},    # 游魂卦
            '风山渐': {'世': 3, '应': 6},      # 归魂卦
            
            # 兑宫八卦
            '兑为泽': {'世': 6, '应': 3},      # 本宫卦
            '泽水困': {'世': 1, '应': 4},      # 一世卦
            '泽地萃': {'世': 2, '应': 5},      # 二世卦
            '泽山咸': {'世': 3, '应': 6},      # 三世卦
            '水山蹇': {'世': 4, '应': 1},      # 四世卦
            '地山谦': {'世': 5, '应': 2},      # 五世卦
            '雷山小过': {'世': 4, '应': 1},    # 游魂卦
            '雷泽归妹': {'世': 3, '应': 6}     # 归魂卦
        }
        
        # 六神配置（按日干配六神）
        self.liushen_by_day = {
            '甲': ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武'],  
            '乙': ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武'],
            '丙': ['朱雀', '勾陈', '螣蛇', '白虎', '玄武', '青龙'],
            '丁': ['朱雀', '勾陈', '螣蛇', '白虎', '玄武', '青龙'],
            '戊': ['勾陈', '螣蛇', '白虎', '玄武', '青龙', '朱雀'],
            '己': ['螣蛇', '白虎', '玄武', '青龙', '朱雀', '勾陈'], 
            '庚': ['白虎', '玄武', '青龙', '朱雀', '勾陈', '螣蛇'],
            '辛': ['白虎', '玄武', '青龙', '朱雀', '勾陈', '螣蛇'],
            '壬': ['玄武', '青龙', '朱雀', '勾陈', '螣蛇', '白虎'],
            '癸': ['玄武', '青龙', '朱雀', '勾陈', '螣蛇', '白虎']
        }
        self.gua_gong_mapping = {
            # 乾宫八卦
            '乾为天': '乾', '天风姤': '乾', '天山遁': '乾', '天地否': '乾',
            '风地观': '乾', '山地剥': '乾', '火地晋': '乾', '火天大有': '乾',
            
            # 坤宫八卦
            '坤为地': '坤', '地雷复': '坤', '地泽临': '坤', '地天泰': '坤',
            '雷天大壮': '坤', '泽天夬': '坤', '水天需': '坤', '水地比': '坤',
            
            # 震宫八卦
            '震为雷': '震', '雷地豫': '震', '雷水解': '震', '雷风恒': '震',
            '地风升': '震', '水风井': '震', '泽风大过': '震', '泽雷随': '震',
            
            # 巽宫八卦
            '巽为风': '巽', '风天小畜': '巽', '风火家人': '巽', '风雷益': '巽',
            '天雷无妄': '巽', '火雷噬嗑': '巽', '山雷颐': '巽', '山风蛊': '巽',
            
            # 坎宫八卦
            '坎为水': '坎', '水泽节': '坎', '水雷屯': '坎', '水火既济': '坎',
            '泽火革': '坎', '雷火丰': '坎', '地火明夷': '坎', '地水师': '坎',
            
            # 离宫八卦
            '离为火': '离', '火山旅': '离', '火风鼎': '离', '火水未济': '离',
            '山水蒙': '离', '风水涣': '离', '天水讼': '离', '天火同人': '离',
            
            # 艮宫八卦
            '艮为山': '艮', '山火贲': '艮', '山天大畜': '艮', '山泽损': '艮',
            '火泽睽': '艮', '天泽履': '艮', '风泽中孚': '艮', '风山渐': '艮',
            
            # 兑宫八卦
            '兑为泽': '兑', '泽水困': '兑', '泽地萃': '兑', '泽山咸': '兑',
            '水山蹇': '兑', '地山谦': '兑', '雷山小过': '兑', '雷泽归妹': '兑'
        }
    
    def find_bagua_by_lines(self, lines: List[str]) -> str:
        """根据三爻线查找八卦"""
        for bagua, symbols in self.bagua_symbols.items():
            if symbols == lines:
                return bagua
        return '未知'
    
    def time_divination(self) -> Dict:
        """时间起卦"""
        now = datetime.now()
        
        # 尝试使用农历日期，如果zhdate库不可用则使用公历
        if ZHDATE_AVAILABLE:
            try:
                lunar_date = ZhDate.from_datetime(now)
                lunar_year = lunar_date.lunar_year
                lunar_month = lunar_date.lunar_month
                lunar_day = lunar_date.lunar_day
                
                lunar_month_name = self.lunar_months[lunar_month - 1]
                lunar_day_name = self.lunar_days[lunar_day]
                
                # 计算年地支
                year_zhi_index = (lunar_year - 4) % 12
                year_zhi = self.dizhi[year_zhi_index]
                
                # 计算时辰地支
                hour = now.hour
                time_mapping = {
                    (23, 0): '子', (1, 2): '丑', (3, 4): '寅', (5, 6): '卯',
                    (7, 8): '辰', (9, 10): '巳', (11, 12): '午', (13, 14): '未',
                    (15, 16): '申', (17, 18): '酉', (19, 20): '戌', (21, 22): '亥'
                }
                
                time_zhi = '子'  # 默认值
                for time_range, zhi in time_mapping.items():
                    if len(time_range) == 2 and time_range[0] <= hour <= time_range[1]:
                        time_zhi = zhi
                        break
                    elif hour == 23 or hour == 0:
                        time_zhi = '子'
                        break
                
                year_num = self.dizhi_map[year_zhi]
                month_num = lunar_month
                day_num = lunar_day
                time_num = self.dizhi_map[time_zhi]
                
                time_info = f"{now.strftime('%Y年%m月%d日 %H:%M:%S')} 农历  {year_zhi}年 {lunar_month_name} {lunar_day_name} {time_zhi}时"
                
            except Exception as e:
                # 如果农历计算失败，回退到公历
                year_num = now.year % 100
                month_num = now.month
                day_num = now.day
                time_num = now.hour
                time_info = f"{now.strftime('%Y年%m月%d日 %H:%M:%S')} (公历)"
        else:
            # zhdate库不可用，使用公历
            year_num = now.year % 100
            month_num = now.month
            day_num = now.day
            time_num = now.hour
            time_info = f"{now.strftime('%Y年%m月%d日 %H:%M:%S')} (公历，建议安装zhdate库以获得更准确的结果)"
        
        # 计算上卦
        upper_sum = year_num + month_num + day_num
        upper_remainder = upper_sum % 8 if upper_sum % 8 != 0 else 8
        upper_gua = self.bagua_map[upper_remainder]
        
        # 计算下卦
        lower_sum = upper_sum + time_num
        lower_remainder = lower_sum % 8 if lower_sum % 8 != 0 else 8
        lower_gua = self.bagua_map[lower_remainder]
        
        # 计算动爻
        dong_yao = lower_sum % 6 if lower_sum % 6 != 0 else 6
        
        # 获取卦名
        gua_name = self.gua_names.get((upper_gua, lower_gua), f"{upper_gua}{lower_gua}")
        
        return {
            'method': 'time',
            'original_gua': gua_name,
            'upper_gua': upper_gua,
            'lower_gua': lower_gua,
            'dong_yao': dong_yao,
            'time_info': time_info
        }
    
    def coin_divination(self, coin_results_list: List[List[str]] = None) -> Dict:
        """铜钱起卦
        
        Args:
            coin_results_list: 可选，传入的铜钱结果列表，每个元素是包含3个'阳'或'阴'的列表
        """
        hexagram = []
        moving_lines = []
        coin_results = []
        
        for i in range(6):
            # 如果传入了铜钱结果，使用传入的结果；否则生成新的随机结果
            if coin_results_list and i < len(coin_results_list):
                coins = coin_results_list[i]
            else:
                # 模拟三枚铜钱投掷
                coins = []
                for _ in range(3):
                    coin = random.choice(['阳', '阴'])
                    coins.append(coin)
            
            coin_results.append(coins)
            yin_count = coins.count('阴')
            
            # 判断爻的性质
            if yin_count == 1:
                line = '━━━'  # 少阳
                moving = False
            elif yin_count == 2:
                line = '━ ━'  # 少阴
                moving = False
            elif yin_count == 3:
                line = '━━━'  # 老阳(动)
                moving = True
            else:  # yin_count == 0
                line = '━ ━'  # 老阴(动)
                moving = True
            
            hexagram.append(line)
            moving_lines.append(moving)
        
        # 分析上下卦
        # hexagram[0]是第1爻（最下面），hexagram[5]是第6爻（最上面）
        # 上卦：第4、5、6爻（索引3,4,5）
        # 下卦：第1、2、3爻（索引0,1,2）
        upper_lines = [hexagram[5], hexagram[4], hexagram[3]]
        lower_lines = [hexagram[2], hexagram[1], hexagram[0]]
        
        upper_gua = self.find_bagua_by_lines(upper_lines)
        lower_gua = self.find_bagua_by_lines(lower_lines)
        
        gua_name = self.gua_names.get((upper_gua, lower_gua), f"{upper_gua}{lower_gua}")
        
        return {
            'method': 'coin',
            'original_gua': gua_name,
            'upper_gua': upper_gua,
            'lower_gua': lower_gua,
            'hexagram': hexagram,
            'moving_lines': moving_lines,
            'coin_results': coin_results
        }
    
    def get_changed_gua(self, result: Dict) -> Dict:
        """获取变卦"""
        if result['method'] in ['time', 'number']:
            # 时间起卦和数字起卦的变卦逻辑
            dong_yao = result['dong_yao']
            upper_gua = result['upper_gua']
            lower_gua = result['lower_gua']
            
            # 获取本卦的爻线
            original_lines = self.bagua_symbols[upper_gua] + self.bagua_symbols[lower_gua]
            
            # 变换动爻
            changed_lines = original_lines.copy()
            line_index = 6 - dong_yao  # 转换为0-based索引
            
            if changed_lines[line_index] == '━━━':
                changed_lines[line_index] = '━ ━'
            else:
                changed_lines[line_index] = '━━━'
            
            # 重新分析上下卦
            # 上卦：索引0,1,2 对应第6,5,4爻
            # 下卦：索引3,4,5 对应第3,2,1爻
            changed_upper = self.find_bagua_by_lines([changed_lines[0], changed_lines[1], changed_lines[2]])
            changed_lower = self.find_bagua_by_lines([changed_lines[3], changed_lines[4], changed_lines[5]])
            
        else:  # coin method
            changed_lines = []
            for i, (line, is_moving) in enumerate(zip(result['hexagram'], result['moving_lines'])):
                if is_moving:
                    changed_lines.append('━ ━' if line == '━━━' else '━━━')
                else:
                    changed_lines.append(line)
            
            # 铜钱起卦的上下卦分析
            changed_upper = self.find_bagua_by_lines([changed_lines[5], changed_lines[4], changed_lines[3]])
            changed_lower = self.find_bagua_by_lines([changed_lines[2], changed_lines[1], changed_lines[0]])
        
        changed_gua_name = self.gua_names.get((changed_upper, changed_lower), f"{changed_upper}{changed_lower}")
        
        return {
            'name': changed_gua_name,
            'upper_gua': changed_upper,
            'lower_gua': changed_lower,
            'lines': changed_lines
        }
    
    def get_detailed_analysis(self, result: Dict, changed_result: Dict) -> str:
        """获取详细分析文本"""
        detail_text = f"""
═══════════════════════════════════════════════
                    起卦详细信息
═══════════════════════════════════════════════

【起卦方法】：{('时间起卦' if result['method'] == 'time' else ('数字起卦' if result['method'] == 'number' else '铜钱起卦'))}

"""
        
        if result['method'] == 'time':
            detail_text += f"""【时间信息】：{result['time_info']}

【本卦】：《{result['original_gua']}》
    上卦：{result['upper_gua']}
    下卦：{result['lower_gua']}
    动爻：第{result['dong_yao']}爻

【变卦】：《{changed_result['name']}》
    上卦：{changed_result['upper_gua']}
    下卦：{changed_result['lower_gua']}

【卦象分析】：
    本卦六爻从第六爻到第一爻呈现分别为："""
            
            # 显示六爻详情
            all_lines = self.bagua_symbols[result['upper_gua']] + self.bagua_symbols[result['lower_gua']]
            for i in range(6):
                line_num = 6 - i
                line = all_lines[i]
                is_dong = line_num == result['dong_yao']
                detail_text += f"\n    第{line_num}爻：{line} {'← 动爻' if is_dong else ''}"
        
        elif result['method'] == 'number':
            detail_text += f"""【数字信息】：{result['numbers_info']}

【本卦】：《{result['original_gua']}》
    上卦：{result['upper_gua']}
    下卦：{result['lower_gua']}
    动爻：第{result['dong_yao']}爻

【变卦】：《{changed_result['name']}》
    上卦：{changed_result['upper_gua']}
    下卦：{changed_result['lower_gua']}

【卦象分析】：
    本卦六爻从下到上分别为："""
            
            # 显示六爻详情 - 从第六爻到第一爻显示
            for i in range(5, -1, -1):
                line = result['hexagram'][i]
                is_moving = result['moving_lines'][i]
                line_num = i + 1
                detail_text += f"\n    第{line_num}爻：{line} {'← 动爻' if is_moving else ''}"
        
        else:  # coin method
            detail_text += f"""【本卦】：《{result['original_gua']}》
    上卦：{result['upper_gua']}
    下卦：{result['lower_gua']}

【变卦】：《{changed_result['name']}》
    上卦：{changed_result['upper_gua']}
    下卦：{changed_result['lower_gua']}

【铜钱摇卦详情】："""
            
            # 从第六爻到第一爻显示
            for i in range(5, -1, -1):
                coin_result = result['coin_results'][i]
                line = result['hexagram'][i]
                is_moving = result['moving_lines'][i]
                line_num = i + 1
                yin_count = coin_result.count('阴')
                
                # 确定爻的性质
                if yin_count == 1:
                    nature = "少阳"
                elif yin_count == 2:
                    nature = "少阴"
                elif yin_count == 3:
                    nature = "老阳(动爻)"
                else:
                    nature = "老阴(动爻)"
                
                detail_text += f"""
    第{line_num}爻：{' '.join(coin_result)} → {line} ({nature})"""
            
            detail_text += f"\n\n【动爻分析】："
            moving_count = sum(result['moving_lines'])
            if moving_count == 0:
                detail_text += "\n    无动爻，以本卦断卦"
            else:
                detail_text += f"\n    共有{moving_count}个动爻："
                # 从第六爻到第一爻显示动爻
                for i in range(5, -1, -1):
                    if result['moving_lines'][i]:
                        detail_text += f"\n    第{i + 1}爻为动爻"
        
        detail_text += f"""

【占断要点】：
    • 本卦代表当前状况
    • 变卦代表事物发展趋势
    • 动爻是变化的关键因素
    • 结合卦辞爻辞进行具体分析

"""
        
        # 添加起卦方法特定信息
        if result['method'] == 'number':
            detail_text += f"""

【数字起卦说明】：
    • 数字起卦是一种简便的起卦方法
    • 通过数字的奇偶性和组合来确定卦象
    • 数字范围：1-10
    • 上卦 = 第一个数字 ÷ 8 的余数（余数为0时取8）
    • 下卦 = 第二个数字 ÷ 8 的余数（余数为0时取8）"""
            
            if result['mode'] == '3_numbers':
                detail_text += """
    • 三数字模式：动爻 = 第三个数字 ÷ 6 的余数（余数为0时取6）"""
            else:
                detail_text += """
    • 两数字模式：动爻 = (第一个数字 + 第二个数字) ÷ 6 的余数（余数为0时取6）

═══════════════════════════════════════════════
                    完毕
═══════════════════════════════════════════════
"""
        
        return detail_text

    def number_divination(self, numbers: List[int], mode: str = 'auto') -> Dict:
        """数字起卦
        
        Args:
            numbers: 数字列表，包含2个或3个1-10的数字
            mode: 模式，'2_numbers'或'3_numbers'或'auto'自动判断
        
        Returns:
            包含起卦结果的字典
        """
        if len(numbers) < 2 or len(numbers) > 3:
            raise ValueError("数字起卦需要2个或3个数字")
        
        # 验证数字范围
        for num in numbers:
            if num < 1 or num > 10:
                raise ValueError("数字必须在1-10范围内")
        
        # 自动判断模式
        if mode == 'auto':
            mode = '3_numbers' if len(numbers) == 3 else '2_numbers'
        
        # 计算上卦（第一个数字）
        upper_num = numbers[0]
        upper_remainder = upper_num % 8 if upper_num % 8 != 0 else 8
        upper_gua = self.bagua_map[upper_remainder]
        
        # 计算下卦（第二个数字）
        lower_num = numbers[1]
        lower_remainder = lower_num % 8 if lower_num % 8 != 0 else 8
        lower_gua = self.bagua_map[lower_remainder]
        
        # 计算动爻
        if mode == '3_numbers' and len(numbers) == 3:
            # 三个数字模式：直接使用第三个数字作为动爻
            dong_yao = numbers[2] % 6 if numbers[2] % 6 != 0 else 6
        else:
            # 两个数字模式：两数相加除以6取动爻
            sum_num = upper_num + lower_num
            dong_yao = sum_num % 6 if sum_num % 6 != 0 else 6
        
        # 获取卦名
        gua_name = self.gua_names.get((upper_gua, lower_gua), f"{upper_gua}{lower_gua}")
        
        # 构建数字信息文本
        if mode == '3_numbers':
            numbers_info = f"数字：{numbers[0]}, {numbers[1]}, {numbers[2]} (上卦:{numbers[0]}, 下卦:{numbers[1]}, 动爻:{numbers[2]})"
        else:
            sum_num = upper_num + lower_num
            numbers_info = f"数字：{numbers[0]}, {numbers[1]} (上卦:{numbers[0]}, 下卦:{numbers[1]}, 动爻:{sum_num}%6={dong_yao})"
        
        # 构建六爻线（类似时间起卦的方式）
        upper_lines = self.bagua_symbols[upper_gua]
        lower_lines = self.bagua_symbols[lower_gua]
        hexagram = upper_lines + lower_lines
        
        # 构建动爻标记（只有动爻位置为True，其他为False）
        moving_lines = [False] * 6
        dong_yao_index = dong_yao - 1  # 转换为0-based索引（第1爻=索引0，第2爻=索引1，...，第6爻=索引5）
        if 0 <= dong_yao_index < 6:
            moving_lines[dong_yao_index] = True
        
        return {
            'method': 'number',
            'original_gua': gua_name,
            'upper_gua': upper_gua,
            'lower_gua': lower_gua,
            'dong_yao': dong_yao,
            'numbers': numbers,
            'mode': mode,
            'numbers_info': numbers_info,
            'hexagram': hexagram,
            'moving_lines': moving_lines
        }
    
    def display_hexagram(self, hexagram: List[str], moving_lines: List[bool] = None) -> str:
        """显示卦象"""
        display_lines = []
        for i, line in enumerate(hexagram):
            line_num = len(hexagram) - i
            if moving_lines and moving_lines[i]:
                display_lines.append(f"第{line_num}爻：{line} ◄动爻")
            else:
                display_lines.append(f"第{line_num}爻：{line}")
        return "\n".join(display_lines)


    def calculate_liuqin(self, shangua, xiagua, hexagram):
        """
        计算六爻的六亲关系
        
        Args:
            shangua: 上卦名称
            xiagua: 下卦名称  
            hexagram: 六爻数组 [第1爻, 第2爻, 第3爻, 第4爻, 第5爻, 第6爻]
            
        Returns:
            list: 六亲列表，从第6爻到第1爻的顺序
        """
        # 根据卦名确定本宫五行（修正错误）
        gua_name = self.gua_names.get((shangua, xiagua), f"{shangua}{xiagua}")
        gua_gong = self.gua_gong_mapping.get(gua_name, xiagua)  # 如果找不到，回退到下卦
        bengong_wuxing = self.bagua_wuxing[gua_gong]
        
        # 获取纳甲地支
        shangua_najia = self.bagua_najia[shangua]
        xiagua_najia = self.bagua_najia[xiagua]
        
        # 正确的组合方式：下卦内卦地支（前3个）+ 上卦外卦地支（后3个）
        # 下卦：第1、2、3爻，上卦：第4、5、6爻
        full_najia = xiagua_najia[:3] + shangua_najia[3:]
        
        # 计算每爻的六亲
        liuqin_result = []
        for i in range(6):
            dizhi = full_najia[i]
            yao_wuxing = self.dizhi_wuxing[dizhi]
            liuqin = self.get_liuqin_relation(bengong_wuxing, yao_wuxing)
            liuqin_result.append(liuqin)
        
        # 返回从第6爻到第1爻的顺序（与显示顺序一致）
        return liuqin_result[::-1]
    
    def get_liuqin_relation(self, bengong_wuxing, yao_wuxing):
        """
        根据五行生克关系确定六亲
        
        Args:
            bengong_wuxing: 本宫五行
            yao_wuxing: 爻的五行
            
        Returns:
            str: 六亲名称
        """
        if bengong_wuxing == yao_wuxing:
            return '兄弟'
        elif self.wuxing_shengke[bengong_wuxing]['生'] == yao_wuxing:
            return '子孙'
        elif self.wuxing_shengke[bengong_wuxing]['克'] == yao_wuxing:
            return '妻财'
        elif self.wuxing_shengke[bengong_wuxing]['被生'] == yao_wuxing:
            return '父母'
        elif self.wuxing_shengke[bengong_wuxing]['被克'] == yao_wuxing:
            return '官鬼'
        else:
            return '未知'  # 理论上不应该出现    

    def get_shi_ying_positions(self, gua_name: str) -> Dict[str, int]:
        """
        获取卦象的世应位置
        
        Args:
            gua_name: 卦名
            
        Returns:
            dict: {'世': 世爻位置, '应': 应爻位置}
        """
        return self.complete_shi_ying_positions.get(gua_name, {'世': 0, '应': 0})
    
    def get_liushen_by_day(self, day_gan: str) -> List[str]:
        """
        根据日干获取六神配置
        
        Args:
            day_gan: 日干（甲、乙、丙等）
            
        Returns:
            list: 六神列表，从第6爻到第1爻的顺序
        """
        liushen = self.liushen_by_day.get(day_gan, self.liushen_by_day['甲'])
        # 六神配置表已经是从初爻到六爻的顺序，需要反转为显示顺序（第6爻到第1爻）
        return liushen[::-1]
    
    def get_najia_dizhi(self, shangua: str, xiagua: str) -> List[str]:
        """
        获取六爻的纳甲地支
        
        Args:
            shangua: 上卦名称
            xiagua: 下卦名称
            
        Returns:
            list: 地支列表，从第6爻到第1爻的顺序
        """
        shangua_najia = self.bagua_najia[shangua]
        xiagua_najia = self.bagua_najia[xiagua]
        
        # 正确的组合方式：下卦内卦地支（前3个）+ 上卦外卦地支（后3个）
        # 下卦：第1、2、3爻，上卦：第4、5、6爻
        full_najia = xiagua_najia[:3] + shangua_najia[3:]
        
        # 返回从第6爻到第1爻的顺序（与显示顺序一致）
        return full_najia[::-1]
    
    def get_complete_analysis(self, result: Dict, day_gan: str = '甲') -> Dict:
        """
        获取完整的六爻分析信息
        
        Args:
            result: 起卦结果
            day_gan: 日干，用于确定六神
            
        Returns:
            dict: 完整的分析信息
        """
        gua_name = result['original_gua']
        shangua = result['upper_gua']
        xiagua = result['lower_gua']
        
        # 获取世应位置
        shi_ying = self.get_shi_ying_positions(gua_name)
        
        # 获取六神
        liushen = self.get_liushen_by_day(day_gan)
        
        # 获取纳甲地支
        najia_dizhi = self.get_najia_dizhi(shangua, xiagua)
        
        # 计算六亲
        if 'hexagram' in result:
            # 铜钱起卦或数字起卦有hexagram字段
            liuqin = self.calculate_liuqin(shangua, xiagua, result['hexagram'])
        else:
            # 时间起卦需要构建hexagram
            upper_lines = self.bagua_symbols[shangua]
            lower_lines = self.bagua_symbols[xiagua]
            hexagram = upper_lines + lower_lines
            liuqin = self.calculate_liuqin(shangua, xiagua, hexagram)
        
        # 获取五行属性
        wuxing_list = []
        for dizhi in najia_dizhi:
            wuxing_list.append(self.dizhi_wuxing[dizhi])
        
        # 构建完整的六爻信息（从第6爻到第1爻）
        liuyao_info = []
        for i in range(6):
            yao_num = 6 - i
            yao_info = {
                '爻位': f'第{yao_num}爻',
                '六神': liushen[i],
                '六亲': liuqin[i],
                '纳甲': najia_dizhi[i],
                '五行': wuxing_list[i],
                '世应': ''
            }
            
            # 标记世应
            if shi_ying['世'] == yao_num:
                yao_info['世应'] = '世'
            elif shi_ying['应'] == yao_num:
                yao_info['世应'] = '应'
            
            # 标记动爻
            if result['method'] in ['time', 'number'] and 'dong_yao' in result:
                if yao_num == result['dong_yao']:
                    yao_info['动爻'] = True
                else:
                    yao_info['动爻'] = False
            elif result['method'] == 'coin' and 'moving_lines' in result:
                # 铜钱起卦的动爻标记
                yao_info['动爻'] = result['moving_lines'][yao_num - 1]
            else:
                yao_info['动爻'] = False
            
            liuyao_info.append(yao_info)
        
        return {
            'gua_name': gua_name,
            'upper_gua': shangua,
            'lower_gua': xiagua,
            'shi_ying_positions': {'shi': shi_ying['世'], 'ying': shi_ying['应']},
            'liushen': [info['六神'] for info in liuyao_info],
            'liuqin': [info['六亲'] for info in liuyao_info],
            'najia_dizhi': [info['纳甲'] for info in liuyao_info],
            'wuxing': [info['五行'] for info in liuyao_info],
            'liuyao_info': liuyao_info,
            'ben_gong_wuxing': self.bagua_wuxing[xiagua],
            'method': result['method']
        }
    

    def get_current_tiangan(self) -> str:
        """自动获取当前日期的天干"""
        """
        补充说明
        该公式适用于 格里历（公历）；
        可用于计算 日干，即当天的天干；
        要扩展至整套的干支（包括地支），还需要类似公式计算“日支”，或者采用累加干支数的方式。
        """
        try:
            # 获取当前日期
            today = datetime.now()
            year = today.year
            month = today.month
            day = today.day
            
            # 处理1月和2月，按上一年的13月和14月计算
            if month <= 2:
                year -= 1
                month += 12
            
            # 计算世纪数和年份后两位
            C = year // 100
            y = year % 100
            
            # 使用日干支计算公式
            # g = 4C + [C/4] + 5y + [y/4] + [3*(M+1) / 5] + d - 3
            g = (4 * C + C // 4 + 5 * y + y // 4 + 
                (3 * (month + 1)) // 5 + day - 3)
            
            # 计算天干序号（g除以10的余数）
            tiangan_index = g % 10
            if tiangan_index == 0:
                tiangan_index = 10
            
            # 转换为天干（序号从1开始，数组从0开始）
            tiangan = self.tiangan[tiangan_index - 1]
            
            return tiangan
            
        except Exception as e:
            # 如果计算失败，返回默认值
            return '甲'
    
    def get_auto_day_gan(self) -> str:
        """获取自动日干（兼容方法）"""
        return self.get_current_tiangan()

def create_session_state():
    """创建会话状态"""
    if 'yijing_core' not in st.session_state:
        st.session_state.yijing_core = YijingCore()
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'changed_result' not in st.session_state:
        st.session_state.changed_result = None
    if 'coin_progress' not in st.session_state:
        st.session_state.coin_progress = 0
    if 'coin_results' not in st.session_state:
        st.session_state.coin_results = []
    