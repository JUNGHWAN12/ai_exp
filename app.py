from __future__ import annotations

import math
import os
import random
from pathlib import Path
from typing import Any

import requests
import streamlit as st

PDF_PATH = Path(__file__).with_name("20260826_ai_understanding_system_ver2.pdf")

st.set_page_config(page_title="AI Understanding Lab", page_icon="🧭", layout="wide", initial_sidebar_state="expanded")

EVENTS: list[dict[str, Any]] = [
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1950,"title":"튜링 테스트","english":"Turing Test","maker":"앨런 튜링","tags":["철학","대화","평가"],"summary":"대화만으로 상대가 사람인지 기계인지 구별할 수 없다면 기계에 지능이 있다고 볼 수 있다는 기준입니다.","meaning":"AI의 성능을 어떻게 판단할 것인가라는 질문을 던졌습니다.","lab":"solar"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1956,"title":"인공지능이라는 이름","english":"Dartmouth Conference","maker":"존 매카시 등","tags":["학문","출발"],"summary":"다트머스 회의에서 Artificial Intelligence라는 용어가 제안되며 독립된 학문 분야로 출범했습니다.","meaning":"서로 다른 연구를 하나의 문제의식 아래 연결했습니다.","lab":"overview"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1958,"title":"퍼셉트론","english":"Perceptron","maker":"프랭크 로젠블랫","tags":["신경망","분류","학습"],"summary":"입력값에 가중치를 적용해 두 범주를 나누는 인공 뉴런의 초기 모델입니다.","meaning":"오늘날 딥러닝의 가장 단순한 뼈대를 직접 계산해 볼 수 있습니다.","lab":"perceptron"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1966,"title":"ELIZA","english":"ELIZA","maker":"조셉 바이젠바움, MIT","tags":["챗봇","패턴 매칭"],"summary":"정해진 패턴과 규칙으로 심리 상담사를 흉내 낸 초기 대화형 프로그램입니다.","meaning":"대화의 자연스러움과 실제 이해는 서로 다를 수 있음을 보여줍니다.","lab":"solar"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1969,"title":"쉐이키","english":"Shakey","maker":"스탠퍼드 연구소","tags":["로봇","계획","센서"],"summary":"센서로 주변을 인식하고 경로를 계획해 움직인 초기 모바일 지능형 로봇입니다.","meaning":"인식·계획·행동을 연결하는 지능 에이전트의 원형입니다.","lab":"overview"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1972,"title":"MYCIN","english":"MYCIN","maker":"스탠퍼드 대학 의대","tags":["전문가 시스템","IF-THEN"],"summary":"의학 규칙을 바탕으로 감염성 질환을 진단하고 항생제를 추천한 규칙 기반 시스템입니다.","meaning":"규칙을 명시하면 특정 영역의 추론을 자동화할 수 있었습니다.","lab":"tree"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1980,"title":"결정트리 ID3","english":"Decision Tree / ID3","maker":"로스 퀸란","tags":["분류","데이터","규칙"],"summary":"데이터의 정보 획득량을 계산해 의사결정 규칙을 나무 구조로 학습합니다.","meaning":"모델이 왜 그런 결정을 했는지 사람이 읽을 수 있는 화이트박스 접근입니다.","lab":"tree"},
    {"phase":"기초를 만든 시대","period":"1950 — 1986","year":1986,"title":"역전파 알고리즘","english":"Backpropagation","maker":"힌턴·럼멜하트 등","tags":["학습","오차","다층 신경망"],"summary":"출력 오차를 뒤쪽에서 앞쪽으로 전달해 여러 층의 가중치를 수정하는 학습법입니다.","meaning":"다층 신경망을 실제로 학습시킬 수 있게 해 AI의 부활을 이끌었습니다.","lab":"backprop"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":1996,"title":"BookMatch","english":"Personalized Recommendation","maker":"아마존","tags":["추천","개인화","상용화"],"summary":"구매·평가 데이터를 분석해 고객 취향에 맞는 책을 추천하는 대규모 상용 시스템입니다.","meaning":"AI가 연구실을 넘어 일상 서비스의 의사결정에 들어온 사례입니다.","lab":"tree"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":1997,"title":"IBM 딥블루","english":"Deep Blue","maker":"IBM","tags":["탐색","체스","계산"],"summary":"고성능 병렬 컴퓨터와 탐색 알고리즘으로 체스 세계 챔피언을 이겼습니다.","meaning":"특정 문제에서 계산 능력과 탐색 전략이 인간을 넘어설 수 있음을 보였습니다.","lab":"search"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":2006,"title":"딥러닝","english":"Deep Learning","maker":"제프리 힌턴","tags":["DNN","표현 학습","GPU"],"summary":"깊은 신경망을 효과적으로 사전 학습하는 방법이 발전하며 현대 AI 혁명의 기반이 마련됐습니다.","meaning":"데이터와 컴퓨팅 파워가 결합해 학습 규모를 크게 확장했습니다.","lab":"deep_learning"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":2011,"title":"IBM 왓슨","english":"Watson","maker":"IBM","tags":["질의응답","자연어","추론"],"summary":"자연어 질문을 분석하고 지식에서 답을 찾아 퀴즈 쇼에서 우승한 시스템입니다.","meaning":"AI가 자연어의 의미를 다루는 방향으로 확장됐습니다.","lab":"solar"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":2014,"title":"GAN과 Alexa","english":"GAN & Voice Assistant","maker":"이안 굿펠로우·아마존","tags":["생성","음성","에이전트"],"summary":"GAN은 새로운 이미지를 생성하고, Alexa는 음성 기반 AI 비서를 대중화했습니다.","meaning":"AI가 분류·예측을 넘어 콘텐츠 생성과 상호작용으로 이동했습니다.","lab":"solar"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":2016,"title":"알파고","english":"AlphaGo","maker":"Google DeepMind·이세돌","tags":["강화학습","바둑","MCTS"],"summary":"딥러닝과 몬테카를로 트리 탐색으로 바둑에서 인간 최고 수준의 직관을 넘어섰습니다.","meaning":"환경과 상호작용하며 좋은 행동을 찾는 강화학습의 가능성을 보여줬습니다.","lab":"search"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":2017,"title":"트랜스포머","english":"Transformer","maker":"Google Research","tags":["Attention","병렬 학습","LLM"],"summary":"어텐션으로 문맥 속 단어의 관계를 학습해 BERT·GPT 등 대규모 언어 모델의 기반이 됐습니다.","meaning":"현재의 생성형 AI를 가능하게 한 핵심 구조입니다.","lab":"attention"},
    {"phase":"확장과 대중화의 시대","period":"1996 — 2023","year":2023,"title":"GPT-4 멀티모달","english":"Multimodal Generative AI","maker":"OpenAI 등","tags":["생성형 AI","텍스트","이미지","음성"],"summary":"텍스트를 넘어 이미지와 음성까지 이해하는 멀티모달 AI가 산업 전반으로 확산됐습니다.","meaning":"AI를 특정 기능이 아니라 자연어로 사용하는 범용 인터페이스로 바꿨습니다.","lab":"solar"},
]

