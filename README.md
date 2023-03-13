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
我看了[這篇論文](https://doi.org/10.48550/arXiv.2101.10897)後打算在程式中以Axial的方式儲存、運算，如果需要寫到檔案再改用一維的方式儲存。
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