# 우리 가족 추억 앨범

사진을 업로드하면 Google Cloud Vision API를 사용하여 이미지를 분석하고, 그에 맞는 추억을 되살리는 질문들을 생성하는 웹 애플리케이션입니다!

## 주요 기능

- 이미지 분석을 통한 장소, 시간, 계절, 날씨, 인원, 분위기 등 파악
- 분석된 내용을 바탕으로 맞춤형 질문 생성
- 답변 입력 및 JSON 형식으로 저장
- 감정 키워드 추출

## 설치 방법

1. Python 3.8 이상 설치

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. Google Cloud Vision API 설정:
   - [Google Cloud Console](https://console.cloud.google.com/)에서 새 프로젝트 생성
   - Vision API 활성화
   - 서비스 계정 생성 및 키 파일 다운로드
   - 다운로드 받은 키 파일을 `vision-api-key.json`으로 저장하여 프로젝트 루트 디렉토리에 위치

4. `secrets.json` 파일 생성:
```json
{
    "GOOGLE_APPLICATION_CREDENTIALS": "./vision-api-key.json"
}
```

## 실행 방법

```bash
streamlit run image_analyzer.py
```

## 파일 구조

- `image_analyzer.py`: 메인 애플리케이션 코드
- `styles.css`: 웹 페이지 스타일 정의
- `requirements.txt`: 필요한 패키지 목록
- `secrets.json`: API 키 설정 파일
- `vision-api-key.json`: Google Cloud Vision API 키 파일 (직접 생성 필요)

## 주의사항

- Google Cloud Vision API 키 파일(`vision-api-key.json`)은 보안을 위해 절대로 공유 금지!!
- API 사용량에 따라 비용이 발생할 수 있다.
- 이미지 분석 결과는 API의 성능에 따라 달라질 수 있다. 
