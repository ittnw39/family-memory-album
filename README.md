# 우리 가족 추억 앨범 (테스트 프로젝트)

> ⚠️ **참고사항**: 이 프로젝트는 Google Cloud Vision API를 활용한 이미지 분석 및 질문 생성 기능을 테스트하기 위한 임시 프로젝트입니다. 향후 다른 프로젝트에서 사용될 AI 기능의 프로토타입으로 개발되었습니다 !

## 프로젝트 데모

### 1. 메인 화면 및 이미지 업로드
<div align="center">
  <img src="https://github.com/user-attachments/assets/d081faf3-7509-46b9-8c23-415fc71b0b95" alt="메인 화면 및 이미지 업로드 데모" width="800"/>
</div>

- 직관적인 사용자 인터페이스로 쉽게 이미지를 업로드할 수 있습니다.
- 드래그 앤 드롭 또는 파일 선택 버튼을 통해 이미지를 업로드할 수 있습니다.

### 2. 이미지 분석 및 질문 생성
<div align="center">
  <img src="https://github.com/user-attachments/assets/82fb3094-054f-4263-bedf-33cce7cfffa6" alt="이미지 분석 및 질문 생성 데모" width="800"/>
</div>

- Vision API를 통해 이미지의 다양한 특성을 자동으로 분석합니다:
  - 장소 및 환경 감지 (실내/실외, 특정 장소 등)
  - 시간대 및 계절 파악
  - 인물 수 및 표정 분석
  - 전반적인 분위기와 활동 파악
- 분석된 결과를 바탕으로 맞춤형 질문이 자동으로 생성됩니다:
  - 장소와 관련된 추억 질문
  - 함께한 사람들에 대한 질문
  - 특별한 순간을 회상하는 질문
  - 감정과 관련된 질문

### 3. 답변 저장 및 다운로드
<div align="center">
  <img src="https://github.com/user-attachments/assets/3e0c4d97-ca43-4ed9-a738-65615b8bb0b9" alt="답변 저장 데모" width="800"/>
</div>

- 각 질문에 대한 답변을 자유롭게 입력할 수 있습니다.
- 입력된 모든 답변과 분석 결과는 JSON 형식으로 저장됩니다.
- 저장된 데이터는 즉시 다운로드 가능합니다.

### 💾 저장 데이터 형식

> 아래는 실제 생성된 JSON 데이터의 예시입니다. 클릭하여 펼쳐보세요.

<details>
<summary><b>📥 JSON 데이터 구조 보기</b></summary>

<div style="height: 300px; overflow-y: auto; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">

```json
{
  "memory_id": "20250214_185038",
  "timestamp": "2025-02-14 18:50:38",
  "image_analysis": {
    "location": "실외",
    "time": "저녁",
    "season": "여름",
    "weather": "맑음",
    "people": "2명의 사람들",
    "mood": "평온한",
    "activity": "일상적인 활동",
    "special_elements": [
      "People",
      "Beach",
      "Body of water",
      "Shorts",
      "Summer"
    ]
  },
  "answers": {
    "질문_1": {
      "question": "바닷가에서 보낸 시간 중 가장 행복했던 순간은 언제였나요?",
      "answer": "맨발로 해변을 걷고 가족들과 불꽃놀이를 즐겼던 순간입니다."
    },
    "질문_2": {
      "question": "더운 여름날이었던 것 같은데, 이 날의 날씨나 분위기가 기억나시나요?",
      "answer": "매우 덥고 햇빛이 강했지만 바다에 들어가서 시원했습니다. 아이들이 굉장히 좋아했습니다."
    },
    "질문_3": {
      "question": "이 사진을 찍게 된 특별한 계기가 있으셨나요?",
      "answer": "아이와 아빠의 뒷모습이 너무 잘어울렸습니다."
    }
  },
  "keywords": {
    "RELATIONSHIPS": [
      "가족",
      "친구"
    ],
    "EMOTIONS": [
      "평온"
    ],
    "ACTIVITIES": [
      "People",
      "Beach",
      "Body of water"
    ],
    "MEMORIES": [
      "추억",
      "소중한 순간"
    ]
  }
}
```

</div>
</details>

## 프로젝트 개요

이 프로젝트는 다음과 같은 AI 기능들을 테스트하고 검증하기 위해 개발되었습니다!

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
- Google Cloud Vision API 키 파일(`vision-api-key.json`)은 보안을 위해 절대로 공유 금지 ! !
- API 사용량에 따라 비용이 발생할 수 있습니다.
- 이미지 분석 결과는 API의 성능에 따라 달라질 수 있습니다.

## 향후 계획

이 프로젝트에서 테스트된 기능들은 향후 다른 프로젝트에서 개선되어 활용될 예정입니다. 이 저장소는 참조용으로 유지됩니다 !
