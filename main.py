import os
import requests
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ==================================
# Gemini API 설정
# ==================================
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Gemini 모델 설정
model = genai.GenerativeModel("gemini-2.0-flash")

# ==================================
# 검색 키워드
# ==================================
keywords = [
    "운영디자이너",
    "서비스디자이너",
    "UI UX 디자이너",
    "웹디자이너",
    "이커머스 디자이너",
    "프로모션 디자이너",
    "콘텐츠 디자이너",
    "디자인 PM",
    "커머스 디자인",
    "프리랜서 디자인 프로젝트"
]

# ==================================
# 대상 플랫폼
# ==================================
sites = [
    "잡코리아", "사람인", "원티드", "로켓펀치", 
    "리멤버", "링크드인", "크몽", "위시켓", 
    "프리모아", "숨고", "오투잡"
]

# ==================================
# 채용 정보 수집
# ==================================
def collect_jobs():
    jobs = []
    for keyword in keywords:
        search_url = f"https://www.google.com/search?q={keyword}+채용"
        try:
            response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
            result = response.text[:1000]
            jobs.append(f"검색 키워드: {keyword}\n검색 결과: {result}\n")
        except Exception as e:
            print(f"Error fetching {keyword}: {e}")
    return "\n".join(jobs)

# ==================================
# Gemini 분석
# ==================================
def analyze_jobs(data):
    prompt = f"""
너는 경력 디자이너 채용 분석 전문가이다.

지원자 정보:
- 디자인 경력 13년 이상
- 구축 프로젝트 경험 5년
- 운영디자인 경험 8년
- 이커머스 플랫폼 운영 경험
- 앱/Web 이벤트 디자인 경험
- 프로모션 디자인 경험
- 디자인 시스템 경험
- Figma 활용 가능
- Photoshop / Illustrator 활용
- 생성형 AI 활용 가능 (AI 이미지 생성, Adobe Firefly 활용)

지원자가 선호하는 직무:
높은 우선순위:
1. 운영디자이너
2. UX/UI 디자이너
3. 서비스 디자이너
4. 이커머스 디자이너
5. 프로모션 디자이너
6. 콘텐츠 디자이너
7. 디자인 PM
8. 커머스 브랜드 디지털 디자인

반드시 제외하거나 낮은 점수를 부여할 직무:
- 신입, 인턴, 단기 아르바이트, 3개월 이하 프로젝트
- 퍼블리셔 중심 업무
- 영상 편집 중심, 모션그래픽 중심, 촬영 중심
- 편집 디자인 중심 업무 (브로슈어, 카탈로그, 리플렛, 인쇄물, 출판, 패키지 등)

평가 기준:
1. 경력 적합도 (30점)
2. 이커머스 경험 활용 가능성 (25점)
3. 운영디자인 경험 활용 가능성 (20점)
4. AI 활용 역량 활용 가능성 (15점)
5. 근무 형태 적합성 (10점)

아래 형식으로 정리:
====================
⭐ 추천 점수 : 00점

회사 :
직무 :
고용 형태 :
근무 형태 :
주요 업무:

적합 이유:
- 

주의 사항:
-

지원 추천:
추천 / 보류 / 비추천
====================

채용 정보:
{data}
"""
    result = model.generate_content(prompt)
    return result.text

# ==================================
# Gmail 발송
# ==================================
def send_email(content):
    sender = os.environ["GMAIL_ID"]
    password = os.environ["GMAIL_PASSWORD"]
    
    message = MIMEText(content, "plain", "utf-8")
    message["Subject"] = f"[AI 디자인 채용 리포트] {datetime.now().strftime('%Y-%m-%d')}"
    message["From"] = sender
    message["To"] = sender
    
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(sender, password)
    smtp.send_message(message)
    smtp.quit()

# ==================================
# 실행
# ==================================
if __name__ == "__main__":
    jobs = collect_jobs()
    report = analyze_jobs(jobs)
    send_email(report)
    print("AI 채용 리포트 발송 완료")
