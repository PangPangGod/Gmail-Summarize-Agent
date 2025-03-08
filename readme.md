### Idea
GMAIL을 이용한 Multiple Agent side project
1. Gmail Agent를 통한 내용 검색(Langchain Gmail Toolkit 이용 -> 특정 내용 Query, Filtering)
2. 파싱을 통해 가져온 내용 Prettify(*request를 통해 내용 요약하기)
3. 가져온 내용을 BS4를 통해서 Parsing, url 추출 후 요약
4. 추출한 내용을 문서화 후 저장

### Todo
1. 구현(성공)
2. 생성한 내용 특정 형식으로 저장
3. 해당 내용들 자동으로 특정 시간마다 실행(.bat), Posting 혹은 파일 저장 후 git 혹은 blog에 올리기.
4. .bat file 실행 테스트해서 동작하게 만들기(.md)

---

### ChangLog
**25/03/08**  
- Update Packages with uv