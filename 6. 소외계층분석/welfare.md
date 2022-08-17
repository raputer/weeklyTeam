## 참조

- [OECD](https://data.oecd.org)
- [나무위키 검색ㅡ저소득층](https://namu.wiki/w/저소득층)
- [e-나라지표](https://www.index.go.kr/unify/idx-info.do?idxCd=8065)
</br></br>


## 필요 데이터

1. 고용율
2. 저소득층 소득변화
3. 소득지원정책
4. 사회적 지출
</br></br>


## 필수사항

- 해당 주제 관련 검색어 현황 WordCloud 사용
- 주제에 맞는 데이터베이스 설계
- 테이블 설계 쿼리 내용

---

### 1. 고용율 관련 데이터

1-1. 실업률 데이터

- 파일 : unemployment_rate.csv
- 출처 : [OECD Data](https://data.oecd.org)
- 사용의도 : Employment 데이터들은 1주일 30시간 미만 등 단시간 근로자 포함해서 단순 고용 여부를 지표화한 것들이 있어서 실업율 변화 데이터를 사용
- 참고 : Market Statistics Earnings Gross earnings: decile ratios Employment rates are sensitive to the economic cycle, but in the longer term they are significantly affected by governments' higher education and income support policies and by policies that facilitate employment of women and disadvantaged groups.

	고용률은 경기 순환에 민감하지만 장기적으로는 정부의 고등 교육 및 소득 지원 정책과 여성 및 취약 계층의 고용을 촉진하는 정책의 영향을 크게 받습니다.
</br></br>


### 2. 저소득층 소득변화 데이터 검색

2-1. 저임금 근로자 비율

- 파일 : 
- 출처 : [e-나라지표](https://www.index.go.kr/unify/idx-info.do?idxCd=8065)
- 저임금근로자 : 중위임금의 2/3에 미달하는 임금을 받는 근로자
	국제적으로 한국은 저임금근로자의 비율이 매우 높은 편에 속한다. 2020년 기준 한국의 저임금근로자비율(16.0%)은 비교대상 국가들 가운데 미국(23.8%)과 캐나다(18.7%) 보다는 낮으나, 일본(10.9%), 뉴질랜드(8.3%)등 보다는 높은 편이며, OECD 국가 평균(14.5%)보다 약간 높은 수준이다.[단위: %]

2-2. 저소득층 소득 변화 

- 파일 : global_income.csv
- 출처 : [OECD iLibrary Decile ratios of gross earnings 2021](https://doi.org/10.1787/data-00302-en)
- 카테고리 : Home  Statistics  OECD Employment and Labour
- 상근 부양 직원의 총 소득에 대한 소득 상위 십분위수 한도, 중위 소득의 2/3 미만을 버는 근로자의 총 부양 고용에서 차지하는 비중
</br></br>


### 3. 저소득층 지원 정책

네이버, 유튜브 등 저소득 지원 키워드 검색으로 WordCloud 분석 후 저소득 지원에 대해서 사람들에게 어떤 정보를 전달하고 있는지  

- 네이버는 검색 후 나오는 첫페이지의 컨텐츠들 헤드라인에 중점
- youtube는 '저소득층' 검색 후 나오는 올해 컨텐츠들 헤드라인, 조회수


__한국의 저소득층 지원 정책__

- 저소득 청년 월세 지원 정책
- 청년희망적금(소득 5천만원 이하 청년 자산형성 지원)

__해외 저소득층 지원 정책__
</br></br>


### 4. 사회적 지출

- 출처 : [OECD Data](https://data.oecd.org/socialexp/social-spending.htm)
- 사회적 지출은 현금 혜택, 재화와 서비스의 직접적인 현물 제공, 사회적 목적을 위한 세제 혜택으로 구성
- 혜택은 저소득 가구, 노인, 장애인, 병자, 실업자 또는 청년을 대상
- 1인당 GDP 또는 USD의 백분율로 측정
