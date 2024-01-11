<img width="300" alt="SCR-20230502-nedr" src="https://github.com/cdsl-research/Alert_pigeon/assets/48035533/ac7468c4-a02e-4287-b8bd-ee9d4aa5f1e5" />

# Alert_pigeon
マイクロサービスで、各サービスのアラートの重大度を出力するソフトウェアです。
確認用にアラートを出力するプログラムも入っています。

前提：KubernetesでIstio，Kialiが導入されている環境
## 使い方
1. config.jsonを設定する
   kialiのURLとクラスタ名、サービス名を指定してください。
2. python3 level_set.py
   重大度を計算して出力します。
3. python3 alert.py
   重大度をもとにしてレイテンシのアラートを行います。locust等を使用して動作確認ができます。
