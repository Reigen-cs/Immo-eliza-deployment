import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Belgian Real Estate Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize dark mode state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Custom CSS for better styling with dark/light mode
def get_theme_css(dark_mode):
    if dark_mode:
        return """
        <style>
            .stApp {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            
            .main-header {
                background: linear-gradient(90deg, #3498db, #2980b9);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .hero-section {
                background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: white;
                text-align: center;
                padding: 4rem 2rem;
                border-radius: 15px;
                margin-bottom: 3rem;
            }
            
            .hero-title {
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
            
            .hero-subtitle {
                font-size: 1.5rem;
                margin-bottom: 0;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            }
            
            .prediction-result {
                background: linear-gradient(90deg, #27ae60, #2ecc71);
                color: white;
                padding: 1.5rem;
                border-radius: 10px;
                text-align: center;
                font-size: 1.2rem;
                margin: 1rem 0;
            }
            
            .error-message {
                background: #e74c3c;
                color: white;
                padding: 1rem;
                border-radius: 5px;
                margin: 1rem 0;
            }
            
            .info-box {
                background: #262730;
                color: #FAFAFA;
                padding: 1rem;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                margin: 1rem 0;
            }
            
            .metric-card {
                background: #262730;
                color: #FAFAFA;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                text-align: center;
            }
            
            .stButton > button {
                background: linear-gradient(90deg, #3498db, #2980b9) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.75rem 2rem !important;
                font-size: 1.1rem !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(90deg, #2980b9, #1f618d) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.4) !important;
            }
            
            .footer {
                background: #262730;
                color: white;
                padding: 2rem;
                border-radius: 10px;
                text-align: center;
                margin-top: 3rem;
            }
            
            .footer h3 {
                margin-bottom: 1rem;
                color: #3498db;
            }
            
            .footer p {
                margin: 0.5rem 0;
                opacity: 0.9;
            }
            
            .theme-toggle {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 999;
                background: #262730;
                border: 2px solid #3498db;
                border-radius: 25px;
                padding: 8px 16px;
                display: flex;
                align-items: center;
                gap: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .theme-toggle:hover {
                background: #3498db;
                transform: scale(1.05);
            }
            
            .theme-toggle-text {
                color: #FAFAFA;
                font-size: 14px;
                font-weight: bold;
            }
            
            .sidebar .stSelectbox label, .sidebar .stNumberInput label, .sidebar .stTextInput label {
                color: #FAFAFA !important;
            }
        </style>
        """
    else:
        return """
        <style>
            .stApp {
                background-color: #FFFFFF;
                color: #262730;
            }
            
            .main-header {
                background: linear-gradient(90deg, #3498db, #2980b9);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .hero-section {
                background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: white;
                text-align: center;
                padding: 4rem 2rem;
                border-radius: 15px;
                margin-bottom: 3rem;
            }
            
            .hero-title {
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }
            
            .hero-subtitle {
                font-size: 1.5rem;
                margin-bottom: 0;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            }
            
            .prediction-result {
                background: linear-gradient(90deg, #27ae60, #2ecc71);
                color: white;
                padding: 1.5rem;
                border-radius: 10px;
                text-align: center;
                font-size: 1.2rem;
                margin: 1rem 0;
            }
            
            .error-message {
                background: #e74c3c;
                color: white;
                padding: 1rem;
                border-radius: 5px;
                margin: 1rem 0;
            }
            
            .info-box {
                background: #ecf0f1;
                padding: 1rem;
                border-radius: 5px;
                border-left: 4px solid #3498db;
                margin: 1rem 0;
            }
            
            .metric-card {
                background: white;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            .stButton > button {
                background: linear-gradient(90deg, #3498db, #2980b9) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.75rem 2rem !important;
                font-size: 1.1rem !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(90deg, #2980b9, #1f618d) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
            }
            
            .footer {
                background: #34495e;
                color: white;
                padding: 2rem;
                border-radius: 10px;
                text-align: center;
                margin-top: 3rem;
            }
            
            .footer h3 {
                margin-bottom: 1rem;
                color: #3498db;
            }
            
            .footer p {
                margin: 0.5rem 0;
                opacity: 0.9;
            }
            
            .theme-toggle {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 999;
                background: white;
                border: 2px solid #3498db;
                border-radius: 25px;
                padding: 8px 16px;
                display: flex;
                align-items: center;
                gap: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .theme-toggle:hover {
                background: #3498db;
                transform: scale(1.05);
            }
            
            .theme-toggle-text {
                color: #262730;
                font-size: 14px;
                font-weight: bold;
            }
            
            .theme-toggle:hover .theme-toggle-text {
                color: white;
            }
        </style>
        """

