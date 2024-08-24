from funcka_bots.keyboards import (
    Keyboard,
    Callback,
    ButtonColor,
)


keyboard = (
    Keyboard(inline=True, one_time=False, owner_id=12412)
    .add_row()
    .add_button(
        Callback(label="Скрыть", payload={"action_name": "close_menu"}),
        ButtonColor.PRIMARY,
    )
)


# VK keyboard builder interface.

# inline - Place the keyboard under the message.
# one_time - The keyboard is disposable.
# owner_id - Owner of the keyboard.abs

# Next, rows are added, and buttons of different types are added to the rows.
# In general, everything is quite simple here.
