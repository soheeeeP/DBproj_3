<u>**Text Mining with Mongo DB project**</u>

**===**

Text Mining 기법 중 하나인 Apriori algorithm을 이용하여 제공된 뉴스 기사들을 분석, 주로 쓰이는 단어들을 구해낸다

**---**

***\*뉴스 기사 전처리\****

> Print Morphs(형태소 분석 및 불용어처리)

- 모든 뉴스 기사에 대해 제공된 형태소 분석 source code와 불용어 리스트 파일을 이용해 텍스트 분석에 불필요한 단어 제거
- 형태소 열이 추가된 상태로 DB를 업데이트
- 사용자로부터 뉴스 기사의 url을 입력 받아 해당하는 뉴스 기사의 형태소 출력



> Print WordSet(한 기사 내의 형태소 집합 구하기)

모든 뉴스 기사에 대해 각 기사에 나오는 단어 확인, 집합을 생성하여 새로운 collection에 저장

사용자로부터 뉴스 기사의 url을 입력 받아 해당하는 뉴스 기사의 wordset 출력



***\*Apriori 알고리즘 구현\****

> Frequent Item Set(min sup을 만족시키는 frequent item 생성)

frequent 1,2,3 itemset 형성, DB에 저장

​	(frequent item: 형태소 집합에 속한 하나의 단어의 support값이 min support count값보다 크거나 같은 item)



> strong 연관 규칙 생성

frequent n-th item set에서의 strong 연관 규칙 생성





| 사용환경 |                                 |
| -------- | ------------------------------- |
| server   | dbpurple.sogang.ac.kr (port-22) |
| OS       | Ubuntu 14.04.5 LTS              |
| DB       | MongoDB 3.0.14                  |
| language | python 2.7.6                    |
| library  | pymongo, MeCab                  |

