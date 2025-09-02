from typing import Dict

class LiuyaoFormatter:
    """六爻分析结果格式化器"""
    
    def __init__(self, yijing_core):
        """初始化格式化器
        
        Args:
            yijing_core: YijingCore实例，用于访问八卦符号等数据
        """
        self.yijing_core = yijing_core
    
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
            all_lines = self.yijing_core.bagua_symbols[result['upper_gua']] + self.yijing_core.bagua_symbols[result['lower_gua']]
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