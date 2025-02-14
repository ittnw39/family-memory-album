# 우리 가족 추억 앨범 (테스트 프로젝트)

> ⚠️ **참고사항**: 이 프로젝트는 Google Cloud Vision API를 활용한 이미지 분석 및 질문 생성 기능을 테스트하기 위한 임시 프로젝트입니다. 향후 다른 프로젝트에서 사용될 AI 기능의 프로토타입으로 개발되었습니다.

## 프로젝트 개요

이 프로젝트는 다음과 같은 AI 기능들을 테스트하고 검증하기 위해 개발되었습니다:
- Google Cloud Vision API를 통한 이미지 분석
- 분석된 데이터를 기반으로 한 맥락 기반 질문 생성
- 사용자 응답 데이터의 JSON 형식 저장 및 관리
- Streamlit을 활용한 웹 인터페이스 구현

## 테스트 가능한 기능

- 이미지 분석을 통한 장소, 시간, 계절, 날씨, 인원, 분위기 등 파악
- 분석된 내용을 바탕으로 맞춤형 질문 생성
- 답변 입력 및 JSON 형식으로 저장
- 감정 키워드 추출

## 설치 방법

1. Python 3.8 이상이 설치되어 있어야 합니다.

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

- 이 프로젝트는 테스트 목적으로 개발되었으며, 프로덕션 환경에서의 사용은 권장되지 않습니다.
- Google Cloud Vision API 키 파일(`vision-api-key.json`)은 보안을 위해 절대로 공유하지 마세요.
- API 사용량에 따라 비용이 발생할 수 있습니다.
- 이미지 분석 결과는 API의 성능에 따라 달라질 수 있습니다.

## 향후 계획

이 프로젝트에서 테스트된 기능들은 향후 다른 프로젝트에서 개선되어 활용될 예정입니다. 이 저장소는 참조용으로 유지됩니다. 