QUIZ = [
    ("1958년 퍼셉트론의 핵심 역할은 무엇인가요?", ["이진 분류", "음성 합성", "이미지 생성", "경로 계획"], 0, "입력에 가중치를 적용해 두 범주를 나누는 초기 인공 뉴런입니다."),
    ("ELIZA는 어떤 방식으로 대화했나요?", ["대규모 사전학습", "패턴 매칭 규칙", "강화학습", "몬테카를로 탐색"], 1, "ELIZA는 정해진 패턴과 규칙으로 상담 대화를 흉내 냈습니다."),
    ("알파고에 사용된 핵심 조합은 무엇인가요?", ["결정트리와 GAN", "역전파와 ID3", "딥러닝과 MCTS", "퍼셉트론과 음성인식"], 2, "알파고는 딥러닝과 몬테카를로 트리 탐색을 함께 사용했습니다."),
    ("트랜스포머의 핵심 메커니즘은 무엇인가요?", ["Attention", "IF-THEN", "센서", "구매 이력"], 0, "어텐션은 문맥 안 단어 간 관계를 계산하는 핵심 장치입니다."),
    ("PDF가 제시하는 AI 발전의 세 가지 동력은 무엇인가요?", ["데이터·GPU·신경망 모델", "로봇·카메라·마이크", "규칙·책·체스", "검색·광고·음성"], 0, "자료는 데이터, 컴퓨팅 파워(GPU), 혁신적 신경망 모델의 결합을 강조합니다."),
]

LAB_LABELS = {
    "perceptron": "퍼셉트론",
    "backprop": "역전파",
    "deep_learning": "딥러닝",
    "tree": "결정트리·추천",
    "search": "탐색과 강화학습",
    "attention": "트랜스포머 어텐션",
    "solar": "ELIZA ↔ Solar 대화",
}

