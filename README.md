# ComputerNetwork

## 検証環境
[TCP技術入門――進化を続ける基本プロトコル](https://github.com/dilmnqvovpnmlib/tcp-book) で公開されていた Vagrant で作成された環境を参考に Docker で TCP の輻輳制御アルゴリズムのシミュレーションの環境構築を行った。

以下のバージョンの Docker を使用した。
- Docker version 19.03.12, build 48a66213fe

ホスト OS は Ubuntu 18.04 を使用した。

コンテナ内の検証環境は以下である。
- Ubuntu 18.04
- ns-3 3.27
- python3

## 起動コマンド
- `docker build -t cn .`
- `docker run -it --rm -v $(pwd):/home/vagrant/ns3/ns-allinone-3.27/ns-3.27/data cn bash`

## シミュレーション実行コマンド (コンテナ内)
- `python3 simulation.py`
