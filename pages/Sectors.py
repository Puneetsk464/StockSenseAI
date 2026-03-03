import streamlit as st
from streamlit.components.v1 import html
from sector_map import SECTOR_MAP

st.set_page_config(
    page_title="Explore Sectors",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- STYLES --------------------
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        text-align: center;
        color: #7c3aed;
        margin-bottom: 1rem;
    }

    .subtitle {
        font-size: 1.3rem !important;
        text-align: center;
        color: #6b7280;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        text-align: center;
        color: #e5e7eb;
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
    }

    .section-subtitle {
        font-size: 1rem;
        text-align: center;
        color: #9ca3af;
        margin-bottom: 0.6rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #070F2B;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 20px;
    }

    .stButton > button {
        background-color: #070F2B;
        color: white;
        border: 1px solid #374151;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #059669 !important;
        color: white !important;
        border: none !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -------------------- MAIN TITLE --------------------
st.markdown('<div class="main-title">Indian Stock Market</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Explore major sectors and discover investment opportunities.</div>',
    unsafe_allow_html=True
)

st.divider()

# -------------------- VIDEO SECTION --------------------
st.markdown('<div class="section-title">Beginner Video Learning Hub</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">New to investing? Start here with simple, beginner-friendly lessons.</div>',
    unsafe_allow_html=True
)

html("""
<style>
.video-carousel {
    width: 100%;
    overflow: hidden;
    padding: 10px 0;
}

.video-track {
    display: flex;
    gap: 24px;
    width: max-content;
    will-change: transform;
}

.video-card {
    min-width: 320px;
    background-color: #070F2B;
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 10px;
    
    display: flex;
    align-items: center;
    justify-content: center;
}

.video-card iframe {
    width: 100%;
    height: 180px;
    border-radius: 8px;
}
</style>

<div class="video-carousel">
    <div class="video-track" id="track">

        <div class="video-card"><iframe src="https://www.youtube.com/embed/3UF0ymVdYLA" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/by9_zHQzeZk" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/RFP3ooXIiyI" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/6e8SJvEqtXo" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/Y2OfXN4jvn0" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/yzRP-mA2eiE" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/veWVgyucBqU" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/810jmf7drFw" allowfullscreen></iframe></div>
        
        <div class="video-card"><iframe src="https://www.youtube.com/embed/WZkXcfr4r3c" allowfullscreen></iframe></div>
        
        <div class="video-card"><iframe src="https://www.youtube.com/embed/9TCLTz3GG3g" allowfullscreen></iframe></div>
        
        <div class="video-card"><iframe src="https://www.youtube.com/embed/4LqTDj0cwPA" allowfullscreen></iframe></div>

        <div class="video-card"><iframe src="https://www.youtube.com/embed/VcCiGpKsu7g" allowfullscreen></iframe></div>


        <div class="video-card"><iframe src="https://www.youtube.com/embed/3UF0ymVdYLA" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/by9_zHQzeZk" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/RFP3ooXIiyI" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/6e8SJvEqtXo" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/Y2OfXN4jvn0" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/yzRP-mA2eiE" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/veWVgyucBqU" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/810jmf7drFw" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/WZkXcfr4r3c" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/9TCLTz3GG3g" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/4LqTDj0cwPA" allowfullscreen></iframe></div>
        <div class="video-card"><iframe src="https://www.youtube.com/embed/VcCiGpKsu7g" allowfullscreen></iframe></div>

    </div>
</div>


<script>
const track = document.getElementById("track");

let pos = 0;
let speed = 0.7;
let paused = false;

// compute half width AFTER layout
const halfWidth = track.scrollWidth / 2;

function animate() {
    if (!paused) {
        pos -= speed;
        if (Math.abs(pos) >= halfWidth) {
            pos = 0;
        }
        track.style.transform = `translateX(${pos}px)`;
    }
    requestAnimationFrame(animate);
}

track.addEventListener("mouseenter", () => paused = true);
track.addEventListener("mouseleave", () => paused = false);

animate();
</script>
""", height=260)

st.divider()

# -------------------- SECTOR CARDS --------------------
cols = st.columns(4)
for i, (sector_name, data) in enumerate(SECTOR_MAP.items()):
    with cols[i % 4]:
        with st.container(border=True):
            st.subheader(f"{data['icon']} {sector_name}")
            st.caption(data["desc"])
            if st.button(
                "Explore →",
                key=f"explore_{sector_name}",
                use_container_width=True
            ):
                st.session_state.selected_sector = sector_name
                st.switch_page("pages/Companies.py")
