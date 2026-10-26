"""Create a reproducible local movie knowledge base (no network required)."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
REAL = [
("The Matrix","Science Fiction|Action","English","Exciting","identity|artificial intelligence|freedom","A hacker discovers that ordinary reality is a computer simulation and joins a fight for human freedom."),
("Inception","Science Fiction|Thriller","English","Thought-provoking","dreams|memory|heist","A skilled thief enters layered dreams for a mission that blurs the line between memory and reality."),
("Interstellar","Science Fiction|Adventure|Drama","English","Emotional","space|family|survival","A former pilot travels beyond Earth to seek a future for humanity while holding on to family."),
("The Dark Knight","Action|Crime|Drama","English","Dark","justice|heroism|chaos","A masked hero faces a criminal whose escalating schemes test the limits of justice."),
("Pulp Fiction","Crime|Drama|Thriller","English","Dark","fate|crime|revenge","Interwoven Los Angeles crime stories collide through chance, loyalty, and consequence."),
("The Shawshank Redemption","Drama","English","Inspirational","hope|friendship|justice","Two prisoners build a lasting friendship and hold on to hope through decades of hardship."),
("Forrest Gump","Drama|Romance","English","Feel-good","history|kindness|love","A kind-hearted man recounts a life that unexpectedly intersects with landmark events."),
("Spirited Away","Animation|Fantasy|Adventure","Japanese","Magical","family|courage|identity","A young girl enters a mysterious spirit world and must find courage to rescue her parents."),
("Parasite","Thriller|Drama|Comedy","Korean","Suspenseful","class|family|deception","Two families from sharply different circumstances become entangled in an unsettling plan."),
("Train to Busan","Horror|Action|Thriller","Korean","Suspenseful","survival|family|zombies","Passengers on a fast train struggle to protect one another during a sudden outbreak."),
("Your Name","Animation|Romance|Fantasy","Japanese","Emotional","connection|identity|time","Two teenagers begin mysteriously exchanging lives and search for a connection across time."),
("Coco","Animation|Family|Fantasy","English","Feel-good","music|family|memory","A young musician visits a vibrant land of ancestors and learns the power of family memory."),
("Toy Story","Animation|Comedy|Family","English","Feel-good","friendship|belonging|adventure","Toys embark on a lively adventure while learning to share friendship and attention."),
("The Grand Budapest Hotel","Comedy|Adventure","English","Quirky","friendship|art|adventure","A concierge and his young protégé become caught in an eccentric caper across Europe."),
("Get Out","Horror|Mystery|Thriller","English","Suspenseful","identity|secrets|social tension","A weekend visit reveals increasingly disturbing secrets behind a welcoming household."),
("Knives Out","Mystery|Comedy|Crime","English","Suspenseful","family|secrets|investigation","A sharp detective untangles a wealthy family's conflicting stories after a death."),
("Mad Max: Fury Road","Action|Adventure|Science Fiction","English","Exciting","survival|freedom|resistance","A high-speed escape across a harsh wasteland becomes a fight for liberation."),
("Arrival","Science Fiction|Drama|Mystery","English","Thought-provoking","language|communication|time","A linguist works to communicate with visitors and confronts the nature of time."),
("The Lion King","Animation|Adventure|Family","English","Inspirational","family|identity|responsibility","A young heir finds the courage to return home and accept responsibility."),
("Dangal","Drama|Sport","Hindi","Inspirational","family|ambition|equality","A former wrestler trains his daughters to pursue a sport against convention."),
("3 Idiots","Comedy|Drama","Hindi","Feel-good","friendship|education|ambition","Three engineering students question pressure and discover what meaningful learning means."),
("Lagaan","Drama|Sport|Romance","Hindi","Inspirational","community|justice|courage","A village risks its future in a cricket match against colonial rulers."),
("Queen","Comedy|Drama","Hindi","Feel-good","independence|travel|confidence","A young woman takes a solo trip that reshapes her sense of confidence and possibility."),
("Taare Zameen Par","Drama|Family","Hindi","Emotional","education|family|creativity","An observant teacher helps a child whose learning differences have gone misunderstood."),
("Andhadhun","Thriller|Crime|Comedy","Hindi","Suspenseful","deception|music|crime","A pianist becomes tangled in a chain of twists after witnessing a troubling crime."),
("Drishyam","Thriller|Crime|Drama","Hindi","Suspenseful","family|secrets|protection","A resourceful father uses careful planning to protect his family from a criminal case."),
("Sairat","Romance|Drama","Marathi","Emotional","love|class|courage","Two young people fall in love across social divisions in a heartfelt rural story."),
("Natsamrat","Drama","Marathi","Emotional","theatre|family|ageing","A celebrated stage actor faces family change after leaving the theatre."),
("Court","Drama","Marathi","Thought-provoking","justice|society|law","An ordinary legal proceeding exposes the systems and assumptions around a folk singer."),
("Killa","Drama|Family","Marathi","Relaxing","friendship|change|childhood","A thoughtful boy adjusts to a new coastal town and finds unexpected friendship."),
("Jai Bhim","Crime|Drama","Tamil","Inspirational","justice|equality|law","A lawyer challenges injustice and seeks accountability for a marginalized family."),
("96","Romance|Drama","Tamil","Emotional","memory|love|school","Former classmates reunite and revisit the choices and feelings of their youth."),
("Vikram","Action|Thriller|Crime","Tamil","Exciting","justice|undercover|crime","An investigator uncovers a hidden network through a series of dangerous operations."),
("Super Deluxe","Drama|Comedy|Thriller","Tamil","Thought-provoking","family|chance|identity","Several surprising stories intersect over a single day in a city."),
("Eega","Fantasy|Action|Romance","Telugu","Quirky","revenge|love|rebirth","A fantastical tale follows a determined hero who returns in an unexpected form."),
("Baahubali: The Beginning","Action|Fantasy|Adventure","Telugu","Exciting","kingdom|family|destiny","A young man's journey uncovers a royal past and a struggle for a kingdom."),
("C/o Kancharapalem","Romance|Drama","Telugu","Thought-provoking","community|love|belonging","Four tender love stories reveal the people and rhythms of a small town."),
("Mahanati","Drama|Biography","Telugu","Emotional","cinema|ambition|legacy","A journalist pieces together the life and work of a celebrated screen performer."),
("Oldboy","Thriller|Mystery|Action","Korean","Dark","revenge|identity|secrets","A man seeks answers after years of unexplained confinement and a sudden release."),
("The Handmaiden","Thriller|Romance|Drama","Korean","Suspenseful","deception|class|desire","A carefully planned con becomes more complicated as loyalties and desires shift."),
("My Neighbor Totoro","Animation|Family|Fantasy","Japanese","Relaxing","family|nature|childhood","Two sisters discover gentle woodland spirits while settling into a new home."),
("Akira","Animation|Science Fiction|Action","Japanese","Dark","power|friendship|city","A friendship is tested amid unrest and extraordinary forces in a futuristic city."),
("Rashomon","Mystery|Drama","Japanese","Thought-provoking","truth|memory|justice","Conflicting testimonies about one event raise questions about truth and perspective."),
("Seven Samurai","Action|Drama|Adventure","Japanese","Inspirational","community|courage|honor","A village recruits skilled defenders to stand against a repeated threat."),
("Pan's Labyrinth","Fantasy|Drama|War","Spanish","Dark","imagination|courage|war","A child escapes into a mythic world while facing danger in wartime Spain."),
("Amélie","Romance|Comedy","French","Feel-good","kindness|community|love","A shy Parisian quietly improves the lives around her and opens herself to love."),
("The Intouchables","Comedy|Drama","French","Feel-good","friendship|accessibility|change","An unlikely friendship brings humor and new perspective to two very different lives."),
("Roma","Drama","Spanish","Thought-provoking","family|memory|class","A domestic worker's daily life anchors a family's changing world in Mexico City."),
("Crouching Tiger, Hidden Dragon","Action|Romance|Fantasy","Mandarin","Emotional","honor|freedom|love","A stolen sword draws warriors together in a graceful story of duty and desire."),
("Hero","Action|Drama|Mystery","Mandarin","Thought-provoking","sacrifice|truth|leadership","A warrior tells layered accounts of an encounter with a powerful ruler."),
("The Host","Horror|Comedy|Drama","Korean","Exciting","family|science|survival","A family faces a strange creature and institutional confusion beside a river."),
("A Separation","Drama|Mystery","Persian","Thought-provoking","family|truth|justice","A separation and a disputed incident reveal difficult choices within two families."),
("City of God","Crime|Drama","Portuguese","Dark","ambition|violence|community","A young photographer witnesses ambition and danger in a changing neighborhood."),
("The Lives of Others","Drama|Thriller","German","Thought-provoking","privacy|art|conscience","A surveillance officer's assignment begins to change his view of the people he observes."),
("Life Is Beautiful","Comedy|Drama|Romance","Italian","Emotional","family|hope|imagination","A father uses playfulness and imagination to protect his child in terrible times."),
("The Secret in Their Eyes","Mystery|Crime|Romance","Spanish","Suspenseful","memory|justice|love","An investigator revisits an old case that has shaped several lives for decades."),
("The Farewell","Comedy|Drama","Mandarin","Emotional","family|culture|goodbye","A family gathers around a beloved grandmother while navigating a difficult secret."),
("Minari","Drama|Family","Korean","Inspirational","family|migration|belonging","A Korean American family builds a new life on a small farm in Arkansas."),
("Everything Everywhere All at Once","Science Fiction|Action|Comedy","English","Thought-provoking","family|identity|possibility","A laundromat owner encounters alternate lives while trying to reconnect with her family."),
]
GENRES = ["Action", "Adventure", "Comedy", "Drama", "Romance", "Science Fiction", "Thriller", "Horror", "Mystery", "Fantasy", "Animation", "Documentary", "Crime", "Family"]
LANGS = ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Korean", "Japanese"]
MOODS = ["Feel-good", "Exciting", "Emotional", "Suspenseful", "Dark", "Inspirational", "Relaxing", "Thought-provoking"]
THEMES = ["friendship|discovery|belonging", "family|courage|change", "nature|community|hope", "mystery|memory|justice", "music|ambition|identity", "science|future|ethics", "travel|adventure|freedom", "love|trust|second chances", "history|culture|resilience", "animals|conservation|wonder", "sport|teamwork|determination", "art|creativity|community"]
COLORS = ["#7c3aed", "#0891b2", "#dc2626", "#d97706", "#059669", "#db2777", "#4f46e5", "#475569"]


def build_rows():
    rows = []
    for i, (title, genres, language, mood, themes, desc) in enumerate(REAL):
        year = 1990 + (i * 7 % 37)
        rows.append([f"M{i+1:03d}", title, genres, year, language, round(6.1 + (i * 17 % 39) / 10, 1), 82 + (i * 13 % 83), mood, themes, "Adult" if i % 5 == 0 else "Teen and adult", 28 + (i * 23 % 73), desc, COLORS[i % len(COLORS)]])
    # The remaining records are clearly labeled fictional examples for rule coverage.
    i = 0
    while len(rows) < 168:
        g1 = GENRES[i % len(GENRES)]; g2 = GENRES[(i * 5 + 3) % len(GENRES)]
        lang = LANGS[i % len(LANGS)]; mood = MOODS[(i * 3) % len(MOODS)]; theme = THEMES[(i * 7) % len(THEMES)]
        title = f"Demo: {g1} of {['Silver Harbor','Quiet Monsoon','Lantern Valley','Amber Skies','Hidden Garden','Last Lighthouse','Paper Kingdom','Blue Comet','Map of Tomorrow','Winter Orchard','Open Road','Glass River'][i % 12]} {i // 12 + 1}"
        desc = f"A fictional {mood.lower()} {g1.lower()} story about {theme.split('|')[0]} and unexpected choices, set among a community facing change."
        rows.append([f"M{len(rows)+1:03d}", title, f"{g1}|{g2}" if g1 != g2 else g1, 1990 + i % 37, lang, round(5.2 + (i * 19 % 48) / 10, 1), 75 + i * 11 % 111, mood, theme, "Family" if "Family" in (g1, g2) else "Teen and adult", 20 + i * 29 % 81, desc, COLORS[i % len(COLORS)]])
        i += 1
    return rows


if __name__ == "__main__":
    path = ROOT / "data" / "movies.csv"; path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["movie_id", "title", "genres", "release_year", "language", "rating", "duration", "mood", "themes", "audience", "popularity", "description", "poster_color"])
        writer.writerows(build_rows())
    print(f"Generated {len(build_rows())} movies at {path}")
