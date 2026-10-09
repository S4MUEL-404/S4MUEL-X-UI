# S4MUEL X-UI

An X-UI installation and management script maintained and customized by **S4MUEL**, based on [yonggekkk/x-ui-yg](https://github.com/yonggekkk/x-ui-yg).

## Quick start

Use an SSH terminal connected to your Linux VPS. Run the following as root:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/S4MUEL-404/S4MUEL-X-UI/main/install.sh)
```

Alternatively:

```bash
bash <(wget -qO- https://raw.githubusercontent.com/S4MUEL-404/S4MUEL-X-UI/main/install.sh)
```

Choose **1** to install. Follow the prompts to set your username, password, panel port, base path, and HTTP/HTTPS mode. Record these values privately. Open the full login URL printed by the script, including the port and base path. Allow the panel port in your VPS provider's firewall and your server firewall if necessary.

After installation, run `x-ui` to open the management menu. Platform support is inherited from upstream: Ubuntu, Debian, CentOS, and Alpine on AMD64 or ARM64. Compatibility depends on the specific OS release and available upstream binaries.

## Everyday tasks

| Task | Main menu option |
| --- | --- |
| Install | 1 |
| Uninstall and delete data | 2 |
| Configure tunnels and subscriptions | 3 |
| Change panel credentials, port, or base path | 4 |
| Stop or restart the panel | 5 |
| Update or restore | 6 |
| Generate or view client configurations and subscriptions | 7 |
| View service logs | 8 |
| Refresh displayed connection information | 13 |
| View project information | 14 |

For routine script updates, choose **6**, then **1**. Upgrading the panel itself is a separate operation: **6**, then **2**.

## Reliability improvements

- Independent management-script updates without restarting the panel.
- HTTPS downloads with HTTP error handling and timeouts.
- Validation of the staged script's shebang, embedded version, and Bash syntax before replacement.
- A backup of the previous script and version record before an atomic replacement on the same filesystem.
- Script restoration from a previous backup.
- Panel data backups before panel upgrades.
- Installation stops on failed settings, certificate configuration, or service restarts.
- Live panel readiness checks before installation or upgrade reports success.
- Login URLs use the observed HTTP/HTTPS protocol instead of relying on certificate marker files.

Existing database filenames, `/etc/x-ui-yg`, the `x-ui` service, and certificate paths are preserved for upstream compatibility.

## Updates, backups, and restoration

Run `x-ui` and choose **6**:

1. **Update the management script only.** Download a candidate beside the installed script, validate it, back up the current script and version record, and replace the script. Download, validation, backup, or replacement failure leaves the previous script in place. The panel is not restarted.
2. **Upgrade the panel.** Stop the service and archive `/etc/x-ui-yg`, including any SQLite WAL files, and `/usr/local/x-ui/bin` before installing upstream binaries. If backup fails, abort the upgrade and attempt to restart the service.
3. **Restore a management script.** Enter the full script backup directory printed during an earlier update. Restore the script and version record without restarting the panel.

Backups are stored in separate owner-only subdirectories under `/usr/local/x-ui/backups/`. Keep an off-server copy of important backups. Panel archives may contain account information, certificates, and subscription credentials.

Panel archives are for manual recovery; automatic rollback of panel binaries is not implemented. Backups in this directory are removed by the uninstall operation, so export them before uninstalling. Do not run concurrent updates.

Syntax and version checks are not a code audit or cryptographic signature verification.

## HTTPS and readiness checks

HTTPS configuration requires both a certificate and its private key. Configuration failures stop installation. After restarting the service, the script probes the saved panel port and base path on `127.0.0.1`. It accepts HTTP 200 and common redirect responses. If HTTPS was requested but only HTTP responds, installation does not report success.

The loopback probe skips certificate verification to accommodate self-signed certificates. It does not prove that browsers trust the certificate, DNS is correct, or an external firewall allows access. A panel bound exclusively to a different interface may fail the loopback check.

## Troubleshooting

- **Login page does not open:** check the complete URL, port, and base path, then check both firewall layers. Refresh panel information with menu **13**.
- **HTTPS setup fails:** confirm that both certificate and private-key files exist and that the configured hostname matches your certificate. Read the reported error before retrying.
- **Service fails to start:** use menu **8** or `journalctl -u x-ui --no-pager -n 100` on systemd systems. On Alpine, use `rc-service x-ui status`; the script's log viewer does not support Alpine.
- **Script update fails:** the old script should remain available. Check connectivity, disk space, and file permissions. Use menu **6 → 3** for a known script backup if needed.
- **Panel upgrade fails:** keep the printed backup path. Panel recovery is manual; avoid uninstalling before exporting the backup.

Do not share passwords, tokens, private keys, or complete subscription URLs in public issues.

## Sources and dependencies

S4MUEL maintains this fork's script changes and branding. Upstream functionality and third-party components retain their original authorship.

- Upstream script: [yonggekkk/x-ui-yg](https://github.com/yonggekkk/x-ui-yg)
- Panel binaries: upstream `xui_yg` release assets; this fork does not rebuild or rebrand the web panel.
- Certificate helper: [acme-yg](https://github.com/yonggekkk/acme-yg)
- WARP helper: [warp-yg](https://github.com/yonggekkk/warp-yg)
- References listed by upstream: [vaxilu/x-ui](https://github.com/vaxilu/x-ui), [MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui), [qist/xray-ui](https://github.com/qist/xray-ui), and [bepass-org/warp-plus](https://github.com/bepass-org/warp-plus).

Upstream states that its panel binaries are not open source. This fork does not add or change licenses for upstream or third-party components. The inherited interactive script and external tools may display Chinese; this repository's documentation is in English.

## Validation

```bash
bash -n install.sh
python3 test_updates.py
python3 test_panel.py
```

The 10 update/restore tests and 5 panel-readiness tests isolate script functions and mock downloads or panel responses. They do not run the installer or access a real server. GitHub Actions runs these checks on pushes and pull requests.

These tests do not validate every installation or upgrade scenario on a live VPS.

## Changelog

### v1.1.1-s4

- Stop installation on failed panel settings or certificate configuration.
- Require both certificate and private key for HTTPS.
- Stop on restart failure; probe the configured panel port and base path before reporting installation or upgrade success.
- Display login URLs using the live protocol.
- Add five panel-readiness regression tests to CI.

### v1.1.0-s4

- Add independent script updates, staged validation, backups, and script restoration.
- Back up panel data before panel upgrades.
- Add 10 isolated update/restore tests and GitHub Actions.

### v1.0.0-s4

- Introduce S4MUEL branding, project documentation, and independent script/version endpoints while preserving upstream compatibility and attribution.
