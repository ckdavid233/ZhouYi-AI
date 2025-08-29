import streamlit as st
import time
import random

# 页面配置
st.set_page_config(
    page_title="铜钱摇晃动画测试",
    page_icon="🪙",
    layout="wide"
)

# CSS样式和动画
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-family: '华文行楷', cursive;
        font-size: 2.5em;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 铜钱容器 */
    .coin-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 30px 0;
        height: 150px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    /* 铜钱基础样式 */
    .coin {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 0 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        position: relative;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    /* 正面（阳面）样式 */
    .coin-yang {
        background: linear-gradient(135deg, #f1c40f, #f39c12);
        border: 4px solid #d68910;
        color: #8b4513;
    }
    
    .coin-yang::before {
        content: "乾";
    }
    
    /* 反面（阴面）样式 */
    .coin-yin {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d);
        border: 4px solid #5d6d7e;
        color: #2c3e50;
    }
    
    .coin-yin::before {
        content: "坤";
    }
    
    /* 摇晃动画 */
    .coin-shaking {
        animation: shake 0.6s infinite;
    }
    
    /* 翻转动画 */
    .coin-flipping {
        animation: flip 2s ease-in-out;
    }
    
    /* 悬浮效果 */
    .coin-floating {
        animation: float 1.5s ease-in-out infinite;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0) rotate(0deg) translateY(0); }
        10% { transform: translateX(-5px) rotate(-3deg) translateY(-2px); }
        20% { transform: translateX(5px) rotate(3deg) translateY(2px); }
        30% { transform: translateX(-4px) rotate(-2deg) translateY(-1px); }
        40% { transform: translateX(4px) rotate(2deg) translateY(1px); }
        50% { transform: translateX(-3px) rotate(-3deg) translateY(-2px); }
        60% { transform: translateX(3px) rotate(3deg) translateY(2px); }
        70% { transform: translateX(-2px) rotate(-1deg) translateY(-1px); }
        80% { transform: translateX(2px) rotate(1deg) translateY(1px); }
        90% { transform: translateX(-1px) rotate(-2deg) translateY(-1px); }
    }
    
    @keyframes flip {
        0% { transform: rotateY(0deg) scale(1); }
        25% { transform: rotateY(90deg) scale(0.7); }
        50% { transform: rotateY(180deg) scale(1.2); }
        75% { transform: rotateY(270deg) scale(0.8); }
        100% { transform: rotateY(360deg) scale(1); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* 结果显示区域 */
    .result-display {
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    
    .result-title {
        font-size: 1.3em;
        font-weight: bold;
        color: #155724;
        margin-bottom: 15px;
    }
    
    .coin-detail {
        display: inline-block;
        margin: 10px;
        padding: 10px 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }
    
    .progress-bar {
        background: #e9ecef;
        border-radius: 10px;
        height: 25px;
        margin: 15px 0;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 10px;
    }
    
    .control-button {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
        margin: 10px;
        transition: all 0.3s ease;
    }
    
    .control-button:hover {
        background: linear-gradient(135deg, #5dade2, #3498db);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'animation_state' not in st.session_state:
    st.session_state.animation_state = 'idle'  # idle, shaking, flipping, result
if 'coin_results' not in st.session_state:
    st.session_state.coin_results = []
if 'current_faces' not in st.session_state:
    st.session_state.current_faces = ['正', '正', '正']
if 'yao_count' not in st.session_state:
    st.session_state.yao_count = 0

# 标题
st.markdown('<h1 class="main-title">🪙 铜钱摇晃动画测试 🪙</h1>', unsafe_allow_html=True)

# 控制按钮
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🎲 开始摇卦", key="start_shake"):
        st.session_state.animation_state = 'shaking'
        st.session_state.current_faces = ['正', '正', '正']
        st.rerun()
    
    if st.button("🔄 重置", key="reset"):
        st.session_state.animation_state = 'idle'
        st.session_state.coin_results = []
        st.session_state.yao_count = 0
        st.rerun()

# 进度显示
if st.session_state.yao_count > 0:
    progress_percent = (st.session_state.yao_count / 6) * 100
    st.markdown(f"""
    <div class="progress-container">
        <h3>起卦进度</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percent}%"></div>
        </div>
        <p>已完成 {st.session_state.yao_count}/6 爻</p>
    </div>
    """, unsafe_allow_html=True)

# 铜钱动画显示
if st.session_state.animation_state == 'idle':
    # 静态显示
    st.markdown("""
    <div class="coin-container">
        <div class="coin coin-yang coin-floating"></div>
        <div class="coin coin-yin coin-floating"></div>
        <div class="coin coin-yang coin-floating"></div>
    </div>
    <div style="text-align: center; color: #7f8c8d; font-style: italic; margin-top: 10px;">
        🌟 点击"开始摇卦"来体验铜钱动画效果 🌟
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.animation_state == 'shaking':
    # 摇晃动画
    st.markdown("""
    <div class="coin-container">
        <div class="coin coin-yang coin-shaking"></div>
        <div class="coin coin-yin coin-shaking"></div>
        <div class="coin coin-yang coin-shaking"></div>
    </div>
    <div style="text-align: center; color: #e74c3c; font-weight: bold; font-size: 1.2em; margin-top: 10px;">
        🪙 铜钱正在激烈摇晃中... 🪙
    </div>
    """, unsafe_allow_html=True)
    
    # 摇晃2秒后进入翻转状态
    time.sleep(1)
    st.session_state.animation_state = 'flipping'
    st.rerun()

# 修复第270-295行的翻转动画代码
elif st.session_state.animation_state == 'flipping':
    # 生成翻转结果
    coins = [random.choice(['阳', '阴']) for _ in range(3)]
    faces = ['正' if coin == '阳' else '反' for coin in coins]
    
    # 修复HTML格式化
    coin_html_parts = []
    for i, (face, coin) in enumerate(zip(faces, coins)):
        coin_class = 'coin-yang' if coin == '阳' else 'coin-yin'
        coin_html_parts.append(f'<div style="text-align: center; margin: 0 10px;"><div class="coin {coin_class} coin-flipping"></div><div style="margin-top: 8px; font-size: 0.9em; color: #666;">第{i+1}枚</div><div style="font-size: 0.8em; color: #888;">{face}面({coin})</div></div>')
    
    coin_html = ''.join(coin_html_parts)
    
    # 使用单行HTML避免渲染问题
    container_html = f'<div class="coin-container">{coin_html}</div><div style="text-align: center; color: #f39c12; font-weight: bold; font-size: 1.2em; margin-top: 10px;">✨ 铜钱正在翻转落地... ✨</div>'
    
    st.markdown(container_html, unsafe_allow_html=True)
    
    # 翻转2秒后显示结果
    time.sleep(2)
    st.session_state.animation_state = 'result'
    
    # 保存结果
    st.session_state.coin_results.append({
        'faces': faces.copy(),
        'coins': coins.copy()
    })
    st.session_state.yao_count += 1
    st.rerun()

elif st.session_state.animation_state == 'result':
    # 显示结果
    faces = st.session_state.current_faces
    coins = ['阳' if f == '正' else '阴' for f in faces]
    
    # 修复第330-360行的代码
    if st.session_state.animation_state == 'completed':
    # 计算爻的性质
        yang_count = coins.count('阳')
        if yang_count == 3:
            nature = "老阴(动爻)"
            nature_desc = "3阳"
            nature_color = "#9b59b6"
        elif yang_count == 2:
            nature = "少阳"
            nature_desc = "2阳1阴"
            nature_color = "#e74c3c"
        elif yang_count == 1:
            nature = "少阴"
            nature_desc = "1阳2阴"
            nature_color = "#3498db"
        else:
            nature = "老阳(动爻)"
            nature_desc = "3阴"
            nature_color = "#9b59b6"
    
        # 显示最终结果 - 修复HTML格式化问题
        coin_html_parts = []
        for i, (face, coin) in enumerate(zip(faces, coins)):
            coin_class = 'coin-yang' if coin == '阳' else 'coin-yin'
            coin_html_parts.append(f'<div style="text-align: center; margin: 0 10px;"><div class="coin {coin_class}"></div><div style="margin-top: 8px; font-size: 0.9em; color: #666;">第{i+1}枚</div><div style="font-size: 0.8em; color: #888;">{face}面({coin})</div></div>')
        
        coin_html = ''.join(coin_html_parts)
        
        # 使用单行HTML字符串避免渲染问题
        result_html = f'<div class="result-display"><div class="result-title">第{st.session_state.yao_count}爻 摇卦结果</div><div style="display: flex; justify-content: center; margin: 20px 0;">{coin_html}</div><div style="margin: 15px 0; padding: 12px; background: white; border-radius: 10px; border-left: 4px solid {nature_color};"><strong>详细结果：</strong> {faces[0]}面({coins[0]}) + {faces[1]}面({coins[1]}) + {faces[2]}面({coins[2]})</div><div style="font-size: 1.3em; font-weight: bold; color: {nature_color}; margin-top: 15px;">→ {nature_desc} → {nature}</div></div>'
        
        st.markdown(result_html, unsafe_allow_html=True)
    # 继续或完成按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state.yao_count < 6:
            if st.button(f"继续摇第{st.session_state.yao_count + 1}爻", key="continue"):
                st.session_state.animation_state = 'shaking'
                st.rerun()
    
    with col3:
        if st.button("查看历史记录", key="history"):
            st.session_state.show_history = not st.session_state.get('show_history', False)
            st.rerun()

# 历史记录显示
if st.session_state.get('show_history', False) and st.session_state.coin_results:
    st.markdown("### 📋 摇卦历史记录")
    
    for i, result in enumerate(reversed(st.session_state.coin_results)):
        yao_num = len(st.session_state.coin_results) - i
        faces = result['faces']
        coins = result['coins']
        
        yin_count = coins.count('阴')
        if yin_count == 1:
            nature = "少阳"
        elif yin_count == 2:
            nature = "少阴"
        elif yin_count == 3:
            nature = "老阳(动爻)"
        else:
            nature = "老阴(动爻)"
        
        st.markdown(f"""
        <div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; padding: 15px; margin: 10px 0;">
            <strong>第{yao_num}爻：</strong> {faces[0]}面({coins[0]}) + {faces[1]}面({coins[1]}) + {faces[2]}面({coins[2]}) → {nature}
        </div>
        """, unsafe_allow_html=True)

# 说明文档
with st.expander("📖 动画效果说明"):
    st.markdown("""
    ### 🎯 动画特效说明
    
    **1. 摇晃动画：**
    - 铜钱会左右摇摆并轻微旋转
    - 模拟真实的摇卦过程
    - 持续约2秒钟
    
    **2. 翻转动画：**
    - 铜钱会进行3D翻转效果
    - 模拟铜钱在空中翻转落地
    - 翻转过程中会有缩放效果
    
    **3. 悬浮效果：**
    - 静态时铜钱会轻微上下浮动
    - 增加视觉吸引力
    
    **4. 正反面显示：**
    - 正面显示"乾"字，金黄色
    - 反面显示"坤"字，银灰色
    - 清晰显示每枚铜钱的状态
    
    ### 🔧 技术实现
    - 使用CSS3动画和关键帧
    - 响应式设计，适配不同屏幕
    - 流畅的过渡效果
    - 真实的物理模拟感
    """)

# 底部信息
st.markdown("""
---
<div style="text-align: center; color: #7f8c8d; font-style: italic;">
🪙 铜钱摇晃动画测试 - 体验传统六爻起卦的视觉魅力 🪙
</div>
""", unsafe_allow_html=True)