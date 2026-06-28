import streamlit as st
from recommend import music, find_song, recommend
from spotify_utils import get_song_details

st.set_page_config(
    page_title="Music Recommender",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Music Recommender")

# ── Session state init ────────────────────────────────────────────────────────
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "song_info" not in st.session_state:
    st.session_state.song_info = None
if "matches" not in st.session_state:
    st.session_state.matches = None
if "searched_song" not in st.session_state:
    st.session_state.searched_song = ""

# ── Input ─────────────────────────────────────────────────────────────────────
selected_song = st.text_input("🎵 Enter a song name:", placeholder="e.g. Believer, Shape of You")

if st.button("🔍 Find Similar Songs"):
    st.session_state.recommendations = None
    st.session_state.song_info       = None
    st.session_state.matches         = None
    st.session_state.searched_song   = selected_song.strip()

    if not selected_song.strip():
        st.warning("Please enter a song name.")
    else:
        matches = find_song(selected_song)

        if matches.empty:
            suggestions = music[
                music['track_name'].str.lower().str.contains(
                    selected_song.strip().lower(), na=False
                )
            ][['track_name', 'artists']].drop_duplicates('track_name').head(8)

            if not suggestions.empty:
                st.warning(f"**'{selected_song}'** not found. Did you mean one of these?")
                for _, row in suggestions.iterrows():
                    st.write(f"• {row['track_name']} — {row['artists']}")
            else:
                st.warning(f"**'{selected_song}'** not found in the dataset.")

        elif len(matches) == 1:
            # Only one match — recommend immediately
            song_idx = matches.index[0]
            song_info, recommendations = recommend(song_idx)
            st.session_state.song_info       = song_info
            st.session_state.recommendations = recommendations

        else:
            # Multiple matches — save them, let user pick
            st.session_state.matches = matches

# ── Disambiguation dropdown (stays visible after selection) ───────────────────
if st.session_state.matches is not None:
    matches = st.session_state.matches
    st.info(f"Multiple versions of **{st.session_state.searched_song}** found. Choose one:")
    choice = st.selectbox(
        "Choose the correct version:",
        options=matches.index,
        format_func=lambda i: (
            f"{music.loc[i, 'track_name']}  —  "
            f"{music.loc[i, 'artists']}  "
            f"({music.loc[i, 'track_genre']})"
        )
    )

    if st.button("▶ Get Recommendations"):
        song_info, recommendations = recommend(choice)
        st.session_state.song_info       = song_info
        st.session_state.recommendations = recommendations
        st.session_state.matches         = None

# ── Show recommendations ──────────────────────────────────────────────────────
if st.session_state.recommendations is not None:
    st.success("Top similar songs:")

    for rec in st.session_state.recommendations:
        img_url, preview = get_song_details(rec['track_name'], rec['artists'])

        with st.container():
            col1, col2 = st.columns([1, 3])

            with col1:
                if img_url:
                    st.image(img_url, width=100)
                else:
                    st.write("🎵 No Image")

            with col2:
                st.markdown(f"### {rec['track_name']}")
                st.markdown(f"**Artist:** {rec['artists']}")
                st.markdown(f"**Genre:** {rec['track_genre']}")
                st.markdown(f"**Match:** {rec['similarity']}%")
                if preview:
                    st.audio(preview, format="audio/mp3")

        st.divider()