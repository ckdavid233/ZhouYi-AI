#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数字起卦的动爻变化逻辑
"""

from yijing_core import YijingCore

def test_number_divination():
    """测试数字起卦的动爻变化"""
    yijing = YijingCore()
    
    # 测试案例1：第3爻动
    print("=== 测试案例1：第3爻动 ===")
    numbers1 = [3, 7, 3]  # 第三个数字3，3%6=3，所以第3爻动
    result1 = yijing.number_divination(numbers1)
    changed1 = yijing.get_changed_gua(result1)
    
    print(f"数字：{numbers1}")
    print(f"动爻：第{result1['dong_yao']}爻")
    print(f"本卦：{result1['original_gua']}")
    print(f"变卦：{changed1['name']}")
    
    # 显示本卦六爻
    print("\n本卦六爻：")
    upper_lines = yijing.bagua_symbols[result1['upper_gua']]
    lower_lines = yijing.bagua_symbols[result1['lower_gua']]
    all_lines = upper_lines + lower_lines
    for i, line in enumerate(all_lines):
        line_num = 6 - i
        is_dong = line_num == result1['dong_yao']
        print(f"第{line_num}爻：{line} {'← 动爻' if is_dong else ''}")
    
    # 显示变卦六爻
    print("\n变卦六爻：")
    for i, line in enumerate(changed1['lines']):
        line_num = 6 - i
        print(f"第{line_num}爻：{line}")
    
    # 验证动爻变化是否正确
    original_dong_line = all_lines[6 - result1['dong_yao']]
    changed_dong_line = changed1['lines'][6 - result1['dong_yao']]
    print(f"\n动爻变化验证：")
    print(f"原动爻（第{result1['dong_yao']}爻）：{original_dong_line}")
    print(f"变动爻（第{result1['dong_yao']}爻）：{changed_dong_line}")
    
    # 检查是否正确变化
    if original_dong_line == '━━━' and changed_dong_line == '━ ━':
        print("✓ 动爻变化正确：阳爻变阴爻")
    elif original_dong_line == '━ ━' and changed_dong_line == '━━━':
        print("✓ 动爻变化正确：阴爻变阳爻")
    else:
        print("✗ 动爻变化错误！")
    
    print("\n" + "="*50 + "\n")
    
    # 测试案例2：第2爻动
    print("=== 测试案例2：第2爻动 ===")
    numbers2 = [5, 8, 2]  # 第三个数字2，2%6=2，所以第2爻动
    result2 = yijing.number_divination(numbers2)
    changed2 = yijing.get_changed_gua(result2)
    
    print(f"数字：{numbers2}")
    print(f"动爻：第{result2['dong_yao']}爻")
    print(f"本卦：{result2['original_gua']}")
    print(f"变卦：{changed2['name']}")
    
    # 显示本卦六爻
    print("\n本卦六爻：")
    upper_lines = yijing.bagua_symbols[result2['upper_gua']]
    lower_lines = yijing.bagua_symbols[result2['lower_gua']]
    all_lines = upper_lines + lower_lines
    for i, line in enumerate(all_lines):
        line_num = 6 - i
        is_dong = line_num == result2['dong_yao']
        print(f"第{line_num}爻：{line} {'← 动爻' if is_dong else ''}")
    
    # 显示变卦六爻
    print("\n变卦六爻：")
    for i, line in enumerate(changed2['lines']):
        line_num = 6 - i
        print(f"第{line_num}爻：{line}")
    
    # 验证动爻变化是否正确
    original_dong_line = all_lines[6 - result2['dong_yao']]
    changed_dong_line = changed2['lines'][6 - result2['dong_yao']]
    print(f"\n动爻变化验证：")
    print(f"原动爻（第{result2['dong_yao']}爻）：{original_dong_line}")
    print(f"变动爻（第{result2['dong_yao']}爻）：{changed_dong_line}")
    
    # 检查是否正确变化
    if original_dong_line == '━━━' and changed_dong_line == '━ ━':
        print("✓ 动爻变化正确：阳爻变阴爻")
    elif original_dong_line == '━ ━' and changed_dong_line == '━━━':
        print("✓ 动爻变化正确：阴爻变阳爻")
    else:
        print("✗ 动爻变化错误！")

if __name__ == "__main__":
    test_number_divination()