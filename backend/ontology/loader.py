from owlready2 import *
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config

# Importar razonadores
from owlready2 import sync_reasoner_pellet

class OntologyLoader:
    """Carga y gestiona la ontología SmartCompareMarket con razonamiento SWRL"""
    
    def __init__(self):
        self.onto = None
        self.world = None
        
    def load(self):
        """Carga la ontología desde el archivo OWL"""
        try:
            # Crear world aislado
            self.world = World()
            
            # Cargar ontología
            onto_path = str(config.ONTOLOGY_FILE)
            self.onto = self.world.get_ontology(f"file://{onto_path}").load()
            
            print(f"[OK] Ontologia cargada: {self.onto.name}")
            print(f"   - Clases: {len(list(self.onto.classes()))}")
            print(f"   - Individuos: {len(list(self.onto.individuals()))}")
            print(f"   - Object Properties: {len(list(self.onto.object_properties()))}")
            print(f"   - Data Properties: {len(list(self.onto.data_properties()))}")

            return self.onto

        except Exception as e:
            print(f"[ERROR] Error cargando ontologia: {e}")
            raise
    
    def run_reasoner(self):
        """Ejecuta el razonador Pellet con soporte SWRL"""
        try:
            print("[REASONER] Ejecutando razonador Pellet...")

            # Ejecutar razonador con inferencias
            with self.onto:
                sync_reasoner_pellet(
                    infer_property_values=config.REASONER_CONFIG["infer_property_values"],
                    debug=config.REASONER_CONFIG["debug"]
                )

            print("[OK] Razonador Pellet ejecutado exitosamente")
            print("   [SWRL] Reglas SWRL que deberian aplicarse:")
            print("      1. DetectarGamer (RAM >= 16GB -> LaptopGamer)")
            print("      2. EncontrarMejorPrecio (precio menor -> esMejorOpcionQue)")
            print("      3. ClasificarPositivas (cal >= 4 -> Resena_Positiva)")
            print("      4. ClasificarNegativas (cal <= 2 -> Resena_Negativa)")

        except Exception as e:
            print(f"[ERROR] Error ejecutando razonador: {e}")
            raise
    
    def save_inferred(self, output_path=None):
        """Guarda la ontología con inferencias"""
        if output_path is None:
            output_path = config.ONTOLOGY_DIR / "SmartCompareMarket_inferred.owl"

        self.onto.save(file=str(output_path))
        print(f"[SAVE] Ontologia inferida guardada en: {output_path}")

# Singleton global
_ontology_loader = None

def get_ontology():
    """Obtiene la instancia singleton del loader"""
    global _ontology_loader
    if _ontology_loader is None:
        _ontology_loader = OntologyLoader()
        _ontology_loader.load()
        _ontology_loader.run_reasoner()
    return _ontology_loader.onto