st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Configuration
API_BASE_URL = "https://immo-eliza-deployment-01ya.onrender.com"  

# Helper functions
def check_api_health():
    """Check if the API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except requests.RequestException as e:
        return False, str(e)

def make_prediction(data):
    """Make a prediction request to the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return False, f"Connection Error: {str(e)}"

# Main app
def main():
    # Theme toggle button
    theme_col1, theme_col2 = st.columns([6, 1])
    with theme_col2:
        if st.button(f"{'🌙' if not st.session_state.dark_mode else '☀️'} {'Dark' if not st.session_state.dark_mode else 'Light'}", 
                    key="theme_toggle", 
                    help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Hero Header with Background Image
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">House Price Prediction Using</div>
        <div class="hero-subtitle">Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Health Check
    with st.sidebar:
        st.subheader("🔧 API Status")
        health_status, health_data = check_api_health()
        
        if health_status:
            st.success("✅ API is healthy")
            if health_data:
                st.json(health_data)
        else:
            st.error("❌ API is not responding")
            st.write(f"Error: {health_data}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Property Information")
        
        # Property basics
        st.write("**Basic Information**")
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            property_type = st.selectbox(
                "Property Type",
                ["APARTMENT", "HOUSE"],
                help="Select the type of property"
            )
            
            bedrooms = st.number_input(
                "Number of Bedrooms",
                min_value=0,
                max_value=20,
                value=2,
                help="Number of bedrooms in the property"
            )
            
            bathrooms = st.number_input(
                "Number of Bathrooms",
                min_value=0,
                max_value=10,
                value=1,
                help="Number of bathrooms"
            )
        
        with col1_2:
            habitable_surface = st.number_input(
                "Habitable Surface (m²)",
                min_value=0,
                max_value=1000,
                value=85,
                help="Living space area in square meters"
            )
            
            province = st.selectbox(
                "Province",
                ["Brussels", "Antwerp", "East Flanders", "West Flanders", "Flemish Brabant", 
                 "Walloon Brabant", "Hainaut", "Liège", "Luxembourg", "Namur", "Limburg"],
                index=0,
                help="Belgian province where the property is located"
            )
            
            postal_code = st.text_input(
                "Postal Code",
                value="1000",
                help="Postal code of the property"
            )
        
        # Energy and additional features
        st.write("**Energy & Features**")
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            epc_score = st.selectbox(
                "EPC Score",
                ["A+", "A", "B", "C", "D", "E", "F", "G"],
                index=2,
                help="Energy Performance Certificate score"
            )
            
            toilets = st.number_input("Number of Toilets", min_value=0, max_value=5, value=1)
            terrace_surface = st.number_input("Terrace Surface (m²)", min_value=0, max_value=200, value=0)
            garden_surface = st.number_input("Garden Surface (m²)", min_value=0, max_value=2000, value=0)
        
        with col2_2:
            # Boolean features
            has_garden = st.checkbox("Has Garden", value=False)
            has_terrace = st.checkbox("Has Terrace", value=False)
            has_fireplace = st.checkbox("Has Fireplace", value=False)
            has_living_room = st.checkbox("Has Living Room", value=True)
        
        # Advanced features (expandable)
        with st.expander("🔧 Advanced Features"):
            col3_1, col3_2 = st.columns(2)
            
            with col3_1:
                has_attic = st.checkbox("Has Attic", value=False)
                has_basement = st.checkbox("Has Basement", value=False)
                has_office = st.checkbox("Has Office", value=False)
                has_dining_room = st.checkbox("Has Dining Room", value=False)
                has_dressing_room = st.checkbox("Has Dressing Room", value=False)
                has_lift = st.checkbox("Has Lift/Elevator", value=False)
            
            with col3_2:
                has_swimming_pool = st.checkbox("Has Swimming Pool", value=False)
                has_air_conditioning = st.checkbox("Has Air Conditioning", value=False)
                has_armored_door = st.checkbox("Has Armored Door", value=False)
                has_visiophone = st.checkbox("Has Visiophone", value=False)
                has_heat_pump = st.checkbox("Has Heat Pump", value=False)
                has_photovoltaic = st.checkbox("Has Solar Panels", value=False)
        
        # Prediction button
        if st.button("🔮 Get Price Prediction", type="primary", use_container_width=True):
            # Prepare data for API
            prediction_data = {
                "type": property_type,
                "bedroomCount": bedrooms,
                "bathroomCount": bathrooms,
                "habitableSurface": habitable_surface,
                "province": province,
                "postCode": postal_code,
                "epcScore": epc_score,
                "toiletCount": toilets,
                "terraceSurface": terrace_surface if terrace_surface > 0 else None,
                "gardenSurface": garden_surface if garden_surface > 0 else None,
                "hasGarden": has_garden,
                "hasTerrace": has_terrace,
                "hasFireplace": has_fireplace,
                "hasLivingRoom": has_living_room,
                "hasAttic": has_attic,
                "hasBasement": has_basement,
                "hasOffice": has_office,
                "hasDiningRoom": has_dining_room,
                "hasDressingRoom": has_dressing_room,
                "hasLift": has_lift,
                "hasSwimmingPool": has_swimming_pool,
                "hasAirConditioning": has_air_conditioning,
                "hasArmoredDoor": has_armored_door,
                "hasVisiophone": has_visiophone,
                "hasHeatPump": has_heat_pump,
                "hasPhotovoltaicPanels": has_photovoltaic,
            }
            
            # Remove None values
            prediction_data = {k: v for k, v in prediction_data.items() if v is not None}
            
            # Make prediction
            with st.spinner("🔄 Making prediction..."):
                success, result = make_prediction(prediction_data)
                
                if success:
                    predicted_price = result.get("predicted_price", 0)
                    st.markdown(f"""
                    <div class="prediction-result">
                        <h2>🎯 Predicted Price</h2>
                        <h1>€{predicted_price:,.2f}</h1>
                        <p>Currency: {result.get('currency', 'EUR')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show additional info
                    st.success(f"✅ Prediction completed at {result.get('timestamp', 'N/A')}")
                    
                    # Show input summary
                    if 'input_summary' in result:
                        st.write("**Input Summary:**")
                        st.json(result['input_summary'])
                    
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        <h3>❌ Prediction Failed</h3>
                        <p>{result}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        
        st.markdown("""
        <div class="info-box">
            <h4>💡 Tips for Better Predictions</h4>
            <ul>
                <li>Provide accurate surface area information</li>
                <li>Select the correct province</li>
                <li>Include all available features</li>
                <li>Ensure postal code is valid</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Price ranges by province (example data)
        st.write("**Average Price Ranges by Province**")
        price_data = {
            "Province": ["Brussels", "Antwerp", "East Flanders", "West Flanders", "Flemish Brabant"],
            "Avg Price (€)": [350000, 280000, 250000, 220000, 320000]
        }
        
        df = pd.DataFrame(price_data)
        st.dataframe(df, use_container_width=True)
        
        # API Information
        st.write("**API Information**")
        st.info(f"API Endpoint: {API_BASE_URL}")
        
        if st.button("🔄 Refresh API Status"):
            st.rerun()

    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🏠 Belgian Real Estate Price Predictor</h3>
        <p>Powered by Machine Learning</p>
        <p>Built with Streamlit & FastAPI</p>
        <p><strong>Made by Floriane, Hanieh and Younes</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()