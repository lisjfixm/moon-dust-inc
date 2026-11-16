# Moon Dust Inc.

three.js 成品（公開倉庫 `lisjfixm/moon-dust-inc`）。原始 Poki 來源：<https://poki.com/zh/g/moon-dust>。

- **目前版本**：1.1.0
- **圖形引擎**：three.js r187（已內嵌於 `index.html`，無外部 CDN 依賴）
- **離線可執行**：無外部 script、無廣告 SDK 連線；Poki 呼叫在離線時為 no-op。
- **線上試玩**：<https://lisjfixm.github.io/moon-dust-inc/>

## 啟動方式

### Windows（建議）

雙擊 `啟動 Moon Dust.bat`。腳本會找 `py`（找不到再找 `python`），在 `127.0.0.1:8782` 啟動靜態伺服器，並開啟 <http://127.0.0.1:8782/index.html>。

### 手動啟動

```bash
python3 -m http.server 8782 --bind 127.0.0.1
# 瀏覽器開啟 http://127.0.0.1:8782/index.html
```

需透過 HTTP 伺服器存取（模組載入與資產 fetch 有限制），不建議直接 `file://` 開啟。

## 自動遊玩模式（Auto-play）

右下角 `AUTO` 開關：開啟後由腳本代玩，關閉即交还操作；開關狀態記住於 localStorage。

- **探索**：持續前進並左右走位，間隔使用 turbo；可用時觸發雷射。
- **回程販賣**：袋子滿且鄰近有 depot 時，走內建回程導航 hook 回到倉庫販賣。
- **升級決策**：讀取經濟系統的 `canBuy / costOf / level / unlocked`，依「權重 ÷ 成本」評分選最優項目，經遊戲公開購買路徑下單；權重偏向煉油廠、背包、機器人、韌體等長線收益。
- **狀態接駁**：自動跳過 intro；暫停、書本、商店等覆蓋層會自動關閉以回到 playing。
- **限制**：無指標鎖定下無法程式化控制視角 yaw，走位以前進＋橫向搖擺為主；地面回收依賴磁鐵／機器人的被動範圍。

實作為獨立 classic `<script>`，掛在打包模組之後，防禦性輪詢 `window.__game`，所有公開呼叫皆包 try/catch。模組原本只在網址帶 `?debug` 時暴露 `window.__game`，本版本改為常駐暴露以供自動模式取用，其餘 debug 行為未開啟。

## GitHub Pages 部署

- 站點：<https://lisjfixm.github.io/moon-dust-inc/>
- 來源：`main` 分支根目錄（legacy build）；根目錄 `index.html` 即線上版本，更新 main 後自動發布。
- 根目錄 `.nojekyll` 停用 Jekyll 處理，避免成品碼被轉換。
- 部署前確認 main 根目錄 `index.html` 為最新版。

## 目錄結構

| 路徑 | 內容 |
|---|---|
| `index.html` | 主頁面：內聯 PokiSDK stub、minified CSS、three.js + 遊戲打包模組（約 1.7 MB），以及模組之後的自動遊玩腳本 |
| `locales/` | 27 個語言 JSON（各 214 鍵）；英文為程式內建 fallback，無 `en.json` |
| `models/` | 24 個 GLB 模型（副檔名 `.bin`，glTF 2.0，內嵌貼圖） |
| `moon/moon-height.bin` | 月球高度圖，自訂二進位原始資料 |
| `sfx/` | 9 個 mp3 + `sfx.json` 音效精靈表（sprite / loops / extra） |
| `ui/` | WebP 介面圖集與頭像 |
| `vfx/atlas.png` | 特效貼圖集（512×512） |
| `啟動 Moon Dust.bat` | Windows 啟動腳本（埠號 8782） |
| `tools/` | 離線檢查腳本（語言對齊、資產體積盤點） |

## 離線與 Poki SDK 說明

- `index.html` 開頭內嵌一組 PokiSDK **no-op stub**：初始化、廣告插播、獎勵廣告、登入等皆為空實作。
- 遊戲模組若偵測不到真實 SDK，會進入 `unavailable` 狀態並記錄警告，廣告流程直接略過。
- 成品不引用任何外部 CDN、外部 JS 檔或遙測網址。

## 架構現況與可維護性（評估結論）

- 遊戲程式與 three.js 打包在單一 `<script type="module">` 中，且已 minified；**沒有可還原的 source map**。
- CSS 為單行 minified 樣式表。
- 除版本常量等字面量外，**不建議直接在 minified 區塊內改邏輯**；手改容易造成行為漂移且難以除錯。
- 若日後需要大量玩法調整，建議先重建一套可讀源碼與打包流程，再回灌成品；本輪未做架構拆分。

## 資產體積審計（基線）

全體約 7.9 MB。最大檔案：

| 檔案 | 大小 | 備註 |
|---|---:|---|
| `moon/moon-height.bin` | 1.8 MB | 自訂高度圖格式，**不可重編**，維持原樣 |
| `index.html` | 1.7 MB | three.js + 遊戲打包體積 |
| `ui/ui-kit.webp` | 869 KB（4096×2471） | **首要優化候選**：可評估裁切空白區、縮減尺寸或重編 WebP |
| `models/cleaner.bin` | 500 KB | GLB；可評估 Draco / meshopt 壓縮或貼圖縮減 |
| `sfx/oneshots.mp3` | 288 KB | 音效精靈；其餘 mp3 已為 12–56 kbps 單聲道，壓縮空間小 |

任何資產重編後必須實跑回歸，確認模型、貼圖、音效與 UI 圖集定位正常，再提交。

## 語言同步慣例

- 新增或修改 UI 字串時，同步更新 `locales/` 下所有語言檔，避免缺鍵。
- 驗證鍵值對齊：

```bash
python3 tools/check-locales.py
```

## 版本規範

每次更新必須三處同步遞增，不得沿用舊版號：

1. `index.html` 頂部 HTML 註解內的 Changelog 區塊
2. 頁面 `<title>`
3. 模組設定物件內的 `version` 常量

## 檢查腳本

| 腳本 | 用途 |
|---|---|
| `tools/check-locales.py` | 比對所有 `locales/*.json` 的鍵集合，回報缺鍵 / 多餘鍵；不一致時離開碼為 1 |
| `tools/audit-assets.py` | 依目錄統計資產體積，並列出超過門檻的大檔 |
