from completion import get_completion
from memory import Memory

SEPARATOR = "\n\n"
MAX_TOKENS = 1000

RULES = '''TODO: Show the rules'''

FIRST_SCENE_TEMPLATE = '''You are the GM for a roleplaying game. Write the backstory and first scene of a game that will lead the players on an exciting adventure. The backstory must answer the questions who, what, when, where, and why. It must include some mystery and hint at danger. It should only refer to events in the past. It must contain three paragraphs. The first scene must present the players with a minor obstacle that they must overcome. It should only refer to events in the present and occur after the events in the backstory. It must be a single paragraph. Prefix the backstory with the string "Backstory: " and the first scene with the string "Scene 1: ". Use the details below for the backstory. Use rich, vivid language.

Players: {players}

Setting: {setting}

'''

NEXT_SCENE_TEMPLATE='''You are the GM for a roleplaying game. Write the next scene of the game below based on the action attempted by the players and its effect. The new scene must meet the following criteria:

- Include the action attempted by the player.
- Include whether the action succeeded or failed based on the effect.
- Take place after the events from the previous scenes.
- When the player overcome an obstacle, present the players with a new and different obstacle that is described in detail.
- Give players the opportunity to take a new action at the end but don't state what choices the players have.
- Be a single paragraph
- Use rich, vivid language.
- Be prefixed with the string "Scene {scene_number}: ".

{history}

Action:
{action}

Effect:
{effect}

'''

FAILURE_EFFECT = "The action failed. The players make no progress in the game."
SUCCESS_EFFECT = "The action succeeded. The players make progress in the game."

def text_input(message):
  print("\n{message}\n".format(message=message))
  return input("> ")

def menu_input(message, choices):
  formatted_choices = ["{i}. {x}".format(i=i+1, x=x) for i, x in enumerate(choices)]

  result = text_input(
    "{message}\n\n{choices}".format(
      message=message,
      choices="\n".join(formatted_choices)
    )
  )

  while True:
    if not result.isnumeric():
      result = text_input("Input is not a number. Please try again.")
      continue

    result = int(result) - 1
    if result < 0 or result >= len(choices):
      result = text_input("Input is not a valid menu item. Please try again.")
      continue

    break

  return result

def main():
  memory = Memory(separator=SEPARATOR, max_tokens=MAX_TOKENS)

  selection = menu_input(
    "Welcome to Roll for AI. A roleplaying game powered by AI. Would you like to see the rules?",
    ["Yes", "No"]
  )

  if selection == 0:
    print("\n{rules}".format(rules=RULES))

  players = text_input("Enter the names of the players separated by commas:")
  players = list(map(lambda x: x.strip(), players.split(",")))

  setting = text_input("Enter the setting for your adventure:")

  prompt = FIRST_SCENE_TEMPLATE.format(players=", ".join(players), setting=setting)
  completion = get_completion(prompt)

  print("\n{completion}".format(completion=completion))
  memory.push(completion)

  scene_number = 2
  while True:
    action = text_input("Enter what the players attempt to do:")
    selection = menu_input("Did the action succeed?", ["Yes", "No"])

    prompt = NEXT_SCENE_TEMPLATE.format(
      scene_number=scene_number,
      history=memory.serialize(),
      action=action,
      effect=SUCCESS_EFFECT if selection == 0 else FAILURE_EFFECT
    )
    completion = get_completion(prompt)

    print("\n{completion}".format(completion=completion))
    memory.push(completion)

    scene_number += 1

if __name__ == "__main__":
    main()
