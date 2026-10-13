import json
import os
import streamlit as st

# Set page configuration clean without hash fragment issues
st.set_page_config(
    page_title="SreyMom VIP - វេបសាយសម្រាយរឿង និងរឿងភាគចិន",
    page_icon="🎬",
    layout="wide",
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


# Custom Styling for Dark Cinematic Theme & Clean UI
st.markdown(
    """
    <style>
    .main {
        background-color: #020617;
        color: #f8fafc;
    }
    .stApp {
        background-color: #020617;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }
    .video-card {
        background-color: #0f172a;
        border-radius: 16px;
        border: 1px solid #1e293b;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .video-card:hover {
        border-color: #e11d48;
    }
    .vip-badge {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #020617;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: bold;
    }
    .ad-banner {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 2px dashed #334155;
        padding: 15px;
        text-align: center;
        border-radius: 12px;
        color: #64748b;
        font-size: 13px;
        margin: 20px 0;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session States
if "current_tab" not in st.session_state:
  st.session_state["current_tab"] = "home"
if "playing_url" not in st.session_state:
  st.session_state["playing_url"] = None
if "playing_title" not in st.session_state:
  st.session_state["playing_title"] = ""
if "checkout_plan" not in st.session_state:
  st.session_state["checkout_plan"] = None
if "is_vip" not in st.session_state:
  st.session_state["is_vip"] = False
if "admin_logged_in" not in st.session_state:
  st.session_state["admin_logged_in"] = False

# Navigation Bar Header using columns
col_logo, col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([3, 1, 1, 1, 1])
with col_logo:
  st.markdown(
      "### 🎬 <span style='color: #e11d48;'>SreyMom</span> VIP",
      unsafe_allow_html=True,
  )
with col_nav1:
  if st.button("🏠 ទំព័រដើម", use_container_width=True):
    st.session_state["current_tab"] = "home"
    st.session_state["checkout_plan"] = None
    st.rerun()
with col_nav2:
  if st.button("📁 រឿងទាំងអស់", use_container_width=True):
    st.session_state["current_tab"] = "movies"
    st.session_state["checkout_plan"] = None
    st.rerun()
with col_nav3:
  if st.button("👑 កញ្ចប់ VIP", use_container_width=True):
    st.session_state["current_tab"] = "vip"
    st.session_state["checkout_plan"] = None
    st.rerun()
with col_nav4:
  if st.button("⚙️ Admin", use_container_width=True):
    st.session_state["current_tab"] = "admin"
    st.session_state["checkout_plan"] = None
    st.rerun()

st.markdown("---")

movies_list = load_movies()
config_data = load_config()

# TAB 1: HOME PAGE
if st.session_state["current_tab"] == "home":
  st.markdown(
      """
        <div class="ad-banner">
            📢 [កន្លែងដាក់ផ្ទាំងពាណិជ្ជកម្ម / Ad Banner - ផ្នែកខាងលើ]
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown(
      """
        <div style="background: linear-gradient(to right, #4c0519, #0f172a, #020617); padding: 40px; border-radius: 20px; border: 1px solid #1e293b; margin-bottom: 30px;">
            <span style="background-color: rgba(225, 29, 72, 0.2); color: #fb7185; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid rgba(225, 29, 72, 0.3);">រឿងពេញនិយមប្រចាំសប្តាហ៍</span>
            <h1 style="font-size: 32px; margin-top: 15px; margin-bottom: 10px;">សម្រាយរឿងភាគចិនថ្មីៗ និងរឿងហ្វូល HD</h1>
            <p style="color: #94a3b8; font-size: 14px; max-width: 600px;">ទស្សនារឿងភាគចិន និងវីដេអូសម្រាយរឿងល្បីៗជាភាសាខ្មែរ ដោយគ្មានការផ្សាយពាណិជ្ជកម្មរំខាននៅលើវេបសាយផ្ទាល់!</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.subheader("🎥 វីដេអូរឿងទើបដាក់បញ្ចូលថ្មីៗ")

  if not movies_list:
    st.info(
        "⚠️ មិនទាន់មានវីដេអូត្រូវបានបញ្ចូលទេ។ សូមចូលទៅកាន់ផ្ទាំង Admin"
        " ដើម្បីបន្ថែម Link រឿង។"
    )
  else:
    cols = st.columns(3)
    for index, movie in enumerate(movies_list):
      col = cols[index % 3]
      with col:
        yt_thumb = get_youtube_thumbnail(movie["url"])
        if yt_thumb:
          st.image(yt_thumb, use_container_width=True)
        else:
          thumb_file = movie.get("thumbnail", "")
          thumb_path = os.path.join(UPLOAD_DIR, thumb_file)
          if thumb_file and os.path.exists(thumb_path):
            st.image(thumb_path, use_container_width=True)
          else:
            st.markdown(
                """<div style="background-color: #1e293b; height: 150px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 35px;">🎬</div>""",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div style="padding: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span class="vip-badge">VIP</span>
                    <span style="font-size: 11px; color: #64748b;">HD 1080p</span>
                </div>
                <h4 style="color: #f1f5f9; font-size: 14px; margin-bottom: 12px; height: 40px; overflow: hidden; text-overflow: ellipsis;">{movie['title']}</h4>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "▶️ ចុចទស្សនា", key=f"home_watch_{index}", use_container_width=True
        ):
          st.session_state["playing_url"] = movie["url"]
          st.session_state["playing_title"] = movie["title"]
          st.session_state["current_tab"] = "watch"
          st.rerun()

  st.markdown(
      """
        <div class="ad-banner">
            📢 [កន្លែងដាក់ផ្ទាំងពាណិជ្ជកម្ម / Ad Banner - ផ្នែកខាងក្រោម]
        </div>
    """,
      unsafe_allow_html=True,
  )

# TAB 2: ALL MOVIES
elif st.session_state["current_tab"] == "movies":
  st.subheader("📁 បញ្ជីរឿង និងសម្រាយរឿងទាំងអស់")
  if not movies_list:
    st.warning("មិនទាន់មានវីដេអូនៅក្នុងប្រព័ន្ធទេ។")
  else:
    cols = st.columns(3)
    for index, movie in enumerate(movies_list):
      col = cols[index % 3]
      with col:
        yt_thumb = get_youtube_thumbnail(movie["url"])
        if yt_thumb:
          st.image(yt_thumb, use_container_width=True)
        else:
          thumb_file = movie.get("thumbnail", "")
          thumb_path = os.path.join(UPLOAD_DIR, thumb_file)
          if thumb_file and os.path.exists(thumb_path):
            st.image(thumb_path, use_container_width=True)
          else:
            st.markdown(
                """<div style="background-color: #1e293b; height: 150px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 35px;">🎬</div>""",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div style="padding: 12px;">
                <h4 style="color: #f1f5f9; font-size: 14px; margin-bottom: 12px; height: 40px; overflow: hidden; text-overflow: ellipsis;">{movie['title']}</h4>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "▶️ ទស្សនា", key=f"all_watch_{index}", use_container_width=True
        ):
          st.session_state["playing_url"] = movie["url"]
          st.session_state["playing_title"] = movie["title"]
          st.session_state["current_tab"] = "watch"
          st.rerun()

# TAB 3: WATCH VIDEO PLAYER WITH VIP GUARD & PASSCODE UNLOCK
elif st.session_state["current_tab"] == "watch":
  if st.button("⬅️ ត្រឡប់ក្រោយ"):
    st.session_state["current_tab"] = "home"
    st.rerun()

  if st.session_state["playing_url"]:
    st.subheader(f"▶️ កំពុងទស្សនា៖ {st.session_state['playing_title']}")

    # VIP ACCESS CHECK (Passcode Guard)
    if not st.session_state["is_vip"]:
      st.markdown(
          """
            <div style="background: linear-gradient(135deg, #4c0519, #0f172a); padding: 30px; border-radius: 20px; border: 2px solid #e11d48; text-align: center; margin: 20px 0;">
                <h2 style="color: #fb7185; margin-bottom: 10px;">🔒 វីដេអូនេះសម្រាប់តែសមាជិក VIP ប៉ុណ្ណោះ!</h2>
                <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 15px;">សូមស្កេន KHQR បង់ប្រាក់ រួចទាក់ទងមកកាន់ Telegram: <a href="https://t.me/SounsovannaZing" target="_blank" style="color: #38bdf8; text-decoration: underline;">@SounsovannaZing</a> ដើម្បីទទួលបាន VIP Key បើកមើល!</p>
            </div>
        """,
          unsafe_allow_html=True,
      )

      col_qr, col_key = st.columns([1, 1])

      with col_qr:
        qr_path = os.path.join(UPLOAD_DIR, "my_qr.png")
        if os.path.exists(qr_path):
          st.image(qr_path, width=230, caption="ស្កេនដើម្បីបង់ប្រាក់តាម KHQR")
        else:
          alt_qr_path = os.path.join(UPLOAD_DIR, "my_qr.jpg")
          if os.path.exists(alt_qr_path):
            st.image(
                alt_qr_path, width=230, caption="ស្កេនដើម្បីបង់ប្រាក់តាម KHQR"
            )
          else:
            st.warning("⚠️ រកមិនឃើញហ្វាលរូបភាព QR Code!")

      with col_key:
        st.markdown("#### 🔑 បញ្ចូល VIP Key ដើម្បី Unlock")
        user_key = st.text_input(
            "វាយបញ្ចូល VIP Key ដែលទទួលបានពី Admin ទីនេះ៖",
            type="password",
        )
        if st.button("🔓 ផ្ទៀងផ្ទាត់ Key", use_container_width=True):
          if user_key.strip() == config_data.get("vip_key", "VIP8888"):
            st.session_state["is_vip"] = True
            st.success("🎉 VIP Key ត្រឹមត្រូវ! វីដេអូត្រូវបាន Unlock រួចរាល់។")
            st.rerun()
          else:
            st.error("❌ VIP Key មិនត្រឹមត្រូវទេ! សូមពិនិត្យម្តងទៀត។")

    else:
      # UNLOCKED PLAYER FOR VIP USERS
      st.markdown(
          """
            <div class="ad-banner" style="margin-bottom: 15px;">
                📢 [ផ្ទាំងពាណិជ្ជកម្មខាងលើវីដេអូ / Sponsor Banner]
            </div>
        """,
          unsafe_allow_html=True,
      )

      st.video(st.session_state["playing_url"])

      st.markdown(
          """
            <div class="ad-banner" style="margin-top: 15px;">
                📢 [ផ្ទាំងពាណិជ្ជកម្មក្រោមវីដេអូ / Sponsor Banner]
            </div>
        """,
          unsafe_allow_html=True,
      )

      if st.button("🔒 ចាកចេញពីសិទ្ធិ VIP (Lock វិញ)"):
        st.session_state["is_vip"] = False
        st.rerun()

  else:
    st.info("សូមជ្រើសរើសវីដេអូណាមួយដើម្បីទស្សនា។")

# TAB 4: VIP SUBSCRIPTION & KHQR CHECKOUT
elif st.session_state["current_tab"] == "vip":
  if st.session_state["checkout_plan"]:
    plan = st.session_state["checkout_plan"]
    if st.button("⬅️ ត្រឡប់ក្រោយទៅរើសកញ្ចប់វិញ"):
      st.session_state["checkout_plan"] = None
      st.rerun()

    st.markdown(
        f"""
        <div style="background-color: #0f172a; padding: 30px; border-radius: 20px; border: 1px solid #1e293b; max-width: 600px; margin: 0 auto; text-align: center;">
            <h2 style="color: #fb7185;">KHQR ទូទាត់ប្រាក់តាមប្រព័ន្ធធនាគារ</h2>
            <p style="color: #cbd5e1; font-size: 15px; margin-bottom: 20px;">កញ្ចប់ដែលបានជ្រើសរើស៖ <b style="color: #38bdf8;">{plan["name"]} ({plan["price"]})</b></p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    qr_path = os.path.join(UPLOAD_DIR, "my_qr.png")
    if os.path.exists(qr_path):
      st.image(qr_path, width=250, caption="ស្កេនដើម្បីបង់ប្រាក់តាម KHQR")
    else:
      alt_qr_path = os.path.join(UPLOAD_DIR, "my_qr.jpg")
      if os.path.exists(alt_qr_path):
        st.image(alt_qr_path, width=250, caption="ស្កេនដើម្បីបង់ប្រាក់តាម KHQR")
      else:
        st.warning(
            "⚠️ រកមិនឃើញហ្វាលរូបភាព QR Code របស់អ្នកទេ។ សូមដាក់រូបភាព QR"
            " Code របស់អ្នកឈ្មោះថា 'my_qr.png' ចូលក្នុង Folder 'uploaded_videos'!"
        )

    st.markdown(
        """
        <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; max-width: 600px; margin: 20px auto; text-align: center;">
            <p style="color: #94a3b8; font-size: 13px;">សូមបើក App ធនាគារណាមួយ (ABA, Acleda, Canadia...) ដើម្បីស្កេនបង់ប្រាក់</p>
            <hr style="border-color: #1e293b; margin: 15px 0;">
            <p style="color: #38bdf8; font-size: 14px;">បន្ទាប់ពីបង់ប្រាក់រួច សូមផ្ញើ Slip មកកាន់ Telegram: <a href="https://t.me/SounsovannaZing" target="_blank" style="color: #fb7185; text-decoration: underline;">@SounsovannaZing</a> ដើម្បីទទួលបាន VIP Key បើកមើល!</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        "<div style='text-align: center;'><h2>👑 កញ្ចប់សមាជិកភាព VIP</h2><p"
        " style='color: #94a3b8;'>ជ្រើសរើសកញ្ចប់ដែលបងពេញចិត្តដើម្បីទស្សនារឿងអត់ដែនកំណត់</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
      st.markdown(
          """
            <div style="background-color: #0f172a; padding: 30px; border-radius: 20px; border: 1px solid #1e293b; text-align: center;">
                <h3 style="color: #f1f5f9;">កញ្ចប់ប្រចាំខែ</h3>
                <p style="color: #94a3b8; font-size: 13px;">សាកសមសម្រាប់ការកម្សាន្តរយៈពេលខ្លី</p>
                <h2 style="color: #fb7185; font-size: 36px; margin: 20px 0;">$4.99 <span style="font-size: 14px; color: #94a3b8;">/ ១ខែ</span></h2>
                <ul style="text-align: left; color: #cbd5e1; font-size: 14px; list-style: none; padding: 0; margin-bottom: 25px;">
                    <li>✅ មើលរឿង VIP ទាំងអស់ឥតកំណត់</li>
                    <li>✅ គុណភាពរូបភាពច្បាស់កម្រិត HD</li>
                    <li>✅ គ្មានពាណិជ្ជកម្មរំខាន</li>
                </ul>
            </div>
        """,
          unsafe_allow_html=True,
      )
      if st.button("💳 ទូទាត់តាម KHQR (កញ្ចប់ប្រចាំខែ)", use_container_width=True):
        st.session_state["checkout_plan"] = {
            "name": "កញ្ចប់ប្រចាំខែ",
            "price": "$4.99",
        }
        st.rerun()

    with col2:
      st.markdown(
          """
            <div style="background: linear-gradient(to bottom, #0f172a, #4c0519); padding: 30px; border-radius: 20px; border: 1px solid #e11d48; text-align: center;">
                <h3 style="color: #f1f5f9;">កញ្ចប់ប្រចាំឆ្នាំ <span style="background-color: #e11d48; font-size: 10px; padding: 2px 8px; border-radius: 6px;">ចំណេញច្រើន</span></h3>
                <p style="color: #94a3b8; font-size: 13px;">សម្រាប់អ្នកគាំទ្រស្នាដៃសម្រាយរឿងដិតដាម</p>
                <h2 style="color: #fb7185; font-size: 36px; margin: 20px 0;">$39.99 <span style="font-size: 14px; color: #94a3b8;">/ ១ឆ្នាំ</span></h2>
                <ul style="text-align: left; color: #cbd5e1; font-size: 14px; list-style: none; padding: 0; margin-bottom: 25px;">
                    <li>✅ មើលរឿង VIP ទាំងអស់ឥតកំណត់</li>
                    <li>✅ គុណភាពរូបភាពច្បាស់កម្រិត 4K</li>
                    <li>✅ ទស្សនាមុនគេពេលមានរឿងថ្មី</li>
                </ul>
            </div>
        """,
          unsafe_allow_html=True,
      )
      if st.button(
          "💳 ទូទាត់តាម KHQR (កញ្ចប់ប្រចាំឆ្នាំ)", use_container_width=True
      ):
        st.session_state["checkout_plan"] = {
            "name": "កញ្ចប់ប្រចាំឆ្នាំ",
            "price": "$39.99",
        }
        st.rerun()

# TAB 5: ADMIN PANEL WITH PASSWORD PROTECTION
elif st.session_state["current_tab"] == "admin":
  st.subheader("⚙️ ប្រព័ន្ធគ្រប់គ្រងវេបសាយ (Admin Panel)")

  # Check if Admin is logged in
  if not st.session_state["admin_logged_in"]:
    st.markdown(
        """
        <div style="background-color: #0f172a; padding: 30px; border-radius: 16px; border: 1px solid #1e293b; max-width: 450px; margin: 40px auto; text-align: center;">
            <h3 style="color: #fb7185; margin-bottom: 15px;">🔒 សូមវាយបញ្ចូលលេខសម្ងាត់ Admin</h3>
            <p style="color: #94a3b8; font-size: 13px;">កន្លែងនេះសម្រាប់តែម្ចាស់វេបសាយប៉ុណ្ណោះ!</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    entered_pass = st.text_input("Admin Password:", type="password")
    if st.button("🔑 ចូលកាន់ផ្ទាំង Admin", use_container_width=True):
      correct_pass = config_data.get("admin_pass", "admin123")
      if entered_pass.strip() == correct_pass:
        st.session_state["admin_logged_in"] = True
        st.success("🎉 ចូល Admin បានសម្រេច!")
        st.rerun()
      else:
        st.error("❌ លេខសម្ងាត់ Admin មិនត្រឹមត្រូវទេ!")
  else:
    # LOGGED IN ADMIN FEATURES
    if st.button("🔒 ចេញពីប្រព័ន្ធ Admin (Logout)"):
      st.session_state["admin_logged_in"] = False
      st.rerun()

    st.markdown("---")

    # SETTINGS FOR VIP KEY & ADMIN PASSWORD
    st.markdown("### 🔑 កំណត់ VIP Key & Admin Password")

    current_key = config_data.get("vip_key", "VIP8888")
    new_vip_key = st.text_input(
        "VIP Key ថ្មី (សម្រាប់ឱ្យអតិថិជនមើលរឿង):",
        value=current_key,
        type="password",
    )

    current_admin_pass = config_data.get("admin_pass", "admin123")
    new_admin_pass = st.text_input(
        "Admin Password ថ្មី (សម្រាប់ចូលផ្ទាំងនេះ):",
        value=current_admin_pass,
        type="password",
    )

    if st.button("💾 រក្សាទុកការកំណត់ទាំងអស់"):
      config_data["vip_key"] = new_vip_key.strip()
      config_data["admin_pass"] = new_admin_pass.strip()
      save_config(config_data)
      st.success("✅ បានរក្សាទុកការកំណត់សុវត្ថិភាពថ្មីជោគជ័យ!")

    st.markdown("---")

    # FORM TO ADD MOVIES
    with st.form("add_movie_form"):
      st.markdown("#### ➕ បន្ថែមរឿងថ្មីចូលវេបសាយ")
      new_title = st.text_input("ចំណងជើងរឿង ឬសម្រាយរឿង")
      new_url = st.text_input(
          "YouTube Link (ប្រព័ន្ធនឹងទាញយក Thumbnail ដោយស្វ័យប្រវត្តិ)"
      )

      submit_btn = st.form_submit_button("💾 រក្សាទុកវីដេអូចូលប្រព័ន្ធ")
      if submit_btn:
        if new_title and new_url:
          movies_list.append(
              {"title": new_title, "url": new_url, "thumbnail": ""}
          )
          save_movies(movies_list)
          st.success(f"បានបន្ថែមរឿង '{new_title}' ជោគជ័យ!")
          st.rerun()
        else:
          st.error(
              "សូមបំពេញចំណងជើងរឿង និង Link វីដេអូឱ្យបានត្រឹមត្រូវ!"
          )

    st.markdown("---")
    st.markdown("### 📋 បញ្ជីវីដេអូដែលមានក្នុងប្រព័ន្ធ")
    if not movies_list:
      st.warning("មិនទាន់មានវីដេអូនៅក្នុងប្រព័ន្ធទេ។")
    else:
      for idx, movie in enumerate(movies_list):
        col_name, col_del = st.columns([4, 1])
        with col_name:
          st.write(f"🎬 **{movie['title']}** — 🔗 `{movie['url']}`")
        with col_del:
          if st.button("🗑️ លុប", key=f"del_{idx}"):
            movies_list.pop(idx)
            save_movies(movies_list)
            st.success("បានលុបរឿងចេញពីប្រព័ន្ធដោយជោគជ័យ!")
            st.rerun()