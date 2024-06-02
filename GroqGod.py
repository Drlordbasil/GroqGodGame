import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class World:
    def __init__(self):
        self.days = 0
        self.entities = []
        self.world_details = ""

    def add_entity(self, entity):
        self.entities.append(entity)

    def update_world_details(self, details):
        self.world_details += details + "\n"

    def simulate_day(self):
        self.days += 1
        print(f"\nDay {self.days}")
        for entity in self.entities:
            entity.interact()

class Entity:
    def __init__(self, name):
        self.name = name

    def interact(self):
        raise NotImplementedError("Subclasses must implement the interact method.")

class Human(Entity):
    def interact(self):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a human named {self.name} in a game world. {world.world_details}",
                }
            ],
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content
        print(f"{self.name}: {response}")

class Angel(Entity):
    def interact(self):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are an angel named {self.name} in a game world. {world.world_details}",
                }
            ],
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content
        print(f"{self.name}: {response}")

class Demon(Entity):
    def interact(self):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a demon named {self.name} in a game world. {world.world_details}",
                }
            ],
            model="llama3-70b-8192",
        )
        response = chat_completion.choices[0].message.content
        print(f"{self.name}: {response}")

world = World()

while True:
    command = input("\nEnter a command (create, spawn, talk, simulate, quit): ")

    if command == "create":
        creation = input("What would you like to create? ")
        world.update_world_details(f"God created {creation}.")
        print(f"You have created {creation}.")

    elif command == "spawn":
        entity_type = input("What type of entity would you like to spawn? (human, angel, demon): ")
        entity_name = input("Enter a name for the entity: ")

        if entity_type == "human":
            entity = Human(entity_name)
        elif entity_type == "angel":
            entity = Angel(entity_name)
        elif entity_type == "demon":
            entity = Demon(entity_name)
        else:
            print("Invalid entity type.")
            continue

        world.add_entity(entity)
        print(f"You have spawned a {entity_type} named {entity_name}.")

    elif command == "talk":
        entity_name = input("Enter the name of the entity you want to talk to: ")
        entity = next((e for e in world.entities if e.name == entity_name), None)

        if entity:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are {entity_name}, a {type(entity).__name__.lower()} in a game world. {world.world_details}",
                    },
                    {
                        "role": "user",
                        "content": input("Enter your message: "),
                    },
                ],
                model="llama3-70b-8192",
            )
            response = chat_completion.choices[0].message.content
            print(f"{entity_name}: {response}")
        else:
            print("Entity not found.")

    elif command == "simulate":
        world.simulate_day()

    elif command == "quit":
        print("Exiting the game.")
        break

    else:
        print("Invalid command.")
