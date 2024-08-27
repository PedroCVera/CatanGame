import random

resource_convertion_dic = {
	"w": "wheat",
	"W": "wood",
	"b": "brick",
	"o": "ore",
	"s": "sheep"
}

class Player:
	def __init__(self, pid):
		self._wood = 0
		self._ore = 0
		self._sheep = 0
		self._brick = 0
		self._wheat = 0
		self._development_cards = []
		self._army = 0
		self._winning_points = 0
		self._player_id = pid

	def get_army(self):
		return self._army

	def add_card(self, card: str):
		self._development_cards.append(card)

	def get_cards(self):
		return self._development_cards

	def has_card(self, card: str):
		print(f"{card} ")
		if card in self._development_cards:
			return True
		return False

	def has_resource(self, resource: str, number: int):
		current_value = getattr(self, f"_{resource}")
		if current_value >= number:
			return True
		return False

	def remove_card(self, card: str):
		if card in self._development_cards:
			self._development_cards.remove(card)
			if card == "Knight":
				self._army += 1

	def get_points(self):
		return self._winning_points

	def remove_winning_points(self, number: int):
		self._winning_points -= number

	def add_winning_point(self, number: int):
		self._winning_points += number
		print(f"Got to {self._winning_points} from {self._winning_points - number}")
		if self._winning_points >= 10:
			return 1
		return 0

	def add_resources(self, res_type: str, quantity: int):
		if res_type == "debug":
			self._wood = quantity
			self._ore = quantity
			self._sheep = quantity
			self._wheat = quantity
			self._brick = quantity
			return
		if hasattr(self, f"_{res_type}"):
			current_value = getattr(self, f"_{res_type}")
			setattr(self, f"_{res_type}", current_value + quantity)
			print(f"Added {res_type} to {current_value + quantity} from {current_value}")
		else:
			print(f"Resource type '{res_type}' does not exist.")
		print(f"Player:{self._player_id} has wood: {self._wood} bricks: {self._brick} ore: {self._ore} sheep: {self._sheep} wheat: {self._wheat}")


	def remove_resources(self, res_type: str, quantity: int):
		if hasattr(self, f"_{res_type}"):
			current_value = getattr(self, f"_{res_type}")
			setattr(self, f"_{res_type}", current_value - quantity)
		else:
			print(f"Resource type '{res_type}' does not exist.")

	def print_resources(self):
		print(f"Player: {self._player_id} has Wood:{self._wood}, Sheep:{self._sheep}, Wheat:{self._wheat}, Brick:{self._brick}, Ore:{self._ore}")

	def get_resources(self):
		resources = 0

		for card in range(self._wood):
			resources += 1
		for card in range(self._ore):
			resources += 1
		for card in range(self._sheep):
			resources += 1
		for card in range(self._brick):
			resources += 1
		for card in range(self._wheat):
			resources += 1

		return resources

	def get_stolen(self):
		resources = []

		print(f"wood: {self._wood} bricks: {self._brick} ore: {self._ore} sheep: {self._sheep} wheat: {self._wheat}")
		for card in range(self._wood):
			resources.append("wood")
		for card in range(self._ore):
			resources.append("ore")
		for card in range(self._sheep):
			resources.append("sheep")
		for card in range(self._brick):
			resources.append("brick")
		for card in range(self._wheat):
			resources.append("wheat")
		if len(resources) > 0:
			random_int = random.randint(0, len(resources) - 1)
			current_value = getattr(self, f"_{resources[random_int]}")
			setattr(self, f"_{resources[random_int]}", current_value - 1)
			return resources[random_int]
		return 0

	def try_settlement(self):
		if self._wood >= 1 and self._sheep >= 1 and self._brick >= 1 and self._wheat >= 1:
			return True
		return False

	def try_card(self):
		if self._wheat >= 1 and self._sheep >= 1 and self._ore >= 1:
			return True
		return False

	def try_road(self):
		if self._wood >= 1 and self._brick >= 1:
			return True
		return False

	def try_city(self):
		if self._wheat >= 2 and self._ore >= 3:
			return True
		return False

	def settlement_cost(self):
		self._wood -= 1
		self._sheep -= 1
		self._wheat -= 1
		self._brick -= 1

	def road_cost(self):
		self._wood -= 1
		self._brick -= 1

	def card_cost(self):
		self._ore -= 1
		self._wheat -= 1
		self._sheep -= 1

	def city_cost(self):
		self._ore -= 3
		self._wheat -= 2

	def monopoly(self, res_type: str):
		buffer = getattr(self, f"_{res_type}")
		setattr(self, f"_{res_type}", 0)
		return buffer

	def discard_half(self):
		buffer = self.get_resources()
		buffer /= 2
		discarded = 0
		while discarded < buffer:
			print(f"Player: {self._player_id} has Wood:{self._wood}, Sheep:{self._sheep}, Wheat:{self._wheat}, Brick:{self._brick}, Ore:{self._ore}")
			resource = input("What do you want to give? wood(W) wheat(w) ore(o) bricks(b) sheep(s)?")
			if resource in resource_convertion_dic:
				if self.has_resource(resource_convertion_dic[resource], 1):
					self.remove_resources(resource_convertion_dic[resource], 1)
					discarded += 1
				else:
					print("You don't have that resource")
			else:
				print("Not a valid input")


