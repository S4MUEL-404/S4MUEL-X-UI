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

## 更新與備份

執行 `x-ui`，選擇選單 6 更新。該選項沿用上游行為，會重新下載面板套件並重啟服務；更新前請備份 `/etc/x-ui-yg/x-ui-yg.db` 或使用面板備份功能。

## 來源與依賴

本版本的品牌與腳本客製化由 S4MUEL 維護；原始功能與上游貢獻保留其原作者歸屬。

- 上游腳本：[yonggekkk/x-ui-yg](https://github.com/yonggekkk/x-ui-yg)
- 面板套件：仍使用上游 `xui_yg` Release；本版本未重新編譯或修改網頁面板。
- 憑證工具：[acme-yg](https://github.com/yonggekkk/acme-yg)
- WARP 工具：[warp-yg](https://github.com/yonggekkk/warp-yg)
- 上游列出的參考專案：[vaxilu/x-ui](https://github.com/vaxilu/x-ui)、[MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui)、[qist/xray-ui](https://github.com/qist/xray-ui)、[bepass-org/warp-plus](https://github.com/bepass-org/warp-plus)

上游 README 聲明面板二進位檔未開源。本儲存庫未新增或變更上游及第三方元件的授權。

## 驗證範圍

已通過 Bash 語法檢查及下載來源檢查；尚未在 Linux VPS 實際安裝驗證。
