import streamlit as st
import json
import requests
import sys
import os
import re

# 添加上级目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yijing_core import YijingCore
from liuyao_data_extractor import extract_liuyao_data, format_for_ai_analysis


# 页面配置
st.set_page_config(
    page_title="AI智能分析",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def generate_ai_prompt(gua_data, complete_analysis, changed_gua_data, question=""):
    """生成发送给AI的提示词 - 增强版本"""
    
    # 使用新的数据提取函数
    extracted_data = extract_liuyao_data(gua_data, complete_analysis, changed_gua_data, question)
    
    # 格式化为AI分析格式
    structured_info = format_for_ai_analysis(extracted_data)
    
    # 构建完整提示词
    prompt = f"""你是一位资深的易经六爻分析大师，拥有数十年的实战经验。请基于以下完整的卦象信息进行深入详细的分析：

{structured_info}
【重要要求】
1. 必须严格按照上述五个部分的顺序和格式输出
2. 每个【】标题必须单独一行，标题后直接开始内容
3. 每部分内容必须充实详细，达到指定字数要求
4. 分析要结合传统易经理论和现代实际情况
5. 语言要专业而通俗，避免过于晦涩的术语
6. 建议要具体可操作，不要空泛的理论
7. 完成【深度问题分析与建议指导】部分后立即结束
8. 绝对不要添加任何总结、结束语、问候语或其他内容
9. 不要重复已经说过的内容
10. 不要出现"现在开始分析"、"请问还有其他问题吗"等提示语
11. 必须全程使用中文回答，绝对不要使用英文或其他语言
12. 如果遇到复杂概念，用中文进行解释，不要切换语言
请严格按照以下格式输出分析结果，每个标题单独一行:

【卦象基本含义】
详细解释本卦和变卦的象征意义，包括：
- 两卦的基本象征和内涵
- 上下卦的具体含义和相互关系
- 卦象所体现的时运特点
- 整体卦象传达的核心信息
要求内容丰富详实，字数控制在150-200字，必须直接开始内容，不要添加任何引导语。

【本卦与变卦关系】
深入分析本卦到变卦的转化过程，包括：
- 变化的内在逻辑和必然性
- 事物发展的阶段性特征
- 变卦所预示的未来趋势
- 变化过程中需要注意的关键点
要求分析透彻，字数控制在200-300字，必须直接开始内容，不要添加任何引导语。

【动爻分析】
重点解读动爻的具体含义和影响，包括：
- 准确获取我发送给你的动爻信息分析，不要自己胡编乱造
- 动爻在整个卦象中的地位和作用
- 动爻对事态发展的具体影响
- 动爻所在位置的特殊意义
- 动爻变化带来的机遇与挑战
要求解读精准，字数控制在200-300字，必须直接开始内容，不要添加任何引导语。

【六神六亲综合分析】
结合六神六亲配置分析事物性质（包括本卦和变卦的六神六亲配置都要分析，而且找到关联的地方），包括：
- 各爻位六神的具体含义和作用
- 六亲关系对事态的影响
- 世应关系的深层含义
- 纳甲五行的生克制化
要求分析全面，字数控制在400-500字，必须直接开始内容，不要添加任何引导语。

【深度问题分析与建议指导】
基于以上卦象分析，针对用户的具体问题进行深入剖析和指导，要求："""

    # 根据是否有问题，给出不同的指导要求
    if question:
        prompt += f"""
- 从卦象角度深入分析当前问题的本质和根源，包括问题产生的深层原因
- 详细解读问题可能的发展走向和结果，分析最好、最坏、最可能的三种情况
- 全面分析问题中的有利因素和不利因素，逐一列举并详细说明
- 给出具体可操作的解决方案和行动建议，包括具体的实施步骤
- 提供时机把握的具体指导，明确什么时候该做什么
- 预测可能遇到的困难和应对策略，提前做好准备
- 给出长远规划和短期行动的建议，制定阶段性目标
- 深入分析人际关系和环境因素的影响，包括贵人、小人、合作伙伴等
- 提供心态调整和思维转变的建议，包括如何保持积极心态
- 给出具体的行动步骤和时间节点，制定详细的行动计划
- 分析成功的关键要素和注意事项，明确成功的标准
- 提供风险防范和应急预案，预防可能的风险
- 分析资源配置和能力提升的建议，包括需要学习什么技能
- 提供沟通技巧和策略建议，如何与相关人员有效沟通
- 给出财务规划和投资建议（如果涉及财运问题）
- 分析健康和生活方式的调整建议（如果涉及健康问题）
- 提供学习和成长的具体方向（如果涉及学业或职业发展）
要求分析全面深入，建议具体可行，内容详实丰富，字数控制在600-800字"""
    else:
        prompt += f"""
- 基于卦象分析当前整体运势和发展趋势，包括近期、中期、长期的运势变化
- 详细指出当前阶段的机遇和挑战，分析如何把握机遇、应对挑战
- 给出生活、工作、感情等各方面的具体建议，每个方面都要详细展开
- 提供行为准则和处事原则的指导，包括做人做事的基本原则
- 分析适合的发展方向和策略选择，明确哪些方向最有前景
- 给出时机把握和风险规避的建议，什么时候进什么时候退
- 深入分析人际关系和社交策略，如何建立和维护良好的人际关系
- 提供财运、健康、学业等方面的详细指导，每个方面都要具体分析
- 给出性格完善和能力提升的建议，包括需要改进的性格缺陷
- 分析环境变化和适应策略，如何在变化中保持优势
- 提供长期规划和阶段性目标，制定人生发展的路线图
- 给出具体的实施方法和注意要点，包括具体的行动指南
- 分析家庭关系和亲情处理，如何平衡家庭和事业
- 提供投资理财和财富积累的建议，如何实现财务自由
- 给出健康养生和生活方式的指导，如何保持身心健康
- 分析学习成长和技能提升的方向，终身学习的规划
- 提供情感生活和婚恋关系的建议，如何经营好感情生活
要求分析全面，建议实用，内容详实丰富，字数控制在800-1000字"""

    prompt += f"""
现在请开始详细分析："""
    
    return prompt

def clean_repeated_content(text, is_final=False):
    """
    优化的重复内容清理函数 - 加强版
    """
    if not text:
        return text
        
    result = text.strip()
    
    # 统一换行符
    result = result.replace('\r\n', '\n').replace('\r', '\n')
    
    # 更精确地截断在合适位置
    # 首先查找【深度问题分析与建议指导】部分的结束
    analysis_pattern = r'【深度问题分析与建议指导】'
    matches = list(re.finditer(analysis_pattern, result))
    
    if len(matches) >= 1:
        # 找到该部分的开始位置
        start_pos = matches[0].end()
        
        # 如果有重复的标题，在第二次出现前截断
        if len(matches) > 1:
            second_pos = matches[1].start()
            result = result[:second_pos]
        else:
            # 在该部分后寻找自然结束点，但允许更长的内容
            # 查找是否有其他不应该出现的内容
            unwanted_start_markers = [
                '现在开始分析',
                '请开始分析',
                '好的，请问',
                '还有其他问题',
                '以上就是',
                '分析完毕',
                '希望对您有帮助'
            ]
            
            # 查找该部分的结束位置（通过下一个标题或内容结束）
            # 寻找下一个【标题】或明显结束标志
            next_title_pattern = r'\n\s*【[^】]*】'
            next_title_match = re.search(next_title_pattern, result[start_pos:])
            
            if next_title_match:
                # 如果找到下一个标题，在该标题前截断
                next_title_pos = start_pos + next_title_match.start()
                # 向前查找句子结束点
                for i in range(next_title_pos - 1, start_pos, -1):
                    if result[i] in '。！？.!?':
                        result = result[:i + 1]
                        break
            else:
                # 如果没找到下一个标题，查找明显的结束标志
                for marker in unwanted_start_markers:
                    marker_pos = result.find(marker, start_pos)
                    if marker_pos > 0:
                        # 在标记前寻找句子结束点
                        for i in range(marker_pos - 1, start_pos, -1):
                            if result[i] in '。！？.!?':
                                result = result[:i + 1]
                                break
                        break
    
    # 移除开头和结尾的unwanted phrases
    unwanted_phrases = [
        r'现在请?开始详?细?分析[：:]?.*?$',
        r'请开始分析[：:]?.*?$',
        r'现在开始分析[：:]?.*?$',
        r'请问您?还有其他问题吗[？?]?.*?$',
        r'好的，请问您?还有其他问题吗[？?]?.*?$',
        r'以上.*?分析.*?$',
        r'希望.*?有帮助.*?$',
        r'分析完毕?.*?$',
        r'【结束】.*?$',
        r'\[DONE\].*?$',
        r'答案[:：]?\s*$',
    ]
    
    for pattern in unwanted_phrases:
        result = re.sub(pattern, '', result, flags=re.MULTILINE | re.DOTALL)
    
    # 移除重复的标题（但保留一个）
    title_pattern = r'(【[^】]+】)(?:\s*\n\s*\1)+'
    result = re.sub(title_pattern, r'\1', result)
    
    # 移除明显的重复段落
    lines = result.split('\n')
    unique_lines = []
    seen_content = set()
    
    for line in lines:
        line = line.strip()
        if not line:
            if unique_lines and unique_lines[-1] != '':
                unique_lines.append('')
            continue
            
        # 检查是否为重复内容（忽略短行和标题）
        if len(line) > 30 and not line.startswith('【'):
            if line in seen_content:
                continue
            seen_content.add(line)
        
        unique_lines.append(line)
    
    result = '\n'.join(unique_lines)
    
    # 清理多余的空白行（最多连续2个换行）
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # 确保每个【】标题前有适当换行，但不要太多
    result = re.sub(r'([^】\n])(\n?【[^】]+】)', r'\1\n\n\2', result)
    result = re.sub(r'^【', '【', result)  # 第一个标题前不需要换行
    
    return result.strip()


def send_to_ai_model_streaming(prompt):
    """发送请求到AI模型并流式显示结果"""
    # 从会话状态获取配置，如果没有则使用默认值
    api_url = st.session_state.get('ai_api_url', 'http://localhost:8000/v1/completions')
    model_name = st.session_state.get('ai_model_name', 'Qwen3-30B-A3B-AWQ')
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 优化的参数设置
    data = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": 20480,  # 减少最大token数避免过度生成
        "temperature": 0.3,  # 降低温度
        "top_p": 0.8,
        "presence_penalty": 0.1,  # 增加惩罚减少重复
        "frequency_penalty": 0.1,  # 增加惩罚减少重复
        "stream": True,
        "stop": ["现在开始分析：", "请开始分析：", "【结束】", "Okay, I need", "Let me", "continue provide", "请 continue", "好的，在用户"] # 添加停止词
    }
    
    # 创建占位符
    result_placeholder = st.empty()
    accumulated_text = ""
    last_display_text = ""
    display_started = False


    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=100, stream=True)
        response.raise_for_status()
        
        # 流式处理响应
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str.strip() == '[DONE]':
                        break
                    
                    try:
                        chunk_data = json.loads(data_str)
                        if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                            delta = chunk_data['choices'][0].get('text', '')
                            if delta:
                                accumulated_text += delta
                                
                                # 实时检查是否应该停止
                                if should_stop_generation(accumulated_text):
                                    break
                                
                                # 检测是否开始正文（检测到第一个标题）
                                if not display_started:
                                    if '【卦象基本含义】' in accumulated_text:
                                        display_started = True
                                        # 从第一个标题开始显示
                                        start_pos = accumulated_text.find('【卦象基本含义】')
                                        accumulated_text = accumulated_text[start_pos:]
                                
                                # 只有开始显示后才进行清理和显示
                                if display_started:
                                    display_text = clean_for_display(accumulated_text)
                                    if display_text != last_display_text:
                                        if (len(display_text) - len(last_display_text) > 3 or 
                                            any(title in display_text and title not in last_display_text 
                                                for title in ['【卦象基本含义】', '【本卦与变卦关系】', '【动爻分析】', '【六神六亲综合分析】', '【深度问题分析与建议指导】'])):
                                            last_display_text = display_text
                                            formatted_text = format_for_display(display_text)
                                            result_placeholder.markdown(formatted_text, unsafe_allow_html=True)
                                    
                    except json.JSONDecodeError:
                        continue
        
        # 最终处理
        if display_started:
            final_result = clean_repeated_content(accumulated_text, is_final=True)
        else:
            # 如果没有检测到正文开始，尝试从整个文本中提取
            final_result = clean_repeated_content(accumulated_text, is_final=True)
            
        st.session_state.ai_analysis_result = final_result
        
        # 最终显示
        formatted_final = format_for_display(final_result)
        result_placeholder.markdown(formatted_final, unsafe_allow_html=True)
        
        return final_result
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败：{str(e)}")
    except Exception as e:
        raise Exception(f"请求处理失败：{str(e)}")


