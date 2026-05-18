import ezdxf
from ezdxf import units
import math
import os
from datetime import datetime

class DXFBuilder:
    def __init__(self):
        self.output_dir = "output_dxf"
        os.makedirs(self.output_dir, exist_ok=True)

    def build_dxf(self, data: dict, nome_pezzo: str = "Pezzo") -> str:
        doc = ezdxf.new(dxfversion="R2018")
        doc.units = units.MM
        msp = doc.modelspace()

        x = y = 0.0
        angle = 0.0

        for elem in data.get("segmenti", []):
            if elem["tipo"] == "linea":
                lunghezza = float(elem.get("lunghezza", 100))
                rad = math.radians(angle)
                x2 = x + lunghezza * math.cos(rad)
                y2 = y + lunghezza * math.sin(rad)
                msp.add_line((x, y), (x2, y2))
                x, y = x2, y2
            elif elem["tipo"] == "piega":
                angle += float(elem.get("angolo", 90))

        filepath = os.path.join(self.output_dir, f"{nome_pezzo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dxf")
        doc.saveas(filepath)
        return filepath
