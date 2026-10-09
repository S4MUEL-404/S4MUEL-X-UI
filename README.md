# S4MUEL X-UI

由 **S4MUEL** 維護與客製化的 X-UI 安裝及管理腳本，基於 [yonggekkk/x-ui-yg](https://github.com/yonggekkk/x-ui-yg)。

## 安裝

在支援的 Linux VPS 上，以 root 執行：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/S4MUEL-404/S4MUEL-X-UI/main/install.sh)
```

或：

```bash
bash <(wget -qO- https://raw.githubusercontent.com/S4MUEL-404/S4MUEL-X-UI/main/install.sh)
```

安裝後使用 `x-ui` 開啟管理選單。系統與架構支援沿用上游：Ubuntu、Debian、CentOS、Alpine；AMD64、ARM64。

## S4MUEL 維護內容

- 終端主選單、安裝提示及使用說明採用 S4MUEL X-UI 品牌。
- 安裝後的管理腳本與版本檢查使用本儲存庫的 `main` 分支。
- 保留 `/etc/x-ui-yg`、`x-ui-yg.db`、`x-ui` 服務與憑證路徑，維持上游相容性。
- 面板功能沿用上游，包括 Hysteria2、Argo、WARP 與本地訂閱。

## 更新、備份與還原

執行 `x-ui`，選擇選單 **6**：

1. **僅更新管理腳本**：HTTPS 下載到目標目錄的暫存檔，檢查 HTTP 狀態、標頭、內嵌版本號與 Bash 語法。備份舊腳本及版本記錄後，以同檔案系統的重新命名替換；不重啟面板。下載、驗證、備份或替換失敗時保留原腳本。
2. **升級面板**：停止服務後，將 `/etc/x-ui-yg`（含 SQLite WAL 檔案）與 `/usr/local/x-ui/bin` 備份至私有目錄，再執行上游套件升級。備份失敗則取消升級並嘗試重新啟動服務。
3. **還原管理腳本**：輸入先前顯示的腳本備份目錄，還原腳本及版本記錄，不重啟面板。

備份目錄位於 `/usr/local/x-ui/backups/`；每次操作會建立獨立、僅擁有者可存取的子目錄。面板資料包含憑證及帳號等敏感資訊，請妥善保管。

面板資料備份供手動救援使用；面板二進位檔升級沒有自動回滾功能。Bash 語法與版本標記檢查不代表完整程式碼審計或套件簽章驗證。請勿同時執行多個更新作業。

## 來源與依賴

本版本的品牌與腳本客製化由 S4MUEL 維護；原始功能與上游貢獻保留其原作者歸屬。

- 上游腳本：[yonggekkk/x-ui-yg](https://github.com/yonggekkk/x-ui-yg)
- 面板套件：仍使用上游 `xui_yg` Release；本版本未重新編譯或修改網頁面板。
- 憑證工具：[acme-yg](https://github.com/yonggekkk/acme-yg)
- WARP 工具：[warp-yg](https://github.com/yonggekkk/warp-yg)
- 上游列出的參考專案：[vaxilu/x-ui](https://github.com/vaxilu/x-ui)、[MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui)、[qist/xray-ui](https://github.com/qist/xray-ui)、[bepass-org/warp-plus](https://github.com/bepass-org/warp-plus)

上游 README 聲明面板二進位檔未開源。本儲存庫未新增或變更上游及第三方元件的授權。

## 驗證

```bash
bash -n install.sh
python3 test_updates.py
```

測試只擷取更新函式，在暫存目錄模擬下載，不執行安裝流程。涵蓋成功更新、部分下載失敗、空白與 HTML 回應、語法錯誤、缺少版本、備份失敗、替換失敗、還原及無效還原。

GitHub Actions 對 push 與 pull request 執行相同檢查。尚未在 Linux VPS 實際安裝或升級面板驗證。

