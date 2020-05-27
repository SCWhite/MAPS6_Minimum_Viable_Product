---
description: 此篇文章將說明MAPSV6的各項功能與機制
---

# MAPSV6-使用完全手冊

{% hint style="info" %}
一般使用者可跳至 [快速安裝方法 ](book/an-zhuang-fang-fa.md)這章節會詳細介紹使用步驟
{% endhint %}

![&#x8A2D;&#x5099;&#x6B63;&#x9762;&#x5716;](.gitbook/assets/83249694_116958706266412_4052263908193337344_n%20%281%29.jpg)

## 目錄:

1. [計畫說明](book/untitled.md)
2. [硬體介紹](book/ying-ti-jie-shao.md)
3. [設計架構](book/she-ji-jia-gou.md)
4. [安裝方法](book/an-zhuang-fang-fa.md)
5. [開機、運作流程](book/kai-ji-yun-zuo-liu-cheng.md)
6. [資料蒐集](book/zi-liao-sou-ji.md)
7. [資料格式](book/zi-liao-ge-shi.md)
8. [資料應用](book/zi-liao-ying-yong.md)
9. [障礙排除](book/zhang-ai-pai-chu.md)

### 預計更新:

### TODO:

#### Fix:

* [ ] Wi-Fi 連線中斷問題\(可能和系統SPI有關\)
* [ ] NB-IOT通訊中 字串消失問題
* [ ] 機體溫度校正
* [ ] TVOC顯示
* [ ] 數值讀取錯誤時 輸出0 \(改為-1 或不送\)

#### Enhance:

* [ ] 系統時區設定
* [ ] 加入本機設定檔\(for GPS/時區/模式 .etc\)
* [ ] 個人化區域網路儀錶板
* [ ] GPS位置設定
* [ ] NB-IOT自動調整電信商
* [ ] 傳輸量計算
* [ ] 螢幕顯示加強與調整

### 版本更新紀錄:

| 版本編號 | 說明 | 其他補充 | 目前線上版本 |
| :--- | :--- | :--- | :--- |
| 0.0.1 | 初始版本 | 沒有更新和watc hdog |  |
| 0.0.2 | 最小可行版 | 加入了WI-FI設定 |  |
| 0.0.3 | 加上外部SD卡 | SD卡和WI-FI有衝突 |  |
| 6.0.0 | 出貨版 | 解掉已知大問題 可穩定執行 |  |
| 6.0.2 | 修改部分機制/提升效率 | 支援UART介面 | &lt;------這裡------ |
| 6.0.3 | 加入NB-IOT功能 | 還不穩定 有遺失buffer問題 |  |
| 6.0.4 | 發現wifi在斷線下不會重新連線 | \(待解\) 目前只能算繞過 |  |
| 6.0.5 | 加入個別設定檔 | GPS/時區/名稱 |  |
| 6.0.6 | 調整螢幕顯示 | 顯示TVOC  |  |
| 6.1.0 | 預計將6.0.3~6.0.6整理好 | \(好累喔\) |  |