def inject_css() -> None:
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --ink:#152238; --muted:#607089; --blue:#3b82f6; --mint:#42d3b2; --paper:#f7f9fc; }
    .stApp { background: radial-gradient(circle at 90% 0%, #e8f0ff 0, transparent 32%), var(--paper); color:var(--ink); }
    html, body, [class*="css"] { font-family:'Gowun Dodum', sans-serif; }
    h1,h2,h3 { font-family:'Space Grotesk','Gowun Dodum',sans-serif; letter-spacing:-.04em; }
    .hero { padding:3.4rem 0 2.4rem; } .eyebrow { color:var(--blue); font-family:'Space Grotesk'; font-weight:700; letter-spacing:.14em; font-size:.78rem; }
    .hero h1 { font-size:clamp(2.6rem, 6vw, 5.4rem); line-height:1; margin:.7rem 0 1.1rem; max-width:780px; }
    .hero p { color:var(--muted); font-size:1.15rem; max-width:690px; line-height:1.75; }
    .card { background:rgba(255,255,255,.82); border:1px solid #e4eaf3; border-radius:24px; padding:1.25rem 1.35rem; min-height:170px; box-shadow:0 15px 45px rgba(39,64,99,.06); }
    .card .year { font-family:'Space Grotesk'; color:var(--blue); font-weight:700; } .card h3 { margin:.55rem 0; font-size:1.35rem; } .card p { color:var(--muted); line-height:1.65; }
    .pill { display:inline-block; background:#eef4ff; color:#3266c0; border-radius:999px; padding:.24rem .6rem; margin:.12rem .18rem .12rem 0; font-size:.78rem; }
    .quote { border-left:4px solid var(--mint); background:#effcf8; border-radius:0 16px 16px 0; padding:1rem 1.2rem; color:#315d56; line-height:1.7; }
    .metric { background:#fff; border:1px solid #e7edf5; border-radius:18px; padding:1rem; } .metric strong { display:block; font:700 2rem 'Space Grotesk'; color:var(--ink); }
    .timeline-line { border-left:2px solid #cfe0ff; padding-left:1.4rem; margin:1rem 0; } .small { color:var(--muted); font-size:.9rem; }
    .loss-chart { background:#fff; border:1px solid #e7edf5; border-radius:18px; padding:1rem; margin:1rem 0; }
    .result-table { width:100%; border-collapse:collapse; background:#fff; border:1px solid #e7edf5; border-radius:14px; overflow:hidden; margin:1rem 0; }
    .result-table th, .result-table td { padding:.7rem .85rem; border-bottom:1px solid #edf1f6; text-align:left; }
    .result-table th { color:var(--muted); font-size:.85rem; background:#f8fafc; }
    </style>""", unsafe_allow_html=True)

def call_solar(messages: list[dict[str, str]]) -> str | None:
    api_key = st.secrets.get("UPSTAGE_API_KEY", os.getenv("UPSTAGE_API_KEY", ""))
    if not api_key:
        return None
    model = st.secrets.get("SOLAR_MODEL", os.getenv("SOLAR_MODEL", "solar-pro4"))
    try:
        response = requests.post("https://api.upstage.ai/v1/chat/completions", headers={"Authorization":f"Bearer {api_key}", "Content-Type":"application/json"}, json={"model":model,"messages":messages,"temperature":0.7,"max_tokens":500}, timeout=35)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except (requests.RequestException, KeyError, IndexError, TypeError) as exc:
        st.warning(f"Solar API에 연결하지 못해 체험용 답변으로 전환했습니다: {exc}")
        return None

def local_tutor(prompt: str) -> str:
    text = prompt.lower()
    if text.strip() in ["ㅇㅇ", "응", "네", "좋아", "알겠어"]:
        return "좋아요. 이번에는 ‘ELIZA와 Solar는 무엇이 다를까?’ 또는 ‘AI는 오늘날 어디에 쓰일까?’라고 질문해 보세요. 질문을 조금 구체적으로 만들수록 더 좋은 답을 얻을 수 있습니다."
    if any(word in text for word in ["eliza", "엘리자"]):
        return "ELIZA는 1966년에 만들어진 초기 챗봇입니다. 사용자의 문장에서 특정 단어나 패턴을 찾은 뒤, 미리 정해 둔 문장 틀에 끼워 넣어 상담사처럼 답했습니다. 그래서 대화하는 느낌은 줄 수 있었지만, 문장의 의미를 실제로 이해한 것은 아니었습니다."
    if any(word in text for word in ["오늘날", "어디에", "활용", "사용", "쓰일", "쓰여"]):
        return "오늘날 AI는 검색·추천, 번역·음성 비서, 문서 요약, 이미지·음악 생성, 질의응답 등에 활용됩니다. 공통점은 많은 데이터에서 패턴을 찾아 사람의 판단이나 창작을 돕는다는 것입니다. 다만 결과가 항상 사실인 것은 아니므로 중요한 내용은 사람이 확인해야 합니다."
    if any(word in text for word in ["차이", "비교", "다른"]):
        return "ELIZA는 정해진 패턴을 찾아 답하는 규칙 기반 챗봇이고, Solar 같은 현대 LLM은 대규모 데이터에서 학습한 언어 패턴과 대화 맥락을 바탕으로 답을 생성합니다. 따라서 Solar가 훨씬 다양한 표현에 대응하지만, 그 답이 항상 정확하다는 뜻은 아닙니다."
    if any(word in text for word in ["튜링", "turing", "생각"]):
        return "튜링 테스트는 대화 상대가 사람인지 기계인지 판별하기 어려운 상황을 지능의 기준으로 삼자는 제안입니다. 다만 대화를 잘하는 것과 실제로 이해하는 것은 같은 의미가 아닐 수 있어요."
    if any(word in text for word in ["퍼셉트론", "perceptron", "가중치"]):
        return "퍼셉트론은 입력값에 가중치를 곱하고 모두 더한 뒤 임계값과 비교해 분류합니다. 아주 단순하지만 신경망의 핵심 아이디어를 계산으로 볼 수 있습니다."
    if any(word in text for word in ["트랜스포머", "attention", "어텐션", "llm"]):
        return "트랜스포머는 문장 안에서 어떤 단어가 다른 단어와 관련 있는지 어텐션으로 계산합니다. 이 구조 덕분에 긴 문맥을 병렬로 처리하는 대규모 언어 모델이 발전했습니다."
    if any(word in text for word in ["알파고", "강화학습", "바둑"]):
        return "알파고는 현재 상태에서 좋은 수를 찾는 과정에 딥러닝과 몬테카를로 트리 탐색을 결합했습니다. 많은 상황에서 어떤 선택이 유리한지 학습한 것이 핵심입니다."
    return "좋은 질문이에요. 사건 하나를 골라 ‘어떤 데이터가 필요했을까?’, ‘사람과 무엇이 달랐을까?’, ‘오늘날 어디에 쓰일까?’를 이어서 질문해 보세요."

def render_home() -> None:
    st.markdown('<div class="hero"><div class="eyebrow">AI UNDERSTANDING LAB · 1950—2023</div><h1>AI는 어떻게<br>여기까지 왔을까?</h1><p>튜링 테스트부터 멀티모달 생성형 AI까지. 역사를 읽고, 원리를 만지고, 직접 질문하며 인공지능의 흐름을 탐험해 보세요.</p></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, number, label in zip(cols, ["16", "2", "5"], ["역사적 사건", "시대별 학습 경로", "직접 풀어보는 퀴즈"]):
        with col: st.markdown(f'<div class="metric"><strong>{number}</strong><span class="small">{label}</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True); st.subheader("두 번의 도약")
    left, right = st.columns(2)
    with left: st.markdown('<div class="card"><div class="year">1950 — 1986</div><h3>기초를 만든 시대</h3><p>지능을 정의하고, 규칙·신경망·전문가 시스템으로 기계가 판단하는 방법을 실험했습니다.</p><span class="pill">튜링 테스트</span><span class="pill">퍼셉트론</span><span class="pill">ELIZA</span><span class="pill">역전파</span></div>', unsafe_allow_html=True)
    with right: st.markdown('<div class="card"><div class="year">1996 — 2023</div><h3>확장과 대중화의 시대</h3><p>데이터와 GPU, 트랜스포머가 만나 AI가 게임·추천·언어·이미지·음성의 도구가 되었습니다.</p><span class="pill">딥블루</span><span class="pill">알파고</span><span class="pill">트랜스포머</span><span class="pill">멀티모달</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True); st.markdown('<div class="quote">역사적 교훈 · AI의 폭발적 발전은 데이터, 컴퓨팅 파워(GPU), 그리고 혁신적인 신경망 모델의 결합에서 시작되었습니다.</div>', unsafe_allow_html=True); st.markdown("<br>", unsafe_allow_html=True)
    st.info("왼쪽 메뉴에서 ‘타임라인’을 먼저 둘러본 뒤 ‘체험실’에서 원리를 직접 조작해 보세요.")

def render_timeline() -> None:
    st.title("AI 타임라인"); st.caption("자료의 두 페이지를 두 개의 학습 구간으로 재구성했습니다. 사건을 선택하면 핵심 개념과 체험 연결점을 확인할 수 있습니다.")
    phase = st.radio("학습 구간", ["기초를 만든 시대", "확장과 대중화의 시대"], horizontal=True)
    events = [event for event in EVENTS if event["phase"] == phase]
    selected_title = st.selectbox("사건 선택", [f'{e["year"]} · {e["title"]}' for e in events]); selected = next(e for e in events if f'{e["year"]} · {e["title"]}' == selected_title)
    tag_html = "".join(f"<span class='pill'>{tag}</span>" for tag in selected["tags"])
    st.markdown(f'<div class="card"><div class="year">{selected["year"]} · {selected["english"]}</div><h2>{selected["title"]}</h2><p><b>{selected["maker"]}</b></p><p>{selected["summary"]}</p><div>{tag_html}</div></div>', unsafe_allow_html=True); st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="quote"><b>왜 중요할까요?</b><br>{selected["meaning"]}</div>', unsafe_allow_html=True)
    if selected["lab"] != "overview": st.success(f"체험 연결: 체험실의 ‘{LAB_LABELS.get(selected['lab'], selected['lab'])}’ 모듈에서 이 아이디어를 직접 확인해 보세요.")
    st.subheader("전체 흐름"); timeline = "".join(f'<p><b>{e["year"]}</b>　{e["title"]} <span class="small">— {e["english"]}</span></p>' for e in events); st.markdown(f'<div class="timeline-line">{timeline}</div>', unsafe_allow_html=True)

def render_perceptron() -> None:
    st.subheader("① 퍼셉트론 실험"); st.caption("입력 × 가중치의 합이 임계값을 넘는지에 따라 0 또는 1을 출력합니다.")
    a,b,c = st.columns(3)
    with a: x1=st.slider("입력 x₁",-2.0,2.0,1.0,0.1); w1=st.slider("가중치 w₁",-2.0,2.0,0.8,0.1)
    with b: x2=st.slider("입력 x₂",-2.0,2.0,1.0,0.1); w2=st.slider("가중치 w₂",-2.0,2.0,0.8,0.1)
    with c: bias=st.slider("편향 b",-2.0,2.0,-0.5,0.1); threshold=st.slider("임계값",-2.0,2.0,0.0,0.1)
    score=x1*w1+x2*w2+bias; output=int(score>=threshold); st.metric("계산 결과",f"{output} (score = {score:.2f})","1 = 활성화" if output else "0 = 비활성화")
    st.code(f"{x1:.1f} × {w1:.1f} + {x2:.1f} × {w2:.1f} + {bias:.1f} = {score:.2f}\n{score:.2f} >= {threshold:.2f} → {output}"); st.info("가중치는 각 입력을 얼마나 중요하게 볼지 조절합니다. 가중치와 편향을 바꾸면서 AND/OR 같은 규칙을 만들어 보세요.")

def render_loss_chart(losses: list[float]) -> None:
    if not losses:
        return
    chart_width, chart_height = 720, 180
    minimum, maximum = min(losses), max(losses)
    spread = maximum - minimum or 1.0
    points = " ".join(
        f"{index * chart_width / max(1, len(losses) - 1):.1f},{chart_height - ((loss - minimum) / spread) * (chart_height - 20) - 10:.1f}"
        for index, loss in enumerate(losses)
    )
    st.markdown(
        f'<div class="loss-chart"><div class="small">학습 손실 변화</div><svg viewBox="0 0 {chart_width} {chart_height + 20}" width="100%" height="180" role="img" aria-label="학습 손실 그래프"><line x1="0" y1="{chart_height}" x2="{chart_width}" y2="{chart_height}" stroke="#dbe4f0"/><polyline points="{points}" fill="none" stroke="#3b82f6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg><div class="small">시작: {losses[0]:.4f} · 마지막: {losses[-1]:.4f}</div></div>',
        unsafe_allow_html=True,
    )

def render_backprop() -> None:
    st.subheader("② 역전파 학습 실험")
    st.caption("한 개의 뉴런을 단순화해, 예측 오차가 가중치와 편향을 어떻게 수정하는지 확인합니다.")
    a, b, c = st.columns(3)
    with a:
        x = st.slider("입력 x", -2.0, 2.0, 1.0, 0.1)
        target = st.slider("정답 y", -5.0, 5.0, 3.0, 0.5)
    with b:
        initial_weight = st.slider("초기 가중치 w", -5.0, 5.0, 0.0, 0.5)
        initial_bias = st.slider("초기 편향 b", -5.0, 5.0, 0.0, 0.5)
    with c:
        learning_rate = st.slider("학습률", 0.01, 1.0, 0.2, 0.01)
        steps = st.slider("학습 반복 횟수", 1, 30, 10)

    weight, bias = initial_weight, initial_bias
    losses = []
    for _ in range(steps):
        prediction = weight * x + bias
        error = prediction - target
        losses.append(0.5 * error * error)
        gradient = error
        weight -= learning_rate * gradient * x
        bias -= learning_rate * gradient
    final_prediction = weight * x + bias
    final_error = final_prediction - target

    m1, m2, m3 = st.columns(3)
    m1.metric("최종 예측", f"{final_prediction:.2f}")
    m2.metric("정답과의 오차", f"{abs(final_error):.2f}")
    m3.metric("최종 손실", f"{losses[-1]:.2f}")
    render_loss_chart(losses)
    st.code(
        "예측 = w × x + b\n"
        "오차 = 예측 - 정답\n"
        "w ← w - 학습률 × 오차 × x\n"
        "b ← b - 학습률 × 오차"
    )
    st.info("실제 다층 신경망에서는 출력층의 오차를 앞쪽 층으로 전달하며 같은 원리를 반복합니다. 이것이 ‘뒤로 전파한다’는 뜻의 역전파입니다.")

def sigmoid(value: float) -> float:
    value = max(-60.0, min(60.0, value))
    return 1.0 / (1.0 + math.exp(-value))

def train_xor(hidden_layers: int, epochs: int, learning_rate: float) -> tuple[list[float], list[float]]:
    architecture = [2] + [3] * hidden_layers + [1]
    rng = random.Random(7)
    weights = [
        [[rng.uniform(-1.0, 1.0) for _ in range(out_size)] for _ in range(in_size)]
        for in_size, out_size in zip(architecture[:-1], architecture[1:])
    ]
    biases = [[rng.uniform(-0.5, 0.5) for _ in range(size)] for size in architecture[1:]]
    dataset = [([0.0, 0.0], 0.0), ([0.0, 1.0], 1.0), ([1.0, 0.0], 1.0), ([1.0, 1.0], 0.0)]
    losses = []

    for _ in range(epochs):
        gradient_weights = [[[0.0 for _ in row] for row in layer] for layer in weights]
        gradient_biases = [[0.0 for _ in layer] for layer in biases]
        total_loss = 0.0
        for features, target in dataset:
            activations = [features]
            for layer_index, layer in enumerate(weights):
                previous = activations[-1]
                current = []
                for j in range(len(layer[0])):
                    value = sum(previous[i] * layer[i][j] for i in range(len(previous))) + biases[layer_index][j]
                    current.append(sigmoid(value) if layer_index == len(weights) - 1 else math.tanh(value))
                activations.append(current)

            prediction = activations[-1][0]
            error = prediction - target
            total_loss += 0.5 * error * error
            deltas: list[list[float] | None] = [None] * len(weights)
            deltas[-1] = [error * prediction * (1.0 - prediction)]
            for layer_index in range(len(weights) - 2, -1, -1):
                current_activation = activations[layer_index + 1]
                next_deltas = deltas[layer_index + 1]
                next_weights = weights[layer_index + 1]
                deltas[layer_index] = [
                    (1.0 - current_activation[i] ** 2) * sum(
                        next_weights[i][j] * next_deltas[j] for j in range(len(next_deltas))
                    )
                    for i in range(len(current_activation))
                ]

            for layer_index, delta_layer in enumerate(deltas):
                assert delta_layer is not None
                for i in range(len(activations[layer_index])):
                    for j in range(len(delta_layer)):
                        gradient_weights[layer_index][i][j] += activations[layer_index][i] * delta_layer[j]
                for j, delta in enumerate(delta_layer):
                    gradient_biases[layer_index][j] += delta

        sample_count = len(dataset)
        for layer_index in range(len(weights)):
            for i in range(len(weights[layer_index])):
                for j in range(len(weights[layer_index][i])):
                    weights[layer_index][i][j] -= learning_rate * gradient_weights[layer_index][i][j] / sample_count
            for j in range(len(biases[layer_index])):
                biases[layer_index][j] -= learning_rate * gradient_biases[layer_index][j] / sample_count
        losses.append(total_loss / sample_count)

    predictions = []
    for features, _ in dataset:
        activation = features
        for layer_index, layer in enumerate(weights):
            activation = [
                sigmoid(sum(activation[i] * layer[i][j] for i in range(len(activation))) + biases[layer_index][j])
                if layer_index == len(weights) - 1
                else math.tanh(sum(activation[i] * layer[i][j] for i in range(len(activation))) + biases[layer_index][j])
                for j in range(len(layer[0]))
            ]
        predictions.append(activation[0])
    return losses, predictions

def render_deep_learning() -> None:
    st.subheader("③ 딥러닝으로 XOR 풀기")
    st.caption("단순한 한 층의 뉴런으로는 어려운 XOR 문제를 은닉층이 있는 작은 신경망으로 학습합니다.")
    a, b, c = st.columns(3)
    with a:
        hidden_layers = st.slider("은닉층 수", 0, 3, 2)
    with b:
        epochs = st.slider("학습 횟수", 100, 2000, 800, 100)
    with c:
        learning_rate = st.slider("학습률", 0.05, 1.0, 0.5, 0.05)

    losses, predictions = train_xor(hidden_layers, epochs, learning_rate)
    architecture = " → ".join(["입력 2"] + ["은닉 뉴런 3"] * hidden_layers + ["출력 1"])
    st.markdown(f'<div class="card"><div class="year">현재 신경망 구조</div><h3>{architecture}</h3><p>앞쪽 층은 입력을 조합해 중간 표현을 만들고, 뒤쪽 층은 그 표현으로 최종 분류를 수행합니다.</p></div>', unsafe_allow_html=True)
    render_loss_chart(losses)

    rows = []
    for features, target, prediction in zip([[0, 0], [0, 1], [1, 0], [1, 1]], [0, 1, 1, 0], predictions):
        rows.append({"입력": str(features), "정답": target, "예측 확률": f"{prediction:.2f}", "분류 결과": int(prediction >= 0.5)})
    table_rows = "".join(
        f'<tr><td>{row["입력"]}</td><td>{row["정답"]}</td><td>{row["예측 확률"]}</td><td>{row["분류 결과"]}</td></tr>'
        for row in rows
    )
    st.markdown(f'<table class="result-table"><thead><tr><th>입력</th><th>정답</th><th>예측 확률</th><th>분류 결과</th></tr></thead><tbody>{table_rows}</tbody></table>', unsafe_allow_html=True)
    accuracy = sum(int((prediction >= 0.5) == bool(target)) for target, prediction in zip([0, 1, 1, 0], predictions)) / 4
    st.metric("최종 정확도", f"{accuracy * 100:.0f}%")
    if hidden_layers == 0:
        st.warning("은닉층이 0개이면 직선 하나로 XOR을 나눠야 하므로 정확히 학습하기 어렵습니다. 은닉층을 1개 이상으로 바꿔 보세요.")
    else:
        st.success("은닉층이 입력을 새로운 표현으로 바꾸면서 직선 하나로 나누기 어려운 XOR 패턴을 해결했습니다.")
    st.caption("교육용으로 작게 만든 신경망이며, 실제 딥러닝 모델의 성능이나 학습 방식을 그대로 재현한 것은 아닙니다.")

def render_tree() -> None:
    st.subheader("② 결정트리·추천 실험"); st.caption("사람이 읽을 수 있는 IF-THEN 규칙만으로도 간단한 추천 시스템을 만들 수 있습니다.")
    genre=st.selectbox("관심 장르",["과학","소설","역사","예술"]); time=st.radio("오늘 읽을 수 있는 시간",["10분","30분","1시간 이상"],horizontal=True)
    recommendations={("과학","10분"):"짧은 과학 뉴스 요약",("과학","30분"):"AI 기술의 역사",("과학","1시간 이상"):"딥러닝 입문서",("소설","10분"):"단편소설 한 편",("소설","30분"):"현대 단편선",("소설","1시간 이상"):"장편소설 첫 장",("역사","10분"):"오늘의 역사 인물",("역사","30분"):"AI 역사 타임라인",("역사","1시간 이상"):"기술사 다큐멘터리",("예술","10분"):"작품 한 점 감상",("예술","30분"):"생성형 AI와 예술",("예술","1시간 이상"):"작품 분석 에세이"}
    result=recommendations[(genre,time)]; st.markdown(f'<div class="card"><div class="year">IF 관심 장르 = {genre} AND 독서 시간 = {time}</div><h3>THEN 추천: {result}</h3><p>규칙이 명확해 결과를 설명할 수 있습니다. 데이터가 많아지면 사람이 직접 쓰는 대신 결정트리가 규칙을 학습하게 할 수 있습니다.</p></div>',unsafe_allow_html=True)

def render_search() -> None:
    st.subheader("③ 탐색과 강화학습 생각 실험"); st.caption("딥블루와 알파고의 핵심 질문: 가능한 선택지가 많을 때, 다음 행동을 어떻게 고를까요?")
    choice=st.radio("어떤 선택 전략을 고르겠어요?",["A: 지금 점수는 높지만 다음 선택이 좁아짐","B: 당장 점수는 낮지만 다음 선택이 많아짐","C: 무작위로 선택"])
    if choice.startswith("A"): st.warning("탐욕적 선택입니다. 당장의 보상은 크지만 긴 게임에서는 불리할 수 있습니다.")
    elif choice.startswith("B"): st.success("탐색을 중시한 선택입니다. 현재 보상뿐 아니라 미래 가능성도 고려합니다.")
    else: st.info("무작위 선택은 새로운 가능성을 발견할 수 있지만 성과가 불안정합니다.")
    st.markdown('<div class="quote">강화학습은 행동 → 환경의 반응 → 보상이라는 경험을 반복하며 더 좋은 정책을 찾습니다.</div>',unsafe_allow_html=True)

def render_attention() -> None:
    st.subheader("④ 트랜스포머 어텐션 보기"); st.caption("문장 속 단어들이 서로 어떤 관계를 참고하는지 단순화해 살펴봅니다.")
    sentence=st.text_input("문장을 입력해 보세요","나는 사과를 먹었다"); words=sentence.split()
    if len(words)<2: st.info("두 단어 이상 입력하면 단어 사이의 관계를 살펴볼 수 있습니다."); return
    focus=st.selectbox("관계를 살펴볼 단어",words); st.write(f"‘{focus}’가 문장 안의 다른 단어를 얼마나 참고할지 상상해 봅시다.")
    cols=st.columns(min(len(words),5)); weights=[max(1,5-abs(i-words.index(focus))) for i in range(len(words))]
    for i,word in enumerate(words):
        with cols[i%len(cols)]: st.metric(word,f"{weights[i]*20}%")
    st.caption("실제 트랜스포머는 학습을 통해 이런 관계의 가중치를 계산하며, 이 화면은 개념 이해를 위한 단순화된 모형입니다.")

def render_solar() -> None:
    st.subheader("⑤ ELIZA에서 Solar까지: AI에게 질문하기"); st.caption("초기 챗봇은 규칙을 따라 답했고, 현대 LLM은 문맥을 바탕으로 답을 생성합니다. 질문의 질과 답변의 한계를 비교해 보세요.")
    api_key = st.secrets.get("UPSTAGE_API_KEY", os.getenv("UPSTAGE_API_KEY", ""))
    if api_key:
        st.caption("🟢 Solar API 연결됨 · 실제 API 응답을 사용합니다.")
    else:
        st.caption("🟠 체험용 로컬 튜터 · Solar API 키를 설정하면 더 다양한 질문에 답합니다.")
    if "messages" not in st.session_state: st.session_state.messages=[]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])
    prompt=st.chat_input("AI 역사에 대해 질문해 보세요")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt}); system={"role":"system","content":"너는 중학생·고등학생을 위한 AI 역사 튜터다. 한국어로 답하고, 어려운 용어는 짧게 풀어 설명하며, 확인되지 않은 사실은 단정하지 마라. 답변은 5문장 이내로 한다."}; answer=call_solar([system]+st.session_state.messages) or local_tutor(prompt); st.session_state.messages.append({"role":"assistant","content":answer}); st.rerun()
    if st.button("대화 초기화"): st.session_state.messages=[]; st.rerun()

def render_lab() -> None:
    st.title("AI 체험실"); st.caption("기술의 이름을 외우는 대신, 입력을 바꿔 보며 원리가 어떻게 결과를 만드는지 확인합니다.")
    module=st.selectbox("체험 모듈",["퍼셉트론","역전파","딥러닝 · XOR","결정트리·추천","탐색과 강화학습","트랜스포머 어텐션","ELIZA ↔ Solar 대화"])
    if module=="퍼셉트론": render_perceptron()
    elif module=="역전파": render_backprop()
    elif module=="딥러닝 · XOR": render_deep_learning()
    elif module=="결정트리·추천": render_tree()
    elif module=="탐색과 강화학습": render_search()
    elif module=="트랜스포머 어텐션": render_attention()
    else: render_solar()

def render_quiz() -> None:
    st.title("마무리 퀴즈"); st.caption("정답을 고른 뒤 제출하면 자료의 핵심 연결고리를 확인할 수 있습니다.")
    with st.form("quiz_form"):
        answers=[st.radio(f"{i}. {q}", options, key=f"quiz_{i}") for i,(q,options,_,_) in enumerate(QUIZ,1)]; submitted=st.form_submit_button("채점하기",type="primary")
    if submitted:
        score=0; feedback=[]
        for (question,options,correct,explanation),answer in zip(QUIZ,answers):
            if answer==options[correct]: score+=1
            else: feedback.append(f"**{question}**  \n{explanation}")
        st.success(f"{len(QUIZ)}문제 중 {score}문제를 맞혔습니다.")
        if feedback: st.markdown("### 다시 볼 포인트"); st.markdown("\n\n".join(feedback))

def main() -> None:
    inject_css()
    with st.sidebar:
        st.markdown("## 🧭 AI Lab"); st.caption("인공지능의 이해 · 역사 편"); page=st.radio("메뉴",["홈","타임라인","체험실","퀴즈"],label_visibility="collapsed"); st.divider(); st.markdown("**오늘의 탐험 순서**"); st.markdown("1. 타임라인에서 사건 고르기\n2. 체험실에서 원리 바꾸기\n3. 퀴즈로 연결 확인하기")
        if PDF_PATH.exists(): st.download_button("원본 PDF 받기",PDF_PATH.read_bytes(),file_name=PDF_PATH.name,mime="application/pdf")
        st.caption("수업용 MVP · 2026")
    if page=="홈": render_home()
    elif page=="타임라인": render_timeline()
    elif page=="체험실": render_lab()
    else: render_quiz()

if __name__=="__main__": main()
