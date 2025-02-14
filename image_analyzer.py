import streamlit as st
import json
import os
from PIL import Image
from google.cloud import vision
import io
from datetime import datetime
import base64

# API 키 설정
with open('./secrets.json') as f:
    secrets = json.loads(f.read())
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = secrets['GOOGLE_APPLICATION_CREDENTIALS']

def load_model():
    """Vision API 클라이언트를 초기화합니다."""
    client = vision.ImageAnnotatorClient()
    print("Vision API client loaded...")
    return client

def analyze_image(image):
    """이미지를 분석하여 기억을 되살리는 질문을 생성하는 함수"""
    try:
        # PIL Image를 bytes로 변환
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        content = img_byte_arr.getvalue()
        
        # Vision API 요청 생성
        image = vision.Image(content=content)
        
        # 이미지 분석 수행
        response = model.label_detection(image=image)
        labels = response.label_annotations
        
        face_response = model.face_detection(image=image)
        faces = face_response.face_annotations
        
        # 결과 분석 및 형식화
        result = {
            "image_analysis": {
                "location": "실내" if any("indoor" in label.description.lower() for label in labels) else "실외",
                "time": "낮" if any("daylight" in label.description.lower() for label in labels) else "저녁",
                "season": get_season_from_labels(labels),
                "weather": get_weather_from_labels(labels),
                "people": f"{len(faces)}명의 사람들",
                "mood": get_mood_from_faces(faces),
                "activity": get_activity_from_labels(labels),
                "special_elements": [label.description for label in labels[:5]]
            },
            "memory_questions": generate_questions(labels, faces),
            "emotional_keywords": {
                "RELATIONSHIPS": ["가족", "친구"] if len(faces) > 1 else ["개인"],
                "EMOTIONS": get_emotions_from_faces(faces),
                "ACTIVITIES": get_activities_from_labels(labels),
                "MEMORIES": ["추억", "소중한 순간"]
            }
        }
        
        return result
    except Exception as e:
        print(f"Error in analyze_image: {str(e)}")
        return None

def get_season_from_labels(labels):
    """라벨에서 계절 정보를 추출"""
    season_keywords = {
        "봄": ["spring", "flower", "cherry blossom"],
        "여름": ["summer", "beach", "swimming"],
        "가을": ["autumn", "fall", "maple"],
        "겨울": ["winter", "snow", "christmas"]
    }
    
    for season, keywords in season_keywords.items():
        if any(any(keyword in label.description.lower() for keyword in keywords) for label in labels):
            return season
    return "알 수 없음"

def get_weather_from_labels(labels):
    """라벨에서 날씨 정보를 추출"""
    weather_keywords = {
        "맑음": ["sunny", "clear sky"],
        "흐림": ["cloudy", "overcast"],
        "비": ["rain", "rainy"],
        "눈": ["snow", "snowy"]
    }
    
    for weather, keywords in weather_keywords.items():
        if any(any(keyword in label.description.lower() for keyword in keywords) for label in labels):
            return weather
    return "맑음"

def get_mood_from_faces(faces):
    """얼굴 표정에서 분위기를 추출"""
    if not faces:
        return "알 수 없음"
    
    joy_count = sum(1 for face in faces if face.joy_likelihood >= 3)
    if joy_count > len(faces) / 2:
        return "즐거운"
    return "평온한"

def get_activity_from_labels(labels):
    """라벨에서 활동 정보를 추출"""
    activities = {
        "식사": ["food", "eating", "dining"],
        "산책": ["walking", "park", "outdoor"],
        "여행": ["travel", "tourist", "sightseeing"],
        "모임": ["gathering", "party", "celebration"]
    }
    
    for activity, keywords in activities.items():
        if any(any(keyword in label.description.lower() for keyword in keywords) for label in labels):
            return activity
    return "일상적인 활동"

def get_emotions_from_faces(faces):
    """얼굴 표정에서 감정을 추출"""
    emotions = []
    for face in faces:
        if face.joy_likelihood >= 3:
            emotions.append("기쁨")
        if face.sorrow_likelihood >= 3:
            emotions.append("슬픔")
        if face.anger_likelihood >= 3:
            emotions.append("화남")
        if face.surprise_likelihood >= 3:
            emotions.append("놀람")
    
    return list(set(emotions)) if emotions else ["평온"]

def get_activities_from_labels(labels):
    """라벨에서 활동 키워드를 추출"""
    return [label.description for label in labels if label.score > 0.8][:3]

