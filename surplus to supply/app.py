import os
import sqlite3
import streamlit as st
from datetime import date

# ---------- PAGE CONFIGURATION ----------

st.set_page_config(
    page_title="Surplus to Supply",
    page_icon="🍲",
    layout="wide"
)

# ---------- PREMIUM DESIGN + GREEN AURORA ----------

st.markdown("""
<style>
:root {
    --bg: #080c09;
    --panel: #151915;
    --border: #30382c;
    --lime: #c5ff41;
    --text: #f2f4ec;
    --muted: #a4ada0;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 15%, #17351e 0%, transparent 42%),
        radial-gradient(ellipse at 85% 40%, #153522 0%, transparent 40%),
        var(--bg) !important;
    background-attachment: fixed !important;
    color: var(--text);
    overflow-x: hidden;
}

/* Animated aurora layer */
.stApp::before {
    content: "";
    position: fixed;
    inset: -35%;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 20% 35%,
            #8aff3930 0%, transparent 32%),
        radial-gradient(ellipse at 70% 25%,
            #29d98228 0%, transparent 35%),
        radial-gradient(ellipse at 55% 75%,
            #b4ff4125 0%, transparent 32%);
    filter: blur(24px);
    animation: auroraDrift 22s ease-in-out infinite alternate;
}

/* Floating glow orbs */
.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        radial-gradient(circle at 12% 28%,
            #c5ff4170 0px, #c5ff4120 4px, transparent 15px),
        radial-gradient(circle at 78% 20%,
            #76ffb355 0px, #76ffb320 5px, transparent 18px),
        radial-gradient(circle at 68% 72%,
            #c5ff4150 0px, #c5ff4118 4px, transparent 16px),
        radial-gradient(circle at 28% 82%,
            #6aff9845 0px, #6aff9815 5px, transparent 18px);
    animation: orbFloat 16s ease-in-out infinite alternate;
}

/* Keep app content above background */
[data-testid="stHeader"],
[data-testid="stMain"],
[data-testid="stBottom"],
[data-testid="stSidebar"] {
    position: relative;
    z-index: 1;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text) !important;
    letter-spacing: -1px;
}

p, label {
    color: #e0e5d9;
}

hr {
    border-color: var(--border);
}

/* Animations */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes limeGlow {
    0%, 100% {
        text-shadow: 0 0 0 rgba(197, 255, 65, 0);
    }
    50% {
        text-shadow: 0 0 18px rgba(197, 255, 65, 0.3);
    }
}

@keyframes auroraDrift {
    0% {
        transform: translate3d(-3%, -2%, 0) rotate(0deg) scale(1);
    }
    50% {
        transform: translate3d(3%, 2%, 0) rotate(5deg) scale(1.05);
    }
    100% {
        transform: translate3d(-1%, 4%, 0) rotate(-4deg) scale(1.1);
    }
}

@keyframes orbFloat {
    0% {
        transform: translate3d(-8px, 8px, 0);
        opacity: .45;
    }
    50% {
        opacity: .9;
    }
    100% {
        transform: translate3d(12px, -14px, 0);
        opacity: .65;
    }
}

/* Hero */
.hero {
    padding: 42px 10px 35px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
    animation: fadeUp 0.8s ease-out both;
}

.hero-label {
    color: var(--lime);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
}

.hero-title {
    color: var(--text);
    font-size: clamp(42px, 7vw, 84px);
    font-weight: 900;
    line-height: 1.02;
    letter-spacing: -3px;
    margin: 22px 0;
}

.hero-accent {
    color: var(--lime);
    animation: limeGlow 4s ease-in-out infinite;
}

.hero-description {
    color: var(--muted);
    font-size: 17px;
    max-width: 650px;
    line-height: 1.7;
}

.hero-footer {
    color: #a0ad92;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 28px;
}

/* Dashboard metric cards */
[data-testid="stMetric"] {
    background: #151915e8;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    transition: border-color 0.25s ease, transform 0.25s ease;
    animation: fadeUp 0.6s ease-out both;
}

[data-testid="stMetric"]:hover {
    border-color: var(--lime);
    transform: translateY(-3px);
}

[data-testid="stMetricValue"] {
    color: var(--lime);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
}

/* Donation cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111711aa;
    border-color: var(--border) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #65764c !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
[data-testid="stFormSubmitButton"] button {
    background: var(--lime) !important;
    color: #10130d !important;
    -webkit-text-fill-color: #10130d !important;
    border: 1px solid var(--lime) !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: background 0.2s ease, transform 0.2s ease;
}

.stButton > button *,
.stFormSubmitButton > button *,
[data-testid="stFormSubmitButton"] button * {
    color: #10130d !important;
    -webkit-text-fill-color: #10130d !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #ddff91 !important;
    border-color: #ddff91 !important;
    transform: translateY(-2px);
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background: var(--panel);
    color: var(--text);
    border-radius: 8px;
}

/* Radio buttons */
.stRadio label {
    color: var(--text);
}

[data-baseweb="radio"] > div:first-child {
    border-color: var(--lime);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #101310;
    border-right: 1px solid var(--border);
}

/* Alerts, tables and expanders */
[data-testid="stAlert"] {
    border-radius: 12px;
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid var(--border);
    border-radius: 12px;
}

[data-testid="stExpander"] {
    border-color: var(--border);
    border-radius: 12px;
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after,
    .hero,
    .hero-accent,
    [data-testid="stMetric"] {
        animation: none !important;
    }

    *, *::before, *::after {
        transition-duration: 0.01ms !important;
    }
}

/* Small screens */
@media (max-width: 600px) {
    .hero-title {
        letter-spacing: -1px;
    }

    .hero {
        padding-top: 25px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- HERO SECTION ----------

st.markdown(
    "<div class='hero'>"
    "<div class='hero-label'>SMART FOOD REDISTRIBUTION</div>"
    "<div class='hero-title'>"
    "TURN SURPLUS.<br>"
    "<span class='hero-accent'>INTO SUSTENANCE.</span>"
    "</div>"
    "<div class='hero-description'>"
    "Every surplus meal is an opportunity. "
    "Connect food donors with people who need it "
    "and turn waste into meaningful impact."
    "</div>"
    "<div class='hero-footer'>"
    "RESCUE FOOD &nbsp; / &nbsp; "
    "CONNECT PEOPLE &nbsp; / &nbsp; "
    "CREATE IMPACT"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)

st.caption("LIVE FOOD REDISTRIBUTION PLATFORM")


# ---------- DATABASE BACKEND ----------
# Keeps the existing donations.db.
# Supports either "location" or "pickup_location" column names.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "donations.db")


def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10)


def get_location_column(conn):
    columns = conn.execute(
        "PRAGMA table_info(donations)"
    ).fetchall()

    names = [column[1] for column in columns]

    if "pickup_location" in names:
        return "pickup_location"

    return "location"


def setup_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                location TEXT NOT NULL,
                available_until TEXT NOT NULL
            )
        """)

        columns = conn.execute(
            "PRAGMA table_info(donations)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        if "status" not in column_names:
            conn.execute("""
                ALTER TABLE donations
                ADD COLUMN status TEXT NOT NULL
                DEFAULT 'Available'
            """)

        # Give older records a default status if the field is blank.
        conn.execute("""
            UPDATE donations
            SET status = 'Available'
            WHERE status IS NULL OR TRIM(status) = ''
        """)


def add_donation(food_name, quantity, location, available_until):
    with get_connection() as conn:
        location_column = get_location_column(conn)

        query = f"""
            INSERT INTO donations
            (food_name, quantity, {location_column},
             available_until, status)
            VALUES (?, ?, ?, ?, 'Available')
        """

        conn.execute(
            query,
            (food_name, quantity, location, available_until)
        )


def get_donations():
    with get_connection() as conn:
        location_column = get_location_column(conn)

        query = f"""
            SELECT id, food_name, quantity, {location_column},
                   available_until, status
            FROM donations
            ORDER BY id DESC
        """

        return conn.execute(query).fetchall()


def accept_donation(donation_id):
    with get_connection() as conn:
        conn.execute("""
            UPDATE donations
            SET status = 'Accepted'
            WHERE id = ? AND status = 'Available'
        """, (donation_id,))


def delete_donation(donation_id):
    # Available if you later want an admin delete feature.
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM donations WHERE id = ?",
            (donation_id,)
        )


