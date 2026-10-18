# 九宫八卦结构可视化图集

## 序言

本图集是45-75号体系的视觉索引。通过8张核心图表，直观展示27宫立方体的几何骨架、赋值转换、路径动力学、寻址半径、跨球连接、连续球面以及动态决策机制。

所有图表均使用SVG代码生成，可无损缩放。读者可将代码复制至任意SVG渲染器查看，或直接阅读本图集。

---

## 第一章：基础骨架

### 图1：十三射线全向信道

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
<circle cx="150" cy="150" r="120" fill="none" stroke="#333"/>
<line x1="210.0" y1="150.0" x2="90.0" y2="150.0" stroke="red" stroke-width="2"/>
<line x1="150.0" y1="210.0" x2="150.0" y2="90.0" stroke="red" stroke-width="2"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="red" stroke-width="2"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<circle cx="150" cy="150" r="4" fill="black"/>
<text x="5" y="20" font-size="11">红=3轴 橙=6面对角 蓝=4体对角</text>
</svg>
```

**图注**：过中宫5的直线共13条（3轴向+6面对角+4体对角），被中宫分为两段，共26条有向信道，覆盖外围全部26宫。中宫是不动核。

### 图2：球体三层嵌套

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
<circle cx="150" cy="150" r="120" fill="none" stroke="#333"/>
<circle cx="150" cy="150" r="80" fill="none" stroke="#999" stroke-dasharray="4"/>
<circle cx="150" cy="150" r="40" fill="none" stroke="#999" stroke-dasharray="4"/>
<circle cx="190.0" cy="150.0" r="4" fill="red"/>
<circle cx="184.6" cy="170.0" r="4" fill="red"/>
<circle cx="170.0" cy="184.6" r="4" fill="red"/>
<circle cx="150.0" cy="190.0" r="4" fill="red"/>
<circle cx="130.0" cy="184.6" r="4" fill="red"/>
<circle cx="115.4" cy="170.0" r="4" fill="red"/>
<circle cx="110.0" cy="150.0" r="4" fill="red"/>
<circle cx="115.4" cy="130.0" r="4" fill="red"/>
<circle cx="130.0" cy="115.4" r="4" fill="red"/>
<circle cx="150.0" cy="110.0" r="4" fill="red"/>
<circle cx="170.0" cy="115.4" r="4" fill="red"/>
<circle cx="184.6" cy="130.0" r="4" fill="red"/>
<circle cx="230.0" cy="150.0" r="4" fill="orange"/>
<circle cx="219.3" cy="190.0" r="4" fill="orange"/>
<circle cx="190.0" cy="219.3" r="4" fill="orange"/>
<circle cx="150.0" cy="230.0" r="4" fill="orange"/>
<circle cx="110.0" cy="219.3" r="4" fill="orange"/>
<circle cx="80.7" cy="190.0" r="4" fill="orange"/>
<circle cx="70.0" cy="150.0" r="4" fill="orange"/>
<circle cx="80.7" cy="110.0" r="4" fill="orange"/>
<circle cx="110.0" cy="80.7" r="4" fill="orange"/>
<circle cx="150.0" cy="70.0" r="4" fill="orange"/>
<circle cx="190.0" cy="80.7" r="4" fill="orange"/>
<circle cx="219.3" cy="110.0" r="4" fill="orange"/>
<circle cx="234.9" cy="150.0" r="4" fill="blue"/>
<circle cx="210.0" cy="210.0" r="4" fill="blue"/>
<circle cx="150.0" cy="234.9" r="4" fill="blue"/>
<circle cx="90.0" cy="210.0" r="4" fill="blue"/>
<circle cx="65.1" cy="150.0" r="4" fill="blue"/>
<circle cx="90.0" cy="90.0" r="4" fill="blue"/>
<circle cx="150.0" cy="65.1" r="4" fill="blue"/>
<circle cx="210.0" cy="90.0" r="4" fill="blue"/>
<text x="5" y="20" font-size="11">红=面心6(R=2) 橙=棱中12(R=2√2) 蓝=顶点8(R=2√3)</text>
</svg>
```

**图注**：27宫立方体内接于半径2√3的球体。26个外围宫分布在三层球壳上，形成完美的同心圆结构。

---

## 第二章：赋值与转换