def generate_questions(labels, faces):
    """분석 결과를 바탕으로 구체적인 질문 생성"""
    questions = []
    
    # 라벨에서 주요 키워드 추출
    keywords = [label.description.lower() for label in labels if label.score > 0.7]
    
    # 장소/환경 관련 질문
    location_keywords = [k for k in keywords if any(word in k for word in ['room', 'park', 'restaurant', 'beach', 'garden', 'house', 'building'])]
    if location_keywords:
        location = location_keywords[0]
        if 'restaurant' in location:
            questions.append(f"이 식당에서 특별히 기억에 남는 음식이나 대화가 있으셨나요?")
        elif 'park' in location or 'garden' in location:
            questions.append(f"이 {location}에서 가족들과 어떤 추억을 만드셨나요?")
        elif 'beach' in location:
            questions.append("바닷가에서 보낸 시간 중 가장 행복했던 순간은 언제였나요?")
        elif 'house' in location or 'room' in location:
            questions.append("이 공간에서 가족들과 나눈 특별한 이야기나 순간이 있으신가요?")

    # 활동 관련 질문
    activity_keywords = [k for k in keywords if any(word in k for word in ['eating', 'playing', 'walking', 'sitting', 'standing', 'celebration', 'party', 'travel'])]
    if activity_keywords:
        activity = activity_keywords[0]
        if 'eating' in activity:
            questions.append("이 날 먹은 음식에 대한 특별한 기억이 있으신가요?")
        elif 'celebration' in activity or 'party' in activity:
            questions.append("이 날 무슨 특별한 행사나 기념일이었나요?")
        elif 'travel' in activity:
            questions.append("이 여행을 계획하게 된 특별한 계기가 있으셨나요?")

    # 감정/표정 관련 질문
    if faces:
        joy_faces = sum(1 for face in faces if face.joy_likelihood >= 3)
        if joy_faces > 0:
            questions.append("모두가 이렇게 환하게 웃고 있는 순간에 어떤 일이 있었나요?")
        if len(faces) > 2:
            questions.append("사진 속 사람들과는 어떤 관계이신가요? 그들과의 특별한 추억이 있다면 들려주세요.")

    # 계절/날씨 관련 질문
    season_keywords = [k for k in keywords if any(word in k for word in ['summer', 'winter', 'spring', 'autumn', 'snow', 'sunny', 'rain'])]
    if season_keywords:
        season = season_keywords[0]
        if 'summer' in season:
            questions.append("더운 여름날이었던 것 같은데, 이 날의 날씨나 분위기가 기억나시나요?")
        elif 'winter' in season or 'snow' in season:
            questions.append("추운 겨울이었을 텐데, 이 날 특별히 기억에 남는 순간이 있으신가요?")
        elif 'spring' in season:
            questions.append("봄날의 따뜻한 기운이 느껴지는데, 이 때의 특별한 기억이 있으신가요?")

    # 물건/소품 관련 질문
    object_keywords = [k for k in keywords if any(word in k for word in ['camera', 'book', 'food', 'toy', 'gift', 'cake'])]
    if object_keywords:
        object_name = object_keywords[0]
        questions.append(f"사진 속에 보이는 {object_name}에 얽힌 이야기가 있으신가요?")

    # 최소 3개의 질문 보장
    if len(questions) < 3:
        default_questions = [
            "이 사진을 찍게 된 특별한 계기가 있으셨나요?",
            "이 순간을 다시 떠올리시면 어떤 감정이 드시나요?",
            "이 사진에서 가장 소중하게 느끼시는 부분은 무엇인가요?"
        ]
        questions.extend(default_questions[:3 - len(questions)])

    # 최대 4개의 질문으로 제한
    return questions[:4]

