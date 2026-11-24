# pnx-csp-pe

Portable Engine fork of the **Common Source Code Project (CSP)** targeting Windows, Linux, and ESP-IDF (ESP32-P4 + ESP32-C6), developed by **MIKAN WORKSHOP** as part of the **FM Phoenix Project**.

## Overview & Architecture
- **Unified GUI with LVGL:** Shares a consistent UI layer built on **LVGL** across both desktop and embedded targets.
- **Desktop Backend (Windows / Linux):** Uses **LVGL + SDL2** for rendering, audio, and input.
- **Embedded Backend (ESP-IDF):** Targets **ESP32-P4 + ESP32-C6** architectures using **LVGL + custom LCD driver**.
- **Upstream Sync:** Forked from [shiranui-deco/csp-ex](https://github.com/shiranui-deco/csp-ex) to decouple the CSP Virtual Machine (`vm/`) from Win32 dependencies.

## Target Platforms & Supported Machines
- **Windows / Linux:** x64 Desktop, **Raspberry Pi 4**, **ClockworkPi uConsole** (LVGL + SDL2)
- **ESP-IDF:** **ESP32-P4 + ESP32-C6** (LVGL + Custom LCD Driver)
- **Machines:** FM-7 / FM-77 / FM-77L4 / FM77AV / FM77AV40 / FM77AV40EX *(In Progress)*

## Related Projects
- **Upstream (Forked from):** [csp-ex](https://github.com/shiranui-deco/csp-ex) - Extended repository based on the Common Source Code Project (CSP) by Toshiya Takeda.

## Credits & License
- Original source code: **Common Source Code Project** by TAKEDA, toshiya (https://takeda-toshiya.my.coocan.jp/)
- Licensed under the **GNU General Public License v2.0 or later (GPL-2.0-or-later)** in accordance with the original project.

---

# pnx-csp-pe (日本語)

武田俊也氏による **Common Source Code Project (CSP)** をベースに、Windows / Linux / ESP-IDF（ESP32-P4 + C6）へのマルチプラットフォーム対応を目指したポータブルエンジンです。サークル「みかん工房（MIKAN WORKSHOP）」による FM不死鳥計画の一環として開発しています。

## 概要
- **マルチプラットフォーム対応:** Windows、Linux（Raspberry Pi 4 / ClockworkPi uConsole 等）、および組み込みマイコン環境（ESP-IDF / ESP32-P4 + C6）の単一コードベースでのビルド・動作を目標としています。
- **共通UIフレームワーク（LVGL）の採用:** すべてのプラットフォームで組み込み向け軽量GUIライブラリである LVGL を採用し、設定メニューやステータス表示などのUIを共通化しています。
  - **Windows / Linux:** LVGL + SDL2 バックエンド
  - **ESP32-P4 + C6:** LVGL + 独自高速LCDドライバ
- **VMコアの分離と還元:** CSPの仮想マシンコア（vm/）をWin32 API依存から切り離し、バグ修正や改善はフォーク元の csp-ex へ還元できる構造を維持しています。

## ターゲット環境
- **Windows:** Windows 10 / 11 (x64 / SDL2 + LVGL)
- **Linux:** Raspberry Pi 4、ClockworkPi uConsole ほか (SDL2 + LVGL)
- **ESP-IDF:** ESP32-P4 + ESP32-C6 (独自LCDドライバ + LVGL)


## 対応機種
- **富士通 FM-7シリーズ:** FM-7 / FM-77 / FM-77L4 / FM77AV / FM77AV40 / FM77AV40EX *(開発中)*

## 関連プロジェクト
- **アップストリーム（フォーク元）:** [csp-ex](https://github.com/shiranui-deco/csp-ex) - 武田俊也氏による Common Source Code Project (CSP) をベースとした拡張リポジトリ。

## クレジット・ライセンス
- オリジナルソースコード: **Common Source Code Project** by TAKEDA, toshiya (https://takeda-toshiya.my.coocan.jp/)
- 本リポジトリはオリジナルプロジェクトに準拠し、**GNU General Public License v2.0 or later (GPL-2.0-or-later)** のもとで公開されています。
