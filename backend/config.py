import os
from pathlib import Path

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent
ONTOLOGY_DIR = BASE_DIR / "ontology"
ONTOLOGY_FILE = ONTOLOGY_DIR / "SmartCompareMarket.owl"

# Configuración del razonador
REASONER_CONFIG = {
    "name": "Pellet",
    "infer_property_values": True,
    "infer_data_property_values": True,
    "debug": False
}

# Configuración Flask
FLASK_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True
}

# CORS
# CORS
CORS_ORIGINS = ["*"]

# Namespace de la ontología
ONTOLOGY_IRI = "http://smartcompare.com/ontologia#"