### 图3：加3/加6/加9截面路径

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="440" height="180" viewBox="0 0 440 180">
<text x="10" y="15" font-size="12">加3 (y=3截面)</text>
<rect x="10" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="45" font-size="14" text-anchor="middle">1</text>
<rect x="50" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="45" font-size="14" text-anchor="middle">4</text>
<rect x="90" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="45" font-size="14" text-anchor="middle">1</text>
<rect x="10" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="50" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="90" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="10" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="125" font-size="14" text-anchor="middle">1</text>
<rect x="50" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="125" font-size="14" text-anchor="middle">1</text>
<rect x="90" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="125" font-size="14" text-anchor="middle">1</text>
<line x1="69" y1="79" x2="69" y2="39" stroke="red" stroke-width="2"/>
<line x1="69" y1="39" x2="69" y2="119" stroke="red" stroke-width="2"/>
<line x1="69" y1="119" x2="69" y2="79" stroke="red" stroke-width="2"/>
<text x="10" y="160" font-size="10" fill="red">红=加3: 5→4→6→5</text>
<text x="150" y="15" font-size="12">加6 (y=3截面)</text>
<rect x="150" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="169" y="45" font-size="14" text-anchor="middle">1</text>
<rect x="190" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="45" font-size="14" text-anchor="middle">4</text>
<rect x="230" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="249" y="45" font-size="14" text-anchor="middle">1</text>
<rect x="150" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="169" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="190" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="230" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="249" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="150" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="169" y="125" font-size="14" text-anchor="middle">1</text>
<rect x="190" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="125" font-size="14" text-anchor="middle">1</text>
<rect x="230" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="249" y="125" font-size="14" text-anchor="middle">1</text>
<line x1="209" y1="79" x2="209" y2="119" stroke="blue" stroke-width="2"/>
<line x1="209" y1="119" x2="209" y2="39" stroke="blue" stroke-width="2"/>
<line x1="209" y1="39" x2="209" y2="79" stroke="blue" stroke-width="2"/>
<text x="150" y="160" font-size="10" fill="blue">蓝=加6: 5→6→4→5</text>
<text x="290" y="15" font-size="12">加9 (z=3截面)</text>
<rect x="290" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="45" font-size="14" text-anchor="middle">4</text>
<rect x="330" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="45" font-size="14" text-anchor="middle">9</text>
<rect x="370" y="20" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="45" font-size="14" text-anchor="middle">4</text>
<rect x="290" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="330" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="370" y="60" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="85" font-size="14" text-anchor="middle">5</text>
<rect x="290" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="125" font-size="14" text-anchor="middle">6</text>
<rect x="330" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="125" font-size="14" text-anchor="middle">1</text>
<rect x="370" y="100" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="125" font-size="14" text-anchor="middle">6</text>
<line x1="309" y1="79" x2="349" y2="79" stroke="green" stroke-width="2"/>
<line x1="349" y1="79" x2="389" y2="79" stroke="green" stroke-width="2"/>
<line x1="389" y1="79" x2="349" y2="79" stroke="green" stroke-width="2"/>
<text x="290" y="160" font-size="10" fill="green">绿=加9: 5→5→5→5</text>
</svg>
```

**图注**：加3与加6是纵向的Z轴三点循环（互为反向）；加9是横向的X轴中宫振荡。

### 图4：新旧赋值4/6分布

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="440" height="340" viewBox="0 0 440 340">
<text x="10" y="15" font-size="13">旧赋值 4/6分布 (黄=4/6)</text>
<text x="10" y="30" font-size="11">z=1</text>
<rect x="10" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="60" font-size="15" text-anchor="middle">8</text>
<rect x="50" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="60" font-size="15" text-anchor="middle">5</text>
<rect x="90" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="60" font-size="15" text-anchor="middle">3</text>
<rect x="10" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="100" font-size="15" text-anchor="middle">1</text>
<rect x="50" y="75" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="69" y="100" font-size="15" text-anchor="middle">6</text>
<rect x="90" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="100" font-size="15" text-anchor="middle">1</text>
<rect x="10" y="115" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="140" font-size="15" text-anchor="middle">9</text>
<rect x="50" y="115" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="140" font-size="15" text-anchor="middle">5</text>
<rect x="90" y="115" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="109" y="140" font-size="15" text-anchor="middle">4</text>
<text x="150" y="30" font-size="11">z=3</text>
<rect x="150" y="35" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="169" y="60" font-size="15" text-anchor="middle">4</text>
<rect x="190" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="60" font-size="15" text-anchor="middle">9</text>
<rect x="230" y="35" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="249" y="60" font-size="15" text-anchor="middle">4</text>
<rect x="150" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="169" y="100" font-size="15" text-anchor="middle">5</text>
<rect x="190" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="100" font-size="15" text-anchor="middle">5</text>
<rect x="230" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="249" y="100" font-size="15" text-anchor="middle">5</text>
<rect x="150" y="115" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="169" y="140" font-size="15" text-anchor="middle">6</text>
<rect x="190" y="115" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="140" font-size="15" text-anchor="middle">1</text>
<rect x="230" y="115" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="249" y="140" font-size="15" text-anchor="middle">6</text>
<text x="290" y="30" font-size="11">z=5</text>
<rect x="290" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="60" font-size="15" text-anchor="middle">7</text>
<rect x="330" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="60" font-size="15" text-anchor="middle">5</text>
<rect x="370" y="35" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="60" font-size="15" text-anchor="middle">2</text>
<rect x="290" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="100" font-size="15" text-anchor="middle">1</text>
<rect x="330" y="75" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="349" y="100" font-size="15" text-anchor="middle">4</text>
<rect x="370" y="75" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="100" font-size="15" text-anchor="middle">1</text>
<rect x="290" y="115" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="140" font-size="15" text-anchor="middle">6</text>
<rect x="330" y="115" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="140" font-size="15" text-anchor="middle">5</text>
<rect x="370" y="115" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="140" font-size="15" text-anchor="middle">1</text>
<text x="10" y="180" font-size="13">新赋值 4/6分布 (黄=4/6)</text>
<text x="10" y="195" font-size="11">z=1</text>
<rect x="10" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="225" font-size="15" text-anchor="middle">8</text>
<rect x="50" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="225" font-size="15" text-anchor="middle">1</text>
<rect x="90" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="225" font-size="15" text-anchor="middle">3</text>
<rect x="10" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="265" font-size="15" text-anchor="middle">7</text>
<rect x="50" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="265" font-size="15" text-anchor="middle">2</text>
<rect x="90" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="109" y="265" font-size="15" text-anchor="middle">7</text>
<rect x="10" y="280" width="38" height="38" fill="#fff" stroke="#333"/><text x="29" y="305" font-size="15" text-anchor="middle">9</text>
<rect x="50" y="280" width="38" height="38" fill="#fff" stroke="#333"/><text x="69" y="305" font-size="15" text-anchor="middle">3</text>
<rect x="90" y="280" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="109" y="305" font-size="15" text-anchor="middle">4</text>
<text x="150" y="195" font-size="11">z=3</text>
<rect x="150" y="200" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="169" y="225" font-size="15" text-anchor="middle">4</text>
<rect x="190" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="225" font-size="15" text-anchor="middle">9</text>
<rect x="230" y="200" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="249" y="225" font-size="15" text-anchor="middle">4</text>
<rect x="150" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="169" y="265" font-size="15" text-anchor="middle">5</text>
<rect x="190" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="265" font-size="15" text-anchor="middle">5</text>
<rect x="230" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="249" y="265" font-size="15" text-anchor="middle">5</text>
<rect x="150" y="280" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="169" y="305" font-size="15" text-anchor="middle">6</text>
<rect x="190" y="280" width="38" height="38" fill="#fff" stroke="#333"/><text x="209" y="305" font-size="15" text-anchor="middle">1</text>
<rect x="230" y="280" width="38" height="38" fill="#ffd700" stroke="#333"/><text x="249" y="305" font-size="15" text-anchor="middle">6</text>
<text x="290" y="195" font-size="11">z=5</text>
<rect x="290" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="225" font-size="15" text-anchor="middle">6</text>
<rect x="330" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="225" font-size="15" text-anchor="middle">7</text>
<rect x="370" y="200" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="225" font-size="15" text-anchor="middle">1</text>
<rect x="290" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="265" font-size="15" text-anchor="middle">3</text>
<rect x="330" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="265" font-size="15" text-anchor="middle">8</text>
<rect x="370" y="240" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="265" font-size="15" text-anchor="middle">3</text>
<rect x="290" y="280" width="38" height="38" fill="#fff" stroke="#333"/><text x="309" y="305" font-size="15" text-anchor="middle">7</text>
<rect x="330" y="280" width="38" height="38" fill="#fff" stroke="#333"/><text x="349" y="305" font-size="15" text-anchor="middle">9</text>
<rect x="370" y="280" width="38" height="38" fill="#fff" stroke="#333"/><text x="389" y="305" font-size="15" text-anchor="middle">2</text>
</svg>
```

