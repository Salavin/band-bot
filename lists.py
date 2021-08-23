class Song:
    def __init__(self, title, length):
        self.title = title
        self.length = length


songs = [Song("Armed Forces Fanfare", 45),
         Song("Bad Guy", 133),
         Song("Beer Barrel", 126),
         Song("Bells", 80),
         Song("Boat", 64),
         Song("Brooklyn", 47),
         Song("Chorale Fights", 60),
         Song("Confident", 69),  # nice
         Song("Cupid Shuffle", 63),
         Song("Cyclone Power", 30),
         Song("Docs Cheers 1", 22),
         Song("Docs Cheers 2", 22),
         Song("Eat 'em up", 29),
         Song("Fanfare", 18),
         Song("Fat Bottom Girls", 72),
         Song("Fights!", 28),
         Song("First Down", 25),
         Song("For I For S", 28),
         Song("Full Throwdown", 172),
         Song("Game of Thrones", 20),
         Song("Happy Birthday", 30),
         Song("Hero 🦀", 10),
         Song("Iron Man", 13),
         Song("Juicy Wiggle", 232),
         Song("Let's Go State", 16),
         Song("Machine", 19),
         Song("Mo Bamba", 49),
         Song("Presidential", 21),
         Song("Rise Sons", 21),
         Song("Sad But True", 15),
         Song("Singing Playing", 135),
         Song("Star Wars 2", 26),
         Song("Star Wars 3", 23),
         Song("Star Wars 4", 35),
         Song("Stuntin'", 85),
         Song("Sweet Caroline", 93),
         Song("Third Down", 17),
         Song("Throwdown", 20),
         Song("Uranus", 16),
         Song("Welper Wings!", 83),
         Song("Whatcha gonna do?", 52),
         Song("Who Knows?", 14),
         Song("Wings", 125)]

cyclone_power = ["Take a shower?",
                 "Eiffel Tower?",
                 "Smell a flower?",
                 "Buy some flower?",
                 "Sweet and sour?",
                 "Eisenhower?",
                 "Protein powder?"]

responses = {"cool": "Ice Cold!",
             "go cyclones": "Yeah! Cyclones!",
             "we love the cyclones": "Yeah! Love!",
             "sense": "Dollars!",
             "dig": "With a shovel!",
             "super": "Super duper dad!",
             "boat": "Stroke!",
             "step show": "Cancelled.",
             "rise sons": "Starts with drums!",
             "hey band": "Hey what?",
             "tweet tweet tweet": "GO STATE",
             "lets go state": "Where are we going?",
             "let's go state": "Where are we going?",
             "cyclone!": "Power!",
             "thirsty": "Hydrate or diedrate!",
             "drink": "Hydrate or diedrate!",
             "clear": "Crystal!",
             "two": "Buh!"
             }

valid_channels = [743519674456866927, 745852024398020659]

sections = {
    "Piccolos": (743522252523569263, "<:piccolo:743968600964071431>"),
    "Clarinets": (743524015171436556, "<:clarinet:743968624577871940>"),
    "Saxophones": (743524158885068850, "<:sax:743967427137896569>"),
    "Mellophones": (743524370848153680, "<:mello:743969375580717097>"),
    "Trumpets": (743524556546900058, "🎺"),
    "Trombones/Bass-bones": (743524720544317491, "<:trombone:743967426885976095>"),
    "Baritones": (743524806309445790, "<:baritone:743968813267025941>"),
    "Sousaphones": (743524994243625012, "<:sousaphone:743969087864045599>"),
    "Drumline": (743525150237917226, "🥁"),
    "Guard": (743525241128484976, "<:guard:743967426865266708>")
}

colleges = {
    "Agriculture and Life Sciences": (743525942101803220, "🐮"),
    "Design": (743526080576749629, "🏫"),
    "Engineering": (743526108741369957, "🧮"),
    "Human Sciences": (743526163552534588, "🩺"),
    "Liberal Arts and Sciences": (743526245668749442, "🤔"),
    "Veterinary Medicine": (743526321476337675, "🐈"),
    "Alumni": (743521900965396551, "🧓")
}
