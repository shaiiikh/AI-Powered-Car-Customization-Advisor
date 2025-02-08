# car_customization.py

def get_customization_suggestions(transcription):
    suggestions = []

    # Define keywords and corresponding suggestions
    keywords = {
        "paint": "Consider a custom paint job to make your car stand out!",
        "interior": "Upgrade your car's interior with luxury leather seats and a high-end sound system.",
        "wheels": "You might want to install custom alloy wheels for a sleek look.",
        "roof": "A panoramic sunroof could enhance the driving experience.",
        "engine": "Consider tuning your engine for improved performance.",
        "lights": "Upgrade to LED or neon underglow lighting for a futuristic look.",
        "sound system": "Enhance your car with a premium sound system.",
        "exhaust": "Upgrade your exhaust system for a more powerful sound and performance.",
        "windows": "Tint your windows for privacy and a sleek, modern touch.",
        "dashboard": "Enhance your dashboard with a digital display or heads-up display (HUD)."
    }

    # Check transcription for keywords
    for word, suggestion in keywords.items():
        if word in transcription.lower():
            suggestions.append(suggestion)

    # Return suggestions if found, else return a default message
    return "\n".join(suggestions) if suggestions else "No specific customizations detected."
