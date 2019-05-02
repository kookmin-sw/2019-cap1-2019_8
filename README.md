![Imgur](https://i.imgur.com/9GT1dUK.jpg?1)
<br>
국민대학교 2019년도 캡스톤 디자인 8조
<br>
<https://kookmin-sw.github.io/2019-cap1-2019_8/>
<br>
# DREAM(Detecting in Real-timE mAlicious document using Machine learning)


## 프로젝트 소개
최근 악성코드 중 문서형 악성코드의 수가 증가하고 있다. 특히 이 문서형 악성코드의 유포 방법이 화두가 되고 있다. 대표적으로 2018년 1월부터 등장한 갠드크랩(GandCrab) 랜섬웨어는 사람들의 이목을 끌 수 있는 문서 파일로 위장하여 유포된다. 그리고 2018년 3월에 전 세계적으로 등장한 시그마(Sigma) 랜섬웨어는 이력서로 위장하여 유포된다. 이처럼 문서형 악성코드는 점점 지능적이고 정교하게 발전하고 있다.  


![Imgur](https://i.imgur.com/IYjTIGo.jpg)
<br>
[바이러스토탈](https://www.virustotal.com/)(VirusTotal)은 의심스러운 파일 및 URL을 분석하고 모든 종류의 악성 코드를 탐지하는 서비스이다. 위 그림은 일주일 동안 유입된 파일의 유형별 수에 대한 바이러스토탈의 그래프이다. 그래프에 따르면 PDF는 55만 개로 3번째를 차지하고 있으며 이 외에도 MS Word, MS Excel 등 우리가 자주 사용하는 문서형 파일이 속해있다.
<br>

![Imgur](https://i.imgur.com/XPbHyfi.jpg?1)

문서형 악성코드로 인한 피해가 지속적으로 발생하고 있지만, 문서형 악성코드를 전문적으로 탐지하는 안티바이러스는 많지 않다. 이는 문서형 악성코드가 쉽게 유포 될 수 있어 사용자들의 PC가 감염되는 사회적 문제를 발생 시킬 수 있다.

본 프로젝트에서는 문서형 악성코드를 탐지할 수 있는 엔진을 제작하여 문서형 악성코드의 유포와 그로 인한 피해가 생기는 것을 막고자 한다.


## Abstract

The number of malicious codes is rapidly increasing worldwide. Recently, damage caused by document type malicious code such as PDF file and MS Office is increasing. However, very few anti-virus softwares are available to detect them professionally. This project develops an engine that detects malicious documents using machine learning. We expect to prevent the spread of malicious documents and to reduce instances of damage caused by document type malicious code. The engine can also be developed as open-source software, so it can be modified and supplemented by multiple users.

## 소개 영상
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/6xbYGKnqqCc/0.jpg)](https://www.youtube.com/watch?v=6xbYGKnqqCc)

## 팀 소개

### Professor : 윤명근


### 문다민(팀장)
![Imgur](https://i.imgur.com/8WF2AQw.jpg?1)
```
Student ID : 20163104
E-Mail : vmfn0401@gmail.com
Role : 기계 학습 모델 설계 및 구축, 엔진 설계 및 개발
```

### 김기환  
![Imgur](https://i.imgur.com/x9BC407.jpg?1)
```
Student ID : 20133194
E-Mail : kihwan@kookmin.ac.kr
Role : 데이터 수집, 데이터 전처리
```

### 김현석
![Imgur](https://i.imgur.com/wnlYFk2.jpg?1)
```
Student ID : 20143050
E-Mail : kjuk02@gmail.com
Role : 데이터 라벨링, 웹 서버 구축
```

### 정혜리
![Imgur](https://i.imgur.com/mIECcrl.jpg?1)
```
Student ID : 20163158
E-Mail : kbi09@kookmin.ac.kr
Role : 데이터 전처리, 특징 
```

### 방유한(외국인)
![Imgur](https://i.imgur.com/o3YcpMP.jpg?1)
```
Student ID : 20163652
E-Mail : fangyuhan@naver.com
Role : 로고 디자인, 유저 인터페이스 구현
```

## Reference
- **URL**
```buildoutcfg
1. https://blog.didierstevens.com/programs/pdf-tools/
2. https://www.av-test.org/en/news/av-test-awards-this-is-the-elite-class-of-it-security-2018/
3. https://github.com/j40903272/MalConv-keras
```
- **PAPER**
```buildoutcfg
1. Kilian Weinberger KILIAN, Anirban Dasgupta ANIRBAN, John Langford et.al. Feature Hashing for Large Scale Multitask Learning. Proc. ICML 2009.
2. Nedim ˇSrndi´c and Pavel Laskov. Detection of Malicious PDF Files Based on Hierarchical Document Structure. In Proceedings of the Network and Distributed System Security Symposium, NDSS 2013
3. 강아름, 정영섭, 김세령 외 3. 문서 구조 및 스트림 오브젝트 분석을 통한 문서형 악성코드 탐지, 한국컴퓨터정보학회 논문지 제23권 제11호(통권 제176호), 2018.11, 85-93 (9 pages)
4. NissimN,CohenA,EloviciY. ALDOCX: Detection of Unknown Malicious Microsoft Office Documents Using Designated Active Learning Methods Based on New Structural Feature Extraction Methodology. IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. 12, NO. 3, MARCH 2017
5. Edward Raff, Jon Barker, Jared Sylvester et.al. Malware Detection by Eating a Whole EXE. AAAI Publications, Workshops at the Thirty-Second AAAI Conference on Artificial Intelligence 2018
```
