<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Swing Tracker</title>
    
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="SwingApp">
    <link rel="apple-touch-icon" href="https://img.icons8.com/fluency/192/bullish.png">

    <!-- ספריות Firebase -->
    <script src="https://www.gstatic.com/firebasejs/10.8.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.8.1/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore-compat.js"></script>
    
    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background-color: #121212; 
            color: #ffffff; 
            margin: 0; 
            padding: 0; 
            overflow: hidden; 
            height: 100vh; 
        }
        
        /* סרגל עליון נקי */
        .app-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 10px 14px; 
            background: #1a1a1a; 
            border-bottom: 1px solid #2d2d2d; 
            height: 52px; 
        }
        .header-title { 
            font-size: 1.1em; 
            font-weight: 700; 
            color: #4caf50; 
            display: flex; 
            align-items: center; 
            gap: 6px; 
        }
        .header-actions { 
            display: flex; 
            align-items: center; 
            gap: 8px; 
        }
        
        .search-container { 
            display: flex; 
            align-items: center; 
            background: #262626; 
            border: 1px solid #3d3d3d; 
            border-radius: 18px; 
            overflow: hidden; 
            height: 32px; 
        }
        .search-container input { 
            background: transparent; 
            border: none; 
            color: #fff; 
            padding: 0 10px; 
            outline: none; 
            width: 80px; 
            font-size: 0.85em; 
        }
        .search-container button { 
            background: #4caf50; 
            border: none; 
            color: white; 
            padding: 0 10px; 
            height: 100%; 
            cursor: pointer; 
        }
        
        .icon-btn { 
            background: #262626; 
            border: 1px solid #3d3d3d; 
            color: #fff; 
            width: 34px; 
            height: 34px; 
            border-radius: 8px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            cursor: pointer; 
            font-size: 1em; 
        }

        /* אזור תוכן מרכזי */
        .app-views { 
            height: calc(100vh - 110px); 
            width: 100%; 
            position: relative; 
            overflow: hidden; 
        }
        .view { 
            display: none; 
            height: 100%; 
            width: 100%; 
            overflow-y: auto; 
        }
        .view.active { 
            display: block; 
        }
        #view-chart { 
            overflow: hidden; 
            position: relative; 
        }
        #tv_chart_container { 
            width: 100%; 
            height: 100%; 
        }

        /* סרגל ניווט תחתון */
        .bottom-nav { 
            position: fixed; 
            bottom: 0; 
            left: 0; 
            right: 0; 
            height: 58px; 
            background: #1a1a1a; 
            border-top: 1px solid #2d2d2d; 
            display: flex; 
            justify-content: space-around; 
            align-items: center; 
            z-index: 950; 
        }
        .nav-btn { 
            flex: 1; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 100%; 
            background: transparent; 
            border: none; 
            color: #888; 
            font-size: 0.75em; 
            cursor: pointer; 
            gap: 3px; 
        }
        .nav-btn.active { 
            color: #4caf50; 
            font-weight: bold; 
        }
        .nav-icon { 
            font-size: 1.3em; 
        }

        /* מסך סורק מניות */
        .screener-list { 
            padding: 12px; 
        }
        .stock-card { 
            background: #1e1e1e; 
            border: 1px solid #2d2d2d; 
            border-radius: 10px; 
            padding: 14px; 
            margin-bottom: 10px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            cursor: pointer; 
            transition: 0.2s; 
        }
        .stock-card:active { 
            background: #282828; 
            border-color: #4caf50; 
        }
        .stock-ticker { 
            font-size: 1.15em; 
            font-weight: bold; 
            color: #4caf50; 
        }
        .stock-sub { 
            font-size: 0.8em; 
            color: #999; 
            margin-top: 2px; 
        }
        .stock-price-box { 
            text-align: left; 
        }
        .stock-price { 
            font-size: 1.1em; 
            font-weight: bold; 
        }

        /* כרטיסיית ניתוח נשלפת מלמטה (Bottom Sheet) */
        .bottom-sheet { 
            position: absolute; 
            bottom: 0; 
            left: 0; 
            right: 0; 
            background: #1e1e1e; 
            border-top: 2px solid #4caf50; 
            border-radius: 16px 16px 0 0; 
            z-index: 900; 
            transition: transform 0.3s cubic-bezier(0.1, 0.9, 0.2, 1); 
            transform: translateY(calc(100% - 44px)); 
            box-shadow: 0 -4px 20px rgba(0,0,0,0.7); 
            max-height: 70%; 
            display: flex; 
            flex-direction: column; 
        }
        .bottom-sheet.expanded { 
            transform: translateY(0); 
        }
        .sheet-handle { 
            height: 44px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 0 16px; 
            cursor: pointer; 
            background: #252525; 
            border-radius: 14px 14px 0 0; 
        }
        .sheet-title { 
            font-weight: bold; 
            font-size: 0.95em; 
            color: #4caf50; 
            display: flex; 
            align-items: center; 
            gap: 8px; 
        }
        .sheet-content { 
            padding: 14px 16px; 
            overflow-y: auto; 
            font-size: 0.9em; 
            line-height: 1.6; 
        }
        
        .stat-tag { 
            display: inline-block; 
            background: #2d2d2d; 
            border: 1px solid #444; 
            padding: 3px 8px; 
            border-radius: 6px; 
            font-size: 0.8em; 
            margin: 2px 4px 4px 0; 
            color: #81c784; 
        }
        .analysis-text-box { 
            background: #252525; 
            border-radius: 8px; 
            padding: 10px; 
            margin-top: 8px; 
            border-right: 3px solid #4caf50; 
        }

        /* מסך תיק השקעות */
        .portfolio-view { 
            padding: 14px; 
        }
        .trade-form { 
            background: #1e1e1e; 
            border: 1px solid #2d2d2d; 
            border-radius: 10px; 
            padding: 14px; 
            margin-bottom: 14px; 
            display: flex; 
            flex-direction: column; 
            gap: 8px; 
        }
        .form-row { 
            display: flex; 
            gap: 8px; 
        }
        .trade-form input { 
            flex: 1; 
            padding: 9px 12px; 
            border-radius: 6px; 
            border: 1px solid #3d3d3d; 
            background: #262626; 
            color: #fff; 
            font-size: 0.9em; 
        }
        .trade-form button { 
            background: #1976d2; 
            color: white; 
            border: none; 
            padding: 11px; 
            border-radius: 6px; 
            font-weight: bold; 
            cursor: pointer; 
        }
        
        .trade-item { 
            background: #1e1e1e; 
            border: 1px solid #2d2d2d; 
            border-right: 4px solid #1976d2; 
            border-radius: 8px; 
            padding: 12px; 
            margin-bottom: 10px; 
        }
        .trade-item.closed { 
            border-right-color: #666; 
            opacity: 0.85; 
        }
        .trade-top { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 6px; 
        }
        .trade-info { 
            font-size: 0.85em; 
            color: #aaa; 
            line-height: 1.5; 
        }
        .trade-actions { 
            margin-top: 10px; 
            display: flex; 
            gap: 8px; 
            align-items: center; 
        }
        
        .btn-action { 
            background: #2a2a2a; 
            color: #fff; 
            border: 1px solid #444; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-size: 0.8em; 
            cursor: pointer; 
        }
        .btn-close-trade { 
            background: #c62828; 
            border-color: #b71c1c; 
        }
        .profit { 
            color: #4caf50; 
            font-weight: bold; 
        }
        .loss { 
            color: #f44336; 
            font-weight: bold; 
        }

        /* תפריט הגדרות נשלף (Settings Drawer) */
        .settings-overlay { 
            position: fixed; 
            inset: 0; 
            background: rgba(0,0,0,0.6); 
            z-index: 998; 
            opacity: 0; 
            pointer-events: none; 
            transition: 0.3s; 
        }
        .settings-overlay.active { 
            opacity: 1; 
            pointer-events: auto; 
        }
        .settings-drawer { 
            position: fixed; 
            top: 0; 
            right: -320px; 
            width: 300px; 
            height: 100vh; 
            background: #1a1a1a; 
            z-index: 999; 
            transition: right 0.3s ease; 
            border-left: 1px solid #333; 
            display: flex; 
            flex-direction: column; 
        }
        .settings-drawer.active { 
            right: 0; 
        }
        .drawer-head { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 16px; 
            border-bottom: 1px solid #2d2d2d; 
        }
        .drawer-body { 
            padding: 16px; 
            overflow-y: auto; 
            display: flex; 
            flex-direction: column; 
            gap: 14px; 
        }
        
        .setting-box { 
            background: #242424; 
            border: 1px solid #333; 
            border-radius: 8px; 
            padding: 12px; 
        }
        .google-btn { 
            background: #4285F4; 
            color: white; 
            border: none; 
            padding: 10px; 
            border-radius: 6px; 
            font-weight: bold; 
            width: 100%; 
            cursor: pointer; 
            margin-top: 8px; 
        }
        .logout-btn { 
            background: #333; 
            color: #ff5252; 
            border: 1px solid #555; 
            padding: 8px; 
            border-radius: 6px; 
            width: 100%; 
            cursor: pointer; 
            margin-top: 8px; 
            font-weight: bold; 
        }

        /* מצב יום */
        body.light-mode { 
            background-color: #f4f6f9; 
            color: #222; 
        }
        body.light-mode .app-header, 
        body.light-mode .bottom-nav, 
        body.light-mode .settings-drawer { 
            background: #fff; 
            border-color: #ddd; 
        }
        body.light-mode .stock-card, 
        body.light-mode .trade-form, 
        body.light-mode .trade-item, 
        body.light-mode .bottom-sheet { 
            background: #fff; 
            border-color: #ddd; 
            color: #222; 
        }
        body.light-mode .sheet-handle, 
        body.light-mode .analysis-text-box, 
        body.light-mode .setting-box { 
            background: #f0f3f6; 
        }
        body.light-mode .trade-form input, 
        body.light-mode .search-container input { 
            background: #f0f0f0; 
            color: #222; 
        }
        body.light-mode .stat-tag { 
            background: #e8f5e9; 
            color: #2e7d32; 
        }
    </style>