def should_stop_generation(text):
    """判断是否应该停止生成 - 改进版"""
    # 如果出现第二个主要标题，应该停止
    main_titles = ['【卦象基本含义】', '【本卦与变卦关系】', '【动爻分析】', '【深度问题分析与建议指导】']
    
    for title in main_titles:
        if text.count(title) > 1:
            return True
    
    # 特殊处理：如果【深度问题分析与建议指导】部分已经完整生成
    # 检查是否包含该部分的所有要求内容
    if '【深度问题分析与建议指导】' in text:
        # 检查是否包含足够的内容（字数判断）
        analysis_section = text.split('【深度问题分析与建议指导】')[-1]
        # 如果该部分内容足够长，且后面出现了其他标题或结束标志，则停止
        if len(analysis_section) > 200:
            # 检查是否出现其他标题或结束标志
            remaining_text = text[text.find('【深度问题分析与建议指导】') + len('【深度问题分析与建议指导】') + len(analysis_section):]
            other_titles = ['【卦象基本含义】', '【本卦与变卦关系】', '【动爻分析】']
            for title in remaining_text:
                if title in remaining_text:
                    return True
            
            # 检查是否出现结束标志
            end_markers = [
                '现在开始分析',
                '请开始分析', 
                '好的，请问',
                '还有其他问题',
                '希望对您有帮助',
                '分析完毕',
                '以上就是'
            ]
            for marker in end_markers:
                if marker in remaining_text:
                    return True
    
    # 如果出现明显的结束标志
    end_markers = [
        '现在开始分析',
        '请开始分析', 
        '好的，请问',
        '还有其他问题',
        '希望对您有帮助',
        '分析完毕',
        '以上就是'
    ]
    
    for marker in end_markers:
        if marker in text:
            return True
    
    # 如果内容过长（防止无限生成）
    if len(text) > 2000:
        return True
        
    return False


