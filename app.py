import json
import os
import streamlit as st

# Set page configuration clean for Mobile-First layout
st.set_page_config(
    page_title="SreyMom VIP - សម្រាយរឿង និងរឿងភាគចិន",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Folder for local assets like QR Code and Thumbnails
UPLOAD_DIR = "uploaded_videos"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)

DB_FILE = "movies_db.json"
CONFIG_FILE = "config.json"


def load_movies():
  if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except:
        return []
  return []


def save_movies(movies):
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=4)


def load_config():
  if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
      try:
        return json.load(f)
      except:
        return {"vip_key": "VIP8888", "admin_pass": "admin123"}
  return {"vip_key": "VIP8888", "admin_pass": "admin123"}


def save_config(config):
  with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=4)


def get_youtube_thumbnail(url):
  """Extract YouTube Thumbnail automatically if it's a YouTube link"""
  if "youtube.com/watch?v=" in url:
    try:
      video_id = url.split("watch?v=")[1].split("&")[0]
      return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    except:
      return None
  elif "youtu.be/" in url:
    try:
      video_id = url.split("youtu.be/")[1].split("?")[0]
      return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    except:
      return None
  return None


# Advanced Pro Mobile CSS Styling
st.markdown(
    """
    <style>
    /* Dark Modern Gradient Background */
    .stApp {
        background: radial-gradient(circle at top, #1e1b4b 0%, #020617 70%, #000000 100%) !important;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .main .block-container {
        max-width: 480px !important;
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* Header Bar */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 15px;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
    }
    .app-title {
        font-size: 18px;
        font-weight: 800;
        background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }

    /* Video Card Styling */
    .movie-card-container {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        margin-bottom: 15px;
    }
    .vip-badge-tag {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #000;
        font-size: 10px;
        font-weight: 900;
        padding: 2px 8px;
        border-radius: 6px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.5);
    }
    .price-tag {
        background: rgba(56, 189, 248, 0.2);
        color: #38bdf8;
        font-size: 11px;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 6px;
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Ad Banner Glassmorphism */
    .ad-banner-pro {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.8));
        border: 1px dashed rgba(244, 63, 94, 0.3);
        border-radius: 14px;
        padding: 12px;
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin: 15px 0;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    div.stButton > button {
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        box-shadow: 0 4px 12px rgba(225, 29, 72, 0.3) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session States
if "current_tab" not in st.session_state:
  st.session_state["current_tab"] = "home"
if "playing_movie" not in st.session_state:
  st.session_state["playing_movie"] = None
if "is_vip" not in st.session_state:
  st.session_state["is_vip"] = False
if "unlocked_movies" not in st.session_state:
  st.session_state["unlocked_movies"] = (
      []
  )  # List of movie titles unlocked individually
if "admin_logged_in" not in st.session_state:
  st.session_state["admin_logged_in"] = False

# Mobile Top Header Bar
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🎬 SREYMOM VIP</div>
        <div style="font-size: 11px; color: #fb7185; background: rgba(244, 63, 94, 0.15); padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(244, 63, 94, 0.3);">
            ● PRO STORE
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

movies_list = load_movies()
config_data = load_config()

# TAB 1: HOME PAGE
if st.session_state["current_tab"] == "home":
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #881337 0%, #0f172a 100%); padding: 22px; border-radius: 18px; border: 1px solid rgba(244, 63, 94, 0.3); margin-bottom: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <span style="background: #f43f5e; color: #fff; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: bold;">SPECIAL OFFER</span>
            <h2 style="font-size: 18px; margin-top: 10px; margin-bottom: 6px; color: #fff;">ទិញដាច់ជារឿង ឬជាសមាជិក VIP</h2>
            <p style="color: #cbd5e1; font-size: 12px; margin: 0;">បងអាចជ្រើសរើសទិញមើលតែ ១ រឿង ឬទិញកញ្ចប់ VIP មើលបានគ្រប់រឿងឥតដែនកំណត់!</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("#### 🎥 រឿងទើបបញ្ចូលថ្មីៗ")

  if not movies_list:
    st.info("⚠️ មិនទាន់មានវីដេអូត្រូវបានបញ្ចូលទេ។ សូមចូលទៅកាន់ Admin Panel។")
  else:
    for index, movie in enumerate(movies_list):
      cols = st.columns([1, 1.3])
      with cols[0]:
        yt_thumb = get_youtube_thumbnail(movie["url"])
        if yt_thumb:
          st.image(yt_thumb, use_container_width=True)
        else:
          st.markdown(
              """<div style="background:#1e293b; height:100px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#64748b;">🎬</div>""",
              unsafe_allow_html=True,
          )

      with cols[1]:
        price = movie.get("price", "$0.99")
        st.markdown(
            f"""
                <div style="display:flex; gap:6px; align-items:center;">
                    <span class="vip-badge-tag">VIP</span>
                    <span class="price-tag">តម្លៃ៖ {price}</span>
                </div>
                <h5 style="font-size: 13px; color: #f8fafc; margin-top: 8px; margin-bottom: 8px;">{movie['title']}</h5>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "▶️ ទស្សនា / ទិញរឿង",
            key=f"home_watch_{index}",
            use_container_width=True,
        ):
          st.session_state["playing_movie"] = movie
          st.session_state["current_tab"] = "watch"
          st.rerun()

      st.markdown(
          "<hr style='border-color: rgba(255,255,255,0.05); margin: 10px 0;'>",
          unsafe_allow_html=True,
      )