</head>
<body>

    <!-- סרגל עליון -->
    <div class="app-header">
        <div class="header-title">
            <span>📈</span>
            <span id="headerSymbol">SPY</span>
        </div>
        <div class="header-actions">
            <div class="search-container">
                <input type="text" id="manualSearch" placeholder="חיפוש מניה..." onkeypress="if(event.key === 'Enter') handleSearch()">
                <button onclick="handleSearch()">🔍</button>
            </div>
            <button class="icon-btn" onclick="toggleSettings(true)">☰</button>
        </div>
    </div>

    <!-- גוף האפליקציה -->
    <div class="app-views">
        
        <!-- 1. מסך סורק מניות -->
        <div id="view-screener" class="view">
            <div class="screener-list" id="stockListContainer">
                <p style="text-align:center; color:#888; padding-top:40px;">טוען תוצאות סריקה...</p>
            </div>
        </div>

        <!-- 2. מסך גרף וניתוח -->
        <div id="view-chart" class="view active">
            <div id="tv_chart_container"></div>
            
            <!-- Bottom Sheet ניתוח נשלף -->
            <div class="bottom-sheet" id="analysisSheet">
                <div class="sheet-handle" onclick="toggleBottomSheet()">
                    <div class="sheet-title">
                        <span>📊</span>
                        <span id="sheetStockTitle">ניתוח טכני והמלצה</span>
                    </div>
                    <span id="sheetArrow" style="font-size:0.8em; color:#888;">▲ החלק להצגה</span>
                </div>
                <div class="sheet-content" id="sheetDetails">
                    <p style="color:#888;">בחר מניה מהסורק להצגת הניתוח המלא.</p>
                </div>
            </div>
        </div>

        <!-- 3. מסך תיק השקעות -->
        <div id="view-portfolio" class="view">
            <div class="portfolio-view">
                <div id="authRequiredNotice" class="setting-box" style="text-align:center; display:none;">
                    <p style="margin:0 0 6px 0;">כדי לנהל תיק עסקאות מסונכרן:</p>
                    <button class="google-btn" onclick="loginGoogle()">התחבר עם Google</button>
                </div>

                <div id="portfolioMainArea">
                    <div class="trade-form">
                        <b style="font-size:0.95em;">הוספת פוזיציה חדשה</b>
                        <div class="form-row">
                            <input type="text" id="tradeTicker" placeholder="סימול (AAPL)">
                            <input type="date" id="tradeDate">
                        </div>
                        <div class="form-row">
                            <input type="number" id="tradePrice" placeholder="שער קנייה ($)" step="0.01">
                            <input type="number" id="tradeComm" placeholder="עמלה ($)" step="0.01">
                        </div>
                        <button onclick="addTrade()">הוסף לתיק</button>
                    </div>

                    <div id="tradesList"><p style="text-align:center; color:#888;">טוען נתונים...</p></div>
                </div>
            </div>
        </div>

    </div>

    <!-- סרגל ניווט תחתון -->
    <div class="bottom-nav">
        <button class="nav-btn" id="nav-screener" onclick="switchNav('screener')">
            <span class="nav-icon">🔍</span>
            <span>סורק</span>
        </button>
        <button class="nav-btn active" id="nav-chart" onclick="switchNav('chart')">
            <span class="nav-icon">📈</span>
            <span>גרף</span>
        </button>
        <button class="nav-btn" id="nav-portfolio" onclick="switchNav('portfolio')">
            <span class="nav-icon">💼</span>
            <span>תיק</span>
        </button>
    </div>

    <!-- תפריט הגדרות נשלף (Settings Drawer) -->
    <div class="settings-overlay" id="settingsOverlay" onclick="toggleSettings(false)"></div>
    <div class="settings-drawer" id="settingsDrawer">
        <div class="drawer-head">
            <b style="font-size:1.05em;">הגדרות מערכת</b>
            <button class="btn-action" onclick="toggleSettings(false)">✕</button>
        </div>
        <div class="drawer-body">
            <div class="setting-box">
                <b>חשבון משתמש</b>
                <div id="userProfileStatus" style="font-size:0.85em; color:#aaa; margin-top:4px;">לא מחובר</div>
                <div id="authActionArea">
                    <button class="google-btn" onclick="loginGoogle()">התחבר עם Google</button>
                </div>
            </div>

            <div class="setting-box">
                <b>תצוגה</b>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                    <span style="font-size:0.9em;">ערכת נושא:</span>
                    <button class="btn-action" id="themeBtn" onclick="toggleTheme()">☀️ מצב יום</button>
                </div>
            </div>

            <div class="setting-box" style="font-size:0.85em; color:#888;">
                <b>סטטוס סריקה:</b>
                <div style="margin-top:4px;">סריקה יומית אוטומטית פעילה.</div>
            </div>
        </div>
    </div>

    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script>
        const firebaseConfig = {
            apiKey: "AIzaSyD0JgU15_MKcwZK0eZIRinqnrOJYppzgp8",
            authDomain: "swing-portfolio.firebaseapp.com",
            projectId: "swing-portfolio",
            storageBucket: "swing-portfolio.firebasestorage.app",
            messagingSenderId: "1021148994913",
            appId: "1:1021148994913:web:d31fadc54acace2cafb920"
        };
        firebase.initializeApp(firebaseConfig);
        const db = firebase.firestore();
        const auth = firebase.auth();

        let currentUser = null;
        let unsubscribeTrades = null;
        let widget = null;
        let currentTheme = 'dark';
        let activeSymbol = 'SPY';

        document.getElementById('tradeDate').valueAsDate = new Date();

        // 1. אתחול גרף TradingView ללא מגבלות עם אינדיקטורים מובנים
        function loadChart(ticker) {
            activeSymbol = ticker;
            document.getElementById('headerSymbol').innerText = ticker;
            const bg = currentTheme === 'light' ? "#ffffff" : "#121212";

            widget = new TradingView.widget({
                "autosize": true,
                "symbol": ticker,
                "interval": "D",
                "timezone": "Etc/UTC",
                "theme": currentTheme,
                "style": "1",
                "locale": "he_IL",
                "enable_publishing": false,
                "backgroundColor": bg,
                "hide_top_toolbar": false,
                "hide_legend": false,
                "save_image": false,
                "container_id": "tv_chart_container",
                "studies": [
                    { id: "MASimple@tv-basicstudies", inputs: { length: 50 }, title: "SMA 50" },
                    { id: "MASimple@tv-basicstudies", inputs: { length: 150 }, title: "SMA 150" },
                    { id: "RSI@tv-basicstudies", inputs: { length: 14 } }
                ]
            });
        }

        // 2. ניווט טאבים תחתון
        function switchNav(tab) {
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

            document.getElementById(`view-${tab}`).classList.add('active');
            document.getElementById(`nav-${tab}`).classList.add('active');

            if (tab === 'chart' && !widget) loadChart(activeSymbol);
            if (tab === 'portfolio') loadTrades();
        }

        // 3. תפריט הגדרות
        function toggleSettings(open) {
            document.getElementById('settingsDrawer').classList.toggle('active', open);
            document.getElementById('settingsOverlay').classList.toggle('active', open);
        }

        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            currentTheme = document.body.classList.contains('light-mode') ? 'light' : 'dark';
            document.getElementById('themeBtn').innerText = currentTheme === 'light' ? '🌙 מצב לילה' : '☀️ מצב יום';
            loadChart(activeSymbol);
        }

        // 4. כרטיסיית ניתוח תחתונה (Bottom Sheet)
        function toggleBottomSheet(forceExpand) {
            const sheet = document.getElementById('analysisSheet');
            const arrow = document.getElementById('sheetArrow');
            const isExp = forceExpand !== undefined ? forceExpand : !sheet.classList.contains('expanded');
            
            sheet.classList.toggle('expanded', isExp);
            arrow.innerText = isExp ? '▼ סגור ניתוח' : '▲ הצג ניתוח והמלצה';
        }

        function renderStockAnalysis(stock) {
            document.getElementById('sheetStockTitle').innerText = `${stock.ticker} - $${stock.price || ''}`;
            
            let badges = '';
            let texts = '';

            if (stock.rsi) badges += `<span class="stat-tag">RSI: ${stock.rsi}</span>`;
            if (stock.volume) badges += `<span class="stat-tag">מחזור: ${Number(stock.volume).toLocaleString()}</span>`;
            if (stock.sma50 || stock.ma50) badges += `<span class="stat-tag">MA50: $${stock.sma50 || stock.ma50}</span>`;
            if (stock.sma150 || stock.ma150) badges += `<span class="stat-tag">MA150: $${stock.sma150 || stock.ma150}</span>`;

            const rec = stock.recommendation || stock.setup || stock.signal;
            if (rec) texts += `<div class="analysis-text-box"><b>אסטרטגיה / המלצה:</b><br>${rec}</div>`;

            const analysis = stock.analysis || stock.reason || stock.summary || stock.notes;
            if (analysis && analysis !== rec) texts += `<div class="analysis-text-box"><b>ניתוח טכני:</b><br>${analysis}</div>`;

            for (let k in stock) {
                if (!['ticker','price','rsi','volume','sma50','ma50','sma150','ma150','recommendation','setup','signal','analysis','reason','summary','notes'].includes(k)) {
                    if (typeof stock[k] === 'string' || typeof stock[k] === 'number') {
                        badges += `<span class="stat-tag">${k}: ${stock[k]}</span>`;
                    }
                }
            }

            document.getElementById('sheetDetails').innerHTML = badges + texts || '<p>אין נתוני ניתוח זמינים.</p>';
            toggleBottomSheet(true);
        }

        function selectStockFromList(stock) {
            loadChart(stock.ticker);
            renderStockAnalysis(stock);
            switchNav('chart');
        }

        function handleSearch() {
            const sym = document.getElementById('manualSearch').value.toUpperCase().trim();
            if (sym) {
                loadChart(sym);
                document.getElementById('sheetStockTitle').innerText = sym;
                document.getElementById('sheetDetails').innerHTML = '<p style="color:#888;">חיפוש ידני - אין נתוני סריקה שמורים.</p>';
                toggleBottomSheet(false);
                switchNav('chart');
            }
        }

        // 5. טעינת נתוני הסורק
        async function loadScreener() {
            try {
                const res = await fetch('screener_results_v2.json?nocache=' + new Date().getTime());
                const data = await res.json();
                const container = document.getElementById('stockListContainer');
                container.innerHTML = '';

                data.stocks.forEach((stock) => {
                    const card = document.createElement('div');
                    card.className = 'stock-card';
                    const rec = stock.recommendation || stock.setup || 'מגמה חיובית';
                    card.innerHTML = `
                        <div>
                            <div class="stock-ticker">${stock.ticker}</div>
                            <div class="stock-sub">${rec}</div>
                        </div>
                        <div class="stock-price-box">
                            <div class="stock-price">$${stock.price || ''}</div>
                            <div style="font-size:0.75em; color:#4caf50; text-align:left;">פתח גרף ➔</div>
                        </div>
                    `;
                    card.onclick = () => selectStockFromList(stock);
                    container.appendChild(card);
                });

                if (data.stocks.length > 0) {
                    activeSymbol = data.stocks[0].ticker;
                    renderStockAnalysis(data.stocks[0]);
                }
            } catch (e) {
                document.getElementById('stockListContainer').innerHTML = '<p style="text-align:center; color:#888; padding-top:40px;">ממתין לסריקה היומית הבאה.</p>';
            }
            loadChart(activeSymbol);
        }

        // 6. התחברות וניהול תיק ב-Firebase
        auth.onAuthStateChanged((user) => {
            currentUser = user;
            const profileStatus = document.getElementById('userProfileStatus');
            const authArea = document.getElementById('authActionArea');
            const authNotice = document.getElementById('authRequiredNotice');
            const mainArea = document.getElementById('portfolioMainArea');

            if (user) {
                profileStatus.innerText = user.email;
                authArea.innerHTML = `<button class="logout-btn" onclick="auth.signOut()">התנתק</button>`;
                authNotice.style.display = 'none';
                mainArea.style.display = 'block';
                loadTrades();
            } else {
                profileStatus.innerText = 'לא מחובר';
                authArea.innerHTML = `<button class="google-btn" onclick="loginGoogle()">התחבר עם Google</button>`;
                authNotice.style.display = 'block';
                mainArea.style.display = 'none';
                if (unsubscribeTrades) unsubscribeTrades();
            }
        });

        function loginGoogle() {
            const p = new firebase.auth.GoogleAuthProvider();
            auth.signInWithPopup(p).catch(e => alert(e.message));
        }

        async function addTrade() {
            if (!currentUser) return;
            const ticker = document.getElementById('tradeTicker').value.toUpperCase().trim();
            const buyPrice = parseFloat(document.getElementById('tradePrice').value);
            const buyComm = parseFloat(document.getElementById('tradeComm').value) || 0;
            const buyDate = document.getElementById('tradeDate').value || new Date().toISOString().split('T')[0];

            if (!ticker || !buyPrice) { alert("הזן סימול ומחיר קנייה."); return; }

            await db.collection("trades").add({
                userId: currentUser.uid, 
                ticker, 
                buyPrice, 
                buyComm, 
                buyDate,
                status: 'open', 
                timestamp: new Date().getTime()
            });

            document.getElementById('tradeTicker').value = '';
            document.getElementById('tradePrice').value = '';
            document.getElementById('tradeComm').value = '';
        }

        async function closeTrade(docId, buyPrice, buyComm) {
            const sellPrice = parseFloat(prompt("שער מכירה ($):"));
            if (!sellPrice) return;
            const sellComm = parseFloat(prompt("עמלת מכירה ($):", "0")) || 0;
            const today = new Date().toISOString().split('T')[0];
            const sellDate = prompt("תאריך מכירה (YYYY-MM-DD):", today) || today;

            const totalCost = buyPrice + buyComm;
            const totalReturn = sellPrice - sellComm;
            const pnlDollars = (totalReturn - totalCost).toFixed(2);
            const pnlPercent = (((totalReturn - totalCost) / totalCost) * 100).toFixed(2);

            await db.collection("trades").doc(docId).update({
                sellPrice, 
                sellComm, 
                sellDate, 
                status: 'closed',
                pnlDollars, 
                pnlPercent
            });
        }

        async function editTrade(docId, dataStr) {
            const trade = JSON.parse(decodeURIComponent(dataStr));
            const newBuyPrice = parseFloat(prompt("שער קנייה:", trade.buyPrice)) || trade.buyPrice;
            const newBuyComm = parseFloat(prompt("עמלת קנייה:", trade.buyComm)) || 0;
            const newBuyDate = prompt("תאריך קנייה (YYYY-MM-DD):", trade.buyDate) || trade.buyDate;

            let updateData = { buyPrice: newBuyPrice, buyComm: newBuyComm, buyDate: newBuyDate };

            if (trade.status === 'closed') {
                const newSellPrice = parseFloat(prompt("שער מכירה:", trade.sellPrice)) || trade.sellPrice;
                const newSellComm = parseFloat(prompt("עמלת מכירה:", trade.sellComm)) || 0;
                const newSellDate = prompt("תאריך מכירה (YYYY-MM-DD):", trade.sellDate) || trade.sellDate;

                const totalCost = newBuyPrice + newBuyComm;
                const totalReturn = newSellPrice - newSellComm;
                updateData.sellPrice = newSellPrice;
                updateData.sellComm = newSellComm;
                updateData.sellDate = newSellDate;
                updateData.pnlDollars = (totalReturn - totalCost).toFixed(2);
                updateData.pnlPercent = (((totalReturn - totalCost) / totalCost) * 100).toFixed(2);
            }

            await db.collection("trades").doc(docId).update(updateData);
        }

        async function deleteTrade(docId) {
            if (confirm("למחוק עסקה זו לצמיתות?")) {
                await db.collection("trades").doc(docId).delete();
            }
        }

        function loadTrades() {
            if (!currentUser) return;
            if (unsubscribeTrades) unsubscribeTrades();

            unsubscribeTrades = db.collection("trades")
                .where("userId", "==", currentUser.uid)
                .onSnapshot((snapshot) => {
                    const container = document.getElementById('tradesList');
                    container.innerHTML = '';

                    if (snapshot.empty) {
                        container.innerHTML = '<p style="text-align:center; color:#888;">התיק ריק כרגע.</p>';
                        return;
                    }

                    const docs = [];
                    snapshot.forEach(doc => docs.push({ id: doc.id, ...doc.data() }));
                    docs.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));

                    docs.forEach((trade) => {
                        const div = document.createElement('div');
                        div.className = `trade-item ${trade.status}`;
                        const safeDataStr = encodeURIComponent(JSON.stringify(trade));

                        let statusHtml = '';
                        if (trade.status === 'open') {
                            statusHtml = `<button class="btn-action btn-close-trade" onclick="closeTrade('${trade.id}', ${trade.buyPrice}, ${trade.buyComm})">סגור פוזיציה</button>`;
                        } else {
                            let pnlClass = trade.pnlDollars >= 0 ? 'profit' : 'loss';
                            statusHtml = `<div class="${pnlClass}">תשואה: ${trade.pnlPercent}% ($${trade.pnlDollars})</div>`;
                        }

                        div.innerHTML = `
                            <div class="trade-top" onclick="loadChart('${trade.ticker}'); switchNav('chart');">
                                <span class="stock-ticker">${trade.ticker}</span>
                                <span style="font-size:0.8em;">${trade.status === 'open' ? '🟢 פתוח' : '⚪ סגור'}</span>
                            </div>
                            <div class="trade-info">
                                <b>קנייה:</b> $${trade.buyPrice} (${trade.buyDate || '-'}) | עמלה: $${trade.buyComm}<br>
                                ${trade.status === 'closed' ? `<b>מכירה:</b> $${trade.sellPrice} (${trade.sellDate || '-'}) | עמלה: $${trade.sellComm}` : ''}
                            </div>
                            <div class="trade-actions">
                                ${statusHtml}
                                <button class="btn-action" onclick="editTrade('${trade.id}', '${safeDataStr}')">✏️ ערוך</button>
                                <button class="btn-action" style="margin-right:auto; color:#ff5252;" onclick="deleteTrade('${trade.id}')">🗑️</button>
                            </div>
                        `;
                        container.appendChild(div);
                    });
                });
        }

        loadScreener();
    </script>
</body>
</html>
