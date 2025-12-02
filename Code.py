mport discord # type: ignore
from discord.ext import commands # type: ignore
from discord.ui import Button, View, Select # type: ignore
import random
import asyncio

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Database de Pokémons
POKEMONS = {
    # Fire Type
    "Charizard": {"hp": 300, "atk": 42, "defense": 78, "spd": 100, "type": "Fire", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png", "moves": ["Flamethrower", "Earthquake", "Dragon Claw"], "mega": True, "mega_multiplier": 2.0},
    "Arcanine": {"hp": 300, "atk": 55, "defense": 80, "spd": 100, "type": "Fire", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/59.png", "moves": ["Wild Charge", "Crunch", "Flare Blitz"], "mega": False},
    "Moltres": {"hp": 300, "atk": 50, "defense": 90, "spd": 90, "type": "Fire", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/146.png", "moves": ["Sky Attack", "Flamethrower", "Roost"], "mega": False},
    "Typhlosion": {"hp": 300, "atk": 42, "defense": 78, "spd": 100, "type": "Fire", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/157.png", "moves": ["Eruption", "Flamethrower", "Focus Blast"], "mega": False},
    "Entei": {"hp": 300, "atk": 56, "defense": 88, "spd": 100, "type": "Fire", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/244.png", "moves": ["Sacred Fire", "Extreme Speed", "Stone Edge"], "mega": False},
    
    # Water Type
    "Blastoise": {"hp": 300, "atk": 42, "defense": 100, "spd": 78, "type": "Water", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png", "moves": ["Hydro Cannon", "Ice Beam", "Earthquake"], "mega": True, "mega_multiplier": 2.0},
    "Lapras": {"hp": 300, "atk": 43, "defense": 80, "spd": 60, "type": "Water", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/131.png", "moves": ["Hydro Pump", "Ice Beam", "Thunderbolt"], "mega": False},
    "Articuno": {"hp": 300, "atk": 43, "defense": 100, "spd": 85, "type": "Water", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/144.png", "moves": ["Hurricane", "Blizzard", "Roost"], "mega": False},
    "Feraligatr": {"hp": 300, "atk": 53, "defense": 100, "spd": 78, "type": "Water", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/160.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/160.png", "moves": ["Waterfall", "Crunch", "Dragon Dance"], "mega": True, "mega_multiplier": 2.0},
    "Suicune": {"hp": 300, "atk": 38, "defense": 115, "spd": 85, "type": "Water", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/245.png", "moves": ["Hydro Pump", "Ice Beam", "Calm Mind"], "mega": False},
    
    # Grass Type
    "Venusaur": {"hp": 300, "atk": 41, "defense": 83, "spd": 80, "type": "Grass", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png", "moves": ["Solar Beam", "Sludge Bomb", "Synthesis"], "mega": True, "mega_multiplier": 2.0},
    "Exeggutor": {"hp": 300, "atk": 48, "defense": 85, "spd": 55, "type": "Grass", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/103.png", "moves": ["Psychic", "Solar Beam", "Wood Hammer"], "mega": False},
    "Vileplume": {"hp": 300, "atk": 40, "defense": 85, "spd": 50, "type": "Grass", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/45.png", "moves": ["Solar Beam", "Sludge Bomb", "Synthesis"], "mega": False},
    "Victreebel": {"hp": 300, "atk": 53, "defense": 65, "spd": 72, "type": "Grass", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/71.png", "moves": ["Solar Beam", "Sludge Bomb", "Weather Ball"], "mega": False},
    "Meganium": {"hp": 300, "atk": 41, "defense": 100, "spd": 80, "type": "Grass", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/154.png", "moves": ["Solar Beam", "Earthquake", "Light Screen"], "mega": False},    # Electric Type
    "Pikachu": {"hp": 300, "atk": 28, "defense": 40, "spd": 90, "type": "Electric", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png", "moves": ["Thunderbolt", "Quick Attack", "Thunder Wave"], "mega": False},
    "Zapdos": {"hp": 300, "atk": 45, "defense": 85, "spd": 100, "type": "Electric", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/145.png", "moves": ["Thunderbolt", "Sky Attack", "Roost"], "mega": False},
    "Electabuzz": {"hp": 300, "atk": 42, "defense": 57, "spd": 105, "type": "Electric", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/125.png", "moves": ["Thunderbolt", "Fire Punch", "Cross Chop"], "mega": False},
    "Ampharos": {"hp": 300, "atk": 38, "defense": 85, "spd": 55, "type": "Electric", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/181.png", "moves": ["Power Gem", "Thunderbolt", "Focus Blast"], "mega": False},
    "Raichu": {"hp": 300, "atk": 45, "defense": 55, "spd": 100, "type": "Electric", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png", "moves": ["Thunderbolt", "Surf", "Earthquake"], "mega": False},
    
    # Ice Type
    "Articuno": {"hp": 300, "atk": 43, "defense": 100, "spd": 85, "type": "Ice", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/144.png", "moves": ["Hurricane", "Blizzard", "Roost"], "mega": False},
    "Lapras": {"hp": 300, "atk": 43, "defense": 80, "spd": 60, "type": "Ice", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/131.png", "moves": ["Hydro Pump", "Ice Beam", "Thunderbolt"], "mega": False},
    "Seel": {"hp": 300, "atk": 23, "defense": 55, "spd": 45, "type": "Ice", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/86.png", "moves": ["Ice Beam", "Aurora Beam", "Horn Drill"], "mega": False},
    "Dewgong": {"hp": 300, "atk": 40, "defense": 70, "spd": 70, "type": "Ice", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/87.png", "moves": ["Ice Beam", "Aurora Beam", "Rest"], "mega": False},
    "Slowbro": {"hp": 300, "atk": 38, "defense": 110, "spd": 30, "type": "Ice", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/80.png", "moves": ["Psychic", "Ice Beam", "Surf"], "mega": False},
    
    # Fighting Type
    "Machamp": {"hp": 300, "atk": 65, "defense": 80, "spd": 55, "type": "Fighting", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/68.png", "moves": ["Dynamic Punch", "Stone Edge", "Bullet Punch"], "mega": False},
    "Primeape": {"hp": 300, "atk": 53, "defense": 60, "spd": 95, "type": "Fighting", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/57.png", "moves": ["Close Combat", "Stone Edge", "U-turn"], "mega": False},
    "Poliwrath": {"hp": 300, "atk": 48, "defense": 95, "spd": 70, "type": "Fighting", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/62.png", "moves": ["Close Combat", "Waterfall", "Focus Punch"], "mega": False},
    "Hitmonlee": {"hp": 300, "atk": 60, "defense": 53, "spd": 87, "type": "Fighting", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/106.png", "moves": ["High Jump Kick", "Stone Edge", "Earthquake"], "mega": False},
    "Hitmonchan": {"hp": 300, "atk": 53, "defense": 79, "spd": 76, "type": "Fighting", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/107.png", "moves": ["Mach Punch", "Ice Punch", "Fire Punch"], "mega": False},
    
    # Poison Type
    "Weezing": {"hp": 300, "atk": 45, "defense": 95, "spd": 60, "type": "Poison", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/110.png", "moves": ["Sludge Bomb", "Toxic Spikes", "Explosion"], "mega": False},
    "Arbok": {"hp": 300, "atk": 48, "defense": 69, "spd": 80, "type": "Poison", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/24.png", "moves": ["Sludge Bomb", "Crunch", "Earthquake"], "mega": False},
    "Vileplume": {"hp": 300, "atk": 40, "defense": 85, "spd": 50, "type": "Poison", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/45.png", "moves": ["Solar Beam", "Sludge Bomb", "Synthesis"], "mega": False},
    "Crobat": {"hp": 300, "atk": 45, "defense": 80, "spd": 130, "type": "Poison", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/169.png", "moves": ["Cross Poison", "Acrobatics", "Brave Bird"], "mega": False},
    "Muk": {"hp": 300, "atk": 53, "defense": 75, "spd": 40, "type": "Poison", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/89.png", "moves": ["Sludge Bomb", "Gunk Shot", "Earthquake"], "mega": False},
    
    # Ground Type
    "Rhyhorn": {"hp": 300, "atk": 55, "defense": 85, "spd": 40, "type": "Ground", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/111.png", "moves": ["Earthquake", "Stone Edge", "Megahorn"], "mega": False},
    "Rhydon": {"hp": 300, "atk": 65, "defense": 100, "spd": 40, "type": "Ground", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/112.png", "moves": ["Earthquake", "Stone Edge", "Megahorn"], "mega": False},
    "Cubone": {"hp": 300, "atk": 38, "defense": 85, "spd": 35, "type": "Ground", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/104.png", "moves": ["Earthquake", "Stone Edge", "Fire Punch"], "mega": False},
    "Marowak": {"hp": 300, "atk": 50, "defense": 110, "spd": 45, "type": "Ground", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/105.png", "moves": ["Earthquake", "Stone Edge", "Bonemerang"], "mega": False},
    "Sandslash": {"hp": 300, "atk": 50, "defense": 110, "spd": 65, "type": "Ground", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/28.png", "moves": ["Earthquake", "Stone Edge", "Swords Dance"], "mega": False},
    
    # Flying Type
    "Pidgeot": {"hp": 300, "atk": 40, "defense": 75, "spd": 91, "type": "Flying", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/18.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/18.png", "moves": ["Brave Bird", "U-turn", "Defog"], "mega": True, "mega_multiplier": 2.0},
    "Farfetchd": {"hp": 300, "atk": 45, "defense": 55, "spd": 60, "type": "Flying", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/83.png", "moves": ["Brave Bird", "Knock Off", "Swords Dance"], "mega": False},
    "Dodrio": {"hp": 300, "atk": 55, "defense": 70, "spd": 100, "type": "Flying", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/85.png", "moves": ["Brave Bird", "Earthquake", "Stone Edge"], "mega": False},
    "Aerodactyl": {"hp": 300, "atk": 53, "defense": 65, "spd": 130, "type": "Flying", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/142.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/142.png", "moves": ["Stone Edge", "Earthquake", "Brave Bird"], "mega": True, "mega_multiplier": 2.0},
    "Dragonite": {"hp": 300, "atk": 67, "defense": 95, "spd": 80, "type": "Flying", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png", "moves": ["Outrage", "Earthquake", "Dragon Dance"], "mega": True, "mega_multiplier": 2.0},    # Psychic Type
    "Alakazam": {"hp": 300, "atk": 25, "defense": 65, "spd": 120, "type": "Psychic", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/65.png", "moves": ["Psychic", "Focus Blast", "Dazzling Gleam"], "mega": True, "mega_multiplier": 2.0},
    "Slowbro": {"hp": 300, "atk": 38, "defense": 110, "spd": 30, "type": "Psychic", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/80.png", "moves": ["Psychic", "Ice Beam", "Surf"], "mega": False},
    "Jynx": {"hp": 300, "atk": 25, "defense": 35, "spd": 95, "type": "Psychic", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/124.png", "moves": ["Psychic", "Focus Blast", "Dazzling Gleam"], "mega": False},
    "Mr. Mime": {"hp": 300, "atk": 23, "defense": 65, "spd": 90, "type": "Psychic", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/122.png", "moves": ["Psychic", "Focus Blast", "Dazzling Gleam"], "mega": False},
    "Espeon": {"hp": 300, "atk": 33, "defense": 65, "spd": 110, "type": "Psychic", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/196.png", "moves": ["Psychic", "Focus Blast", "Dazzling Gleam"], "mega": False},
    
    # Bug Type
    "Scyther": {"hp": 300, "atk": 55, "defense": 80, "spd": 105, "type": "Bug", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/123.png", "moves": ["X-Scissor", "Superpower", "Swords Dance"], "mega": False},
    "Butterfree": {"hp": 300, "atk": 28, "defense": 50, "spd": 95, "type": "Bug", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/12.png", "moves": ["Bug Buzz", "Dazzling Gleam", "Sleep Powder"], "mega": False},
    "Beedrill": {"hp": 300, "atk": 45, "defense": 40, "spd": 75, "type": "Bug", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/15.png", "moves": ["X-Scissor", "Close Combat", "Poison Jab"], "mega": False},
    "Heracross": {"hp": 300, "atk": 65, "defense": 95, "spd": 85, "type": "Bug", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/214.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/214.png", "moves": ["Close Combat", "Stone Edge", "Earthquake"], "mega": True, "mega_multiplier": 2.0},
    "Scizor": {"hp": 300, "atk": 65, "defense": 100, "spd": 65, "type": "Bug", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/212.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/212.png", "moves": ["Bullet Punch", "X-Scissor", "Superpower"], "mega": True, "mega_multiplier": 2.0},    # Rock Type
    "Golem": {"hp": 300, "atk": 60, "defense": 130, "spd": 45, "type": "Rock", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/76.png", "moves": ["Stone Edge", "Earthquake", "Close Combat"], "mega": False},
    "Onix": {"hp": 300, "atk": 23, "defense": 160, "spd": 70, "type": "Rock", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/95.png", "moves": ["Stone Edge", "Earthquake", "Dragon Dance"], "mega": False},
    "Kabutops": {"hp": 300, "atk": 58, "defense": 105, "spd": 80, "type": "Rock", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/141.png", "moves": ["Stone Edge", "Waterfall", "Swords Dance"], "mega": False},
    "Omastar": {"hp": 300, "atk": 30, "defense": 125, "spd": 55, "type": "Rock", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/139.png", "moves": ["Stone Edge", "Hydro Pump", "Ice Beam"], "mega": False},
    "Tyranitar": {"hp": 300, "atk": 67, "defense": 110, "spd": 61, "type": "Rock", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/248.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/248.png", "moves": ["Stone Edge", "Earthquake", "Crunch"], "mega": True, "mega_multiplier": 1.3},    # Ghost Type
    "Gengar": {"hp": 300, "atk": 33, "defense": 60, "spd": 130, "type": "Ghost", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png", "moves": ["Shadow Ball", "Psychic", "Focus Blast"], "mega": True, "mega_multiplier": 2.0},
    "Haunter": {"hp": 300, "atk": 25, "defense": 45, "spd": 95, "type": "Ghost", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/93.png", "moves": ["Shadow Ball", "Psychic", "Focus Blast"], "mega": False},
    "Gastly": {"hp": 300, "atk": 18, "defense": 30, "spd": 80, "type": "Ghost", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/92.png", "moves": ["Shadow Ball", "Psychic", "Hypnosis"], "mega": False},
    "Misdreavus": {"hp": 300, "atk": 30, "defense": 60, "spd": 85, "type": "Ghost", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/200.png", "moves": ["Shadow Ball", "Psychic", "Dazzling Gleam"], "mega": False},
    "Sableye": {"hp": 300, "atk": 38, "defense": 75, "spd": 50, "type": "Ghost", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/202.png", "moves": ["Shadow Ball", "Close Combat", "Recover"], "mega": False},
    
    # Dragon Type
    "Dragonite": {"hp": 300, "atk": 67, "defense": 95, "spd": 80, "type": "Dragon", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/149.png", "moves": ["Outrage", "Earthquake", "Dragon Dance"], "mega": False},
    "Dratini": {"hp": 300, "atk": 32, "defense": 45, "spd": 50, "type": "Dragon", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/147.png", "moves": ["Dragon Rage", "Waterfall", "Outrage"], "mega": False},
    "Dragonair": {"hp": 300, "atk": 42, "defense": 65, "spd": 70, "type": "Dragon", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/148.png", "moves": ["Dragon Pulse", "Waterfall", "Outrage"], "mega": False},
    "Seadra": {"hp": 300, "atk": 33, "defense": 95, "spd": 85, "type": "Dragon", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/117.png", "moves": ["Dragon Pulse", "Hydro Pump", "Ice Beam"], "mega": False},
    "Horsea": {"hp": 300, "atk": 20, "defense": 70, "spd": 70, "type": "Dragon", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/116.png", "moves": ["Dragon Pulse", "Hydro Pump", "Focus Energy"], "mega": False},
    
    # Dark Type
    "Tyranitar": {"hp": 300, "atk": 67, "defense": 110, "spd": 61, "type": "Dark", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/248.png", "moves": ["Stone Edge", "Earthquake", "Crunch"], "mega": False},
    "Umbreon": {"hp": 300, "atk": 33, "defense": 110, "spd": 65, "type": "Dark", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/197.png", "moves": ["Dark Pulse", "Close Combat", "Moonlight"], "mega": False},
    "Houndoom": {"hp": 300, "atk": 45, "defense": 50, "spd": 95, "type": "Dark", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/229.png", "moves": ["Crunch", "Flamethrower", "Nasty Plot"], "mega": False},
    "Poochyena": {"hp": 300, "atk": 28, "defense": 35, "spd": 35, "type": "Dark", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/261.png", "moves": ["Crunch", "Bite", "Toxic Spikes"], "mega": False},
    "Absol": {"hp": 300, "atk": 65, "defense": 60, "spd": 75, "type": "Dark", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/359.png", "moves": ["Superpower", "Psycho Cut", "Close Combat"], "mega": False},
    
    # Steel Type
    "Steelix": {"hp": 300, "atk": 43, "defense": 200, "spd": 30, "type": "Steel", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/208.png", "mega_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/208.png", "moves": ["Heavy Slam", "Earthquake", "Stone Edge"], "mega": True, "mega_multiplier": 2.0},
    "Magneton": {"hp": 300, "atk": 35, "defense": 95, "spd": 100, "type": "Steel", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/82.png", "moves": ["Thunderbolt", "Flash Cannon", "Volt Switch"], "mega": False},
    "Magnemite": {"hp": 300, "atk": 18, "defense": 70, "spd": 45, "type": "Steel", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/81.png", "moves": ["Thunderbolt", "Flash Cannon", "Volt Switch"], "mega": False},
    "Beldum": {"hp": 300, "atk": 28, "defense": 80, "spd": 30, "type": "Steel", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/374.png", "moves": ["Take Down", "Iron Head", "Bullet Punch"], "mega": False},
    "Metang": {"hp": 300, "atk": 38, "defense": 100, "spd": 50, "type": "Steel", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/375.png", "moves": ["Take Down", "Iron Head", "Meteor Mash"], "mega": False},
}

# Vantagens de tipo
TYPE_ADVANTAGE = {
    "Fire": {"advantage": ["Grass", "Ice", "Bug", "Steel"], "weakness": ["Water", "Ground", "Rock"]},
    "Water": {"advantage": ["Fire", "Ground", "Rock"], "weakness": ["Electric", "Grass"]},
    "Grass": {"advantage": ["Water", "Ground", "Rock"], "weakness": ["Fire", "Ice", "Poison", "Flying", "Bug"]},
    "Electric": {"advantage": ["Water", "Flying"], "weakness": ["Ground"]},
    "Ice": {"advantage": ["Grass", "Flying", "Ground", "Dragon"], "weakness": ["Fire", "Fighting", "Rock", "Steel"]},
    "Fighting": {"advantage": ["Normal", "Ice", "Rock", "Dark", "Steel"], "weakness": ["Flying", "Psychic", "Fairy"]},
    "Poison": {"advantage": ["Grass", "Fairy"], "weakness": ["Ground", "Psychic"]},
    "Ground": {"advantage": ["Fire", "Electric", "Poison", "Rock", "Steel"], "weakness": ["Water", "Grass", "Ice"]},
    "Flying": {"advantage": ["Grass", "Fighting", "Bug"], "weakness": ["Electric", "Ice", "Rock"]},
    "Psychic": {"advantage": ["Fighting", "Poison"], "weakness": ["Bug", "Ghost", "Dark"]},
    "Bug": {"advantage": ["Grass", "Psychic", "Dark"], "weakness": ["Fire", "Flying", "Rock"]},
    "Rock": {"advantage": ["Fire", "Ice", "Flying", "Bug"], "weakness": ["Water", "Grass", "Fighting", "Ground", "Steel"]},
    "Ghost": {"advantage": ["Psychic", "Ghost"], "weakness": ["Ghost", "Dark"]},
    "Dragon": {"advantage": ["Dragon"], "weakness": ["Ice", "Dragon", "Fairy"]},
    "Dark": {"advantage": ["Psychic", "Ghost"], "weakness": ["Fighting", "Bug", "Fairy"]},
    "Steel": {"advantage": ["Ice", "Rock", "Fairy"], "weakness": ["Fire", "Water", "Ground"]},
}

class PokemonBattle:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.team1 = []  # Lista de 6 Pokémons
        self.team2 = []  # Lista de 6 Pokémons
        self.hp_team1 = {}  # Dicionário de HP de cada Pokémon da equipe 1
        self.hp_team2 = {}  # Dicionário de HP de cada Pokémon da equipe 2
        self.mega_used1 = False  # Mega usado por player 1
        self.mega_used2 = False  # Mega usado por player 2
        self.mega_active1 = {}  # Pokémons em mega evolução (player 1)
        self.mega_active2 = {}  # Pokémons em mega evolução (player 2)
        self.current_pokemon1_index = 0
        self.current_pokemon2_index = 0
        self.turn = 1
    
    @property
    def pokemon1(self):
        if self.current_pokemon1_index < len(self.team1):
            return self.team1[self.current_pokemon1_index]
        return None
    
    @property
    def pokemon2(self):
        if self.current_pokemon2_index < len(self.team2):
            return self.team2[self.current_pokemon2_index]
        return None
    
    def get_effective_hp(self, pokemon, player):
        """Get HP considering mega evolution"""
        if player == 1:
            base_hp = POKEMONS[pokemon].get("hp", 300)
            if pokemon in self.mega_active1:
                return int(base_hp * self.mega_active1[pokemon])
            return base_hp
        else:
            base_hp = POKEMONS[pokemon].get("hp", 300)
            if pokemon in self.mega_active2:
                return int(base_hp * self.mega_active2[pokemon])
            return base_hp
    
    def get_effective_atk(self, pokemon, player):
        """Get ATK considering mega evolution"""
        base_atk = POKEMONS[pokemon].get("atk", 0)
        if player == 1 and pokemon in self.mega_active1:
            return int(base_atk * self.mega_active1[pokemon])
        elif player == 2 and pokemon in self.mega_active2:
            return int(base_atk * self.mega_active2[pokemon])
        return base_atk
    
    @property
    def hp1(self):
        pokemon = self.pokemon1
        if pokemon:
            return self.hp_team1.get(pokemon, self.get_effective_hp(pokemon, 1))
        return 0
    
    @hp1.setter
    def hp1(self, value):
        pokemon = self.pokemon1
        if pokemon:
            self.hp_team1[pokemon] = value
    
    @property
    def hp2(self):
        pokemon = self.pokemon2
        if pokemon:
            return self.hp_team2.get(pokemon, self.get_effective_hp(pokemon, 2))
        return 0
    
    @hp2.setter
    def hp2(self, value):
        pokemon = self.pokemon2
        if pokemon:
            self.hp_team2[pokemon] = value
        
    def get_type_multiplier(self, attacker_type, defender_type):
        """Calcula o multiplicador de dano baseado no tipo"""
        if attacker_type in TYPE_ADVANTAGE:
            advantages = TYPE_ADVANTAGE[attacker_type].get("advantage", [])
            if defender_type in advantages:
                return 1.5
        if attacker_type in TYPE_ADVANTAGE:
            weakness = TYPE_ADVANTAGE[attacker_type].get("weakness", [])
            if defender_type in weakness:
                return 0.5
        return 1.0
    
    def calculate_damage(self, attacker_pokemon, defender_pokemon, attacker_type, player):
        """Calcula o dano do ataque - DIVIDIDO POR 2, considerando mega evolução"""
        base_damage = random.randint(15, 25) + self.get_effective_atk(attacker_pokemon, player)
        type_multiplier = self.get_type_multiplier(POKEMONS[attacker_pokemon]["type"], POKEMONS[defender_pokemon]["type"])
        defense_reduction = POKEMONS[defender_pokemon]["defense"] // 2
        final_damage = max(5, int(((base_damage * type_multiplier) - (defense_reduction * 0.3)) / 2))
        return final_damage, type_multiplier
    
    def activate_mega(self, pokemon_name, player):
        """Ativa a mega evolução de um Pokémon"""
        if POKEMONS[pokemon_name].get("mega", False):
            multiplier = POKEMONS[pokemon_name].get("mega_multiplier", 2.0)
            if player == 1:
                if not self.mega_used1:
                    self.mega_active1[pokemon_name] = multiplier
                    self.mega_used1 = True
                    return True
            else:
                if not self.mega_used2:
                    self.mega_active2[pokemon_name] = multiplier
                    self.mega_used2 = True
                    return True
        return False

class PokemonSelectionView(View):
    def __init__(self, battle, player_number, page=0, category_index=0):
        super().__init__(timeout=60)
        self.battle = battle
        self.player_number = player_number
        self.page = page
        # Lista de tipos (categorias) disponíveis
        self.types = sorted({POKEMONS[n]["type"] for n in POKEMONS})
        # mantém índice válido
        self.category_index = category_index % max(1, len(self.types))

        # seleciona pokémons da categoria atual
        current_type = self.types[self.category_index]
        category_pokemons = [name for name in POKEMONS.keys() if POKEMONS[name]["type"] == current_type]

        select = Select(
            placeholder=f"Player {player_number}: Choose your Pokémon! (Type: {current_type})",
            options=[
                discord.SelectOption(label=name, value=name, emoji=self.get_emoji(POKEMONS[name]["type"]))
                for name in category_pokemons
            ]
        )
        select.callback = self.select_pokemon
        self.add_item(select)

        # Botões: navegar categorias (prev/next)
        prev_cat = Button(label="⬅️ Prev Category", style=discord.ButtonStyle.secondary)
        prev_cat.callback = self.prev_category
        self.add_item(prev_cat)

        next_cat = Button(label="Next Category ➡️", style=discord.ButtonStyle.secondary)
        next_cat.callback = self.next_category
        self.add_item(next_cat)

    def get_emoji(self, type_name):
        emojis = {
            "Fire": "🔥", "Water": "💧", "Electric": "⚡", "Grass": "🌿",
            "Ice": "❄️", "Fighting": "✊", "Poison": "☠️", "Ground": "🏔️",
            "Flying": "🕊️", "Psychic": "🧠", "Bug": "🐛", "Rock": "🪨",
            "Ghost": "👻", "Dragon": "🐉", "Dark": "🌑", "Steel": "⚙️"
        }
        return emojis.get(type_name, "❓")

    async def select_pokemon(self, interaction: discord.Interaction):
        selected = interaction.data.get("values", [None])[0]
        if selected is None:
            await interaction.response.defer()
            return

        if self.player_number == 1:
            if selected not in self.battle.team1:
                self.battle.team1.append(selected)
        else:
            if selected not in self.battle.team2:
                self.battle.team2.append(selected)

        await interaction.response.defer()

    async def prev_category(self, interaction: discord.Interaction):
        new_index = (self.category_index - 1) % len(self.types)
        new_view = PokemonSelectionView(self.battle, self.player_number, page=0, category_index=new_index)
        await interaction.response.edit_message(view=new_view)

    async def next_category(self, interaction: discord.Interaction):
        new_index = (self.category_index + 1) % len(self.types)
        new_view = PokemonSelectionView(self.battle, self.player_number, page=0, category_index=new_index)
        await interaction.response.edit_message(view=new_view)

class BattleActionView(View):
    def __init__(self, battle, is_player1_turn):
        super().__init__(timeout=30)
        self.battle = battle
        self.is_player1_turn = is_player1_turn
        self.action = None
        self.used_mega = False
        
        pokemon = self.battle.pokemon1 if is_player1_turn else self.battle.pokemon2
        moves = POKEMONS[pokemon]["moves"]
        
        for i, move in enumerate(moves):
            button = Button(label=move, style=discord.ButtonStyle.primary)
            button.callback = lambda interaction, m=move: self.attack(interaction, m)
            self.add_item(button)
        
        # Botão de Mega Evolução (se disponível)
        can_mega = POKEMONS[pokemon].get("mega", False)
        if can_mega:
            if is_player1_turn and not self.battle.mega_used1:
                mega_button = Button(label="🔥 Mega Evolution", style=discord.ButtonStyle.danger)
                mega_button.callback = self.use_mega
                self.add_item(mega_button)
            elif not is_player1_turn and not self.battle.mega_used2:
                mega_button = Button(label="🔥 Mega Evolution", style=discord.ButtonStyle.danger)
                mega_button.callback = self.use_mega
                self.add_item(mega_button)
    
    async def attack(self, interaction: discord.Interaction, move: str):
        self.action = move
        await interaction.response.defer()
        self.stop()
    
    async def use_mega(self, interaction: discord.Interaction):
        pokemon = self.battle.pokemon1 if self.is_player1_turn else self.battle.pokemon2
        if self.battle.activate_mega(pokemon, 1 if self.is_player1_turn else 2):
            self.used_mega = True
            # Criar embed com imagem de mega evolução
            mega_embed = discord.Embed(
                title=f"🔥 MEGA EVOLUTION! {pokemon} Mega Evolved!",
                description=f"**{pokemon}** gained **2x HP and ATK**!" if pokemon != "Tyranitar" else f"**{pokemon}** gained **1.3x HP and ATK**!",
                color=discord.Color.red()
            )
            mega_image = POKEMONS[pokemon].get("mega_image", POKEMONS[pokemon]["image"])
            mega_embed.set_image(url=mega_image)
            await interaction.response.send_message(embed=mega_embed, ephemeral=False)
        else:
            await interaction.response.send_message("❌ Mega evolution already used!", ephemeral=True)

# Classe do botão para atribuir cargo
class VerifiedButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🍀 Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        role_id = 1445216877252186155
        
        guild = interaction.guild
        role = guild.get_role(role_id)
        
        if role is None:
            await interaction.response.send_message("❌ Role not found!", ephemeral=True)
            return
        
        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ You have gained the {role.mention} role!",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to assign this role!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error assigning role: {str(e)}",
                ephemeral=True
            )

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} connected successfully!")
    bot.add_view(VerifiedButtonView())

@bot.command(name="criar_botao")
@commands.has_permissions(administrator=True)
async def criar_botao(ctx):
    """Command to create the verification button message"""
    embed = discord.Embed(
        title="Verification",
        description="Click the button below to get the verified bot role!",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed, view=VerifiedButtonView())
    await ctx.send("✅ Button message created!")

@bot.command(name="Pokebattle")
async def pokebattle(ctx, opponent: discord.User = None):
    """Start a Pokémon battle!"""
    if opponent is None:
        await ctx.send("❌ You need to mention a user to battle!\nUsage: `!Pokebattle @username`")
        return
    
    if opponent == ctx.author:
        await ctx.send("❌ You can't battle yourself!")
        return
    
    if opponent.bot:
        await ctx.send("❌ You can't battle a bot!")
        return
    
    # Aviso importante
    warning_embed = discord.Embed(
        title="⚠️ Important Warning",
        description="DO NOT choose while typing otherwise you get disconnected!",
        color=discord.Color.yellow()
    )
    await ctx.send(embed=warning_embed)
    
    battle = PokemonBattle(ctx.author, opponent)
    
    # Player 1 selects 6 Pokémons
    for pokemon_num in range(1, 7):
        embed1 = discord.Embed(
            title="🔴 Pokémon Battle Started!",
            description=f"{ctx.author.mention} vs {opponent.mention}",
            color=discord.Color.red()
        )
        embed1.add_field(name=f"Team Selection - Pokémon {pokemon_num}/6", value=f"{ctx.author.mention}, choose your Pokémon #{pokemon_num}!", inline=False)
        if battle.team1:
            embed1.add_field(name="Current Team", value=", ".join(battle.team1), inline=False)
        msg1 = await ctx.send(embed=embed1, view=PokemonSelectionView(battle, 1, 0))
        
        # Wait for player 1 selection
        await asyncio.sleep(1)
        timeout = 0
        selected_count = len(battle.team1)
        while len(battle.team1) == selected_count and timeout < 120:
            await asyncio.sleep(1)
            timeout += 1
        
        if len(battle.team1) == selected_count:
            await ctx.send(f"❌ Player 1 didn't select Pokémon #{pokemon_num} in time!")
            return
    
    # Player 2 selects 6 Pokémons
    for pokemon_num in range(1, 7):
        embed2 = discord.Embed(
            title="🔴 Pokémon Battle Started!",
            description=f"{ctx.author.mention} vs {opponent.mention}",
            color=discord.Color.blue()
        )
        embed2.add_field(name=f"Team Selection - Pokémon {pokemon_num}/6", value=f"{opponent.mention}, choose your Pokémon #{pokemon_num}!", inline=False)
        if battle.team2:
            embed2.add_field(name="Current Team", value=", ".join(battle.team2), inline=False)
        msg2 = await ctx.send(embed=embed2, view=PokemonSelectionView(battle, 2, 0))
        
        # Wait for player 2 selection
        await asyncio.sleep(1)
        timeout = 0
        selected_count = len(battle.team2)
        while len(battle.team2) == selected_count and timeout < 120:
            await asyncio.sleep(1)
            timeout += 1
        
        if len(battle.team2) == selected_count:
            await ctx.send(f"❌ Player 2 didn't select Pokémon #{pokemon_num} in time!")
            return
    
    # Initialize HP for all team members
    for pokemon in battle.team1:
        battle.hp_team1[pokemon] = POKEMONS[pokemon]["hp"]
    for pokemon in battle.team2:
        battle.hp_team2[pokemon] = POKEMONS[pokemon]["hp"]
    
    # Battle starts
    battle_log = []
    
    while battle.current_pokemon1_index < len(battle.team1) and battle.current_pokemon2_index < len(battle.team2):
        current_p1 = battle.pokemon1
        current_p2 = battle.pokemon2
        
        if current_p1 is None or current_p2 is None:
            break
        
        # Create battle embed
        embed = discord.Embed(
            title="⚔️ Pokémon Battle!",
            color=discord.Color.orange()
        )
        
        # Adicionar status de mega evolução
        p1_mega = "🔥 MEGA" if current_p1 in battle.mega_active1 else ""
        p2_mega = "🔥 MEGA" if current_p2 in battle.mega_active2 else ""
        
        embed.add_field(
            name=f"🔴 {ctx.author.name}'s {current_p1} {p1_mega}",
            value=f"❤️ HP: {battle.hp1}/{battle.get_effective_hp(current_p1, 1)}",
            inline=True
        )
        embed.add_field(
            name=f"🔵 {opponent.name}'s {current_p2} {p2_mega}",
            value=f"❤️ HP: {battle.hp2}/{battle.get_effective_hp(current_p2, 2)}",
            inline=True
        )
        
        embed.set_image(url=POKEMONS[current_p1]["image"])
        
        if battle_log:
            embed.add_field(name="Last Turn", value=battle_log[-1], inline=False)
        
        embed.add_field(name="Turn", value=f"Round {battle.turn}", inline=False)
        embed.add_field(name="🔄 Player 1 Turn", value=f"{ctx.author.mention}, choose your move!", inline=False)
        
        view1 = BattleActionView(battle, True)
        msg = await ctx.send(embed=embed, view=view1)
        
        try:
            await asyncio.wait_for(view1.wait(), timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("❌ Player 1 took too long! Forfeiting...")
            return
        
        if view1.action:
            damage, multiplier = battle.calculate_damage(current_p1, current_p2, view1.action, 1)
            battle.hp2 -= damage
            battle.hp2 = max(0, battle.hp2)
            
            mult_text = ""
            if multiplier > 1:
                mult_text = " 🔥 **Super Effective!**"
            elif multiplier < 1:
                mult_text = " ❄️ **Not very effective...**"
            
            battle_log.append(f"{ctx.author.name}'s {current_p1} used **{view1.action}**! Dealt {damage} damage{mult_text}")
        
        if battle.hp2 <= 0:
            battle.current_pokemon2_index += 1
            if battle.current_pokemon2_index < len(battle.team2):
                next_pokemon = battle.pokemon2
                battle.hp_team2[next_pokemon] = POKEMONS[next_pokemon]["hp"]
                battle_log.append(f"🔵 {opponent.name} sent out {next_pokemon}!")
            continue
        
        # Player 2 attacks
        embed2 = discord.Embed(
            title="⚔️ Pokémon Battle!",
            color=discord.Color.orange()
        )
        
        # Adicionar status de mega evolução
        p1_mega = "🔥 MEGA" if current_p1 in battle.mega_active1 else ""
        p2_mega = "🔥 MEGA" if current_p2 in battle.mega_active2 else ""
        
        embed2.add_field(
            name=f"🔴 {ctx.author.name}'s {current_p1} {p1_mega}",
            value=f"❤️ HP: {battle.hp1}/{battle.get_effective_hp(current_p1, 1)}",
            inline=True
        )
        embed2.add_field(
            name=f"🔵 {opponent.name}'s {current_p2} {p2_mega}",
            value=f"❤️ HP: {battle.hp2}/{battle.get_effective_hp(current_p2, 2)}",
            inline=True
        )
        
        embed2.set_image(url=POKEMONS[current_p2]["image"])
        embed2.add_field(name="Last Turn", value=battle_log[-1], inline=False)
        embed2.add_field(name="Turn", value=f"Round {battle.turn}", inline=False)
        embed2.add_field(name="🔄 Player 2 Turn", value=f"{opponent.mention}, choose your move!", inline=False)
        
        view2 = BattleActionView(battle, False)
        msg = await ctx.send(embed=embed2, view=view2)
        
        try:
            await asyncio.wait_for(view2.wait(), timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("❌ Player 2 took too long! Forfeiting...")
            return
        
        if view2.action:
            damage, multiplier = battle.calculate_damage(current_p2, current_p1, view2.action, 2)
            battle.hp1 -= damage
            battle.hp1 = max(0, battle.hp1)
            
            mult_text = ""
            if multiplier > 1:
                mult_text = " 🔥 **Super Effective!**"
            elif multiplier < 1:
                mult_text = " ❄️ **Not very effective...**"
            
            battle_log.append(f"{opponent.name}'s {current_p2} used **{view2.action}**! Dealt {damage} damage{mult_text}")
        
        if battle.hp1 <= 0:
            battle.current_pokemon1_index += 1
            if battle.current_pokemon1_index < len(battle.team1):
                next_pokemon = battle.pokemon1
                battle.hp_team1[next_pokemon] = POKEMONS[next_pokemon]["hp"]
                battle_log.append(f"🔴 {ctx.author.name} sent out {next_pokemon}!")
        
        battle.turn += 1
    
    # Battle ends
    winner = ctx.author if battle.current_pokemon1_index < len(battle.team1) else opponent
    winner_team = battle.team1 if battle.current_pokemon1_index < len(battle.team1) else battle.team2
    
    embed_final = discord.Embed(
        title="🏆 Battle Over!",
        color=discord.Color.gold()
    )
    embed_final.add_field(name="Winner", value=f"🎉 {winner.mention}", inline=False)
    embed_final.add_field(name="Remaining Team", value=", ".join(winner_team[winner.current_pokemon1_index if winner == ctx.author else winner.current_pokemon2_index:]), inline=False)
    embed_final.add_field(name="Battle Summary", value="\n".join(battle_log[-5:]), inline=False)
    
    await ctx.send(embed=embed_final)

# Execute o bot com seu token
TOKEN = "YouToken"
bot.run(TOKEN)