# TAB 2: ALL MOVIES
elif st.session_state["current_tab"] == "movies":
  st.markdown("#### 📁 បញ្ជីវីដេអូរឿងទាំងអស់")
  if not movies_list:
    st.warning("មិនទាន់មានវីដេអូនៅក្នុងប្រព័ន្ធទេ។")
  else:
    for index, movie in enumerate(movies_list):
      cols = st.columns([1, 1.3])
      with cols[0]:
        yt_thumb = get_youtube_thumbnail(movie["url"])
        if yt_thumb:
          st.image(yt_thumb, use_container_width=True)
        else:
          st.markdown(
              """<div style="background:#1e293b; height:100px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#64748b;">🎬</div>""",
              unsafe_allow_html=True,
          )

      with cols[1]:
        price = movie.get("price", "$0.99")
        st.markdown(
            f"""
                <span class="price-tag">តម្លៃ៖ {price}</span>
                <h5 style="font-size: 13px; color: #f8fafc; margin-top: 8px; margin-bottom: 8px;">{movie['title']}</h5>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "▶️ ទស្សនា / ទិញរឿង",
            key=f"all_watch_{index}",
            use_container_width=True,
        ):
          st.session_state["playing_movie"] = movie
          st.session_state["current_tab"] = "watch"
          st.rerun()

      st.markdown(
          "<hr style='border-color: rgba(255,255,255,0.05); margin: 10px 0;'>",
          unsafe_allow_html=True,
      )

# TAB 3: WATCH VIDEO PLAYER
elif st.session_state["current_tab"] == "watch":
  if st.button("⬅️ ត្រឡប់ក្រោយ"):
    st.session_state["current_tab"] = "home"
    st.rerun()

  movie = st.session_state.get("playing_movie")
  if movie:
    st.markdown(
        f"<h4 style='font-size: 15px;'>▶️ {movie['title']}</h4>",
        unsafe_allow_html=True,
    )

    # Check if user is VIP OR has unlocked this specific movie
    is_movie_unlocked = (
        st.session_state["is_vip"]
        or movie["title"] in st.session_state["unlocked_movies"]
    )

    if not is_movie_unlocked:
      movie_price = movie.get("price", "$0.99")
      movie_single_key = movie.get("movie_key", "M1234")

      st.markdown(
          f"""
            <div style="background: linear-gradient(135deg, #4c0519, #0f172a); padding: 20px; border-radius: 16px; border: 1px solid #f43f5e; text-align: center; margin: 15px 0;">
                <h3 style="color: #fb7185; font-size: 16px; margin-bottom: 8px;">🔒 រឿងនេះត្រូវការបង់ប្រាក់ដើម្បីមើល</h3>
                <p style="color: #38bdf8; font-weight: bold; font-size: 14px;">• ទិញមើលតែរឿងនេះ៖ {movie_price}<br>• ឬទិញសមាជិក VIP (មើលបានគ្រប់រឿង)</p>
                <p style="color: #cbd5e1; font-size: 11px;">ស្កេន KHQR បង់ប្រាក់ រួចផ្ញើ Slip ទៅ Telegram: <a href="https://t.me/SounsovannaZing" target="_blank" style="color: #fb7185;">@SounsovannaZing</a></p>
            </div>
        """,
          unsafe_allow_html=True,
      )

      qr_png = os.path.join(UPLOAD_DIR, "my_qr.png")
      qr_jpg = os.path.join(UPLOAD_DIR, "my_qr.jpg")

      if os.path.exists(qr_png):
        st.image(qr_png, use_container_width=True)
      elif os.path.exists(qr_jpg):
        st.image(qr_jpg, use_container_width=True)
      else:
        st.warning("⚠️ រកមិនឃើញរូបភាព QR Code!")

      st.markdown("##### 🔑 បញ្ចូល Key ដើម្បី Unlock មើលរឿង")
      user_key = st.text_input(
          "វាយបញ្ចូល VIP Key ឬ Movie Key ទីនេះ៖", type="password"
      )
      if st.button("🔓 ផ្ទៀងផ្ទាត់ Key", use_container_width=True):
        entered_k = user_key.strip()
        global_vip_key = config_data.get("vip_key", "VIP8888")

        if entered_k == global_vip_key:
          st.session_state["is_vip"] = True
          st.success("🎉 Key VIP ត្រឹមត្រូវ! លោកអ្នកអាចមើលបានគ្រប់រឿង។")
          st.rerun()
        elif entered_k == movie_single_key:
          st.session_state["unlocked_movies"].append(movie["title"])
          st.success(f"🎉 បាន Unlock រឿង '{movie['title']}' ជោគជ័យ!")
          st.rerun()
        else:
          st.error("❌ Key មិនត្រឹមត្រូវទេ! សូមពិនិត្យម្តងទៀត។")

    else:
      st.markdown(
          """<div class="ad-banner-pro">📢 [ផ្ទាំងពាណិជ្ជកម្មលើវីដេអូ]</div>""",
          unsafe_allow_html=True,
      )
      st.video(movie["url"])
      st.markdown(
          """<div class="ad-banner-pro">📢 [ផ្ទាំងពាណិជ្ជកម្មក្រោមវីដេអូ]</div>""",
          unsafe_allow_html=True,
      )

      if st.button("🔒 ចាកចេញពីការមើល (Lock វិញ)"):
        st.session_state["is_vip"] = False
        st.session_state["unlocked_movies"] = []
        st.rerun()

# TAB 4: VIP SUBSCRIPTION
elif st.session_state["current_tab"] == "vip":
  st.markdown("#### 👑 កញ្ចប់សមាជិកភាព VIP (មើលបានគ្រប់រឿង)")

  col1, col2 = st.columns(2)
  with col1:
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.8); padding: 15px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.1); text-align: center;">
            <h4 style="font-size: 14px;">ប្រចាំខែ</h4>
            <h2 style="color: #fb7185; font-size: 22px;">$4.99</h2>
            <p style="font-size: 11px; color: #94a3b8;">មើលគ្រប់រឿង HD ឥតដែនកំណត់</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        """
        <div style="background: linear-gradient(to bottom, #0f172a, #4c0519); padding: 15px; border-radius: 14px; border: 1px solid #f43f5e; text-align: center;">
            <h4 style="font-size: 14px;">ប្រចាំឆ្នាំ</h4>
            <h2 style="color: #fb7185; font-size: 22px;">$39.99</h2>
            <p style="font-size: 11px; color: #94a3b8;">មើលគ្រប់រឿង 4K ចំណេញច្រើន</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

  st.markdown("---")
  qr_png = os.path.join(UPLOAD_DIR, "my_qr.png")
  qr_jpg = os.path.join(UPLOAD_DIR, "my_qr.jpg")

  if os.path.exists(qr_png):
    st.image(qr_png, use_container_width=True)
  elif os.path.exists(qr_jpg):
    st.image(qr_jpg, use_container_width=True)

  st.markdown(
      """
    <div style="text-align: center; font-size: 12px; color: #94a3b8; margin-top: 10px;">
        បន្ទាប់ពីស្កេនបង់ប្រាក់រួច សូមផ្ញើ Slip ទៅ Telegram: <a href="https://t.me/SounsovannaZing" target="_blank" style="color: #fb7185;">@SounsovannaZing</a>
    </div>
""",
      unsafe_allow_html=True,
  )

# TAB 5: ADMIN PANEL
elif st.session_state["current_tab"] == "admin":
  st.markdown("#### ⚙️ ប្រព័ន្ធគ្រប់គ្រង Admin")

  if not st.session_state["admin_logged_in"]:
    entered_pass = st.text_input("Admin Password:", type="password")
    if st.button("🔑 ចូល Admin", use_container_width=True):
      if entered_pass.strip() == config_data.get("admin_pass", "admin123"):
        st.session_state["admin_logged_in"] = True
        st.rerun()
      else:
        st.error("❌ Password មិនត្រឹមត្រូវ!")
  else:
    if st.button("🔒 Logout Admin"):
      st.session_state["admin_logged_in"] = False
      st.rerun()

    st.markdown("---")
    new_vip_key = st.text_input(
        "VIP Key មើលបានគ្រប់រឿង៖",
        value=config_data.get("vip_key", "VIP8888"),
        type="password",
    )
    new_admin_pass = st.text_input(
        "Admin Password ថ្មី៖",
        value=config_data.get("admin_pass", "admin123"),
        type="password",
    )

    if st.button("💾 រក្សាទុក Key & Password"):
      config_data["vip_key"] = new_vip_key.strip()
      config_data["admin_pass"] = new_admin_pass.strip()
      save_config(config_data)
      st.success("✅ បានរក្សាទុកជោគជ័យ!")

    st.markdown("---")
    with st.form("add_movie_form"):
      st.markdown("##### ➕ បន្ថែមរឿងថ្មី (កំណត់តម្លៃ & Key រឿងនីមួយៗ)")
      new_title = st.text_input("ចំណងជើងរឿង")
      new_url = st.text_input("YouTube Link")
      new_price = st.text_input("តម្លៃរឿង (ឧ. $0.99 ឬ 4,000៛)", value="$0.99")
      new_m_key = st.text_input(
          "Key សម្រាប់ Unlock តែរឿងនេះមួយ (ឧ. M101)", value="M101"
      )

      if st.form_submit_button("💾 រក្សាទុករឿង"):
        if new_title and new_url:
          movies_list.append({
              "title": new_title,
              "url": new_url,
              "price": new_price.strip(),
              "movie_key": new_m_key.strip(),
              "thumbnail": "",
          })
          save_movies(movies_list)
          st.success("បានបន្ថែមរឿង និងរៀបចំតម្លៃជោគជ័យ!")
          st.rerun()

    st.markdown("---")
    st.markdown("##### 📋 បញ្ជីវីដេអូរឿងដែលមាន")
    for idx, movie in enumerate(movies_list):
      c1, c2 = st.columns([3, 1])
      c1.write(
          f"🎬 **{movie['title']}**\n\n💰 តម្លៃ៖ `{movie.get('price', '$0.49')}`"
          f" | 🔑 Key: `{movie.get('movie_key', 'N/A')}`"
      )
      if c2.button("🗑️ លុប", key=f"del_{idx}"):
        movies_list.pop(idx)
        save_movies(movies_list)
        st.rerun()

# PRO MOBILE BOTTOM NAVIGATION BAR
st.markdown("<br><br>", unsafe_allow_html=True)
b_col1, b_col2, b_col3, b_col4 = st.columns(4)

with b_col1:
  if st.button("🏠", use_container_width=True):
    st.session_state["current_tab"] = "home"
    st.rerun()
with b_col2:
  if st.button("📁", use_container_width=True):
    st.session_state["current_tab"] = "movies"
    st.rerun()
with b_col3:
  if st.button("👑", use_container_width=True):
    st.session_state["current_tab"] = "vip"
    st.rerun()
with b_col4:
  if st.button("⚙️", use_container_width=True):
    st.session_state["current_tab"] = "admin"
    st.rerun()