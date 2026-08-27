# AI Understanding Lab

`20260826_ai_understanding_system_ver2.pdf`의 인공지능 역사 내용을 바탕으로 만든 학생용 Streamlit 체험형 MVP입니다.

## 포함 기능

- 1950~1986년 / 1996~2023년의 16개 사건 타임라인
- 퍼셉트론 가중치·편향 조작 실험
- IF-THEN 기반 결정트리·추천 실험
- 탐색과 강화학습 생각 실험
- 트랜스포머 어텐션 개념 시각화
- ELIZA와 현대 LLM을 비교하는 질문 체험
- 5문항 마무리 퀴즈
- 원본 PDF 다운로드

## 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Solar API 연결

Solar 없이도 대화 모듈은 로컬 fallback으로 동작합니다. API를 연결하려면 PowerShell에서 다음처럼 실행합니다.

```powershell
$env:UPSTAGE_API_KEY="발급받은_API_키"
$env:SOLAR_MODEL="solar-pro4"
streamlit run app.py
```

배포 환경에서는 Streamlit secrets에 다음을 설정할 수 있습니다.

```toml
UPSTAGE_API_KEY = "..."
SOLAR_MODEL = "solar-pro4"
```

API 키는 코드나 Git 저장소에 직접 넣지 않습니다.
