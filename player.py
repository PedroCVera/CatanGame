import random

class Player:
	def __init__(self):
		self._wood = 0
		self._ore = 0
		self._sheep = 0
		self._brick = 0
		self._wheat = 0
		self._development_cards = []
		self._cavaliers = 0

	def get_cavaliers(self):
		return self._cavaliers

	def add_card(self, card: str):
		self._development_cards.append(card)

	def has_cavaliers(self):
		if "cavalier" in self._development_cards:
			return True

	def remove_card(self, card: str):
		if card in self._development_cards:
			self._development_cards.remove(card)
			if card == "cavalier":
				self._cavaliers += 1

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
		print(f"wood: {self._wood} bricks: {self._brick} ore: {self._ore} sheep: {self._sheep} wheat: {self._wheat}")


	def remove_resources(self, res_type: str, quantity: int):
		if hasattr(self, f"_{res_type}"):
			current_value = getattr(self, f"_{res_type}")
			setattr(self, f"_{res_type}", current_value - quantity)
		else:
			print(f"Resource type '{res_type}' does not exist.")

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
