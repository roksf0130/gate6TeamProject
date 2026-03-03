import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import streamlit as st

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD  = (0.229, 0.224, 0.225)

# 페이지 설정
st.set_page_config(page_title='ResNet50 테스트', layout='centered')
st.title(body='ResNet50 테스트', width='stretch', text_alignment='center')


ALLOW_LABEL = "반입 가능한 물품"

THRESH_ALLOW = 0.85
THRESH_REVIEW = 0.60

@st.cache_resource
def load_model(ckpt_path: str, device: str):
    ckpt = torch.load(ckpt_path, map_location=device)
    class_names = ckpt["class_names"]
    img_size = int(ckpt.get("img_size", 224))

    try:
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    except Exception:
        model = models.resnet50(pretrained=True)

    model.fc = nn.Linear(model.fc.in_features, len(class_names))
    model.load_state_dict(ckpt["model_state_dict"])
    model.to(device)
    model.eval()

    tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    return model, tf, class_names


@torch.no_grad()
def predict_with_probs(model, tf, img, device):
    x = tf(img).unsqueeze(0).to(device)
    logits = model(x)
    probs = torch.softmax(logits, dim=1).squeeze(0)  # (C,)
    return probs.detach().cpu()


def topk_from_probs(probs, class_names, topk=3):
    topk = min(topk, probs.numel())
    vals, idxs = torch.topk(probs, k=topk)
    results = [(class_names[i], float(v)) for v, i in zip(vals.tolist(), idxs.tolist())]
    return results


st.title("기내 반입 가능/불가능 판별")
st.caption("ResNet50 기반 (이진 판정: '반입 가능한 물품'만 가능으로 처리)")

ckpt_path = st.text_input("Checkpoint path", "best_model_resnet50_8class.pth")
device = "cuda" if torch.cuda.is_available() else "cpu"
st.write("Device:", device)

try:
    model, tf, class_names = load_model(ckpt_path, device)
except Exception as e:
    st.error(f"모델 로드 실패: {e}")
    st.stop()

if ALLOW_LABEL not in class_names:
    st.error(f"'{ALLOW_LABEL}' 라벨이 모델 class_names에 없습니다.\n"
             f"현재 class_names: {class_names}")
    st.stop()

allow_idx = class_names.index(ALLOW_LABEL)

uploaded = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png", "webp", "bmp"])
topk = st.slider("Top-K 표시", 1, min(10, len(class_names)), 3)
show_all_probs = st.checkbox("전체 클래스 확률 보기", value=False)

st.markdown("---")
st.subheader("판정 기준(Threshold)")
st.write(f"- ✅ 가능: {ALLOW_LABEL} 확률 ≥ **{THRESH_ALLOW:.2f}**")
st.write(f"- ⚠️ 재확인: **{THRESH_REVIEW:.2f}** ≤ 확률 < **{THRESH_ALLOW:.2f}**")
st.write(f"- ❌ 불가: 확률 < **{THRESH_REVIEW:.2f}**")

if uploaded is not None:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded", use_container_width=True)

    probs = predict_with_probs(model, tf, img, device)
    allow_prob = float(probs[allow_idx].item())

    results = topk_from_probs(probs, class_names, topk=topk)
    st.subheader("모델 예측 (Top-K)")
    for rank, (label, prob) in enumerate(results, start=1):
        st.write(f"Top{rank}: {label} — {prob:.4f}")

    st.markdown("---")
    st.subheader("최종 판정 (기내 반입 가능/불가)")
    st.write(f"'{ALLOW_LABEL}' 확률: **{allow_prob:.4f}**")

    if allow_prob >= THRESH_ALLOW:
        st.success("✅ 기내 반입 가능합니다.")
    elif allow_prob >= THRESH_REVIEW:
        st.warning("⚠️ 재확인 필요: 판별 확률이 애매합니다. (추가 확인 권장)")
        st.error("❌ 보수적으로는 기내 반입 불가로 안내합니다.")
    else:
        st.error("❌ 기내 반입 불가합니다.")

    if show_all_probs:
        st.markdown("---")
        st.subheader("전체 클래스 확률")
        sorted_items = sorted([(class_names[i], float(probs[i].item())) for i in range(len(class_names))],
                              key=lambda x: x[1], reverse=True)
        for label, p in sorted_items:
            st.write(f"{label}: {p:.4f}")