setup_database()



# ---------- PORTAL NAVIGATION ----------

st.divider()

st.markdown(
    "<p style='color:#c5ff41; letter-spacing:3px;"
    "font-size:12px; font-weight:bold;'>"
    "SELECT YOUR EXPERIENCE</p>",
    unsafe_allow_html=True
)

role_choice = st.radio(
    "Choose your portal",
    ["🥗 Donor", "🤝 Receiver", "📊 Dashboard"],
    horizontal=True,
    label_visibility="collapsed"
)

role = role_choice.split(" ", 1)[1]
donations = get_donations()


# ---------- DONOR PORTAL ----------

if role == "Donor":
    st.header("🥗 Donor Portal")
    st.write("List surplus food for people who need it.")

    with st.form("donation_form", clear_on_submit=True):
        food_name = st.text_input("Food Name")

        quantity = st.number_input(
            "Quantity (in meals)",
            min_value=1,
            step=1
        )

        location = st.text_input("Pickup Location")

        expiry = st.date_input(
            "Food Available Until",
            min_value=date.today()
        )

        submitted = st.form_submit_button("Submit Donation")

        if submitted:
            if not food_name.strip() or not location.strip():
                st.warning(
                    "Please enter both the food name "
                    "and pickup location."
                )
            elif expiry < date.today():
                st.warning(
                    "The availability date cannot be in the past."
                )
            else:
                add_donation(
                    food_name.strip(),
                    int(quantity),
                    location.strip(),
                    str(expiry)
                )
                st.success("Donation saved successfully!")
                st.rerun()

    st.divider()
    st.header("📋 Donation Records")

    if donations:
        for item in donations:
            donation_id, name, qty, loc, until, status = item

            with st.container(border=True):
                st.subheader(name)
                st.write(f"Donation ID: {donation_id}")
                st.write(f"Quantity: {qty} meals")
                st.write(f"Pickup Location: {loc}")
                st.write(f"Available Until: {until}")

                if status == "Accepted":
                    st.success("Status: Accepted")
                else:
                    st.info("Status: Available")
    else:
        st.info("You haven't listed any donations yet.")


