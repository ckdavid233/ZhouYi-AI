import streamlit as st
import time
import sys
import os

# 添加上级目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from yijing_core import YijingCore, create_session_state
from liuyao_formatter import LiuyaoFormatter
# 页面配置
st.set_page_config(
    page_title="主页",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .gua-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .gua-title {
        font-size: 1.8em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    .hexagram-line {
        font-family: '等线', monospace;
        font-size: 1.2em;
        font-weight: bold;
        margin: 5px 0;
        padding: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
    }
    .moving-line {
        font-family: '等线', monospace;
        font-size: 1.2em;
        font-weight: bold;
        margin: 5px 0;
        padding: 8px;
        color: #ff6b6b;
        background: rgba(255,107,107,0.2) !important;
        border-left: 4px solid #ff6b6b;
        border-radius: 5px;
    }
    .method-button {
        margin: 10px 0;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .time-button {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
    }
    .time-button:hover {
        background: linear-gradient(135deg, #5dade2, #3498db);
        transform: translateY(-2px);
    }
    .coin-button {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
    }
    .coin-button:hover {
        background: linear-gradient(135deg, #ec7063, #e74c3c);
        transform: translateY(-2px);
    }
    .number-button {
        background: linear-gradient(135deg, #f39c12, #d68910);
        color: white;
    }
    .number-button:hover {
        background: linear-gradient(135deg, #f4d03f, #f39c12);
        transform: translateY(-2px);
    }
    .detail-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        white-space: pre-wrap;
        font-family: '微软雅黑', sans-serif;
    }
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        margin: 10px 0;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        height: 100%;
        transition: width 0.3s ease;
    }
    .number-input-box {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .number-display {
        font-size: 1.5em;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin: 10px 0;
        padding: 10px;
        background: #ecf0f1;
        border-radius: 5px;
    }


    /* 铜钱动画样式 */
    .coin-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
        height: 120px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .coin {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        margin: 0 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        position: relative;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .coin-yang {
        background: linear-gradient(135deg, #f1c40f, #f39c12);
        border: 3px solid #d68910;
        color: #8b4513;
    }
    
    .coin-yang::before {
        content: "乾";
    }
    
    .coin-yin {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        border: 3px solid #5d6d7e;
        color: #2c3e50;
    }
    
    .coin-yin::before {
        content: "坤";
    }
    
    .coin-shaking {
        animation: shake 0.6s infinite;
    }
    
    .coin-flipping {
        animation: flip 1.5s ease-in-out;
    }
    
    .coin-floating {
        animation: float 1.5s ease-in-out infinite;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0) rotate(0deg) translateY(0); }
        10% { transform: translateX(-3px) rotate(-2deg) translateY(-1px); }
        20% { transform: translateX(3px) rotate(2deg) translateY(1px); }
        30% { transform: translateX(-2px) rotate(-1deg) translateY(-1px); }
        40% { transform: translateX(2px) rotate(1deg) translateY(1px); }
        50% { transform: translateX(-3px) rotate(-2deg) translateY(-1px); }
        60% { transform: translateX(3px) rotate(2deg) translateY(1px); }
        70% { transform: translateX(-1px) rotate(-1deg) translateY(0); }
        80% { transform: translateX(1px) rotate(1deg) translateY(0); }
        90% { transform: translateX(-1px) rotate(-1deg) translateY(0); }
    }
    
    @keyframes flip {
        0% { transform: rotateY(0deg) scale(1); }
        25% { transform: rotateY(90deg) scale(0.8); }
        50% { transform: rotateY(180deg) scale(1.1); }
        75% { transform: rotateY(270deg) scale(0.9); }
        100% { transform: rotateY(360deg) scale(1); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .coin-result-display {
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# 初始化会话状态
create_session_state()

# 数字起卦相关会话状态
if 'number_input' not in st.session_state:
    st.session_state.number_input = ""
if 'parsed_numbers' not in st.session_state:
    st.session_state.parsed_numbers = []

# 主标题
st.markdown("<h1 class='main-header'>🌟 六爻算卦 - 易经占卜系统 🌟</h1>", unsafe_allow_html=True)

# 侧边栏
st.sidebar.title("🔿 起卦方法")
st.sidebar.markdown("---")

# 起卦方法选择
method = st.sidebar.radio(
    "选择起卦方法：",
    ["📅 时间起卦", "🪙 铜钱起卦", "🔢 数字起卦"],
    index=0
)

# 主要内容区域
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🎯 起卦控制")
    
    if method == "📅 时间起卦":
        if st.button("📅 进行时间起卦", key="time_button", help="根据当前时间进行起卦"):
            with st.spinner("正在根据时间起卦..."):
                time.sleep(0.5)  # 模拟计算过程
                result = st.session_state.yijing_core.time_divination()
                changed_result = st.session_state.yijing_core.get_changed_gua(result)
                st.session_state.current_result = result
                st.session_state.changed_result = changed_result
                st.success("时间起卦完成！")
                st.rerun()
    
    elif method == "🔢 数字起卦":
        st.markdown("### 🔢 数字起卦")
        st.markdown("**请让问卦者随口报出数字：**")
        
        # 手动输入数字
        number_input = st.text_input(
            "请输入2-3个数字（1-10），用空格或逗号分隔：",
            value=st.session_state.number_input,
            placeholder="例如：3 7 或 5,8,2",
            key="number_text_input",
            help="可以输入2个数字（两数相加取动爻）或3个数字（第三个数字直接作为动爻）"
        )
        
        # 解析输入的数字
        if number_input != st.session_state.number_input:
            st.session_state.number_input = number_input
            try:
                # 解析数字
                import re
                numbers_str = re.split(r'[,，\s]+', number_input.strip())
                numbers = [int(n) for n in numbers_str if n.strip() and n.strip().isdigit()]
                
                # 验证数字
                valid_numbers = []
                for num in numbers:
                    if 1 <= num <= 10:
                        valid_numbers.append(num)
                
                st.session_state.parsed_numbers = valid_numbers
            except:
                st.session_state.parsed_numbers = []
        
        # 显示解析结果
        if st.session_state.parsed_numbers:
            numbers = st.session_state.parsed_numbers
            
            if len(numbers) >= 2:
                st.markdown("<div class='number-input-box'>", unsafe_allow_html=True)
                st.markdown("**解析的数字：**")
                st.markdown(f"<div class='number-display'>{' - '.join(map(str, numbers))}</div>", unsafe_allow_html=True)
                
                if len(numbers) == 2:
                    st.markdown(f"**上卦数字：** {numbers[0]}")
                    st.markdown(f"**下卦数字：** {numbers[1]}")
                    st.markdown(f"**动爻计算：** ({numbers[0]}+{numbers[1]}) ÷ 6 取余数")
                elif len(numbers) >= 3:
                    st.markdown(f"**上卦数字：** {numbers[0]}")
                    st.markdown(f"**下卦数字：** {numbers[1]}")
                    st.markdown(f"**动爻数字：** {numbers[2]}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 数字起卦按钮
                if st.button("🔢 开始数字起卦", key="number_divination_button"):
                    try:
                        with st.spinner("正在进行数字起卦..."):
                            time.sleep(1)
                            result = st.session_state.yijing_core.number_divination(numbers)
                            changed_result = st.session_state.yijing_core.get_changed_gua(result)
                            st.session_state.current_result = result
                            st.session_state.changed_result = changed_result
                            st.success("数字起卦完成！")
                            st.rerun()
                    except Exception as e:
                        st.error(f"数字起卦失败：{str(e)}")
            else:
                st.warning("请输入至少2个有效数字（1-10）")
        else:
            st.info("等待输入数字...")
    
    else:  # 铜钱起卦
        # 初始化动画状态
        if 'coin_animation_state' not in st.session_state:
            st.session_state.coin_animation_state = None
        
        if st.button("🪙 开始铜钱起卦", key="coin_button", help="通过模拟铜钱摇卦进行起卦"):
            st.session_state.coin_progress = 0
            st.session_state.coin_results = []
            st.session_state.current_result = None
            st.session_state.changed_result = None
            st.session_state.auto_divination = True
            st.session_state.coin_animation_state = 'shaking'
            st.rerun()
        
        # 自动进行铜钱起卦
        if st.session_state.get('auto_divination', False):
            if st.session_state.coin_progress < 6:
                st.markdown("### 🪙 铜钱起卦进行中")
                
                # 进度条
                progress_percent = (st.session_state.coin_progress / 6) * 100
                st.markdown(f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percent}%"></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.write(f"进度：{st.session_state.coin_progress}/6 爻")
                st.info(f"正在摇第{st.session_state.coin_progress + 1}爻...")
                
                # 显示铜钱动画
                if st.session_state.coin_animation_state == 'shaking':
                    # 摇晃动画
                    st.markdown("""
                    <div class="coin-container">
                        <div class="coin coin-yang coin-shaking"></div>
                        <div class="coin coin-yin coin-shaking"></div>
                        <div class="coin coin-yang coin-shaking"></div>
                    </div>
                    <div style="text-align: center; color: #e74c3c; font-weight: bold; margin-top: 10px;">
                        🪙 铜钱正在激烈摇晃中... 🪙
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 摇晃1秒后进入翻转状态
                    time.sleep(1)
                    st.session_state.coin_animation_state = 'flipping'
                    st.rerun()
                
                elif st.session_state.coin_animation_state == 'flipping':
                    # 生成铜钱结果
                    coins = []
                    for _ in range(3):
                        import random
                        coin = random.choice(['阳', '阴'])
                        coins.append(coin)
                    
                    # 翻转动画
                    coin_html_parts = []
                    for i, coin in enumerate(coins):
                        coin_class = 'coin-yang' if coin == '阳' else 'coin-yin'
                        coin_html_parts.append(f'<div class="coin {coin_class} coin-flipping"></div>')
                    
                    coin_html = ''.join(coin_html_parts)
                    
                    st.markdown(f"""
                    <div class="coin-container">
                        {coin_html}
                    </div>
                    <div style="text-align: center; color: #f39c12; font-weight: bold; margin-top: 10px;">
                        ✨ 铜钱正在翻转落地... ✨
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 翻转1.5秒后显示结果
                    time.sleep(1.5)
                    
                    # 保存结果并显示
                    st.session_state.coin_results.append(coins)
                    st.session_state.coin_progress += 1
                    
                    # 显示当前爻的结果
                    yin_count = coins.count('阴')
                    if yin_count == 1:
                        nature = "少阳"
                        nature_color = "#e74c3c"
                    elif yin_count == 2:
                        nature = "少阴"
                        nature_color = "#3498db"
                    elif yin_count == 3:
                        nature = "老阳(动爻)"
                        nature_color = "#9b59b6"
                    else:
                        nature = "老阴(动爻)"
                        nature_color = "#9b59b6"
                    
                    # 显示结果
                    coin_result_html = []
                    for i, coin in enumerate(coins):
                        coin_class = 'coin-yang' if coin == '阳' else 'coin-yin'
                        face = '正' if coin == '阳' else '反'
                        coin_result_html.append(f'<div style="text-align: center; margin: 0 8px;"><div class="coin {coin_class}"></div><div style="margin-top: 5px; font-size: 0.8em; color: #666;">{face}面({coin})</div></div>')
                    
                    result_html = ''.join(coin_result_html)
                    
                    st.markdown(f"""
                    <div class="coin-result-display">
                        <div style="font-weight: bold; margin-bottom: 10px;">第{st.session_state.coin_progress}爻 摇卦结果</div>
                        <div style="display: flex; justify-content: center; margin: 15px 0;">
                            {result_html}
                        </div>
                        <div style="font-size: 1.1em; font-weight: bold; color: {nature_color}; margin-top: 10px;">
                            {' '.join(coins)} → {nature}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 如果完成6爻，计算最终结果
                    if st.session_state.coin_progress >= 6:
                        time.sleep(1)
                        # 使用实际摇卦结果进行计算
                        result = st.session_state.yijing_core.coin_divination(st.session_state.coin_results)
                        changed_result = st.session_state.yijing_core.get_changed_gua(result)
                        st.session_state.current_result = result
                        st.session_state.changed_result = changed_result
                        st.session_state.auto_divination = False
                        st.session_state.coin_animation_state = None
                        st.success("铜钱起卦完成！")
                        st.rerun() 
                    else:
                        # 继续下一爻
                        time.sleep(1)
                        st.session_state.coin_animation_state = 'shaking'
                        st.rerun()
        
        # 显示历史摇卦结果（始终显示，让用户看到过程）
        if st.session_state.coin_results:
            st.markdown("### 📋 摇卦历史记录")
            # 从第六爻到第一爻显示（倒序显示）
            for i in range(len(st.session_state.coin_results) - 1, -1, -1):
                coin_result = st.session_state.coin_results[i]
                yin_count = coin_result.count('阴')
                if yin_count == 1:
                    nature = "少阳"
                elif yin_count == 2:
                    nature = "少阴"
                elif yin_count == 3:
                    nature = "老阳(动爻)"
                else:
                    nature = "老阴(动爻)"
                st.success(f"第{i+1}爻：{' '.join(coin_result)} → {nature}")

with col2:
    st.markdown("### 🌟 起卦结果")
    
    if st.session_state.current_result is None:
        st.info("请选择起卦方法并开始起卦")
        
        # 显示使用说明
        st.markdown("### 📖 使用说明")
        st.markdown("""
        **时间起卦：**
        - 根据当前年、月、日、时进行起卦
        - 自动计算上卦、下卦和动爻
        - 适合快速占卜
        
        **铜钱起卦：**
        - 模拟传统三枚铜钱摇卦
        - 需要摇6次，每次对应一爻
        - 更接近传统起卦方式
        
        **数字起卦：**
        - 让问卦者随口报出1-10的数字
        - 2个数字：第一个为上卦，第二个为下卦，两数相加除以6取动爻
        - 3个数字：第一个为上卦，第二个为下卦，第三个直接作为动爻
        - 适合面对面起卦，增加随机性
        
        **结果解读：**
        - **本卦**：代表当前状况
        - **变卦**：代表未来发展趋势
        - **动爻**：变化的关键因素
        """)
    
    else:
        result = st.session_state.current_result
        changed_result = st.session_state.changed_result
        
        # 创建标签页
        tab1, tab2, tab3 = st.tabs(["📊 本卦", "🔄 变卦", "📝 详细信息"])
        
        with tab1:
            st.markdown(f"<div class='gua-display'>", unsafe_allow_html=True)
            st.markdown(f"<div class='gua-title'>本卦：《{result['original_gua']}》</div>", unsafe_allow_html=True)
            
            # 添加日干选择器
            st.markdown("### 📅 日干配置")
            current_tiangan = st.session_state.yijing_core.get_current_tiangan()
            st.info(f"当前日干：{current_tiangan}（自动获取）")
            selected_day_gan = current_tiangan
            
            try:
                # 获取完整分析
                complete_analysis = st.session_state.yijing_core.get_complete_analysis(result, selected_day_gan)
                
                # 统一显示逻辑：所有方法都从第6爻到第1爻显示（从上到下）
                if result['method'] == 'time':
                    # 时间起卦显示
                    upper_lines = st.session_state.yijing_core.bagua_symbols[result['upper_gua']]
                    lower_lines = st.session_state.yijing_core.bagua_symbols[result['lower_gua']]
                    all_lines = upper_lines + lower_lines
                    
                    # 从第6爻到第1爻显示（从上到下）
                    for i, line in enumerate(all_lines):
                        line_num = 6 - i
                        is_dong = line_num == result['dong_yao']
                        css_class = "moving-line" if is_dong else "hexagram-line"
                        if is_dong:
                            if line == '━━━':  
                                dong_text = " ◄动爻⭕"
                            else:  
                                dong_text = " ◄动爻❌"
                        else:
                            dong_text = ""
                        
                        # 获取详细信息
                        yao_index = line_num - 1  # 转换为0-5索引
                        liushen = complete_analysis['liushen'][5-yao_index]  # 六神数组是正序的
                        liuqin = complete_analysis['liuqin'][5-yao_index]    # 六亲数组是正序的
                        najia = complete_analysis['najia_dizhi'][5-yao_index] # 纳甲数组是正序的
                        wuxing = complete_analysis['wuxing'][5-yao_index]
                        
                        # 世应标记
                        shi_ying_mark = ""
                        if line_num == complete_analysis['shi_ying_positions']['shi']:
                            shi_ying_mark = " 【世】"
                        elif line_num == complete_analysis['shi_ying_positions']['ying']:
                            shi_ying_mark = " 【应】"
                        
                        # 显示完整信息
                        detail_info = f" {liuqin} {najia}{wuxing}{shi_ying_mark}"
                        st.markdown(f"<div class='{css_class}'>{liushen}  第{line_num}爻：{line} | {detail_info}{dong_text}</div>", unsafe_allow_html=True)
                    
                elif result['method'] == 'number':
                    # 数字起卦显示
                    upper_lines = st.session_state.yijing_core.bagua_symbols[result['upper_gua']]
                    lower_lines = st.session_state.yijing_core.bagua_symbols[result['lower_gua']]
                    all_lines = upper_lines + lower_lines
                    
                    # 从第6爻到第1爻显示（从上到下）
                    for i, line in enumerate(all_lines):
                        line_num = 6 - i
                        is_dong = line_num == result['dong_yao']
                        css_class = "moving-line" if is_dong else "hexagram-line"
                        if is_dong:
                            if line == '━━━':  
                                dong_text = " ◄动爻⭕"
                            else:  
                                dong_text = " ◄动爻❌"
                        else:
                            dong_text = ""
                        
                        # 获取详细信息
                        yao_index = line_num - 1
                        liushen = complete_analysis['liushen'][5-yao_index]
                        liuqin = complete_analysis['liuqin'][5-yao_index]
                        najia = complete_analysis['najia_dizhi'][5-yao_index]
                        wuxing = complete_analysis['wuxing'][5-yao_index]
                        
                        # 世应标记
                        shi_ying_mark = ""
                        if line_num == complete_analysis['shi_ying_positions']['shi']:
                            shi_ying_mark = " 【世】"
                        elif line_num == complete_analysis['shi_ying_positions']['ying']:
                            shi_ying_mark = " 【应】"
                        
                        # 显示完整信息
                        detail_info = f"{liuqin} {najia}{wuxing}{shi_ying_mark}"
                        st.markdown(f"<div class='{css_class}'>{liushen}  第{line_num}爻：{line} | {detail_info}{dong_text}</div>", unsafe_allow_html=True)
                    
                else:  # coin method
                    # 铜钱起卦显示
                    for i in range(5, -1, -1):
                        line = result['hexagram'][i]
                        is_moving = result['moving_lines'][i]
                        line_num = i + 1
                        css_class = "moving-line" if is_moving else "hexagram-line"
                        if is_moving:
                            coin_result = result['coin_results'][i]
                            yin_count = coin_result.count('阴')
                            if yin_count == 3:
                                dong_text = " ◄动爻⭕"
                            else:
                                dong_text = " ◄动爻❌"
                        else:
                            dong_text = ""
                        
                        # 获取详细信息
                        yao_index = line_num - 1
                        liushen = complete_analysis['liushen'][5-yao_index]
                        liuqin = complete_analysis['liuqin'][5-yao_index]
                        najia = complete_analysis['najia_dizhi'][5-yao_index]
                        wuxing = complete_analysis['wuxing'][5-yao_index]
                        
                        # 世应标记
                        shi_ying_mark = ""
                        if line_num == complete_analysis['shi_ying_positions']['shi']:
                            shi_ying_mark = " 【世】"
                        elif line_num == complete_analysis['shi_ying_positions']['ying']:
                            shi_ying_mark = " 【应】"
                        
                        # 显示完整信息
                        detail_info = f"{liuqin} {najia}{wuxing}{shi_ying_mark}"
                        st.markdown(f"<div class='{css_class}'>{liushen}  第{line_num}爻：{line} | {detail_info}{dong_text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                # 如果分析失败，显示原有的简单格式
                st.error(f"详细分析失败：{str(e)}，显示基本信息")
                # 这里保留原有的显示逻辑作为备用
                if result['method'] == 'time':
                    upper_lines = st.session_state.yijing_core.bagua_symbols[result['upper_gua']]
                    lower_lines = st.session_state.yijing_core.bagua_symbols[result['lower_gua']]
                    all_lines = upper_lines + lower_lines
                    
                    for i, line in enumerate(all_lines):
                        line_num = 6 - i
                        is_dong = line_num == result['dong_yao']
                        css_class = "moving-line" if is_dong else "hexagram-line"
                        dong_text = " ◄动爻" if is_dong else ""
                        st.markdown(f"<div class='{css_class}'>第{line_num}爻：{line}{dong_text}</div>", unsafe_allow_html=True)
            
            st.markdown(f"**上卦：** {result['upper_gua']}")
            st.markdown(f"**下卦：** {result['lower_gua']}")
            if result['method'] == 'time':
                st.markdown(f"**动爻：** 第{result['dong_yao']}爻")
                st.markdown(f"**时间：** {result['time_info']}")
            elif result['method'] == 'number':
                st.markdown(f"**动爻：** 第{result['dong_yao']}爻")
                st.markdown(f"**数字：** {result['numbers_info']}")
            else:
                moving_lines_text = "、".join([f"第{i+1}爻" for i, is_moving in enumerate(result['moving_lines']) if is_moving])
                st.markdown(f"**动爻：** {moving_lines_text if moving_lines_text else '无'}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown(f"<div class='gua-display'>", unsafe_allow_html=True)
            st.markdown(f"<div class='gua-title'>变卦：《{changed_result['name']}》</div>", unsafe_allow_html=True)
            
            # 变卦也使用相同的日干
            try:
                # 为变卦创建一个临时的result结构
                changed_result_for_analysis = {
                    'original_gua': changed_result['name'],  # 修复：使用'name'而不是'changed_gua'
                    'upper_gua': changed_result['upper_gua'],
                    'lower_gua': changed_result['lower_gua'],
                    'method': result['method']
                }
                
                # 如果是铜钱起卦，添加hexagram字段
                if result['method'] == 'coin':
                    changed_result_for_analysis['hexagram'] = changed_result['lines']
                
                # 获取变卦的完整分析
                changed_analysis = st.session_state.yijing_core.get_complete_analysis(changed_result_for_analysis, selected_day_gan)
                # 显示变卦的六爻信息
                if result['method'] == 'coin':
                    # 铜钱起卦变卦显示：从第6爻到第1爻显示
                    for i in range(5, -1, -1):
                        line = changed_result['lines'][i]
                        line_num = i + 1
                        
                        # 获取详细信息
                        yao_index = line_num - 1
                        liushen = changed_analysis['liushen'][5-yao_index]
                        liuqin = changed_analysis['liuqin'][5-yao_index]
                        najia = changed_analysis['najia_dizhi'][5-yao_index]
                        wuxing = changed_analysis['wuxing'][5-yao_index]

                        # 世应标记
                        shi_ying_mark = ""
                        if line_num == changed_analysis['shi_ying_positions']['shi']:
                            shi_ying_mark = " 【世】"
                        elif line_num == changed_analysis['shi_ying_positions']['ying']:
                            shi_ying_mark = " 【应】"
                        
                        # 显示完整信息
                        detail_info = f"{liuqin} {najia}{wuxing}{shi_ying_mark}"
                        st.markdown(f"<div class='hexagram-line'>{liushen}  第{line_num}爻：{line} | {detail_info}</div>", unsafe_allow_html=True)
                else:
                    # 时间起卦和数字起卦的变卦显示
                    upper_lines = st.session_state.yijing_core.bagua_symbols[changed_result['upper_gua']]
                    lower_lines = st.session_state.yijing_core.bagua_symbols[changed_result['lower_gua']]
                    all_lines = upper_lines + lower_lines
                    
                    for i, line in enumerate(all_lines):
                        line_num = 6 - i
                        
                        # 获取详细信息
                        yao_index = line_num - 1
                        liushen = changed_analysis['liushen'][5-yao_index]
                        liuqin = changed_analysis['liuqin'][5-yao_index]
                        najia = changed_analysis['najia_dizhi'][5-yao_index]
                        wuxing = changed_analysis['wuxing'][5-yao_index]

                        # 世应标记
                        shi_ying_mark = ""
                        if line_num == changed_analysis['shi_ying_positions']['shi']:
                            shi_ying_mark = " 【世】"
                        elif line_num == changed_analysis['shi_ying_positions']['ying']:
                            shi_ying_mark = " 【应】"
                        
                        # 显示完整信息
                        detail_info = f"{liuqin} {najia}{wuxing}{shi_ying_mark}"
                        st.markdown(f"<div class='hexagram-line'>{liushen}  第{line_num}爻：{line} | {detail_info}</div>", unsafe_allow_html=True)
                        
            except Exception as e:
                # 如果分析失败，显示原有的简单格式
                st.error(f"变卦详细分析失败：{str(e)}，显示基本信息")
                if result['method'] == 'coin':
                    for i in range(5, -1, -1):
                        line = changed_result['lines'][i]
                        line_num = i + 1
                        st.markdown(f"<div class='hexagram-line'>第{line_num}爻：{line}</div>", unsafe_allow_html=True)
                else:
                    upper_lines = st.session_state.yijing_core.bagua_symbols[changed_result['upper_gua']]
                    lower_lines = st.session_state.yijing_core.bagua_symbols[changed_result['lower_gua']]
                    all_lines = upper_lines + lower_lines
                    
                    for i, line in enumerate(all_lines):
                        line_num = 6 - i
                        st.markdown(f"<div class='hexagram-line'>第{line_num}爻：{line}</div>", unsafe_allow_html=True)
            
            st.markdown(f"**上卦：** {changed_result['upper_gua']}")
            st.markdown(f"**下卦：** {changed_result['lower_gua']}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            # 获取当前日干
            current_tiangan = st.session_state.yijing_core.get_current_tiangan()
            
            try:
                # 获取完整分析
                complete_analysis = st.session_state.yijing_core.get_complete_analysis(result, current_tiangan)
                
                # 显示详细信息
                st.markdown("### 📊 卦象详细信息")
                
                # 基本信息
                formatter = LiuyaoFormatter(st.session_state.yijing_core)
                detail_text = formatter.get_detailed_analysis(result, changed_result)
                st.markdown(f"<div class='detail-box'>{detail_text}</div>", unsafe_allow_html=True)
                
                # 六亲六神详细信息
                st.markdown("### 🔮 六亲六神详细信息")
                
                # 本卦六亲六神
                st.markdown("#### 📊 本卦六亲六神")
                st.markdown(f"**日干：** {current_tiangan}")
                st.markdown(f"**世爻：** 第{complete_analysis['shi_ying_positions']['shi']}爻")
                st.markdown(f"**应爻：** 第{complete_analysis['shi_ying_positions']['ying']}爻")
                
                # 创建表格显示六亲六神
                import pandas as pd
                
                # 准备表格数据（从第6爻到第1爻）
                table_data = []
                for i in range(6):
                    line_num = 6 - i
                    yao_index = line_num - 1
                    
                    # 获取爻的符号
                    if result['method'] == 'coin':
                        yao_symbol = result['hexagram'][yao_index]
                        is_dong = result['moving_lines'][yao_index]
                    else:
                        upper_lines = st.session_state.yijing_core.bagua_symbols[result['upper_gua']]
                        lower_lines = st.session_state.yijing_core.bagua_symbols[result['lower_gua']]
                        all_lines = upper_lines + lower_lines
                        yao_symbol = all_lines[i]
                        is_dong = line_num == result.get('dong_yao', 0)
                    
                    # 世应标记
                    shi_ying = ""
                    if line_num == complete_analysis['shi_ying_positions']['shi']:
                        shi_ying = "世"
                    elif line_num == complete_analysis['shi_ying_positions']['ying']:
                        shi_ying = "应"
                    
                    # 动爻标记
                    if result['method'] == 'coin' and is_dong:
                        # 铜钱起卦：区分老阳老阴
                        yin_count = result['coin_results'][yao_index].count('阴')
                        if yin_count == 3:
                            dong_mark = "⭕老阳"
                        elif yin_count == 0:
                            dong_mark = "❌老阴"
                        else:
                            dong_mark = "动"  # 理论上不会出现
                    elif (result['method'] in ['time','number']) and is_dong:
                        if yao_symbol == '━━━': 
                            dong_mark = "⭕老阳"
                        else:  
                            dong_mark = "❌老阴"
                    else:
                        dong_mark = "动" if is_dong else ""
                    
                    table_data.append({
                        "爻位": f"第{line_num}爻",
                        "爻象": yao_symbol,
                        "六神": complete_analysis['liushen'][i],
                        "六亲": complete_analysis['liuqin'][i],
                        "纳甲": complete_analysis['najia_dizhi'][i],
                        "五行": complete_analysis['wuxing'][i],
                        "世应": shi_ying,
                        "动静": dong_mark,
                        
                    })
                
                # 显示表格
                df = pd.DataFrame(table_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # 变卦六亲六神（如果有动爻）
                if result['method'] == 'coin':
                    has_moving = any(result['moving_lines'])
                else:
                    has_moving = 'dong_yao' in result and result['dong_yao'] > 0
                
                if has_moving:
                    st.markdown("#### 🔄 变卦六亲六神")
                    
                    # 为变卦创建分析结构
                    changed_result_for_analysis = {
                        'original_gua': changed_result['name'],
                        'upper_gua': changed_result['upper_gua'],
                        'lower_gua': changed_result['lower_gua'],
                        'method': result['method']
                    }
                    
                    if result['method'] == 'coin':
                        changed_result_for_analysis['hexagram'] = changed_result['lines']
                    
                    # 获取变卦分析
                    changed_analysis = st.session_state.yijing_core.get_complete_analysis(changed_result_for_analysis, current_tiangan)
                    
                    # 变卦表格数据
                    changed_table_data = []
                    for i in range(6):
                        line_num = 6 - i
                        yao_index = line_num - 1
                        
                        # 获取变卦爻的符号
                        if result['method'] == 'coin':
                            yao_symbol = changed_result['lines'][yao_index]
                        else:
                            upper_lines = st.session_state.yijing_core.bagua_symbols[changed_result['upper_gua']]
                            lower_lines = st.session_state.yijing_core.bagua_symbols[changed_result['lower_gua']]
                            all_lines = upper_lines + lower_lines
                            yao_symbol = all_lines[i]
                        
                        # 世应标记
                        shi_ying = ""
                        if line_num == changed_analysis['shi_ying_positions']['shi']:
                            shi_ying = "世"
                        elif line_num == changed_analysis['shi_ying_positions']['ying']:
                            shi_ying = "应"
                        
                        changed_table_data.append({
                            "爻位": f"第{line_num}爻",
                            "爻象": yao_symbol,
                            "六神": changed_analysis['liushen'][i],
                            "六亲": changed_analysis['liuqin'][i],
                            "纳甲": changed_analysis['najia_dizhi'][i],
                            "五行": changed_analysis['wuxing'][i],
                            "世应": shi_ying
                        })
                    
                    # 显示变卦表格
                    changed_df = pd.DataFrame(changed_table_data)
                    st.dataframe(changed_df, use_container_width=True, hide_index=True)
                
            except Exception as e:
                # 如果获取详细分析失败，显示基本信息
                st.error(f"获取详细分析失败：{str(e)}")
                formatter = LiuyaoFormatter(st.session_state.yijing_core)
                detail_text = formatter.get_detailed_analysis(result, changed_result)
                st.markdown(f"<div class='detail-box'>{detail_text}</div>", unsafe_allow_html=True)
        
        # 重新起卦按钮
        col_button1, col_button2 = st.columns([1, 1])
        
        with col_button1:
            if st.button("🔄 重新起卦", key="reset_button"):
                st.session_state.current_result = None
                st.session_state.changed_result = None
                st.session_state.coin_progress = 0
                st.session_state.coin_results = []
                st.session_state.number_input = ""
                st.session_state.parsed_numbers = []
                st.rerun()
        
        with col_button2:
            if st.button("🤖 AI智能分析", key="ai_analysis_button"):
                st.switch_page("pages/AI智能分析.py")
            st.caption("点击进入AI分析页面，输入问题获取智能解读")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
    "🌟 六爻智慧系统 - 传承千年易经文化 | 启迪人生智慧 🌟"
    "</div>", unsafe_allow_html=True
)
