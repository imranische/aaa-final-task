import click
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
        """
        self.name = name
        self.size = size
        self.recipe = self.set_recipe()
        self.order_type = order_type
        self.cook_time = random.randint(7, 15)
        if order_type == 'delivery':
            self.delivery_time = random.randint(5, 45)
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


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool):
    """Готовит и доставляет пиццу"""
    if delivery:
        order_status = 'delivery'
    else:
        order_status = 'dine_in'
    if pizza.capitalize() not in Pizza.availible_recipes:
        click.echo('Некоректное имя пиццы. Сейчас у нас в наличии:')
        print(*Pizza.availible_recipes)
    else:
        new_order = Pizza(pizza, order_type=order_status)
        click.echo(
            f'Заказ принят. Спасибо! Вы заказали {new_order.name} {new_order.size} с опцией {new_order.order_type}')
        click.echo(f"👨‍🍳 Ожидаемое время приготовления {new_order.cook_time} мин")
        if new_order.order_type == 'delivery':
            click.echo(f"🚗 Ожидаемое время доставки {new_order.delivery_time} мин")
            click.echo(f"🏠 Заказ будет у вас примерно через {new_order.cook_time + new_order.delivery_time} мин")
        return new_order


@cli.command()
def menu():
    """Выводит меню"""
    my_menu = Pizza.menu()
    for item in my_menu:
        click.echo(f'{item} {my_menu[item]["pizza_symbol"]}:')
        for el in my_menu[item]['recipe']:
            click.echo(f'- {el}')
        click.echo()


cli.add_command(order)
cli.add_command(menu)


if __name__ == '__main__':
    cli()