def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_file, encoding='utf-8') as f:
        st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """바이너리 파일을 다운로드할 수 있는 HTML 링크를 생성합니다."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">📥 {file_label}</a>'
    return href

def main():
    load_css()

    # 메인 컨테이너
    with st.container():
        # 헤더 섹션
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("""
                <div class="title-container">
                    <span class="emoji-decoration">👨‍👩‍👧‍👦</span>
                    <span class="main-title">우리 가족 추억 앨범</span>
                    <span class="emoji-decoration">💝</span>
                    <div class="sub-title">
                        사진으로 되살리는 소중한 기억
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # 세션 상태 초기화
    if 'memory_data' not in st.session_state:
        st.session_state.memory_data = {}
    if 'current_answers' not in st.session_state:
        st.session_state.current_answers = {}
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    
    # 이미지 업로드 섹션
    uploaded_file = st.file_uploader("가족 사진을 업로드해주세요", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # 이미지 표시
        image = Image.open(uploaded_file)
        st.image(image, caption='소중한 추억이 담긴 사진', use_container_width=True)
        
        # 분석 버튼
        if st.button("추억 분석하기") or st.session_state.analysis_result is not None:
            if st.session_state.analysis_result is None:
                with st.spinner('사진 속 이야기를 분석하고 있습니다...'):
                    result = analyze_image(image)
                    if result:
                        st.session_state.analysis_result = result
                        st.session_state.current_answers = {}  # 새로운 분석시 답변 초기화
            
            result = st.session_state.analysis_result
            if result:
                # 현재 시간을 기준으로 고유 ID 생성
                memory_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # 분석 결과 표시
                with st.expander("📸 사진 속 이야기", expanded=True):
                    analysis = result['image_analysis']
                    st.write("📍 장소:", analysis['location'])
                    st.write("🕒 시간:", analysis['time'])
                    st.write("🌸 계절:", analysis['season'])
                    st.write("☀️ 날씨:", analysis['weather'])
                    st.write("👨‍👩‍👧‍👦 함께한 사람들:", analysis['people'])
                    st.write("💕 분위기:", analysis['mood'])
                    st.write("🎈 활동:", analysis['activity'])
                    st.write("✨ 특별한 요소들:", ", ".join(analysis['special_elements']))
                
                # 감정 키워드 표시
                with st.expander("💝 이 사진의 키워드", expanded=True):
                    keywords = result['emotional_keywords']
                    st.write("가족관계:", ", ".join(keywords['RELATIONSHIPS']))
                    st.write("감정:", ", ".join(keywords['EMOTIONS']))
                    st.write("활동:", ", ".join(keywords['ACTIVITIES']))
                    st.write("추억:", ", ".join(keywords['MEMORIES']))
                
                # 추억 질문 표시 및 답변 입력
                st.markdown("### 💭 추억을 되살리는 질문")
                
                # 답변 입력 및 저장
                for i, question in enumerate(result['memory_questions'], 1):
                    st.info(f"{i}. {question}")
                    key = f"answer_{i}"
                    if key not in st.session_state.current_answers:
                        st.session_state.current_answers[key] = ""
                    
                    answer = st.text_area(
                        f"답변 {i}",
                        value=st.session_state.current_answers[key],
                        key=key,
                        height=100,
                        on_change=update_answer,
                        args=(key,)
                    )
                
                # 모든 답변이 입력되었는지 확인
                all_answered = all(len(st.session_state.current_answers.get(f"answer_{i}", "").strip()) > 0 
                                 for i in range(1, len(result['memory_questions']) + 1))
                
                # 답변 저장 버튼
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    if st.button("답변 저장하기", disabled=not all_answered, use_container_width=True):
                        if all_answered:
                            # 답변 데이터 구성
                            answers = {}
                            for i, question in enumerate(result['memory_questions'], 1):
                                answers[f"질문_{i}"] = {
                                    "question": question,
                                    "answer": st.session_state.current_answers[f"answer_{i}"]
                                }
                            
                            # 메모리 데이터 구성
                            memory_data = {
                                "memory_id": memory_id,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "image_analysis": result['image_analysis'],
                                "answers": answers,
                                "keywords": result['emotional_keywords']
                            }
                            
                            # JSON 파일로 저장
                            json_filename = f"memory_{memory_id}.json"
                            with open(json_filename, 'w', encoding='utf-8') as f:
                                json.dump(memory_data, f, ensure_ascii=False, indent=2)
                            
                            # 다운로드 링크 생성
                            st.markdown(
                                f'<div style="text-align: center;">{get_binary_file_downloader_html(json_filename, "추억 데이터 다운로드")}</div>', 
                                unsafe_allow_html=True
                            )
                            
                            # 임시 파일 삭제
                            os.remove(json_filename)
                            
                            st.success("답변이 성공적으로 저장되었습니다!")
                        else:
                            st.warning("모든 질문에 답변을 입력해주세요.")
            else:
                st.error("사진 분석 중 오류가 발생했습니다. 다시 시도해주세요.")

def update_answer(key):
    """텍스트 영역의 값이 변경될 때 호출되는 콜백 함수"""
    st.session_state.current_answers[key] = st.session_state[key]

# 전역변수 초기화 및 실행
model = load_model()

if __name__ == "__main__":
    main() 