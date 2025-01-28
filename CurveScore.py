import numpy as np

class CurveScore:
    def __init__(self):
        pass

    def curveScore(self, x_coords, y_coords):
        if len(x_coords) < 2:
            return 

        total_distance = sum(
            np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            for x1, y1, x2, y2 in zip(x_coords[:-1], y_coords[:-1], x_coords[1:], y_coords[1:])
        )
        
        straight_line_distance = np.sqrt((x_coords[-1] - x_coords[0])**2 + (y_coords[-1] - y_coords[0])**2)
        
        if total_distance == 0:
            return 0

        path_efficiency = 1 - (straight_line_distance / total_distance)
        
        angles = []
        for i in range(1, len(x_coords) - 1):
            v1 = (x_coords[i] - x_coords[i-1], y_coords[i] - y_coords[i-1])
            v2 = (x_coords[i+1] - x_coords[i], y_coords[i+1] - y_coords[i])
            
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            angle = np.arccos(dot_product / (norm_v1 * norm_v2 + 1e-9))
            angles.append(abs(angle))
        
        angular_change_score = sum(angles) / len(angles) if angles else 0
        
        curviness_score = path_efficiency + angular_change_score
        return curviness_score