def clean_for_display(text):
    """为实时显示清理文本 - 改进版"""
    if not text:
        return text
        
    # 基本清理
    result = text.strip()
    
    # 移除开始分析的提示
    result = re.sub(r'现在请?开始详?细?分析[：:]?.*?(?=【|$)', '', result, flags=re.MULTILINE | re.DOTALL)
    
    # 检查是否有重复的主标题，但只在内容足够长时才截断
    main_titles = ['【卦象基本含义】', '【本卦与变卦关系】', '【动爻分析】', '【深度问题分析与建议指导】']
    
    for title in main_titles:
        # 只有当标题出现次数大于1且内容足够长时才考虑截断
        title_count = result.count(title)
        if title_count > 1:
            # 检查每个标题后的内容长度
            parts = result.split(title)
            # 如果有足够的部分且中间部分足够长，则保留前两部分
            if len(parts) >= 3 and len(parts[1]) > 50:
                result = title.join(parts[:3])
            elif len(parts) >= 2:
                # 如果第二部分较短，可能是正在生成中，暂时不截断
                if len(parts[1]) < 50 and title_count == 2:
                    # 保留所有内容，等待更多内容生成
                    pass
                else:
                    # 在第二次出现的位置截断
                    first_pos = result.find(title)
                    second_pos = result.find(title, first_pos + 1)
                    # 尝试找到更自然的结束点
                    for i in range(second_pos - 1, max(0, second_pos - 200), -1):
                        if result[i] in '。！？.!?':
                            result = result[:i + 1]
                            break
                    else:
                        result = result[:second_pos]
    
    # 移除明显的结束语，但避免在内容生成过程中移除
    end_patterns = [
        r'(?:现在开始|请开始|好的请问|还有其他问题|希望.*?有帮助|分析完毕).*?$',
    ]
    
    for pattern in end_patterns:
        # 只有在内容足够长时才移除结束语
        if len(result) > 300:
            result = re.sub(pattern, '', result, flags=re.MULTILINE | re.DOTALL)
    
    return result.strip()


