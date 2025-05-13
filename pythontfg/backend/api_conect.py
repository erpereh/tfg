
def buscar_mensajes(selected_red_social: str) -> list:
    match selected_red_social:
        case "instagram":
            return recargar_instagram()
        case "twitter":
            return recargar_twitter()
        case "facebook":
            return recargar_facebook()
        case "linkedin":
            return recargar_linkedin()
        case _:
            print("Red social no reconocida.")
            return []

def recargar_instagram() -> list:
    print("Recargando mensajes de Instagram...")
    return []

def recargar_twitter() -> list:
    print("Recargando mensajes de Twitter...")
    return []

def recargar_facebook() -> list:
    print("Recargando mensajes de Facebook...")
    return []

def recargar_linkedin() -> list:
    print("Recargando mensajes de LinkedIn...")
    return []
