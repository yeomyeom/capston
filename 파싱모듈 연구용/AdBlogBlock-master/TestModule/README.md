### README for Testcase Crawl module of AdBlogBlock 


##### Author : RE-A & yeomyeom(Parsing.py)
------------------
당신이 입력해야 할 곳은 Main.py의 맨 위 2군데입니다.


### searchWord = "입력할 검색어" (ex: "신림 미용실" ) 
### MAX_NUMBER_TO_SEARCH = 최대 검색할 수 (ex: 100) 


단, 이 수는 10단위여야 하고, 네이버는 검색 결과를 1000개까지만 제공하기 때문에 1000까지만 입력해야 합니다. 

즉 10~1000개가 대상입니다.


Main.py를 실행하면 **CrawlResult.txt** (크롤링한 URL이 저장된 파일)과 

**result.txt** (파싱된 텍스트가 저장)이 생성됩니다.

result.txt는 기존 파일 내용에 계속 덧붙여지는 형식으로 추가됩니다.

------------------------

**nounCount.py**는
맨 위의 open할 파일명만 바꿔주면 해당 파일의 한국어 어휘를 분석하여 TOP 100개의 어휘를 추려내줍니다.
결과는 **Statistic.txt**로 저장됩니다.