**图注**：旧赋值的4/6贯穿全方体（含Z轴两端），新赋值的4/6集中在中层，Z轴改为2-5-8（雷风恒）。

---

## 第三章：路径与动力学

### 图5：r=4邻域覆盖

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
<circle cx="150" cy="150" r="120" fill="#e0f7fa" stroke="#00acc1" stroke-width="2"/>
<text x="150" y="120" font-size="14" text-anchor="middle" fill="#006064">r=4 邻域</text>
<text x="150" y="145" font-size="14" text-anchor="middle" fill="#006064">覆盖124个位置</text>
<circle cx="150" cy="150" r="5" fill="red"/>
<text x="150" y="175" font-size="12" fill="red" text-anchor="middle">中宫5</text>
<circle cx="60" cy="150" r="4" fill="blue"/>
<circle cx="240" cy="150" r="4" fill="blue"/>
<text x="40" y="170" font-size="10">顶点</text>
<text x="230" y="170" font-size="10">顶点</text>
<text x="10" y="20" font-size="12">图5：r=4邻域覆盖，全值可达</text>
</svg>
```

**图注**：r=4的邻域半径为124个位置，远超27宫总数，保证了任何目标值在邻域内都有候选。这是解决卡死问题的根本原因。

### 图6：双球体跨界桥接

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
<circle cx="100" cy="100" r="80" fill="#fff3e0" stroke="#ff9800" stroke-width="2"/>
<text x="100" y="60" font-size="14" text-anchor="middle">旧球体</text>
<text x="100" y="80" font-size="12" text-anchor="middle">(7个5)</text>
<circle cx="300" cy="100" r="80" fill="#e8f5e9" stroke="#4caf50" stroke-width="2"/>
<text x="300" y="60" font-size="14" text-anchor="middle">新球体</text>
<text x="300" y="80" font-size="12" text-anchor="middle">(3个5)</text>
<line x1="180" y1="100" x2="220" y2="100" stroke="#333" stroke-width="2" stroke-dasharray="4,2"/>
<text x="200" y="90" font-size="12" text-anchor="middle">4 &lt;--&gt; 8</text>
<text x="200" y="115" font-size="12" text-anchor="middle">6 &lt;--&gt; 2</text>
<text x="10" y="20" font-size="12">图6：双球体跨界桥接（乘2覆卦）</text>
</svg>
```

