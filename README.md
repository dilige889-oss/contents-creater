# contents-creater

템플릿 기반 패션·화보 스타일 이미지 생성 파이프라인 (비노출 콘텐츠 전용).

## 구성
- `creator/prompts.py` — YAML 템플릿의 변수 조합을 생성 작업(Job)으로 펼침
- `creator/safety.py` — 노출·선정적 표현, 미성년자, 실존 인물 관련 프롬프트 차단 및 안전 네거티브 프롬프트 자동 추가
- `creator/backends.py` — `mock`(GPU 없이 테스트용) / `diffusers`(SDXL, CUDA GPU 필요)
- `creator/postprocess.py` — 색보정(warm/cool/film), 업스케일, 썸네일, 콜라주
- `templates/` — 에디토리얼 화보, 일관된 가상 캐릭터 예시 템플릿

## 사용법
```bash
pip install -r requirements.txt
python -m creator.cli templates/editorial_portrait.yaml --backend mock --grade warm
# GPU 환경: requirements.txt의 선택 패키지 설치 후
python -m creator.cli templates/editorial_portrait.yaml --backend diffusers --upscale 1.5
```
결과물: `output/<템플릿명>/`에 PNG, 썸네일, `collage.jpg`, 프롬프트·시드가 기록된 `manifest.json`.

## 일관된 캐릭터 팁
- 캐릭터 설명 문구와 시드를 고정하세요 (`templates/consistent_character.yaml`).
- 더 강한 일관성이 필요하면 직접 만든 가상 캐릭터 이미지로 LoRA를 학습해 사용하세요. 실존 인물 사진으로는 학습하지 마세요.

## 테스트
```bash
python -m pytest tests
```
