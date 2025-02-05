# car_customization.py

# Function to get car customization suggestions based on transcription
def get_customization_suggestions(transcription):
    # Predefined templates or logic to generate suggestions
    suggestions = []

    # Example logic: If the transcription mentions specific car parts, generate suggestions accordingly
    if "paint" in transcription:
        suggestions.append("Consider a custom paint job to make your car stand out!")
    if "interior" in transcription:
        suggestions.append("Upgrade your car's interior with luxury leather seats and a high-end sound system.")
    if "wheels" in transcription:
        suggestions.append("You might want to install custom alloy wheels for a sleek look.")
    if "roof" in transcription:
        suggestions.append("A panoramic sunroof could enhance the driving experience.")
    if "engine" in transcription:
        suggestions.append("Consider tuning your engine for improved performance.")

    # If no specific customization is found, suggest a general option
    if not suggestions:
        suggestions.append("Let’s start with a custom paint job or interior upgrade!")

    # Join the suggestions into a formatted string to display
    return "\n".join(suggestions)
