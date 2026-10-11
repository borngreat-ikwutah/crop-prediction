"""
Crop Disease Treatment Database
Contains Food and Agriculture Organization (FAO) and IITA/NRCRI recommendations
tailored for Cassava, Maize, and Tomato smallholders in Enugu and Southeastern Nigeria.
"""

TREATMENTS = {
    "Cassava_Mosaic": {
        "disease_name": "African Cassava Mosaic Disease (CMD)",
        "crop": "Cassava",
        "pathogen_type": "Viral (Begomovirus / Geminiviridae)",
        "vector": "Whitefly (Bemisia tabaci) and infected stem cuttings",
        "severity": "High",
        "symptoms": "Severe mosaic pattern, chlorosis, twisted/distorted leaflets, and stunted cassava tuber development.",
        "fao_advice": (
            "1. Roguing: Inspect cassava fields weekly during the first 2-3 months. Uproot and burn any infected plants immediately to prevent field transmission.\n"
            "2. Clean Planting Material: Use certified CMD-resistant stem cuttings from accredited sources (e.g. IITA / NRCRI Umudike varieties like TMS 30572, TMS 98/0505, or TME 419 / 'Obasanjo-2').\n"
            "3. Vector Control: Manage whitefly populations using organic neem seed oil extract (5ml per liter of water) or approved biopesticides sprayed in the early morning.\n"
            "4. Sanitation: Disinfect machetes and knives in a 10% bleach solution between cuttings to stop sap transmission."
        ),
        "short_treatment": "Uproot and burn infected plants immediately; plant certified resistant varieties (TMS 30572 / TME 419); spray neem extract to control whiteflies."
    },
    "Maize_Blight": {
        "disease_name": "Northern & Southern Corn Leaf Blight",
        "crop": "Maize",
        "pathogen_type": "Fungal (Exserohilum turcicum / Bipolaris maydis)",
        "vector": "Wind-borne and rain-splashed fungal spores, infected crop debris",
        "severity": "Medium-High",
        "symptoms": "Elongated, cigar-shaped grayish-green to tan necrotic lesions on leaves, leading to premature leaf death and reduced grain fill.",
        "fao_advice": (
            "1. Crop Rotation: Rotate maize with non-grass crops such as cowpea, groundnut, or soybean for at least 2 cropping seasons to break fungal lifecycle.\n"
            "2. Resistant Varieties: Plant certified blight-tolerant maize seeds (e.g. Oba Super 1, Oba Super 2, SAMMAZ series recommended for the Guinea savannah and rainforest transitions).\n"
            "3. Field Hygiene: Deep-plow or burn infected maize crop residues after harvest to bury fungal inoculum.\n"
            "4. Fungicide Application: In persistent humid conditions or high lesion incidence before silking, apply azoxystrobin or mancozeb according to package rates.\n"
            "5. Water Management: Avoid overhead watering; ensure adequate plant spacing (75cm x 25cm) for good ventilation."
        ),
        "short_treatment": "Rotate crops with legumes (cowpea/soybean); plant resistant hybrids (Oba Super); apply Mancozeb fungicide if humidity is high."
    },
    "Tomato_Early_Blight": {
        "disease_name": "Tomato Early Blight",
        "crop": "Tomato",
        "pathogen_type": "Fungal (Alternaria solani)",
        "vector": "Soil-borne spores, rain splash, wind, and infected seeds",
        "severity": "Medium-High",
        "symptoms": "Concentric rings ('target board' pattern) with yellow halos on older lower leaves, leaf drop, and collar rot on stems.",
        "fao_advice": (
            "1. Lower Leaf Pruning: Remove and safely discard lower leaves within 20cm of the soil to stop soil-splashed spores.\n"
            "2. Mulching: Apply a 5-8cm layer of dry grass, straw, or wood shavings around tomato bases to eliminate rain splash from soil.\n"
            "3. Staking & Trellising: Tie tomato vines to sturdy bamboo stakes to enhance sunlight penetration and accelerate leaf drying.\n"
            "4. Fungicide Intervention: Apply copper oxychloride, mancozeb, or chlorothalonil at the first sign of concentric lesions, repeating every 7-10 days in rainy weather.\n"
            "5. Crop Rotation: Avoid planting tomatoes following peppers, eggplants, or Irish potatoes for at least 3 years."
        ),
        "short_treatment": "Prune lower leaves touching soil; mulch around base to prevent rain splash; stake plants for airflow; apply copper-based fungicide or Mancozeb."
    },
    "Healthy": {
        "disease_name": "Healthy Crop Foliage",
        "crop": "Cassava / Maize / Tomato",
        "pathogen_type": "None",
        "vector": "N/A",
        "severity": "None",
        "symptoms": "Vibrant green color, intact leaf margins, normal venation, no lesions or chlorosis detected.",
        "fao_advice": (
            "1. Routine Scouting: Walk through the farm in a 'W' pattern twice weekly, checking leaf undersides for early pests or spore dust.\n"
            "2. Balanced Nutrition: Apply recommended split applications of balanced NPK fertilizer (e.g. 15:15:15 or 20:10:10) and well-cured compost.\n"
            "3. Soil Moisture: Maintain consistent soil moisture via drip or furrow irrigation without waterlogging root zones.\n"
            "4. Weed Control: Keep the field weed-free, particularly during the critical first 8 weeks of establishment."
        ),
        "short_treatment": "Crop is healthy! Maintain regular scouting, balanced organic/NPK nutrition, proper plant spacing, and clean weeding."
    },
}

LABELS = [
    "Cassava_Mosaic",
    "Maize_Blight",
    "Tomato_Early_Blight",
    "Healthy",
]


def get_treatment(disease_key: str) -> str:
    """Retrieve full FAO treatment advice text for a predicted disease key."""
    record = TREATMENTS.get(disease_key)
    if not record:
        return "Unknown crop disease. Consult the Enugu State Agricultural Development Programme (ENADEP) or an agricultural extension officer for field diagnosis."
    return record["fao_advice"]


def get_treatment_record(disease_key: str) -> dict:
    """Retrieve complete disease metadata record."""
    return TREATMENTS.get(
        disease_key,
        {
            "disease_name": disease_key,
            "crop": "Unknown",
            "pathogen_type": "Unknown",
            "vector": "Unknown",
            "severity": "Unknown",
            "symptoms": "Unknown",
            "fao_advice": "Consult an agricultural extension agent.",
            "short_treatment": "Consult an extension officer.",
        },
    )
