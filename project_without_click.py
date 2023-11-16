import random


class Pizza:
    availible_recipes = {
        'Margherita': {
            'pizza_symbol': '🧀',
            'recipe': ['tomato sause', 'mozzarella', 'tomatoes']
            },
        'Peperroni': {
            'pizza_symbol': '🍕',
            'recipe': ['tomato sause', 'mozzarella', 'peperroni']
            },
        'Hawaiian': {
            'pizza_symbol': '🍍',
            'recipe': ['tomato sause', 'mozzarella', 'chicken', 'pineapples']
            }
        }

    orders = []

    def __init__(self, name, size='XL', order_type='delivery'):
        """
        self.name - имя пиццы
        self.size - размер пиццы
        self.recipe - рецепт пиццы
        self.order_type - тип заказа (delivery/din_in)
        self.cook_time - время приготовления пиццы: случайное число от 7 до 15 мин
        self.delivery_time - время приготовления пиццы: случайное число от 7 до 15 мин (только для доставки)
        self.order_id - id заказа
        """
        self.name = name.lower()
        self.size = size
        self.recipe = self.set_recipe()
        self.order_type = order_type
        self.cook_time = random.randint(7, 15)
        if order_type == 'delivery':
            self.delivery_time = random.randint(5, 45)
        # создаём id заказа
        self.order_id = next(__class__.id_generator)
        # сохраняем все экземпляры класса в список orders, чтобы не потерять наши заказы
        self.__class__.orders.append(self)

    def set_recipe(self):
        """
        Возвращает рецепт пиццы, являющейся экземпляром класса Pizza.
        Используется для вызова метода pizza_dict
        """
        name = self.name.capitalize()

        if name in self.__class__.availible_recipes:
            recipe = {name: self.__class__.availible_recipes[name]}
            return recipe
        return

    def pizza_dict(self):
        """
        Используется в качестве метода dict(). Выводит рецепт экземпляра класса Pizza
        """
        for key, value in self.recipe.items():
            print(f'{key}:\n')
            for el in value:
                print(f'— {el}')

    @classmethod
    def menu(cls):
        """
        Возвращает меню в виде словаря
        """
        return cls.availible_recipes

    @staticmethod
    def counter():
        """
        Генератор натуральных чисел для присвоения заказам их id
        """
        i = 1
        while True:
            yield i
            i += 1

    id_generator = counter()


def order():
    """Готовит и доставляет пиццу"""
    print('Здравствуйте! Сейчас у нас в наличии следующие пиццы:')
    print(*Pizza.availible_recipes)
    pizza = input('Какую пиццу вы хотите заказать?').capitalize()
    while pizza not in Pizza.availible_recipes:
        print('Некоректное имя пиццы. Сейчас у нас в наличии:')
        print(*Pizza.availible_recipes)
        pizza = input('Какую пиццу вы хотите заказать?').capitalize()

    order_status = input('Для доставки введите "delivery", для обеда в пиццерии - "dine_in"').lower()
    while order_status not in {'delivery', 'dine_in'}:
        order_status = input('Некоректная опция. Введите "delivery" или "dine_in"').lower()

    pizza_size = input('Укажите размер пиццы ("L" или "XL"):').upper()
    while pizza_size not in {'L', 'XL'}:
        pizza_size = input('Некоректный размер. Введите "L" или "XL"').upper()

    new_order = Pizza(pizza, size=pizza_size, order_type=order_status)
    print(f'Заказ №{new_order.order_id} принят. Спасибо! Вы заказали {new_order.name} {new_order.size} с опцией {new_order.order_type}')
    print(f"👨‍🍳 Ожидаемое время приготовления {new_order.cook_time} мин")
    if new_order.order_type == 'delivery':
        print(f"🚗 Ожидаемое время доставки {new_order.delivery_time} мин")
        print(f"🏠  Заказ будет у вас примерно через {new_order.cook_time + new_order.delivery_time} мин")
    return new_order


def print_order_list():
    """
    Выводит список всех сделанных заказов
    """
    print('Были заказаны пиццы:')
    for el in Pizza.orders:
        if el.order_type == 'delivery':
            order_type = 'на доставку'
        else:
            order_type = 'в пицерии'

        print(f'{el.order_id}) {el.name.capitalize()} {el.size} {order_type}')


def menu():
    """Выводит меню"""
    my_menu = Pizza.menu()
    print('Наше меню:')
    for item in my_menu:
        print(f'{item} {my_menu[item]["pizza_symbol"]}:')
        for el in my_menu[item]['recipe']:
            print(f'- {el}')
        print()


if __name__ == '__main__':
    # сначала покажем меню, а потом попросим сделать заказ
    # количество заказов определяет пользователь
    menu()
    order()
    print('Хотите сделать ещё заказ? Нажмите "yes". Если нет - нажмите любую кнопку')
    answer = input().lower()
    while answer == 'yes':
        order()
        print('Хотите сделать ещё заказ? Нажмите "yes". Если нет - нажмите любую кнопку')
        answer = input().lower()

    # выведем все сделанные заказы
    print_order_list()
