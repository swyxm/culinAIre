from openai import OpenAI
from django.http import JsonResponse
from django.db import models
from .models import flavorMetrics
import json

client = OpenAI()
weighting = []

def analyzeFlavor(mealName, review, rating):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": """You are a culinary and flavor expert. Your task is to evaluate a dish you are given across 7 metrics: 
                    Sweetness, Saltiness, Spiciness, Sourness, Bitterness, Tanginess, Richness (How flavorful/creamy/heavy it is). 
                    You will evaluate these metrics with a number from 0 to 10.  Base this evaluation on how dominant a specific 
                    flavor aspect is in the dish. i.e., Butter Chicken would be higher on the spiciness, tanginess, and richness metrics. 
                    Strictly avoid jumping to the edge cases of 0 to 10 or giving each category the same number unless absolutely necessary. 
                    Honestly evaluate the nuances of the flavor profile of the dish. In many cases, you will have to guess all the ingredients
                    used. In that case, just make an educated guess. Format your response with the 7 numbers space-seperated. That is all."""
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"Dish: {mealName} Additional Context: {review} "
            }
        ]
        }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )


    responseString = response.choices[0].message.content.strip()
    print(responseString)
    weightedMetrics = list(map(float, responseString.split()))
    weightedMetrics = [metric * (rating / 10) for metric in weightedMetrics]
    
    # Retrieve or create the cumulative metrics record
    cumulativeMetrics, created = flavorMetrics.objects.get_or_create(id=1)

    # Update cumulative sums and increment count
    cumulativeMetrics.sweetness += weightedMetrics[0]
    cumulativeMetrics.saltiness += weightedMetrics[1]
    cumulativeMetrics.spiciness += weightedMetrics[2]
    cumulativeMetrics.sourness += weightedMetrics[3]
    cumulativeMetrics.bitterness += weightedMetrics[4]
    cumulativeMetrics.tanginess += weightedMetrics[5]
    cumulativeMetrics.richness += weightedMetrics[6]
    cumulativeMetrics.count += 1

    # Save the updated record
    cumulativeMetrics.save()

    # Calculate averages
    avgMetrics = [
        cumulativeMetrics.sweetness / cumulativeMetrics.count,
        cumulativeMetrics.saltiness / cumulativeMetrics.count,
        cumulativeMetrics.spiciness / cumulativeMetrics.count,
        cumulativeMetrics.sourness / cumulativeMetrics.count,
        cumulativeMetrics.bitterness / cumulativeMetrics.count,
        cumulativeMetrics.tanginess / cumulativeMetrics.count,
        cumulativeMetrics.richness / cumulativeMetrics.count,
    ]

    print(avgMetrics)
    print(cumulativeMetrics.count)
    print(cumulativeMetrics.count)
    # Return response with the current weighted metrics and overall averages
    return JsonResponse({
        'flavorProfile': weightedMetrics,
        'responseString': responseString,
        'avgMetrics': avgMetrics
    })
