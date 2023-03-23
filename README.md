# CoffeeAI
嘗試解決 [Coffee](https://boardgamegeek.com/boardgame/94746/coffee)(2011發行的桌遊)  
規則參考[nestorgames](https://www.nestorgames.com/rulebooks/COFFEE_EN.pdf)
# 預計進度  
* 實作遊戲  
* 實作神經網路<--現在在這
* 實作selfplay、MCTS等  
* 實作訓練  
* 測試訓練  
* 製作UI  
其中實作細節會參考以前的repo，如[2048](https://github.com/kennychenfs/2048-ai)
# 實作想法
## 資料儲存
我看了[這篇論文](https://doi.org/10.48550/arXiv.2101.10897)後打算在程式中以Axial的方式儲存、運算。儲存資料時，輸入如果是binary的，可以用np.packbits()，儲存的量可以少很多。不過矩陣我認為可以直接用二維方式儲存，就和game.py中board一樣，因為邊界外的部分其實不太影響。  
在寫程式時，我都是因為儲存資料和管理資料的障礙而寫不好，我希望這樣先定下方法可以做好。  
## 訓練資料儲存
棋盤用np.packbits存成binary，然後train.py訓練時用np.unpackbits轉回來，讀取檔案是train.py的工作。    
## 用哪些資料訓練
參考KataGo的方法，以檔名方式載入所有棋局，再找最新的一些棋局shuffle後訓練。  
因此也需要shuffle.py來shuffle棋局。
## 神經網路
上面HexCNN的論文沒有講清楚實作該如何做，所以我自己想了一個方法。  
資料使用axial座標儲存，所以我想到直接把正常的Conv2D當作axial座標，但是把kernel在超出邊界的部分權重設為0。也就是自定義layer，在build時把指定位置用mask設為0。也要自定義model，在train_step完後手動把設為0。  
效能方面，其實超出邊界的部分只有1/4，所以並不會嚴重影響。  
# 關於Board
```
Use flat-top orientation and axial coordinates(https://www.redblobgames.com/grids/hexagons/#coordinates-axial)
for example, size 3 pointy top:
    02
  01  13
00  12  24
  11  23
10  22  34
  21  33
20  32  44
  31  43
    42

size 3 flat-top:
    00  01  02
  10  11  12  13
20  21  22  23  24
  31  32  33  34
    42  43  44

In pure text I think flat-top looks better.
```
方向編號：10：1、01：2、11：3  
現在以數字輸出，以後再做UI