def format_for_display(text):
    """格式化文本用于显示"""
    if not text:
        return text
        
    # 确保标题前后有适当的换行
    # 使用更安全的方式处理标题格式化，避免在内容生成过程中出现不完整的HTML标签
    formatted = re.sub(r'(【[^】]+】)', r'<br><strong>\1</strong><br>', text)
    
    # 处理第一个标题前不需要换行
    formatted = re.sub(r'^<br>', '', formatted)
    
    # 处理可能的不完整HTML标签（在流式生成过程中可能出现）
    # 确保<strong>标签是成对出现的
    open_strong_count = formatted.count('<strong>')
    close_strong_count = formatted.count('</strong>')
    
    # 如果<strong>标签数量多于</strong>标签，添加缺失的</strong>标签
    if open_strong_count > close_strong_count:
        formatted += '</strong>' * (open_strong_count - close_strong_count)
    
    # 包装在样式div中
    return f'<div class="result-box" style="line-height: 1.8; font-family: \'Microsoft YaHei\', sans-serif;">{formatted}</div>'


# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-family: '华文行楷', cursive;
        font-size: 2.5em;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .ai-text {
        font-family: '微软雅黑', 'Microsoft YaHei', sans-serif;
        font-weight: bold;
        font-style: normal;
        display: inline-block;
        transform: skewX(-5deg);
    }
    .analysis-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .yao-detail {
        color: #2c3e50 !important;
        font-size: 18px;
        line-height: 1.8;
        font-weight: 500;
    }
    .yao-detail.dong-yao {
        color: #ff6b6b !important;
        font-weight: bold;
        font-size: 18px;
    }
    .result-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Microsoft YaHei', sans-serif;
        line-height: 1.8;
        font-size: 18px;
    }
    .result-box strong {
        color: #2c3e50;
        font-size: 1.1em;
        display: block;
        margin: 15px 0 8px 0;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 5px;
    }
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    .back-button {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 0;
    }
    .back-button:hover {
        background: linear-gradient(135deg, #bdc3c7, #95a5a6);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'ai_analysis_result' not in st.session_state:
    st.session_state.ai_analysis_result = None
if 'ai_analyzing' not in st.session_state:
    st.session_state.ai_analyzing = False
if 'ai_api_url' not in st.session_state:
    st.session_state.ai_api_url = 'http://localhost:8000/v1/completions'
if 'ai_model_name' not in st.session_state:
    st.session_state.ai_model_name = 'Qwen3-30B-A3B-AWQ'

# 返回按钮
if st.button("← 返回主页"):
    st.switch_page("pages/主页.py")

# 主标题
st.markdown("<h1 class='main-header'>🤖 <span class='ai-text'>AI</span>卦象智能分析</h1>", unsafe_allow_html=True)

# AI配置区域
st.markdown("### ⚙️ AI模型配置")
with st.expander("点击配置AI模型设置", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        api_url = st.text_input(
            "API地址",
            value=st.session_state.ai_api_url,
            placeholder="例如：http://localhost:8000/v1/completions",
            key="api_url_input"
        )
        
        if api_url != st.session_state.ai_api_url:
            st.session_state.ai_api_url = api_url
            st.success("API地址已更新")
    
    with col2:
        model_name = st.text_input(
            "模型名称",
            value=st.session_state.ai_model_name,
            placeholder="例如：Qwen3-30B-A3B-AWQ",
            key="model_name_input"
        )
        
        if model_name != st.session_state.ai_model_name:
            st.session_state.ai_model_name = model_name
            st.success("模型名称已更新")
    
    st.markdown("**使用说明：**")
    st.markdown("- API地址：本地AI服务的完整URL，通常为 `http://localhost:8000/v1/completions`")
    st.markdown("- 模型名称：您要使用的AI模型名称，根据您的本地服务配置填写")
    st.markdown("- 修改配置后，下次分析时会自动使用新设置")

# 检查是否有卦象数据
if 'current_result' not in st.session_state or st.session_state.current_result is None:
    st.error("请先在主页进行起卦操作！")
    if st.button("← 返回主页起卦"):
        st.switch_page("pages/主页.py")
else:
    # 获取卦象数据
    gua_data = st.session_state.current_result
    changed_gua_data = st.session_state.changed_result
    
    # 初始化YijingCore实例
    if 'yijing_core' not in st.session_state:
        st.session_state.yijing_core = YijingCore()
    
    # 获取当前日干
    selected_day_gan = st.session_state.yijing_core.get_current_tiangan()
    
    # 用户问题输入
    st.markdown("### 🤔 占卜问题")
    question = st.text_input(
        "请输入您想咨询的问题（可选）：",
        placeholder="例如：是否应该接受这份工作？感情发展如何？投资决策建议？",
        key="question_input"
    )
    
    # 显示卦象信息
    st.markdown("### 📊 卦象信息")
    
    # 获取完整分析信息
    try:
        complete_analysis = st.session_state.yijing_core.get_complete_analysis(gua_data, selected_day_gan)
        
        # 为变卦创建临时result结构
        changed_result_for_analysis = {
            'original_gua': changed_gua_data['name'],
            'upper_gua': changed_gua_data['upper_gua'],
            'lower_gua': changed_gua_data['lower_gua'],
            'method': gua_data['method']
        }
        
        # 如果是铜钱起卦，添加hexagram字段
        if gua_data['method'] == 'coin':
            changed_result_for_analysis['hexagram'] = changed_gua_data['lines']
        
        changed_analysis = st.session_state.yijing_core.get_complete_analysis(changed_result_for_analysis, selected_day_gan)
        
    except Exception as e:
        st.error(f"获取详细分析失败：{str(e)}")
        complete_analysis = None
        changed_analysis = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='analysis-box'>", unsafe_allow_html=True)
        st.markdown(f"**本卦：《{gua_data['original_gua']}》**")
        st.markdown(f"**上卦：** {gua_data['upper_gua']}")
        st.markdown(f"**下卦：** {gua_data['lower_gua']}")
        
        if gua_data['method'] == 'time':
            st.markdown(f"**起卦方法：** 年月日时起卦")
            st.markdown(f"**动爻：** 第{gua_data['dong_yao']}爻")
            st.markdown(f"**时间：** {gua_data['time_info']}")
        elif gua_data['method'] == 'number':
            st.markdown(f"**起卦方法：** 数字起卦")
            st.markdown(f"**动爻：** 第{gua_data['dong_yao']}爻")
            st.markdown(f"**数字：** {gua_data['numbers_info']}")
        else:
            st.markdown(f"**起卦方法：** 铜钱起卦")
            st.markdown(f"**动爻：** {sum(gua_data['moving_lines'])}个动爻")
        
        # 显示六爻详细信息（本卦）
        if complete_analysis:
            st.markdown("\n**六爻详情：**")
            if gua_data['method'] == 'time':
                # 时间起卦显示
                upper_lines = st.session_state.yijing_core.bagua_symbols[gua_data['upper_gua']]
                lower_lines = st.session_state.yijing_core.bagua_symbols[gua_data['lower_gua']]
                all_lines = upper_lines + lower_lines
                
                for i, line in enumerate(all_lines):
                    line_num = 6 - i
                    is_dong = line_num == gua_data['dong_yao']
                    dong_text = " ◄动爻" if is_dong else ""
                    
                    # 获取详细信息
                    yao_index = line_num - 1
                    liushen = complete_analysis['liushen'][5-yao_index]
                    liuqin = complete_analysis['liuqin'][5-yao_index]
                    najia = complete_analysis['najia_dizhi'][5-yao_index]
                    
                    # 世应标记
                    shi_ying_mark = ""
                    if line_num == complete_analysis['shi_ying_positions']['shi']:
                        shi_ying_mark = " 【世】"
                    elif line_num == complete_analysis['shi_ying_positions']['ying']:
                        shi_ying_mark = " 【应】"
                    
                    # 显示完整信息
                    detail_info = f" {liuqin} {najia}{shi_ying_mark}"
                    css_class = "yao-detail dong-yao" if is_dong else "yao-detail"
                    st.markdown(f"<div class='{css_class}'>{liushen}  第{line_num}爻：{line} | {detail_info}{dong_text}</div>", unsafe_allow_html=True)
                    
            elif gua_data['method'] == 'number':
                # 数字起卦显示
                upper_lines = st.session_state.yijing_core.bagua_symbols[gua_data['upper_gua']]
                lower_lines = st.session_state.yijing_core.bagua_symbols[gua_data['lower_gua']]
                all_lines = upper_lines + lower_lines
                
                for i, line in enumerate(all_lines):
                    line_num = 6 - i
                    is_dong = line_num == gua_data['dong_yao']
                    dong_text = " ◄动爻" if is_dong else ""
                    
                    # 获取详细信息
                    yao_index = line_num - 1
                    liushen = complete_analysis['liushen'][5-yao_index]
                    liuqin = complete_analysis['liuqin'][5-yao_index]
                    najia = complete_analysis['najia_dizhi'][5-yao_index]
                    
                    # 世应标记
                    shi_ying_mark = ""
                    if line_num == complete_analysis['shi_ying_positions']['shi']:
                        shi_ying_mark = " 【世】"
                    elif line_num == complete_analysis['shi_ying_positions']['ying']:
                        shi_ying_mark = " 【应】"
                    
                    # 显示完整信息
                    detail_info = f"{liuqin} {najia}{shi_ying_mark}"
                    css_class = "yao-detail dong-yao" if is_dong else "yao-detail"
                    st.markdown(f"<div class='{css_class}'>{liushen}  第{line_num}爻：{line} | {detail_info}{dong_text}</div>", unsafe_allow_html=True)
                    
            else:  # coin method
                # 铜钱起卦显示
                for i in range(5, -1, -1):
                    line = gua_data['hexagram'][i]
                    is_moving = gua_data['moving_lines'][i]
                    line_num = i + 1
                    dong_text = " ◄动爻" if is_moving else ""
                    
                    # 获取详细信息
                    yao_index = line_num - 1
                    liushen = complete_analysis['liushen'][5-yao_index]
                    liuqin = complete_analysis['liuqin'][5-yao_index]
                    najia = complete_analysis['najia_dizhi'][5-yao_index]
                    
                    # 世应标记
                    shi_ying_mark = ""
                    if line_num == complete_analysis['shi_ying_positions']['shi']:
                        shi_ying_mark = " 【世】"
                    elif line_num == complete_analysis['shi_ying_positions']['ying']:
                        shi_ying_mark = " 【应】"
                    
                    # 显示完整信息
                    detail_info = f"{liuqin} {najia}{shi_ying_mark}"
                    css_class = "yao-detail dong-yao" if is_moving else "yao-detail"
                    st.markdown(f"<div class='{css_class}'>{liushen}  第{line_num}爻：{line} | {detail_info}{dong_text}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='analysis-box'>", unsafe_allow_html=True)
        st.markdown(f"**变卦：《{changed_gua_data['name']}》**")
        st.markdown(f"**上卦：** {changed_gua_data['upper_gua']}")
        st.markdown(f"**下卦：** {changed_gua_data['lower_gua']}")
        
        # 显示变卦的六爻详细信息
        if changed_analysis:
            st.markdown("\n**六爻详情：**")
            if gua_data['method'] == 'coin':
                # 铜钱起卦变卦显示：从第6爻到第1爻显示
                for i in range(5, -1, -1):
                    line = changed_gua_data['lines'][i]
                    line_num = i + 1
                    
                    # 获取详细信息
                    yao_index = line_num - 1
                    liushen = changed_analysis['liushen'][5-yao_index]
                    liuqin = changed_analysis['liuqin'][5-yao_index]
                    najia = changed_analysis['najia_dizhi'][5-yao_index]
                    
                    # 世应标记
                    shi_ying_mark = ""
                    if line_num == changed_analysis['shi_ying_positions']['shi']:
                        shi_ying_mark = " 【世】"
                    elif line_num == changed_analysis['shi_ying_positions']['ying']:
                        shi_ying_mark = " 【应】"
                    
                    # 显示完整信息
                    detail_info = f"{liuqin} {najia}{shi_ying_mark}"
                    st.markdown(f"<div class='yao-detail'>{liushen}  第{line_num}爻：{line} | {detail_info}</div>", unsafe_allow_html=True)
            else:
                # 时间起卦和数字起卦的变卦显示
                upper_lines = st.session_state.yijing_core.bagua_symbols[changed_gua_data['upper_gua']]
                lower_lines = st.session_state.yijing_core.bagua_symbols[changed_gua_data['lower_gua']]
                all_lines = upper_lines + lower_lines
                
                for i, line in enumerate(all_lines):
                    line_num = 6 - i
                    
                    # 获取详细信息
                    yao_index = line_num - 1
                    liushen = changed_analysis['liushen'][5-yao_index]
                    liuqin = changed_analysis['liuqin'][5-yao_index]
                    najia = changed_analysis['najia_dizhi'][5-yao_index]
                    
                    # 世应标记
                    shi_ying_mark = ""
                    if line_num == changed_analysis['shi_ying_positions']['shi']:
                        shi_ying_mark = " 【世】"
                    elif line_num == changed_analysis['shi_ying_positions']['ying']:
                        shi_ying_mark = " 【应】"
                    
                    # 显示完整信息
                    detail_info = f"{liuqin} {najia}{shi_ying_mark}"
                    st.markdown(f"<div class='yao-detail'>{liushen}  第{line_num}爻：{line} | {detail_info}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # AI分析按钮
    if st.button("🚀 开始AI分析", key="analyze_button", disabled=st.session_state.ai_analyzing):
        if not question:
            st.warning("建议输入问题以获得更精准的分析")
        # 开始AI分析
        st.session_state.ai_analyzing = True
        
        try:
            # 生成提示词
            prompt = generate_ai_prompt(gua_data, complete_analysis, changed_gua_data, question)
            
            # 显示结果标题
            st.markdown("### 📝 AI分析结果")
            
            # 发送请求到AI模型并流式显示结果
            with st.spinner("正在调用AI模型进行分析，请稍候..."):
                response = send_to_ai_model_streaming(prompt)
                
            st.session_state.ai_analyzing = False
            
        except Exception as e:
            st.session_state.ai_analyzing = False
            st.error(f"AI分析失败：{str(e)}")
    
    # 显示重新分析按钮
    if st.session_state.ai_analysis_result:
        if st.button("🔄 重新分析"):
            st.session_state.ai_analysis_result = None
            st.rerun()


# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
    "🤖 AI卦象分析系统 - 基于深度学习的易经智慧 | 仅供参考娱乐 🤖"
    "</div>", unsafe_allow_html=True
)