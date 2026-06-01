#fake_headline_generator
import random
subjects=[
    "Elon Musk",
    "A Grumpy Neighbour",
    "Virat Kohli",
    "A Talking Parrot",
    "The Local Chaiwala"
]
actions=[
    "challenges",
    "gets stuck in",
    "proposes to",
    "accidentally buys",
    "invents a new flavor of"
]
places_or_things=[
    "on Mars",
    "The Taj Mahal",
    "inside a Samosa",
    "at a Wedding",
    "a Flying Carpet",
]
# start the headline generation loop
 
while True:
    subject = random.choice(subjects)
    action = random.choice(actions)
    place_or_thing = random.choice(places_or_things)

    headline = (f"BREAKING NEWS :  {subject} {action} {place_or_thing}")
    print(f"\n{headline}") 
    user_input=input("\nDo you want another Headline? (yes/no):").strip().lower() #input will be either yes or no
    if user_input == "yes":
        continue
    elif user_input == "no":
         print("Thanks for using the Fake Headline Generator, Have a good day!")
         break
    else:
        print("Invalid Entry")
        break