**图注**：新旧球体之间的边界通过2的幂次建立桥接。旧球体的4与新球体的8互连，旧球体的6与新球体的2互连。

---

## 第四章：混合与连续

### 图7：球面大圆插值 vs 直线插值

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
<circle cx="150" cy="150" r="100" fill="none" stroke="#333" stroke-width="2"/>
<circle cx="80" cy="90" r="5" fill="red"/>
<text x="60" y="80" font-size="10">p1</text>
<circle cx="220" cy="210" r="5" fill="red"/>
<text x="230" y="220" font-size="10">p2</text>
<path d="M 80 90 A 100 100 0 0 1 220 210" fill="none" stroke="blue" stroke-width="3"/>
<line x1="80" y1="90" x2="220" y2="210" stroke="#999" stroke-dasharray="4"/>
<text x="140" y="170" font-size="12" fill="blue">大圆(slerp)</text>
<text x="120" y="120" font-size="12" fill="#999">直线(过球心)</text>
<text x="10" y="20" font-size="12">图7：球面大圆插值 vs 直线插值</text>
</svg>
```

**图注**：直线插值穿过球心，导致归一化除零；大圆插值（slerp）沿球面走，保持半径恒定，完美解决连续化问题。

### 图8：动态阈值v2的T值波动

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
<line x1="50" y1="170" x2="380" y2="170" stroke="#333"/>
<line x1="50" y1="170" x2="50" y2="20" stroke="#333"/>
<text x="380" y="185" font-size="12">步数</text>
<text x="30" y="30" font-size="12">阈值T</text>
<text x="35" y="70" font-size="12">3</text>
<text x="35" y="120" font-size="12">2</text>
<text x="35" y="170" font-size="12">1</text>
<polyline points="50,120 100,120 100,70 150,70 150,170 200,170 200,120 250,120 250,70 300,70 300,120 350,120" fill="none" stroke="red" stroke-width="2"/>
<text x="60" y="110" font-size="10" fill="blue">T=2</text>
<text x="110" y="60" font-size="10" fill="blue">T=3(放宽)</text>
<text x="160" y="160" font-size="10" fill="blue">T=1(挑剔)</text>
<text x="210" y="110" font-size="10" fill="blue">T=2</text>
<text x="260" y="60" font-size="10" fill="blue">T=3</text>
<text x="10" y="20" font-size="12">图8：动态阈值v2的T值波动</text>
</svg>
```

**图注**：动态阈值v2的T值随状态在1到3之间波动。找不到时放宽，找到高级别后挑剔，路径将断时强制偏转，彻底解决卡死问题。

---

## 附录：图表索引

| 图号 | 名称 | 对应文档 |
|---|---|---|
| 图1 | 十三射线全向信道 | 48号、49号 |
| 图2 | 球体三层嵌套 | 58号、59号 |
| 图3 | 加3/加6/加9截面路径 | 55号、70号 |
| 图4 | 新旧赋值4/6分布 | 53号 |
| 图5 | r=4邻域覆盖 | 66号、72号 |
| 图6 | 双球体跨界桥接 | 57号、59号 |
| 图7 | 球面大圆插值 vs 直线插值 | 61号 |
| 图8 | 动态阈值v2的T值波动 | 55号、68号 |
