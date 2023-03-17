# CoffeeAI
嘗試解決 [Coffee](https://boardgamegeek.com/boardgame/94746/coffee)(2011發行的桌遊)
# 預計進度  
* 實作遊戲<--現在在這  
* 實作神經網路  
* 實作selfplay、MCTS等  
* 實作訓練  
* 測試訓練  
* 製作UI  
其中實作細節會參考以前的repo，如[2048](https://github.com/kennychenfs/2048-ai)
# 實作想法
我看了[這篇論文](https://doi.org/10.48550/arXiv.2101.10897)後打算在程式中以Axial的方式儲存、運算。儲存資料時，輸入如果是binary的，可以用np.packbits()，儲存的量可以少很多。不過矩陣我認為可以直接用二維方式儲存，就和game.py中board一樣，因為邊界外的部分其實不太影響。  
在寫程式時，我都是因為儲存資料和管理資料的障礙而寫不好，我希望這樣先定下方法可以做好。
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