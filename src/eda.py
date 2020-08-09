from typing import Dict, List

from manga109.typing import Page


def count_bodies(pages: List[Page]) -> Dict[str, int]:
    bodies: Dict[str, int] = {}
    for page in pages:
        for body in page.bodies:
            if body.character not in bodies:
                bodies[body.character] = 1
            else:
                bodies[body.character] += 1
    return bodies


def count_faces(pages: List[Page]) -> Dict[str, int]:
    faces: Dict[str, int] = {}
    for page in pages:
        for face in page.faces:
            if face.character not in faces:
                faces[face.character] = 1
            else:
                faces[face.character] += 1
    return faces
