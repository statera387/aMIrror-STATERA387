import streamlit as st
import numpy as np
import time
import random

# Page configuration
st.set_page_config(
    page_title="Voice Authenticity Monitor",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS for watery depths background
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, 
        #001122 0%,
        #003344 30%,
        #004466 60%,
        #0088aa 100%);
}
</style>
""", unsafe_allow_html=True)

# Helper function to simulate voice features
def simulate_voice_features(baseline_mode=True):
    if baseline_mode:
        pitch = random.uniform(120, 180)
        energy = random.uniform(0.3, 0.7)
        rate = random.uniform(140, 180)
        centeredness = random.uniform(0.6, 0.9)
    else:
        pitch = random.uniform(100, 220)
        energy = random.uniform(0.2, 0.9)
        rate = random.uniform(120, 220)
        centeredness = random.uniform(0.3, 0.9)
    
    return pitch, energy, rate, centeredness

# Initialize session state
if 'baseline_samples' not in st.session_state:
    st.session_state.baseline_samples = []
if 'baseline_complete' not in st.session_state:
    st.session_state.baseline_complete = False
if 'recording_active' not in st.session_state:
    st.session_state.recording_active = False
if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False
if 'recording_timer' not in st.session_state:
    st.session_state.recording_timer = 30

# Header
st.title("🎤 Voice Authenticity Monitor")
st.write("Detect when you shift from your authentic voice to mirroring others")

# Sidebar with mirroring information
with st.sidebar:
    st.header("🪞 What is Voice Mirroring?")
    st.write("""
    **Voice mirroring** happens when you unconsciously adopt someone else's:
    - Speaking pace and rhythm
    - Vocal pitch and tone
    - Energy levels
    - Speech patterns
    """)
    
    st.subheader("⚠️ Why it matters:")
    st.write("""
    - Can indicate loss of authentic self
    - May signal people-pleasing behavior
    - Often happens during stress
    - Can lead to feeling disconnected
    """)

    st.subheader("🎯 Common triggers:")
    st.write("""
    - Job interviews
    - Meeting authority figures
    - Social pressure situations
    - Trying to fit in
    - Stressful conversations
    """)
    
    st.subheader("✨ Benefits of awareness:")
    st.write("""
    - Stay true to yourself
    - Maintain personal power
    - Build authentic relationships
    - Reduce social anxiety
    """)

st.divider()

# Baseline Recording Section
st.header("🎯 Step 1: Record Your Authentic Voice Baseline")

if not st.session_state.baseline_complete:
    st.write("First, we need to capture your natural speaking voice when you're relaxed and being yourself.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if not st.session_state.recording_active:
            if st.button("🔴 Start Baseline Recording", type="primary"):
                st.session_state.recording_active = True
                st.session_state.recording_timer = 30
                st.rerun()
        else:
            if st.button("⏹️ Stop Recording", type="secondary"):
                st.session_state.recording_active = False
                st.rerun()

    with col2:
        if st.session_state.recording_active:
            st.info(f"🎤 Recording... {st.session_state.recording_timer} seconds remaining")
            st.write("**Speak naturally about:**")
            st.write("• Your favorite hobby or interest")
            st.write("• What you did yesterday")
            st.write("• A place you'd like to visit")
        else:
            st.write("Click 'Start Recording' to begin capturing your baseline voice")
    
    # Recording simulation
    if st.session_state.recording_active:
        # Simulate recording progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(30):
            progress = (i + 1) / 30
            progress_bar.progress(progress)
            status_text.text(f"Recording... {30 - i} seconds remaining")
            
            # Collect baseline sample
            pitch, energy, rate, centeredness = simulate_voice_features(baseline_mode=True)
            st.session_state.baseline_samples.append({
                'pitch': pitch,
                'energy': energy,
                'rate': rate,
                'centeredness': centeredness
            })
            
            time.sleep(1)
        
        # Complete baseline recording
        st.session_state.recording_active = False
        st.session_state.baseline_complete = True
        st.success("✅ Baseline recording complete!")
        st.rerun()

else:
    # Show baseline analysis
    st.success("✅ Baseline recording completed!")
    
    # Calculate baseline averages
    baseline_pitch = np.mean([s['pitch'] for s in st.session_state.baseline_samples])
    baseline_energy = np.mean([s['energy'] for s in st.session_state.baseline_samples])
    baseline_rate = np.mean([s['rate'] for s in st.session_state.baseline_samples])
    baseline_centeredness = np.mean([s['centeredness'] for s in st.session_state.baseline_samples])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Baseline Pitch", f"{baseline_pitch:.1f} Hz")
    with col2:
        st.metric("Baseline Energy", f"{baseline_energy:.2f}")
    with col3:
        st.metric("Baseline Rate", f"{baseline_rate:.0f} WPM")
    with col4:
        st.metric("Baseline Centeredness", f"{baseline_centeredness:.2f}")
    
    if st.button("🔄 Reset Baseline", type="secondary"):
        st.session_state.baseline_samples = []
        st.session_state.baseline_complete = False
        st.session_state.monitoring_active = False
        st.rerun()
st.divider()

# Live Monitoring Section
st.header("🔍 Step 2: Live Voice Monitoring")

if st.session_state.baseline_complete:
    if not st.session_state.monitoring_active:
        if st.button("🎤 Start Live Monitoring", type="primary"):
            st.session_state.monitoring_active = True
            st.rerun()
    else:
        if st.button("⏸️ Stop Monitoring", type="secondary"):
            st.session_state.monitoring_active = False
            st.rerun()
    
    # Live monitoring display
    if st.session_state.monitoring_active:
        st.info("🎤 **Live monitoring active** - Speak naturally and we'll detect any voice mirroring")
        
        # Get current voice sample
        current_pitch, current_energy, current_rate, current_centeredness = simulate_voice_features(baseline_mode=False)
        
        # Calculate deviations from baseline
        pitch_deviation = abs(current_pitch - baseline_pitch) / baseline_pitch
        energy_deviation = abs(current_energy - baseline_energy) / baseline_energy if baseline_energy > 0 else 0
        rate_deviation = abs(current_rate - baseline_rate) / baseline_rate
        centeredness_deviation = abs(current_centeredness - baseline_centeredness) / baseline_centeredness if baseline_centeredness > 0 else 0
        
        # Overall mirroring score
        mirroring_score = (pitch_deviation + energy_deviation + rate_deviation + centeredness_deviation) / 4
        # Display current metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pitch_color = "normal" if pitch_deviation < 0.2 else "inverse"
            st.metric("Current Pitch", f"{current_pitch:.1f} Hz", 
                     f"{current_pitch - baseline_pitch:+.1f}", delta_color=pitch_color)
        
        with col2:
            energy_color = "normal" if energy_deviation < 0.3 else "inverse"
            st.metric("Current Energy", f"{current_energy:.2f}", 
                     f"{current_energy - baseline_energy:+.2f}", delta_color=energy_color)
        
        with col3:
            rate_color = "normal" if rate_deviation < 0.2 else "inverse"
            st.metric("Current Rate", f"{current_rate:.0f} WPM", 
                     f"{current_rate - baseline_rate:+.0f}", delta_color=rate_color)
        
        with col4:
            center_color = "normal" if centeredness_deviation < 0.2 else "inverse"
            st.metric("Centeredness", f"{current_centeredness:.2f}", 
                     f"{current_centeredness - baseline_centeredness:+.2f}", delta_color=center_color)
        
        # Mirroring alert system
        if mirroring_score > 0.4:
            st.error("🚨 **HIGH MIRRORING DETECTED** - You may be adopting someone else's speaking style!")
        elif mirroring_score > 0.25:
            st.warning("⚠️ **Moderate mirroring detected** - Your voice is shifting from baseline")
        else:
            st.success("✅ **Authentic voice maintained** - You're speaking naturally")
        # Mirroring score gauge
        st.subheader("🎯 Voice Mirroring Score")
        mirroring_percentage = min(mirroring_score * 100, 100)
        
        # Create a visual gauge
        gauge_color = "🟢" if mirroring_percentage < 25 else "🟡" if mirroring_percentage < 40 else "🔴"
        st.write(f"{gauge_color} **{mirroring_percentage:.1f}%** mirroring detected")
        
        progress_bar = st.progress(mirroring_percentage / 100)
        
        # Auto-refresh for live monitoring
        time.sleep(2)
        st.rerun()
        
else:
    st.info("👆 Complete your baseline recording first to enable live monitoring")

st.divider()

# Challenge Scenarios Section
st.header("🎭 Step 3: Practice Scenarios")
st.write("Test your voice authenticity in challenging situations where mirroring commonly occurs")

if st.session_state.baseline_complete:
    scenario_options = [
        "🎤 Job Interview Pressure",
        "👔 Meeting with Authority Figure", 
        "🎉 Social Gathering",
        "📞 Important Phone Call",
        "💼 Client Presentation",
        "🤝 Networking Event"
    ]
    
    selected_scenario = st.selectbox("Choose a challenging scenario:", scenario_options)
    # Scenario descriptions and tips
    scenario_details = {
        "🎤 Job Interview Pressure": {
            "description": "You're in a high-stakes interview. The interviewer has a very formal, clipped speaking style.",
            "challenge": "Resist matching their overly formal tone while remaining professional",
            "tip": "Stay grounded in your natural speaking rhythm and warmth"
        },
        "👔 Meeting with Authority Figure": {
            "description": "Your boss speaks very quickly and with high energy during a performance review.",
            "challenge": "Don't speed up your speech or raise your energy unnaturally",
            "tip": "Maintain your natural pace to project confidence and authenticity"
        },
        "🎉 Social Gathering": {
            "description": "You're at a party where everyone is speaking loudly and using lots of slang.",
            "challenge": "Avoid adopting speech patterns that don't feel natural to you",
            "tip": "You can be social without losing your authentic voice"
        }
    }
    
    if selected_scenario in scenario_details:
        details = scenario_details[selected_scenario]
        
        st.write(f"**Scenario:** {details['description']}")
        st.write(f"**Challenge:** {details['challenge']}")
        st.write(f"**💡 Tip:** {details['tip']}")
        
        if st.button("🎯 Start Scenario Practice"):
            st.info("Scenario practice would integrate with live monitoring above!")

else:
    st.info("Complete your baseline recording to unlock practice scenarios")

    
    