# ---------- RECEIVER PORTAL ----------

elif role == "Receiver":
    st.header("🤝 Receiver Portal")
    st.write("Browse available food and accept a donation.")

    available = [
        d for d in donations
        if d[5] == "Available" and d[4] >= str(date.today())
    ]

    accepted = [
        d for d in donations
        if d[5] == "Accepted"
    ]

    st.metric("Available Donations", len(available))

    if available:
        for item in available:
            donation_id, name, qty, loc, until, status = item

            with st.container(border=True):
                st.subheader(name)
                st.write(f"Donation ID: {donation_id}")
                st.write(f"Quantity: {qty} meals")
                st.write(f"Pickup Location: {loc}")
                st.write(f"Available Until: {until}")

                if st.button(
                    "Accept Donation",
                    key=f"accept_{donation_id}"
                ):
                    accept_donation(donation_id)
                    st.success("Donation accepted!")
                    st.rerun()
    else:
        st.info("No available donations right now.")

    st.divider()
    st.subheader("Previously Accepted Donations")

    if accepted:
        for item in accepted:
            st.write(
                f"✅ {item[1]} — {item[2]} meals — "
                f"Pickup: {item[3]}"
            )
    else:
        st.write("No donations have been accepted yet.")


# ---------- DASHBOARD ----------

elif role == "Dashboard":
    st.header("📊 Project Dashboard")
    st.write("Live statistics from the food donation database.")

    total = len(donations)

    available_count = sum(
        1 for d in donations
        if d[5] == "Available" and d[4] >= str(date.today())
    )

    accepted_count = sum(
        1 for d in donations if d[5] == "Accepted"
    )

    meals = sum(d[2] for d in donations)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Donations", total)
    col2.metric("Available Donations", available_count)
    col3.metric("Accepted Donations", accepted_count)
    col4.metric("Total Meals Listed", meals)

    st.divider()
    st.subheader("📈 Acceptance Rate")

    if total > 0:
        rate = (accepted_count / total) * 100
        st.progress(rate / 100)
        st.write(
            f"{rate:.1f}% of donations have been accepted."
        )
    else:
        st.info("Submit a donation to see the acceptance rate.")

    st.divider()
    st.subheader("🍱 Donation Status Breakdown")

    status_data = {
        "Status": ["Available", "Accepted"],
        "Donations": [
            available_count,
            accepted_count
        ]
    }

    st.bar_chart(
        status_data,
        x="Status",
        y="Donations"
    )

    st.subheader("🥗 Meals by Food Donation")

    if donations:
        food_data = {
            "Food": [d[1] for d in donations],
            "Meals": [d[2] for d in donations]
        }

        st.bar_chart(
            food_data,
            x="Food",
            y="Meals"
        )
    else:
        st.info("No donation records to chart yet.")

    st.divider()
    st.subheader("📋 All Donation Records")

    if donations:
        for item in donations:
            with st.container(border=True):
                st.write(f"**{item[1]}**")
                st.write(f"Quantity: {item[2]} meals")
                st.write(f"Location: {item[3]}")
                st.write(f"Available Until: {item[4]}")
                st.write(f"Status: {item[5]}")
    else:
        st.info(
            "Donation statistics will appear here "
            "after submissions."
        )

    st.caption(
        "Surplus to Supply | Food Redistribution Prototype"
    )