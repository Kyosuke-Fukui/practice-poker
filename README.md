# practice-poker
高レートポーカープレイヤーのプレイ履歴からアクションを予想するゲーム

## 使い方
* プレイ履歴のデータを前処理（preprocessing.py）
* 前処理したデータを読み込み、ゲームを作成。各ストリートでのアクションを入力する（practice.py）

## 留意点
* 履歴から抽出するのはハンドをショウしたゲームのみ
* 過去にポットを獲得したプレイヤーのアクションを予想する形のため、実質的にフォールドの選択肢はない
* 実際行われたプレイと一致した場合のみ正解としているが、現実的には各アクションにEVの差がほぼない場合も存在するし、
そもそもポーカーとは相手のプレイ傾向からアクションを最適化していくものなので、同一のハンド、ボードで一律に正解が存在するわけではない
