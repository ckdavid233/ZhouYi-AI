import json
from yijing_core import YijingCore

def extract_liuyao_data(gua_data, complete_analysis, changed_gua_data, question):
    basic_info = {
        "起卦方法": get_method_name(gua_data['method']),
        "本卦":{
            "卦名": gua_data['original_gua'],
            "上卦": gua_data['upper_gua'],
            "下卦": gua_data['lower_gua']
        },
        "变卦":{
            "卦名": changed_gua_data['name'],
            "上卦": changed_gua_data['upper_gua'],
            "下卦": changed_gua_data['lower_gua']
        },
        "用户问题": question if question else "无特定问题"
    }
    dong_yao_info = extract_moving_lines(gua_data)
    liu_yao_details = extract_liuyao_details(gua_data, complete_analysis)
    shi_ying = {
        "世爻位置": complete_analysis['shi_ying_positions']['shi'],
        "应爻位置": complete_analysis['shi_ying_positions']['ying']
    }
    return {
        "基本信息": basic_info,
        "动爻信息": dong_yao_info,
        "爻位分析": liu_yao_details,
        "世应关系": shi_ying
    }

def get_method_name(method):
    method_map = {
        'time': '年月日时起卦',
        'coin': '铜钱起卦',
        'number': '数字起卦'
    }
    return method_map.get(method, '未知方法')

def extract_moving_lines(gua_data):
    if gua_data['method'] in ['time', 'number']:
        return {
            "动爻数量" : 1,
            "动爻位置" : [gua_data['dong_yao']],
            "动爻描述" : f"第{gua_data['dong_yao']}爻为动爻"
        }
    else:
        moving_positions = [i+1 for i, is_moving in enumerate(gua_data['moving_lines']) if is_moving]
        return {
            "动爻数量" : len(moving_positions),
            "动爻位置" : moving_positions,
            "动爻描述" : f"第{','.join(map(str, moving_positions))}爻为动爻" if moving_positions else "无动爻"
        }

def extract_liuyao_details(gua_data, complete_analysis):
    liuyao_list = []
    yijing_core = YijingCore()

    if gua_data['method'] in ['time', 'number']:
        upper_lines = yijing_core.bagua_symbols[gua_data['upper_gua']]
        lower_lines = yijing_core.bagua_symbols[gua_data['lower_gua']]
        all_lines = upper_lines + lower_lines
        for i, line in enumerate(all_lines):
            line_num = 6 - i
            is_dong = line_num == gua_data['dong_yao']
            yao_index = line_num - 1

            yao_info = build_yao_info(line_num, line, is_dong, complete_analysis, yao_index)
            liuyao_list.append(yao_info)
    else:
        for i in range(5, -1, -1):
            line = gua_data['hexagram'][i]
            is_moving = gua_data['moving_lines'][i]
            line_num = i + 1
            yao_index = line_num - 1
            yao_info = build_yao_info(line_num, line, is_moving, complete_analysis, yao_index)
            liuyao_list.append(yao_info)

    return liuyao_list

def build_yao_info(line_num, line, is_dong, complete_analysis, yao_index):
    """构建单个爻的详细信息"""
    # 世应标记
    shi_ying_mark = ""
    if line_num == complete_analysis['shi_ying_positions']['shi']:
        shi_ying_mark = "世"
    elif line_num == complete_analysis['shi_ying_positions']['ying']:
        shi_ying_mark = "应"
    
    return {
        "爻位": line_num,
        "爻象": line,
        "阴阳": "阳爻" if line == "━━━" else "阴爻",
        "是否动爻": is_dong,
        "六神": complete_analysis['liushen'][5-yao_index],
        "六亲": complete_analysis['liuqin'][5-yao_index],
        "纳甲地支": complete_analysis['najia_dizhi'][5-yao_index],
        "五行": complete_analysis['wuxing'][5-yao_index],
        "世应": shi_ying_mark,
        "动静状态": "动爻" if is_dong else "静爻"
    }


def format_for_ai_analysis(extracted_data):
    """
    将提取的数据格式化为适合AI分析的结构化文本
    """
    basic_info = extracted_data["基本信息"]
    dong_yao_info = extracted_data["动爻信息"]
    liuyao_details = extracted_data["爻位分析"]
    shi_ying = extracted_data["世应关系"]
    
    formatted_text = f"""【六爻算卦完整信息】

=== 基础卦象信息 ===
起卦方法：{basic_info["起卦方法"]}
本卦：《{basic_info["本卦"]["卦名"]}》（{basic_info["本卦"]["上卦"]}上{basic_info["本卦"]["下卦"]}下）
变卦：《{basic_info["变卦"]["卦名"]}》（{basic_info["变卦"]["上卦"]}上{basic_info["变卦"]["下卦"]}下）
用户问题：{basic_info["用户问题"]}

=== 动爻信息 ===
{dong_yao_info["动爻描述"]}
动爻数量：{dong_yao_info["动爻数量"]}个

=== 世应关系 ===
世爻：第{shi_ying["世爻位置"]}爻
应爻：第{shi_ying["应爻位置"]}爻

=== 六爻详细配置 ==="""
    
    # 添加每一爻的详细信息
    for yao in liuyao_details:
        shi_ying_text = f"【{yao['世应']}】" if yao['世应'] else ""
        dong_text = "◄动爻" if yao['是否动爻'] else ""
        
        formatted_text += f"""
第{yao['爻位']}爻：{yao['爻象']} | {yao['六神']} {yao['六亲']} {yao['纳甲地支']}({yao['五行']}) {shi_ying_text} {dong_text}"""
    
    return formatted_text

def format_for_json_output(extracted_data):
    """将数据格式化为JSON格式便于程序处理"""
    return json.dumps(extracted_data, ensure_ascii=False, indent=2)

def format_for_display(extracted_data):
    """格式化为用户友好的显示格式"""
    formatted = format_for_ai_analysis(extracted_data)
    
    # 添加分析建议
    formatted += f"""

=== 分析要点提示 ===
1. 重点关注动爻：{extracted_data['动爻信息']['动爻描述']}
2. 世应关系：世爻代表求测者，应爻代表所测之事
3. 六神配置：反映事物的性质和发展趋势
4. 六亲关系：体现人事关系和利益得失
5. 五行生克：分析事物间的相互作用关系"""
    
    return formatted


