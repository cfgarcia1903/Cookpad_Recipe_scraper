import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import quote

def scrape_recipe(recipe_name: str) -> Dict[str, List[str]]:
    """
    Scrapes a recipe from the Cookpad website by searching for the recipe name 
    and extracting the title, ingredients, and instructions from the first recipe found.
    
    Args:
        recipe_name (str): The name of the recipe to search for on Cookpad.

    Returns:
        Dict[str, List[str]]: A dictionary containing the recipe title, 
                               ingredients, and instructions.
                               - "title" (str): The recipe title.
                               - "ingredients" (List[str]): A list of ingredients.
                               - "instructions" (List[str]): A list of instructions.
    
    Raises:
        Exception: If there is an error accessing the recipe page.
    """ 
    # Perform a Google search with the recipe name and limit to Cookpad site
    quoted_name=quote(recipe_name)
    country='pe'  #Peru
    search_url= f"https://cookpad.com/{country}/buscar/{quoted_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)",
    }

    resp = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")

    for link in soup.find_all("a", href=True):
        if f"/recetas/" in link['href'] and f"/recetas/nuevo" not in link['href']:
            print("https://cookpad.com" + link['href'])
            recipe_url = "https://cookpad.com" + link['href']
            break
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    res = requests.get(recipe_url, headers=headers)
    
    if res.status_code != 200:
        raise Exception(f"Error accesing recipe: code {res.status_code}")
    
    soup = BeautifulSoup(res.content, "html.parser")
    
    # Title
    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "Title not found"
    
    # Ingredients
    ingredients = []
    ingredient_section = soup.find_all("li", class_="py-sm border-b last:border-0 border-cookpad-gray-300 border-dashed")
    if ingredient_section:
        for li in ingredient_section:
            ingredients.append(li.text.strip())
    
    ## Instrucciones         This also gets the dish description by accident
    #instructions = []
    #instruction_section = soup.find_all("div", {"dir": "auto"})
    #for section in instruction_section:
    #    # Ahora buscar el <p> dentro de cada div con dir="auto" y clase mb-sm overflow-wrap-anywhere
    #    step_section = section.find_all("p", class_="mb-sm overflow-wrap-anywhere")
    #    for step in step_section:
    #        instructions.append(step.text.strip())

    # Instructions
    instructions = []
    step_section = soup.find_all("li", class_="step")
    for step in step_section:
        instruction_text = step.find("div", {"dir": "auto"})
        if instruction_text:
            p_tag = instruction_text.find("p", class_="mb-sm overflow-wrap-anywhere")
            if p_tag:
                instructions.append(p_tag.text.strip())    


    return {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions,
    }
    
if __name__ == "__main__":
    
    recipe=scrape_recipe('arroz chaufa')
    print(recipe['title'])
    print(recipe['ingredients'])       
    print(recipe['instructions'])

